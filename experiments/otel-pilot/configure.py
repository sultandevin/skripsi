"""Generate an isolated pilot from the pinned upstream Compose configuration."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / '.research/opentelemetry-demo'
OUT = ROOT / '.research/otel-pilot'
REVISION = '63649d6d6a59de88fb421b88c3c3a6185b6d21ad'
actual = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip()
if actual != REVISION:
    raise SystemExit(f'Unexpected source revision: {actual}')
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'data').mkdir(exist_ok=True)
env = dict(os.environ, DEMO_VERSION='2.0.2')
config = json.loads(subprocess.check_output(
    ['docker', 'compose', 'config', '--format', 'json'], cwd=REPO, env=env, text=True))
selected = {'checkout', 'accounting', 'quote'}
def include(name):
    if name in selected_done:
        return
    selected_done.add(name)
    if name != 'otel-collector':
        for dependency in config['services'][name].get('depends_on', {}):
            include(dependency)
selected_done = set()
for name in sorted(selected):
    include(name)
services = {name: config['services'][name] for name in sorted(selected_done)}
for name, service in services.items():
    service.pop('container_name', None)
    service.pop('build', None)
    service.pop('ports', None)
    service['restart'] = 'no'
    service.setdefault('environment', {})['OTEL_TRACES_SAMPLER'] = 'always_on'
    service['environment']['OTEL_BSP_SCHEDULE_DELAY'] = '1000'
services['otel-collector'] = {
    'image': config['services']['otel-collector']['image'],
    'command': ['--config=/etc/pilot.json'],
    'user': '0:0',
    'volumes': [f'{OUT}/collector.json:/etc/pilot.json:ro', f'{OUT}/data:/data'],
    'networks': {'default': {}},
    'restart': 'no',
}
collector = {
    'receivers': {'otlp': {'protocols': {
        'grpc': {'endpoint': '0.0.0.0:4317'}, 'http': {'endpoint': '0.0.0.0:4318'}}}},
    'processors': {'batch': {'timeout': '1s'}},
    'exporters': {f'file/{signal}': {'path': f'/data/{signal}.jsonl'}
                  for signal in ['traces', 'logs', 'metrics']},
    'service': {'pipelines': {
        signal: {'receivers': ['otlp'], 'processors': ['batch'], 'exporters': [f'file/{signal}']}
        for signal in ['traces', 'logs', 'metrics']}}
}
(OUT / 'collector.json').write_text(json.dumps(collector, indent=2) + '\n')
pilot = {'name': 'porv-otel-pilot', 'services': services,
         'networks': {'default': {'name': 'porv-otel-pilot', 'driver': 'bridge'}}}
(OUT / 'compose.json').write_text(json.dumps(pilot, indent=2) + '\n')
print(f'Prepared {len(services)} services in {OUT}')
