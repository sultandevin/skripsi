"""Apply the reviewed checkpoint patch, or confirm it is already applied."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / '.research/opentelemetry-demo'
PATCH = ROOT / 'experiments/otel-pilot/business-checkpoints.patch'
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
if revision != '63649d6d6a59de88fb421b88c3c3a6185b6d21ad':
    raise SystemExit('Checkpoint patch requires the pinned 2.0.2 revision')
applied = subprocess.run(['git', 'apply', '--reverse', '--check', str(PATCH)],
                         cwd=REPO, capture_output=True).returncode == 0
if applied:
    print('Checkpoint patch already applied.')
else:
    subprocess.run(['git', 'apply', '--check', str(PATCH)], cwd=REPO, check=True)
    subprocess.run(['git', 'apply', str(PATCH)], cwd=REPO, check=True)
    print('Applied checkpoint patch.')
