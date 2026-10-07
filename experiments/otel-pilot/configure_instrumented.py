"""Apply a local image override without changing the preserved baseline config."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.research/otel-pilot'
config = json.loads((OUT / 'compose.json').read_text())
config['services']['checkout']['image'] = 'pornv-pilot-checkout:checkpoints-v3'
config['services']['accounting']['image'] = 'pornv-pilot-accounting:checkpoints-v3'
for service in ['checkout', 'accounting']:
    config['services'][service]['environment']['PORNV_ACTION_JOURNAL'] = '/tmp/pornv-actions.jsonl'
config['services']['accounting']['environment']['OTEL_DOTNET_AUTO_TRACES_ADDITIONAL_SOURCES'] = 'PORnV.Accounting'
config['services']['otel-collector']['stop_grace_period'] = '45s'
(OUT / 'compose.instrumented.json').write_text(json.dumps(config, indent=2) + '\n')
print(OUT / 'compose.instrumented.json')
