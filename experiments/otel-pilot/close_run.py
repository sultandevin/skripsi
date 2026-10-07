"""Freeze source processes and reconcile a fresh, isolated normal order.

Run only after run_order.py, with no other requests in this pilot epoch.
Leaves source containers paused and the collector stopped for inspection.
"""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import sys
import time

from check_completeness import reconcile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.research/otel-pilot'
COMPOSE = ['docker', 'compose', '-f', str(OUT / 'compose.instrumented.json')]
run = Path(sys.argv[1]).resolve()
if (run / 'closure.json').exists():
    raise SystemExit('This run already has a closure snapshot; use check_completeness.py to recheck it')
manifest = json.loads((run / 'manifest.json').read_text())
if manifest['observation_profile'] != 'business-checkpoints-v3':
    raise SystemExit('Closure requires the v3 independent action-ledger profile')


def offsets(which):
    result = subprocess.check_output(COMPOSE + ['exec', '-T', 'kafka',
        '/opt/kafka/bin/kafka-get-offsets.sh', '--bootstrap-server', 'kafka:9092',
        '--topic', 'orders', '--time', which], text=True)
    return {':'.join(line.split(':')[:2]): int(line.split(':')[2])
            for line in result.splitlines() if line.startswith('orders:')}


def copy_journal(service):
    subprocess.run(['docker', 'cp', f'pornv-otel-pilot-{service}-1:/tmp/pornv-actions.jsonl',
                    str(run / f'{service}-actions.jsonl')], check=True, capture_output=True)


# This wait is only a readiness bound. Exact reconciliation below determines
# completeness; elapsed time or a quiet collector never proves completeness.
deadline = time.monotonic() + 45
while True:
    try:
        copy_journal('accounting')
        rows = [json.loads(line) for line in (run / 'accounting-actions.jsonl').read_text().splitlines()]
        if any(row['order_id'] == manifest['order_id'] for row in rows):
            break
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        pass
    if time.monotonic() >= deadline:
        raise SystemExit('Accounting readiness timed out: completeness remains unestablished')
    time.sleep(1)

# Give the source SDKs a chance to export while they are still running. This
# does not establish completeness; the frozen ledger may still contain more.
time.sleep(3)
subprocess.run(COMPOSE + ['pause', 'checkout', 'accounting'], check=True)
cut = {'protocol': 'single-order-frozen-checkpoints-v1',
       'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'sources': {}}
for service in ['checkout', 'accounting']:
    copy_journal(service)
    info = json.loads(subprocess.check_output(['docker', 'inspect',
                     f'pornv-otel-pilot-{service}-1'], text=True))[0]
    state = info['State']
    cut['sources'][service] = {
        'container_id': info['Id'], 'image': info['Image'],
        'paused': state['Paused'], 'running': state['Running'],
        'oom_killed': state['OOMKilled'], 'restart_count': info['RestartCount'],
        'journal_sha256': hashlib.sha256((run / f'{service}-actions.jsonl').read_bytes()).hexdigest()}
subprocess.run(['docker', 'cp', 'pornv-otel-pilot-accounting-1:/tmp/pornv-actions.jsonl.phase',
                str(run / 'accounting-phase.txt')], check=True, capture_output=True)
cut['accounting_phase'] = (run / 'accounting-phase.txt').read_text()
cut['broker_start'] = offsets('-2')
cut['broker_end'] = offsets('-1')
# Allow already emitted OTLP traffic to reach the collector. If the SDK was
# frozen before export, reconciliation fails safely rather than assuming flush.
time.sleep(5)
subprocess.run(COMPOSE + ['stop', '-t', '45', 'otel-collector'], check=True)
collector = json.loads(subprocess.check_output(['docker', 'inspect',
                       'pornv-otel-pilot-otel-collector-1'], text=True))[0]
cut['collector_stopped'] = not collector['State']['Running'] and collector['State']['ExitCode'] == 0
cut['collector_state'] = collector['State']
snapshot = run / 'collector-snapshot'
snapshot.mkdir(exist_ok=True)
for path in (OUT / 'data').glob('*.jsonl'):
    shutil.copyfile(path, snapshot / path.name)
(run / 'closure.json').write_text(json.dumps(cut, indent=2) + '\n')
for gate in ['inspect_run.py', 'check_business_events.py']:
    result = subprocess.run([sys.executable, str(ROOT / 'experiments/otel-pilot' / gate), str(run)])
    if result.returncode:
        verdict = {'status': 'inconclusive', 'failures': [f'{gate} could not validate the closed evidence'],
                   'note': 'An evidence failure is not an application-fault verdict.'}
        (run / 'completeness-checks.json').write_text(json.dumps(verdict, indent=2) + '\n')
        manifest['completeness'] = 'inconclusive'
        (run / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        if (run / 'business-events.json').exists():
            projection = json.loads((run / 'business-events.json').read_text())
            projection['complete'] = False
            (run / 'business-events.json').write_text(json.dumps(projection, indent=2) + '\n')
        raise SystemExit(json.dumps(verdict))
raw = json.loads((run / 'order-trace.otlp.json').read_text())
cut['selected_span_dropped_events'] = sum(
    int(span.get('droppedEventsCount', 0))
    for resource in raw.get('resourceSpans', []) for scope in resource.get('scopeSpans', [])
    for span in scope.get('spans', []) if any(event['name'].startswith('order.publish.')
        or event['name'] == 'order.accounting.processed' for event in span.get('events', [])))
(run / 'closure.json').write_text(json.dumps(cut, indent=2) + '\n')
result = reconcile(run)
print(json.dumps(result, indent=2))
sys.exit(0 if result['status'] == 'complete-for-declared-scope' else 3)
