"""Reset only this pilot's containers/volumes, preserving telemetry exports."""
import datetime
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.research/otel-pilot'
subprocess.run(['docker', 'compose', '-f', str(OUT / 'compose.json'),
                'down', '--volumes'], check=True)
data = OUT / 'data'
if data.exists() and any(data.iterdir()):
    archive = OUT / 'archives' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    archive.parent.mkdir(exist_ok=True)
    data.rename(archive)
    print(f'Preserved telemetry in {archive}')
data.mkdir(exist_ok=True)
