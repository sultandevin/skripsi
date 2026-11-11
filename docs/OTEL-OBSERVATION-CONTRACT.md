# OpenTelemetry Demo business-checkpoint contract, pilot v3

This contract covers one isolated order in the pinned 2.0.2 checkout-to-accounting path. It is a pilot contract, not a production completeness guarantee. Raw automatic instrumentation is preserved alongside the additional business records.

| Checkpoint | Exact recording point | Meaning |
| --- | --- | --- |
| `order.publish.initiated` | Before putting the serialized order onto the asynchronous producer input channel | The application is about to attempt sending this message; publication has not yet completed |
| `order.publish.client_succeeded` | After the producer success channel returns this request's message object | The producer client reports success in `NoResponse` mode; this is not a broker acknowledgement |
| `order.accounting.processed` | After accounting parses the order and calls its existing order-recording log function | Processing completed according to this revision's behavior: parsing and recording, without a database update |

Every checkpoint carries `app.order.id` and a generated `app.message.id`. Retransmission of the same message retains its message identity; distinct attempts from distinct calls receive new identities. A repeated delivery is not automatically a second forbidden business effect.

The publisher puts message identity and the send-attempt event identity into Kafka headers. Accounting records the predecessor on its processing event in the application-defined `porv.predecessors` attribute. The identifier follows the prototype adapter's OTLP event format `traceId:spanId:event:index`. In v2 the initiated checkpoint is the producer's first event; the integration gate checks that reference against the actual exported event rather than assuming it resolved.

The recorded dependencies are:

```text
publication attempt ──→ client reported success
                   └─→ accounting processed
```

Client success and accounting processing are not ordered relative to one another. The upstream producer uses `sarama.NoResponse`, so its success notification is not evidence of broker acknowledgement. In the repeat pilot its reported offset stayed zero while the consumer correctly recorded offset one. The business projection therefore omits producer offset metadata and retains the consumer's Kafka position. Order/message identity, the propagated event reference, and matching topic/partition establish correspondence without timestamp ordering. Broker-confirmed publication would require a separately documented transport configuration change. See the [pinned producer configuration](https://github.com/open-telemetry/opentelemetry-demo/blob/63649d6d6a59de88fb421b88c3c3a6185b6d21ad/src/checkout/kafka/producer.go).

The original Kafka receive link remains an ordinary unannotated SDK link. It is not relabeled causal globally. A new accounting business activity uses the explicitly propagated trace context and records the specific event predecessor. Custom activities are subscribed via `OTEL_DOTNET_AUTO_TRACES_ADDITIONAL_SOURCES=porv.Accounting`, using the existing automatic SDK. See the [OpenTelemetry manual-instrumentation instructions](https://github.com/open-telemetry/opentelemetry-dotnet-instrumentation/blob/v1.11.0/docs/manual-instrumentation.md).

## Limits and validation

- The pilot runs one order at a time, with Kafka overload/republication flags disabled. Upstream shares producer success/error channels across requests. A mismatched producer result produces no successful checkpoint; this instrumentation does not claim concurrency-safe acknowledgement attribution or fix that producer design.
- Accounting logging indicates the log call returned; it does not guarantee durable persistence of a log record or exactly-once processing.
- Business completion is recorded as an SDK span event after the action; a receive-span start is not substituted for completion.
- `check_business_events.py` reconciles the three checkpoints, identities, transport position and explicit event reference. It saves a projection of those business records without changing the raw export.
- The checkpoint gate alone writes `complete: false`. The v3 closure gate below can establish completeness for a narrowly declared checkpoint scope. Historical v2 observations remain incomplete.
- A candidate normal DFA can accept attempt → client success → processing and attempt → processing → client success. Failure, retry and terminal policies must be specified before this becomes the official model.
- Instrumentation additions are saved separately in `experiments/otel-pilot/business-checkpoints.patch`; no business-fault patch is included.

## V3 controlled completeness scope

The supported profile is a fresh broker topic, one partition, one successful order, one message, no other requests, no overload flag, and no source restarts. It covers only the three checkpoint types for that order through a recorded freeze of checkout and accounting. It does not establish completeness of automatic spans, the whole application, failed runs, or future deliveries after resuming services.

Checkout writes a separate JSONL action ledger before emitting each selected checkpoint. Accounting writes its ledger after the existing order-log call and before emitting its processing checkpoint. Each append is flushed to disk, outside the telemetry SDK/export path. Write failure terminates the source process. These journals are trusted experiment instrumentation, not an independent implementation of business semantics: they witness the same recording points, independently of telemetry collection. Their added disk I/O changes timing and makes this profile unsuitable for unqualified performance comparisons.

Accounting also maintains an atomically replaced phase marker: `processing` before entering its business operation, `idle` only after the operation and span disposal return. A freeze in `processing` is inconclusive because the action may precede its journal write. Checkout's successful synchronous response is the sender-operation boundary; the harness sends no additional request. Source processes are paused, not assumed to have flushed merely because a delay elapsed.

The runner copies frozen journals and container state, queries Kafka's earliest/latest offsets, lets already emitted traffic drain, and stops the collector to close the exported snapshot. Reconciliation requires:

- Both sources frozen without an OOM or restart, with the same image IDs as the submitted order, and accounting idle.
- Broker offsets exactly `[0, 1)` on `orders:0`; accounting's separate ledger covers that sole stored offset. This is broker offset evidence, not a content-level independent Kafka consumer or a publisher acknowledgement.
- Exactly the supported three action records, with matching order/message identity and unique event IDs, and exact one-to-one coverage by the exported checkpoint projection.
- Matching processing offset and causal references, unchanged frozen-journal hashes, and no reported dropped events on selected spans.

Only then does `check_completeness.py` set the projection's `complete` field for this scope. Missing telemetry, missing journal data, unexpected actions/messages, an in-progress accounting operation, or restarted sources leave collection inconclusive. Seeing three events or waiting for a quiet collector alone is insufficient. The phase check guards the action-to-journal gap; exact reconciliation guards the journal-to-export gap. Duplicate or retry experiments require an expanded ledger/model/closure policy rather than applying this normal-run gate unchanged.

This collection result supplies evidence to a future conformance checker. It is neither a DFA acceptance result nor an application-fault verdict. General crash recovery, independent business-state oracles, meaningful business-fault cases, and wider workflows remain separate work.
