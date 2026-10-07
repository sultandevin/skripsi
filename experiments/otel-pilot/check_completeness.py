"""Reconcile a frozen, fresh, single-order checkpoint experiment.

This is a collection gate, not the thesis's existential conformance verifier.
The action-ledger writers and freeze runner are trusted experiment machinery.
"""
import hashlib
import json
from pathlib import Path
import sys


def reconcile(run):
    projection = json.loads((run / 'business-events.json').read_text())
    projection['complete'] = False
    (run / 'business-events.json').write_text(json.dumps(projection, indent=2) + '\n')
    manifest = json.loads((run / 'manifest.json').read_text())
    cut = json.loads((run / 'closure.json').read_text())
    failures = []

    def require(condition, reason):
        if not condition:
            failures.append(reason)

    require(cut['protocol'] == 'single-order-frozen-checkpoints-v1', 'Unknown closure protocol')
    require(manifest['observation_profile'] == 'business-checkpoints-v3', 'Action-ledger profile required')
    require(cut['broker_start'] == {'orders:0': 0} and cut['broker_end'] == {'orders:0': 1},
            'Requires a fresh, single-partition topic with exactly one stored message')
    ledger = []
    for service in ['checkout', 'accounting']:
        state = cut['sources'][service]
        require(state['paused'] and state['running'] and not state['oom_killed']
                and state['restart_count'] == 0, f'{service} did not freeze cleanly')
        require(state['image'] == manifest['application_image_ids'][service], f'{service} image changed')
        path = run / f'{service}-actions.jsonl'
        require(hashlib.sha256(path.read_bytes()).hexdigest() == state['journal_sha256'],
                f'{service} journal changed after freeze')
        ledger.extend(json.loads(line) | {'service': service}
                      for line in path.read_text().splitlines() if line)
    require(len(ledger) == 3 and len({row['id'] for row in ledger}) == 3,
            'Ledger is outside the supported three-action normal-run scope')
    require(all(row['order_id'] == manifest['order_id'] for row in ledger), 'Unexpected order in ledger')
    require(sorted(row['type'] for row in ledger) == sorted([
        'order.publish.initiated', 'order.publish.client_succeeded', 'order.accounting.processed']),
        'Unexpected action types in ledger')
    require(len({row['message_id'] for row in ledger}) == 1
            and all(row['message_id'] for row in ledger), 'Action ledger message identity mismatch')
    events = projection['events']
    require(len(events) == len(ledger) and {e['id'] for e in events} == {r['id'] for r in ledger},
            'Exported checkpoints do not cover the frozen action ledger exactly')
    # Audit the entire saved exporter snapshot, including matching records in
    # unrelated trace IDs which trace-based inspection might otherwise omit.
    exported = []
    exported_records = {}
    dropped = 0
    names = {'order.publish.initiated', 'order.publish.client_succeeded', 'order.accounting.processed'}
    def value(item):
        if 'arrayValue' in item:
            return [value(child) for child in item['arrayValue'].get('values', [])]
        return next(iter(item.values()))
    def attributes(entries):
        return {entry['key']: value(entry['value']) for entry in entries}
    for line in (run / 'collector-snapshot/traces.jsonl').read_text().splitlines():
        batch = json.loads(line)
        for resource in batch.get('resourceSpans', []):
            service = attributes(resource['resource'].get('attributes', [])).get('service.name')
            if service not in ['checkout', 'accounting']:
                continue
            for scope in resource.get('scopeSpans', []):
                for span in scope.get('spans', []):
                    selected = False
                    for index, event in enumerate(span.get('events', [])):
                        if event['name'] not in names:
                            continue
                        selected = True
                        metadata = attributes(span.get('attributes', [])) | attributes(event.get('attributes', []))
                        require(metadata.get('app.order.id') == manifest['order_id'], 'Unexpected order in raw checkpoints')
                        identity = f"{span['traceId']}:{span['spanId']}:event:{index}"
                        exported.append(identity)
                        exported_records[identity] = (event['name'], service, metadata)
                    if selected:
                        dropped += int(span.get('droppedEventsCount', 0))
    require(sorted(exported) == sorted(event['id'] for event in events),
            'Projection differs from the full closed exporter checkpoint set')
    require(dropped == 0, 'Closed exporter reports dropped selected-span events')
    for event in events:
        if event['id'] not in exported_records:
            continue
        kind, service, metadata = exported_records[event['id']]
        require(event['type'] == kind and event['service'] == service
                and event['correlation']['app.order.id'] == metadata.get('app.order.id')
                and event['attributes'].get('app.message.id') == metadata.get('app.message.id'),
                'Projection identity differs from raw exporter record')
        if kind == 'order.accounting.processed':
            require(event['predecessors'] == metadata.get('pornv.predecessors', []),
                    'Projection causal reference differs from raw exporter record')
            for key in ['messaging.destination.name', 'messaging.kafka.destination.partition',
                        'messaging.kafka.message.offset']:
                require(str(event['attributes'].get(key)) == str(metadata.get(key)),
                        f'Projection transport metadata differs from raw exporter: {key}')
    by_id = {e['id']: e for e in events}
    initiated_ids = [row['id'] for row in ledger if row['type'] == 'order.publish.initiated']
    for event in events:
        if event['type'] == 'order.publish.client_succeeded':
            require(event['predecessors'] == initiated_ids, 'Client causal reference differs')
    for row in ledger:
        event = by_id.get(row['id'])
        if event is None:
            continue
        require(event['type'] == row['type'] and event['service'] == row['service']
                and event['correlation']['app.order.id'] == row['order_id']
                and event['attributes'].get('app.message.id') == row['message_id'],
                'Checkpoint identity differs from independent action record')
        if row['type'] == 'order.accounting.processed':
            require(row['topic'] == 'orders' and row['partition'] == 0 and row['offset'] == 0,
                    'Accounting did not cover the stored broker offset')
            require(event['predecessors'] == [row['predecessor']], 'Accounting causal reference differs')
            require(str(event['attributes'].get('messaging.kafka.message.offset')) == str(row['offset']),
                    'Accounting offset differs')
            require(event['attributes'].get('messaging.destination.name') == row['topic']
                    and str(event['attributes'].get('messaging.kafka.destination.partition')) == str(row['partition']),
                    'Accounting topic/partition differs from action ledger')
    require(cut['collector_stopped'], 'Collector export snapshot was not closed')
    require(cut['accounting_phase'] == 'idle', 'Accounting was frozen inside an action; ledger may lag')
    require(cut['selected_span_dropped_events'] == 0, 'SDK reports dropped selected-span events')
    projection['complete'] = not failures
    projection['completeness_scope'] = 'Three checkpoint types for one order, through the recorded source freeze'
    (run / 'business-events.json').write_text(json.dumps(projection, indent=2) + '\n')
    result = {'status': 'complete-for-declared-scope' if not failures else 'inconclusive',
              'failures': failures, 'order_id': manifest['order_id'],
              'scope': projection['completeness_scope'],
              'note': 'No claim about all application spans, future retries, conformance, or business correctness.'}
    manifest['completeness'] = result['status']
    manifest['completeness_scope'] = projection['completeness_scope']
    (run / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (run / 'completeness-checks.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    run = Path(sys.argv[1]).resolve()
    try:
        result = reconcile(run)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {'status': 'inconclusive', 'failures': [f'Missing or malformed closure evidence: {error}']}
        (run / 'completeness-checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    sys.exit(0 if result['status'] == 'complete-for-declared-scope' else 3)
