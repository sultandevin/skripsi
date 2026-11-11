"""Check evidence failures and timestamp independence using a captured run."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
run = Path(sys.argv[1]).resolve()
original = json.loads((run / 'order-trace.otlp.json').read_text())
reference = json.loads((run / 'business-checks.json').read_text())
out = run / 'controls'
out.mkdir(exist_ok=True)
results = {}
for case in ['message-mismatch', 'broken-predecessor', 'missing-processing-record', 'clock-shift']:
    raw = copy.deepcopy(original)
    for resource in raw['resourceSpans']:
        service = next(a['value']['stringValue'] for a in resource['resource']['attributes'] if a['key'] == 'service.name')
        shift = 300_000_000_000 if service == 'accounting' else -300_000_000_000
        for scope in resource['scopeSpans']:
            for span in scope['spans']:
                if case == 'clock-shift':
                    for key in ['startTimeUnixNano', 'endTimeUnixNano']:
                        span[key] = str(int(span[key]) + shift)
                    for event in span.get('events', []):
                        event['timeUnixNano'] = str(int(event['timeUnixNano']) + shift)
                if case == 'missing-processing-record':
                    span['events'] = [e for e in span.get('events', []) if e['name'] != 'order.accounting.processed']
                for event in span.get('events', []):
                    if event['name'] != 'order.accounting.processed':
                        continue
                    for attr in event.get('attributes', []):
                        if case == 'message-mismatch' and attr['key'] == 'app.message.id':
                            attr['value'] = {'stringValue': 'wrong-message'}
                        if case == 'broken-predecessor' and attr['key'] == 'porv.predecessors':
                            attr['value'] = {'arrayValue': {'values': [{'stringValue': 'missing:event:0'}]}}
    path = out / case
    path.mkdir(exist_ok=True)
    for name in ['manifest.json', 'accounting-otel-logs.json']:
        shutil.copyfile(run / name, path / name)
    (path / 'order-trace.otlp.json').write_text(json.dumps(raw, indent=2) + '\n')
    result = subprocess.run(['python3', str(ROOT / 'experiments/otel-pilot/check_business_events.py'), str(path)],
                            text=True, capture_output=True)
    (path / 'diagnostic.txt').write_text(result.stdout + result.stderr)
    if case == 'clock-shift':
        assert result.returncode == 0, result.stderr
        checked = json.loads((path / 'business-checks.json').read_text())
        assert checked['edges'] == reference['edges'], 'Clock shift changed causal edges'
        results[case] = {'checkpoints_matched': True, 'causal_edges_unchanged': True}
    else:
        assert result.returncode != 0, f'{case} incorrectly passed the evidence gate'
        results[case] = {'evidence_gate_failed': True, 'diagnostic': result.stderr.splitlines()[-1]}
(out / 'summary.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
