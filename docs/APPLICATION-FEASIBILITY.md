# External application feasibility comparison

Assessed on 6 October 2026 (Asia/Jakarta). This is a static source and local-environment assessment, not a completed execution experiment. No application was deployed and no telemetry dataset was collected.

Follow-up on 7 October: Docker became available and the OpenTelemetry Demo execution pilot passed its initial correlation/export/reset checks. See [pilot results](OTEL-PILOT-RESULTS.md) for evidence and remaining instrumentation work. The assessment below preserves the original static findings.

## Recommendation

Keep OpenTelemetry Demo as the proposal's existing first execution target. Treat Microsoft eShop as the stronger alternative for evaluating business-state violations, conditional on deployment and instrumentation feasibility. Neither has passed the execution gate yet; this assessment does not change the proposal's selected application.

The decisive tradeoff is observation integration versus independently checkable business effects. OpenTelemetry Demo already targets telemetry demonstrations, but its pinned accounting implementation only parses and logs orders. eShop persists an explicit order lifecycle and has concrete transition guards, giving a stronger application oracle, at the cost of a larger setup and additional instrumentation work.

## Frozen source revisions

| Application | Inspected revision | License |
| --- | --- | --- |
| OpenTelemetry Demo 2.0.2 | `63649d6d6a59de88fb421b88c3c3a6185b6d21ad` | Apache-2.0 |
| Microsoft eShop | `dc7ea499cd356924fb6689b3702964a5869dbae9` (main resolved during assessment) | MIT |

Sources: [OTel revision](https://github.com/open-telemetry/opentelemetry-demo/tree/63649d6d6a59de88fb421b88c3c3a6185b6d21ad), [eShop revision](https://github.com/dotnet/eShop/tree/dc7ea499cd356924fb6689b3702964a5869dbae9). Current website documentation can describe behavior absent from these revisions; source at the revision takes precedence.

## Comparison

| Criterion | OpenTelemetry Demo | Microsoft eShop |
| --- | --- | --- |
| Bounded workflow | Successful order publication by checkout, followed by accounting processing | Order submitted, awaiting validation, stock confirmed, paid, then explicitly shipped; cancellation modeled separately |
| Asynchronous transport | Kafka `orders` topic | RabbitMQ integration-event bus |
| Existing observation support | Checkout producer span injects trace context into Kafka headers; accounting uses automatic instrumentation | Event bus explicitly injects/extracts trace context and creates publish/receive activities; shared defaults configure OTel and OTLP export |
| Correlation | Order ID in checkout result and serialized message; propagation into consumer business events must be verified | Order ID in business events and stored order; background processing and later HTTP shipping require explicit cross-trace correlation |
| Independent outcome evidence | Controlled action records, checkout response and accounting processing record; no accounting database at this revision | Stored order state, catalog inventory, and independent action records; final state alone does not prove the history |
| Business-model fit | Narrow publish/process model; do not impose exactly-once accounting effects | Clear transition guards and normal failure branches; stock availability check is distinct from reservation and later stock deduction |
| Useful concurrency | Selected accounting path is mainly a chain; a second consumer is potential fan-out, not a demonstrated join | Core status progression is mainly a chain; paid-event subscribers provide potential independent branches, not a demonstrated business join |
| Minimal setup | Checkout needs its normal service dependencies, not just Kafka and accounting | Candidate subset: ordering, catalog, order processor, payment processor, RabbitMQ, PostgreSQL, plus identity or a justified test-auth configuration |
| Execution status | Unverified | Unverified |

Subset deployment is a proposal to test, not a confirmed supported configuration. Broker and database reset procedures, image availability, required memory, export compatibility and repeatability remain unmeasured.

## OpenTelemetry Demo findings

The checkout source performs preparation, payment, shipping, cart clearing, email attempt, and Kafka publication. Payment and shipping are sequential. Email failure is logged but does not necessarily fail checkout. Kafka publication failure also does not necessarily fail the returned checkout response. Therefore HTTP success alone cannot label successful publication or complete accounting processing.

The producer records success and offset metadata, but shared producer success/error channels are read by individual requests. Under concurrent requests, correspondence between the observed acknowledgement and a particular request needs verification; do not assume the success attribute alone proves that request's message was acknowledged. Start calibration with isolated orders.

The accounting consumer parses an `OrderResult` and writes a log. It has auto-commit enabled and contains no database write or duplicate-business-effect guard. Repeated delivery must not automatically be labeled a business violation. The `kafkaQueueProblems` flag republishes messages as an overload mechanism; it is not independent proof of an application fault.

Proposed observation contract:

- Record a publication milestone after acknowledgement of the corresponding message, with order ID and stable message identity.
- Record an accounting-processing milestone after successful parse and the declared processing action.
- Match producer and consumer using verified transport identity/context; retain order ID for workflow grouping.
- Establish completion through controlled collection and action reconciliation. Absence of a consumer event by a deadline is insufficient proof of a missing action in an unbounded asynchronous workflow.

Sources: [checkout](https://github.com/open-telemetry/opentelemetry-demo/blob/63649d6d6a59de88fb421b88c3c3a6185b6d21ad/src/checkout/main.go), [accounting consumer](https://github.com/open-telemetry/opentelemetry-demo/blob/63649d6d6a59de88fb421b88c3c3a6185b6d21ad/src/accounting/Consumer.cs), [accounting log](https://github.com/open-telemetry/opentelemetry-demo/blob/63649d6d6a59de88fb421b88c3c3a6185b6d21ad/src/accounting/Log.cs), [deployment dependencies](https://github.com/open-telemetry/opentelemetry-demo/blob/63649d6d6a59de88fb421b88c3c3a6185b6d21ad/docker-compose.yml).

## Microsoft eShop findings

The order aggregate permits progression from Submitted to AwaitingValidation to StockConfirmed to Paid. Shipping explicitly throws unless the order is Paid. Shipping is triggered by a separate API action, so Paid is a legitimate endpoint for a bounded payment workflow; an observation ending at Paid must not be rejected simply because shipping has not been requested. Choose either a payment workflow ending at Paid or a controlled fulfillment workflow including the explicit shipping request.

Catalog stock confirmation checks available quantity without reserving it. Stock deduction occurs in a separate subscriber after the Paid event. The model must not require deduction before Paid, or invent a requirement that shipping waits for deduction. Additional subscribers can be included as independent branches only if their completion and correlation can be observed reliably.

Payment is simulated and configurable for success/failure. A normal failed payment is an allowed business branch, not an injected violation. Candidate violations include deliberately bypassing the paid-before-shipped guard, or changing state without the required earlier transition. These are proposed research patches, not existing experiment controls. Duplicate message delivery is a transport condition; classify a violation only if it causes a business effect forbidden by the chosen specification.

Domain events are dispatched before database changes are committed. Instrumenting domain-event-handler entry as a completed state transition would be premature. Record business completion after successful transaction commit. Integration events are published after commit through the transaction behavior, which offers a useful point to examine for instrumentation.

The grace-period processor polls stored orders and publishes a later event. A database handoff does not automatically preserve the original trace or record its business dependency. Explicit order correlation and predecessor references may be required. The separate shipping HTTP request similarly requires a recorded dependency on the committed Paid state, rather than ordering by its timestamp.

Sources: [order aggregate](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs), [stock check](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs), [stock deduction](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToPaidIntegrationEventHandler.cs), [payment handler](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/PaymentProcessor/IntegrationEvents/EventHandling/OrderStatusChangedToStockConfirmedIntegrationEventHandler.cs), [transaction behavior](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/Ordering.API/Application/Behaviors/TransactionBehavior.cs), [ordering context](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/Ordering.Infrastructure/OrderingContext.cs), [background processor](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/OrderProcessor/Services/GracePeriodManagerService.cs), [API](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/Ordering.API/Apis/OrdersApi.cs), [event bus](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/EventBusRabbitMQ/RabbitMQEventBus.cs).

## Local environment check

- WSL reports approximately 7.6 GiB RAM and 16 GiB swap. This is environment inventory, not a measured application capacity result.
- Linux `docker version` reports that Docker Desktop WSL integration is unavailable.
- Windows `docker.exe version` finds a client but cannot connect to the Docker Desktop Linux engine pipe. No running engine was reachable through that command.
- No Linux `dotnet` executable was found. Windows `dotnet.exe --list-sdks` returns no SDKs; installed Windows runtimes are .NET 8.0.20.
- The inspected eShop revision requests .NET SDK 10.0.302 with `latestFeature` roll-forward. The repository also requires Aspire tooling and a container runtime.

Execution cannot yet be assessed in this environment. Docker Desktop must be running with usable WSL integration for the planned Linux container experiments. eShop additionally requires compatible SDK/Aspire tooling. No packages were installed or desktop settings changed during this comparison.

Sources: [SDK pin](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/global.json), [eShop prerequisites](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/README.md), [application host](https://github.com/dotnet/eShop/blob/dc7ea499cd356924fb6689b3702964a5869dbae9/src/eShop.AppHost/AppHost.cs).

## Execution gate and proposed pilot

1. Make the container engine available; verify the pinned images/build dependencies can be obtained. For eShop, provide the required SDK and Aspire tooling.
2. Run the smallest faithful service subset, retain one order at a time initially, and demonstrate resetting application and broker state.
3. Produce one normal workflow and reconcile business actions, stored state or processing records, message identities and SDK-exported telemetry. Verify OTLP JSON can be consumed by the research adapter; exporter configuration alone does not establish this.
4. Freeze the business-event mapping, causal edge sources and controlled completeness conditions. Do not infer edges merely from shared service or span membership.
5. Demonstrate one independently established business violation through a documented patch. Keep business-logic and instrumentation patches separate.
6. Derive timestamp-offset and telemetry-loss inputs from the collected observation while preserving application-fact labels separately. Mark known loss inconclusive.
7. Run a small repeated pilot before freezing the official corpus. Measure memory and setup effort rather than estimating feasibility from repository size.

Both selected core workflows are predominantly sequential. They can test real SDK integration, causal reconstruction, clock sensitivity and application-fault detection. They do not by themselves establish a benefit from exploring multiple concurrent orderings. Keep the controlled concurrent application and synthetic branching cases for that question; do not manufacture extra business dependencies in either external model.
