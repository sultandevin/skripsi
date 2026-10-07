# OpenTelemetry Demo pilot results

Executed on 7 October 2026 (Asia/Jakarta).

## Outcome

The first execution milestone passed: the pinned demo can run locally, accept an order, publish it through Kafka, process it in accounting, and export usable SDK-generated OTLP JSON. Three normal orders were reconciled, including one after a clean application/broker reset. Keep OpenTelemetry Demo as the first external target while completing the observation contract. This is a feasibility result, not a completed workflow-conformance or application-fault experiment.

## What ran

- Source checkout: `63649d6d6a59de88fb421b88c3c3a6185b6d21ad` (release 2.0.2).
- Application images: versioned `ghcr.io/open-telemetry/demo:2.0.2-*` images; their exact digests are recorded in `.research/otel-pilot/image-manifest.json`. These release images were not rebuilt or independently proven equivalent to the checkout.
- Thirteen services: checkout, accounting, cart, currency, email, payment, product-catalog, shipping, quote, flagd, Kafka, Valkey and the collector.
- Normal business logic was retained. No background load generator, dashboard stack or host service ports were enabled. The collector exported traces, logs and metrics to local JSONL files.
- Requests used the upstream gRPC API with a unique user/cart, one known product and simulated payment details. The grpcurl 1.9.3 client was obtained from its upstream release, checksum-verified, and packaged in a local scratch image.
- Docker Desktop and WSL integration were working. One unrelated existing PostgreSQL container was left untouched.

The collector image tag is `0.120.0`, while its startup log reports binary version `0.120.1`; preserve both values and the recorded image digest instead of silently assuming they agree.

## Observations

| Run (UTC identifier) | Order ID | Retained spans across linked traces | Accounting evidence |
| --- | --- | --- | --- |
| `20261007T111630Z-ada7272d` | `8d26d50f-c240-11f1-940f-4ed46abd6049` | 44 | Process log and one matching OTLP log |
| `20261007T111733Z-69d25755` | `b2601b33-c240-11f1-940f-4ed46abd6049` | 38 | Process log and one matching OTLP log |
| `20261007T111913Z-9a503f08` (after reset) | `edfc91cf-c240-11f1-8e42-3a0d8f5a823f` | 44 | Process log and one matching OTLP log |

Each run included checkout's `prepared`, `charged` and `shipped` span events. Each also included an accounting Kafka receive span in a **separate trace**, linked to the observed checkout Kafka producer span. The link carried trace/span identity but no PORnV causal annotation. Accounting's order log did not carry a trace/span context in the inspected records. Do not equate a receive-span boundary with completion of the accounting business action.

The initial consumer reported an unknown `orders` topic before checkout's first publication created it; processing later succeeded. Startup broker health does not establish topic readiness. The clean reset removed only the pilot's containers/volumes, archived its exports and recreated the application; the third message's consumer record had offset zero. Future official runs should establish topic readiness explicitly before measurement.

Follow-up instrumentation exposed that the upstream producer uses `sarama.NoResponse`. Its logged success and producer offset are not broker-acknowledgement evidence: the reported offset stayed zero on a later message whose consumer offset was one. The earlier interpretation of that producer log was too strong. The reset conclusion above uses the consumer record; see [the corrected checkpoint contract](OTEL-OBSERVATION-CONTRACT.md).

A single Docker memory snapshot summed to approximately 765 MiB across pilot containers. It is not a peak-memory, instrumentation-overhead or capacity benchmark.

## Adapter smoke check

The existing PORnV binary read the first run's aggregated ordinary OTLP JSON successfully and returned `inconclusive` (exit code 3). The smoke protocol matched checkout's `charged` and `shipped` events using `app.order.id`.

Diagnostics identified an unannotated accounting link, unestablished completeness and an unresolved causal reference across workflow grouping. The parser/export path therefore works, but native instrumentation does not yet satisfy the research observation contract. The old prototype implements causal-prerequisite rules rather than the thesis's existential DFA search; this smoke check does not validate that algorithm or establish a conformance verdict.

## Evidence and reproduction

- Tracked setup and scripts: [pilot instructions](../experiments/otel-pilot/README.md).
- Tracked compact measurements: [pilot observations](../experiments/otel-pilot/pilot-observations.json).
- Raw per-run responses, OTLP trace objects, matched accounting logs, inspection summaries and checksums: `.research/otel-pilot/runs/<run-id>/`.
- First-epoch raw exports: `.research/otel-pilot/archives/20261007T111817.960743Z/`.
- Post-reset raw exports: `.research/otel-pilot/data/`.
- Deployment configuration, image manifest, startup/reset logs and memory snapshot: `.research/otel-pilot/`.

The raw artifacts and upstream checkout are intentionally ignored by Git but remain available locally. Generated traces contain synthetic addresses and simulated payment data. The pilot services were stopped after collection; images and evidence were preserved for the next stage.

## Next stage

1. Freeze a narrow publication-to-accounting workflow. Declare whether its terminal business action is successful parse/recording, without inventing a database effect or exactly-once requirement absent from this revision.
2. Add explicit SDK business milestones for the send attempt, corresponding client-reported publication result, and successful accounting processing. Give each a stable event identity and order correlation. Retain the original raw observations alongside instrumented outputs. A broker acknowledgement would require a separately documented change to the current `NoResponse` configuration.
3. Establish and record the direction and identity of the message dependency, including the observed cross-trace link. Tie the receive and processing points using instrumented execution order. Do not simply label every general span link causal.
4. Reconcile required actions and exports under controlled termination to establish completeness. Timeout or HTTP response alone is insufficient.
5. Define an independent application-fault oracle and a documented fault patch consistent with the selected business requirement. Duplicate transport delivery alone is not a business violation. If this narrow workflow cannot support a meaningful fault case without inventing new requirements, reassess eShop before official data collection.
6. Once the contract and existential verifier are ready, run normal/fault pairs and derived clock-shift/telemetry-loss cases. Clock shifts retain the graph and application labels; known telemetry loss revokes completeness. Keep application-fault and observation-compatibility labels separate.

At the baseline stage, fault patches, completeness instrumentation, the existential verifier and formal comparison runs remained outstanding. The selected external path is predominantly sequential, so controlled concurrent/synthetic cases remain necessary to evaluate search across alternative orderings.

## Business-checkpoint follow-up, 7 October 2026

Added and exercised a separate instrumentation patch: [business checkpoint patch](../experiments/otel-pilot/business-checkpoints.patch). Checkout now records the send attempt and the matching client-success notification. It propagates order/message correlation and the send-attempt event identity in Kafka headers. Accounting records its processing completion after its original order log call and attaches the explicit predecessor. The [v2 contract](OTEL-OBSERVATION-CONTRACT.md) defines the recording points and causal meaning.

The first version incorrectly called the producer notification a broker acknowledgement. A repeat run disproved that interpretation: checkout reported offset zero while accounting recorded offset one. Inspection of `kafka/producer.go` confirmed `sarama.NoResponse`. The correction retains that native transport behavior, renames the checkpoint `order.publish.client_succeeded`, omits the unsupported producer offset from the business projection, and records the real Kafka position at the consumer. Two earlier v1 runs are preserved with a superseded-contract annotation; they are not valid broker-acknowledgement evidence or official evaluation samples.

The corrected v2 runs passed the checkpoint gate:

| Run | Order ID | Actual consumer offset | Result |
| --- | --- | --- | --- |
| `20261007T121529Z-1d9c87ff` | `caa0fb7e-c248-11f1-b0c4-de5ecdb1ef4d` | 0 | All three checkpoints, matching identities and explicit predecessor |
| `20261007T121616Z-b111653d` | `e66326f4-c248-11f1-b0c4-de5ecdb1ef4d` | 1 | All three checkpoints, matching identities and explicit predecessor |

In both runs the accounting order log's trace/span context matched the new processing activity. Original automatic receive spans/links were retained. The new business activity was exported by the existing automatic .NET SDK with its custom source registered; no general SDK link was silently declared causal.

Derived evidence controls on the first v2 run behaved as expected:

- Changing the processing message identity failed the matching gate.
- Replacing its predecessor with an absent event identity failed the reference gate.
- Removing its processing checkpoint failed the three-checkpoint gate; this is evidence loss, not proof of an application violation.
- Shifting accounting timestamps forward five minutes and other services backward five minutes retained the same checkpoint matches and causal edges. This validates the observation projection's independence from timestamps, not the unimplemented existential verifier or superiority over a comparator.

Compact results are in [checkpoint observations](../experiments/otel-pilot/checkpoint-observations.json). Requests, responses, complete raw trace objects, matched logs, projections, gate results and evidence checksums are preserved under `.research/otel-pilot/runs/<run-id>/`; derived controls are under the first v2 run's `controls/`. Build logs and `checkpoint-build-manifest.json` record image IDs, the instrumentation patch hash, .NET SDK image digest and Go 1.27.1. The accounting assembly was built with a pinned SDK container and overlaid onto the release runtime; checkout was compiled from the patched source and overlaid onto its release image.

The corrected projection is still explicitly incomplete. The pilot services were stopped after collection. No application-fault patch, completeness assertion or existential-verifier result was produced in this stage. Next: define controlled workflow closure and independent action/message reconciliation before evaluating missing or extra actions as business faults.

## Controlled completeness follow-up, 7 October 2026

The v3 instrumentation adds a separate synced action ledger to checkout/accounting and an accounting operation-phase marker. [The current contract](OTEL-OBSERVATION-CONTRACT.md) limits completeness to the three business checkpoint types for one successful order in a fresh, single-partition broker epoch, through a recorded source freeze. The journals witness the selected action boundaries independently of SDK export; they are trusted experiment instrumentation, not an independent business-state oracle.

The closure runner pauses the two sources, copies their action records and process state, queries the broker's stored-offset range, drains already emitted telemetry, and stops the collector. The collection gate reconciles the full exporter snapshot with both journals and the selected projection. A source frozen in the middle of accounting processing is inconclusive: an action could have occurred before its journal write. Matching journal/export records guards the later export gap. Broker evidence checks offsets rather than independently decoding Kafka payloads.

| Run | Outcome | Evidence |
| --- | --- | --- |
| `20261007T122825Z-f877b33d` | Inconclusive | All three checkpoints matched, but the collector image's one-second stop timeout caused exit 137 before shutdown completed |
| `20261007T123126Z-58dbb2bd` | Complete for declared checkpoint scope | Three independent action records matched three exported checkpoints; accounting covered the sole broker offset 0; sources frozen with accounting idle; collector exited normally |
| `20261007T123321Z-648ec7ba` | Complete for declared checkpoint scope | Same result in a separate fresh epoch and a different order/message, with the same source image IDs |

The runner and instrumented configuration now explicitly allow 45 seconds for collector shutdown. The first failed attempt is retained as inconclusive rather than retroactively relabeled complete.

Eight derived evidence controls on the first successful closed observation passed their expected outcomes. Removing an exported checkpoint, removing a journal record, recording accounting as busy, adding a broker message, recording a source restart, inserting an extra checkpoint under an unrelated trace ID, and reporting dropped span events all revoked completeness. Moving accounting timestamps forward five minutes and checkout timestamps backward five minutes preserved completeness. These seven negative controls and one clock control are modified saved evidence, not eight additional application executions or injected business faults.

Compact execution/control results and build provenance are in [completeness observations](../experiments/otel-pilot/completeness-observations.json). Each run preserves frozen journals, closure metadata, the full collector snapshot, selected raw trace, projection, collection verdict, and checksums under `.research/otel-pilot/runs/<run-id>/`. The source instrumentation patch and image IDs are recorded. The pilot services were stopped after saving the observations.

This milestone establishes bounded checkpoint collection completeness under the stated controlled-run assumptions. It does not assert completeness of every automatic span or general crash/retry/concurrent workflows. The added synced writes affect timing; these samples do not establish unqualified performance comparisons. No application-fault label, DFA verdict, or formal comparison result has been produced. The next implementation milestone is to freeze the normal DFA and terminal policy, then implement the thesis's existential checker; the existing prototype still checks causal prerequisites rather than existential DFA conformance. Meaningful business-fault cases still require a documented requirement and independent application oracle.
