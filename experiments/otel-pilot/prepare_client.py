"""Build a tiny local client image from the checksum-verified grpcurl release."""
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.research/otel-pilot/tools'
OUT.mkdir(parents=True, exist_ok=True)
base = 'https://github.com/fullstorydev/grpcurl/releases/download/v1.9.3/'
filename = 'grpcurl_1.9.3_linux_x86_64.tar.gz'
with urllib.request.urlopen(base + filename, timeout=60) as response:
    archive = response.read()
with urllib.request.urlopen(base + 'grpcurl_1.9.3_checksums.txt', timeout=60) as response:
    checksums = response.read().decode()
expected = next(line.split()[0] for line in checksums.splitlines() if line.split()[-1] == filename)
if hashlib.sha256(archive).hexdigest() != expected:
    raise SystemExit('grpcurl release checksum mismatch')
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
    binary = OUT / 'grpcurl'
    binary.write_bytes(tar.extractfile('grpcurl').read())
    binary.chmod(0o755)
(OUT / 'release.sha256').write_text(expected + '  ' + filename + '\n')
(OUT / 'Dockerfile').write_text('FROM scratch\nCOPY grpcurl /grpcurl\nENTRYPOINT ["/grpcurl"]\n')
subprocess.run(['docker', 'build', '-t', 'porv-pilot-grpcurl:1.9.3', str(OUT)], check=True)
