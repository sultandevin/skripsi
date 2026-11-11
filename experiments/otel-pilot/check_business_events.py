"""Validate the three business checkpoints and their message identity."""
import json
from pathlib import Path
import sys

run = Path(sys.argv[1]).resolve()
manifest = json.loads((run / 'manifest.json').read_text())
raw = json.loads((run / 'order-trace.otlp.json').read_text())
def value(v):
    if 'arrayValue' in v:
        return [value(x) for x in v['arrayValue'].get('values', [])]
    return next(iter(v.values()))
def attrs(entries):
    return {a['key']: value(a['value']) for a in entries}
names = {'order.publish.initiated', 'order.publish.client_succeeded', 'order.accounting.processed'}
events = []
for resource in raw.get('resourceSpans', []):
    service = attrs(resource['resource'].get('attributes', [])).get('service.name')
    for scope in resource.get('scopeSpans', []):
        for span in scope.get('spans', []):
            inherited = attrs(span.get('attributes', []))
            for i, event in enumerate(span.get('events', [])):
                if event['name'] not in names:
                    continue
                metadata = inherited | attrs(event.get('attributes', []))
                if event['name'] != 'order.accounting.processed':
                    # NoResponse producer offsets are not broker evidence. Preserve
                    # them in the raw export, but omit them from this projection.
                    metadata.pop('messaging.kafka.message.offset', None)
                events.append({
                    'id': f"{span['traceId']}:{span['spanId']}:event:{i}",
                    'type': event['name'], 'service': service,
                    'traceId': span['traceId'], 'spanId': span['spanId'],
                    'timestamp': event['timeUnixNano'],
                    'correlation': {'app.order.id': metadata.get('app.order.id')},
                    'attributes': metadata,
                    'predecessors': metadata.get('porv.predecessors', []),
                })
if sorted(e['type'] for e in events) != sorted(names):
    raise SystemExit(f'Expected three distinct checkpoints, observed {[e["type"] for e in events]}')
by_type = {e['type']: e for e in events}
initiated = by_type['order.publish.initiated']
client = by_type['order.publish.client_succeeded']
processed = by_type['order.accounting.processed']
assert all(e['correlation']['app.order.id'] == manifest['order_id'] for e in events), 'Order mismatch'
message_ids = {e['attributes'].get('app.message.id') for e in events}
assert len(message_ids) == 1 and None not in message_ids and '' not in message_ids, 'Message identity mismatch'
assert initiated['id'] in processed['predecessors'], 'Processing lacks its recorded send-attempt predecessor'
assert client['traceId'] == initiated['traceId'] and client['spanId'] == initiated['spanId'], 'Publisher span mismatch'
assert int(client['id'].rsplit(':', 1)[1]) > int(initiated['id'].rsplit(':', 1)[1]), 'Publisher event order mismatch'
for key in ['messaging.destination.name', 'messaging.kafka.destination.partition']:
    assert str(client['attributes'][key]) == str(processed['attributes'][key]), f'Transport mismatch: {key}'
# Projection uses the declared local event order and the explicitly propagated
# reference. It intentionally adds no client-success -> processing dependency.
client['predecessors'] = [initiated['id']]
projection = {'complete': False, 'events': events}
(run / 'business-events.json').write_text(json.dumps(projection, indent=2) + '\n')
result = {'status': 'checkpoints-matched', 'order_id': manifest['order_id'],
          'message_id': next(iter(message_ids)), 'event_count': len(events),
          'kafka_offset': str(processed['attributes']['messaging.kafka.message.offset']),
          'edges': [[initiated['id'], client['id']], [initiated['id'], processed['id']]],
          'completeness': 'not-established',
          'note': 'Checkpoint validation is not an existential-conformance or application-fault verdict.'}
log_path = run / 'accounting-otel-logs.json'
if log_path.exists():
    records = json.loads(log_path.read_text())
    assert any(record.get('traceId') == processed['traceId'] and record.get('spanId') == processed['spanId']
               for record in records), 'Accounting log context does not match processing checkpoint'
    result['accounting_log_context_matched'] = True
(run / 'business-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
