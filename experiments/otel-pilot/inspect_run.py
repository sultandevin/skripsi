"""Reconcile a pilot response with raw SDK telemetry and process logs."""
import collections
import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.research/otel-pilot'
run = Path(sys.argv[1]).resolve()
manifest = json.loads((run / 'manifest.json').read_text())
order_id = manifest['order_id']
def attrs(entries):
    return {a['key']: next(iter(a['value'].values())) for a in entries}
def read_lines(name):
    path = OUT / 'data' / name
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
traces = read_lines('traces.jsonl')
logs = read_lines('logs.jsonl')
spans = []
for batch in traces:
    for resource in batch.get('resourceSpans', []):
        service = attrs(resource['resource'].get('attributes', [])).get('service.name')
        for scope in resource.get('scopeSpans', []):
            for span in scope.get('spans', []):
                spans.append((service, span))
checkout = [span for service, span in spans if service == 'checkout'
            and attrs(span.get('attributes', [])).get('app.order.id') == order_id]
trace_ids = {span['traceId'] for span in checkout}
checkout_trace_ids = set(trace_ids)
# Follow links to observed producer spans, retaining the links without assigning
# business-causality semantics or altering the raw SDK evidence.
while True:
    observed = {(s['traceId'], s['spanId']) for _, s in spans if s['traceId'] in trace_ids}
    linked_ids = {s['traceId'] for _, s in spans
                  if any((link['traceId'], link['spanId']) in observed for link in s.get('links', []))}
    if linked_ids <= trace_ids:
        break
    trace_ids |= linked_ids
related = [(service, span) for service, span in spans if span['traceId'] in trace_ids]
matched_logs = []
for batch in logs:
    for resource in batch.get('resourceLogs', []):
        service = attrs(resource['resource'].get('attributes', [])).get('service.name')
        for scope in resource.get('scopeLogs', []):
            for record in scope.get('logRecords', []):
                if service == 'accounting' and order_id in json.dumps(record):
                    matched_logs.append(record)
process_logs = subprocess.check_output(
    ['docker', 'compose', '-f', str(OUT / 'compose.json'), 'logs', '--no-color', 'accounting'], text=True)
(run / 'accounting-process.log').write_text(process_logs)
checkout_logs = subprocess.check_output(
    ['docker', 'compose', '-f', str(OUT / 'compose.json'), 'logs', '--no-color', 'checkout'], text=True)
(run / 'checkout-process.log').write_text(checkout_logs)
(run / 'accounting-otel-logs.json').write_text(json.dumps(matched_logs, indent=2) + '\n')
filtered = {'resourceSpans': []}
for batch in traces:
    for resource in batch.get('resourceSpans', []):
        selected = copy.deepcopy(resource)
        scopes = []
        for scope in selected.get('scopeSpans', []):
            scope['spans'] = [s for s in scope.get('spans', []) if s['traceId'] in trace_ids]
            if scope['spans']:
                scopes.append(scope)
        selected['scopeSpans'] = scopes
        if scopes:
            filtered['resourceSpans'].append(selected)
(run / 'order-trace.otlp.json').write_text(json.dumps(filtered, indent=2) + '\n')
ids = {span['spanId'] for _, span in related}
accounting_spans = [span for service, span in related if service == 'accounting']
summary = {
    'order_id': order_id, 'trace_ids': sorted(trace_ids),
    'span_count': len(related),
    'services': dict(collections.Counter(service for service, _ in related)),
    'accounting_otel_log_matches': len(matched_logs),
    'accounting_process_log_contains_order': order_id in process_logs,
    'accounting_spans_in_checkout_trace': sum(s['traceId'] in checkout_trace_ids for s in accounting_spans),
    'accounting_spans_in_linked_traces': sum(s['traceId'] not in checkout_trace_ids for s in accounting_spans),
    'accounting_parent_ids_present': [s.get('parentSpanId') in ids for s in accounting_spans],
    'accounting_links': [link for s in accounting_spans for link in s.get('links', [])],
    'checkout_events': [e['name'] for s in checkout for e in s.get('events', [])],
    'completeness': 'not-established',
    'interpretation': 'Correlation and processing evidence only; no conformance or application-fault verdict.',
}
(run / 'inspection.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
if not checkout or not matched_logs or order_id not in process_logs:
    raise SystemExit('Pilot evidence gate incomplete; inspect raw outputs.')
