"""Derived evidence-loss controls; these are not extra application runs."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

from check_completeness import reconcile

run = Path(sys.argv[1]).resolve()
original = json.loads((run / 'business-events.json').read_text())
if not original['complete']:
    raise SystemExit('Requires a reconciled complete observation')
cases = ['missing-export', 'missing-action-ledger', 'busy-accounting',
         'extra-broker-message', 'source-restarted', 'unlinked-extra-export',
         'reported-dropped-events', 'clock-shift']
summary = []
for case in cases:
    target = run / 'completeness-controls' / case
    target.mkdir(parents=True, exist_ok=True)
    for name in ['manifest.json', 'closure.json', 'checkout-actions.jsonl', 'accounting-actions.jsonl']:
        shutil.copyfile(run / name, target / name)
    (target / 'collector-snapshot').mkdir(exist_ok=True)
    shutil.copyfile(run / 'collector-snapshot/traces.jsonl', target / 'collector-snapshot/traces.jsonl')
    projection = copy.deepcopy(original)
    cut = json.loads((target / 'closure.json').read_text())
    if case == 'missing-export':
        projection['events'] = [e for e in projection['events'] if e['type'] != 'order.accounting.processed']
    elif case == 'missing-action-ledger':
        (target / 'accounting-actions.jsonl').write_text('')
        cut['sources']['accounting']['journal_sha256'] = hashlib.sha256(b'').hexdigest()
    elif case == 'busy-accounting':
        cut['accounting_phase'] = 'processing'
    elif case == 'extra-broker-message':
        cut['broker_end']['orders:0'] = 2
    elif case == 'source-restarted':
        cut['sources']['accounting']['restart_count'] = 1
    elif case in ['unlinked-extra-export', 'reported-dropped-events']:
        snapshot = target / 'collector-snapshot/traces.jsonl'
        batches = [json.loads(line) for line in snapshot.read_text().splitlines()]
        for batch in batches:
            found = False
            for resource in batch.get('resourceSpans', []):
                for scope in resource.get('scopeSpans', []):
                    for span in list(scope.get('spans', [])):
                        if any(e['name'] == 'order.accounting.processed' for e in span.get('events', [])):
                            if case == 'unlinked-extra-export':
                                extra = copy.deepcopy(span)
                                extra['traceId'] = '1' * 32
                                extra['spanId'] = '2' * 16
                                scope['spans'].append(extra)
                            else:
                                span['droppedEventsCount'] = 1
                            found = True
                            break
                    if found: break
                if found: break
            if found: break
        snapshot.write_text(''.join(json.dumps(batch) + '\n' for batch in batches))
    elif case == 'clock-shift':
        for event in projection['events']:
            event['timestamp'] = str(int(event['timestamp']) +
                (300_000_000_000 if event['service'] == 'accounting' else -300_000_000_000))
    (target / 'closure.json').write_text(json.dumps(cut, indent=2) + '\n')
    (target / 'business-events.json').write_text(json.dumps(projection, indent=2) + '\n')
    result = reconcile(target)
    expected = 'complete-for-declared-scope' if case == 'clock-shift' else 'inconclusive'
    if result['status'] != expected:
        raise SystemExit(f'Unexpected result in {case}: {result}')
    summary.append({'case': case, 'status': result['status'], 'failures': result['failures']})
(run / 'completeness-control-results.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
