"""Submit one isolated order and save request/response evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / '.research/opentelemetry-demo'
OUT = ROOT / '.research/otel-pilot'
run_id = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
run = OUT / 'runs' / run_id
run.mkdir(parents=True)
user_id = 'pornv-pilot-' + run_id

def invoke(name, address, method, request):
    (run / f'{name}-request.json').write_text(json.dumps(request, indent=2) + '\n')
    result = subprocess.run([
        'docker', 'run', '--rm', '--network', 'pornv-otel-pilot',
        '-v', f'{REPO}/pb:/protos:ro', 'pornv-pilot-grpcurl:1.9.3',
        '-plaintext', '-import-path', '/protos', '-proto', 'demo.proto',
        '-max-time', '45', '-d', json.dumps(request), address, method,
    ], text=True, capture_output=True)
    (run / f'{name}-response.json').write_text(result.stdout)
    (run / f'{name}-stderr.txt').write_text(result.stderr)
    if result.returncode:
        raise SystemExit(f'{name} failed: {result.stderr}')
    return json.loads(result.stdout)

invoke('add-item', 'cart:7070', 'oteldemo.CartService/AddItem',
       {'userId': user_id, 'item': {'productId': 'OLJCESPC7Z', 'quantity': 1}})
response = invoke('checkout', 'checkout:5050', 'oteldemo.CheckoutService/PlaceOrder', {
    'userId': user_id, 'userCurrency': 'USD',
    'address': {'streetAddress': '123 Pilot Street', 'city': 'Jakarta',
                'state': 'Jakarta', 'country': 'Indonesia', 'zipCode': '10110'},
    'email': 'pilot@example.com',
    'creditCard': {'creditCardNumber': '4432801561520454', 'creditCardCvv': 672,
                   'creditCardExpirationYear': 2030, 'creditCardExpirationMonth': 12},
})
manifest = {'run_id': run_id, 'user_id': user_id,
            'order_id': response['order']['orderId'], 'status': 'checkout-returned',
            'source_revision': '63649d6d6a59de88fb421b88c3c3a6185b6d21ad',
            'completeness': 'not-established',
            'note': 'Checkout success alone does not establish Kafka/accounting completion.'}
images = {service: subprocess.check_output(
    ['docker', 'inspect', '--format', '{{.Image}}', f'pornv-otel-pilot-{service}-1'], text=True).strip()
    for service in ['checkout', 'accounting']}
manifest['application_image_ids'] = images
checkout_image = subprocess.check_output(
    ['docker', 'inspect', '--format', '{{.Config.Image}}', 'pornv-otel-pilot-checkout-1'], text=True).strip()
manifest['observation_profile'] = 'business-' + checkout_image.rsplit(':', 1)[-1] if 'checkpoints-v' in checkout_image else 'native-v0'
if manifest['observation_profile'].startswith('business-checkpoints-v'):
    manifest['instrumentation_patch_sha256'] = hashlib.sha256(
        (ROOT / 'experiments/otel-pilot/business-checkpoints.patch').read_bytes()).hexdigest()
(run / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'run_directory': str(run), 'order_id': manifest['order_id']}))
