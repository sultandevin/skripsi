# OpenTelemetry Demo execution pilot

This pilot uses upstream revision `63649d6d6a59de88fb421b88c3c3a6185b6d21ad` and versioned `2.0.2-*` service images. It preserves checkout dependencies, adds accounting and quote, removes background load and dashboards, and replaces the collector configuration with OTLP receivers and JSON file exporters. It does not change application business logic.

Prerequisites: working Docker Engine/Compose, Python 3, and the pinned checkout in `.research/opentelemetry-demo`. Raw data and generated deployment files are ignored by Git. Run commands from the research workspace root.

```sh
git clone --depth 1 --branch 2.0.2 https://github.com/open-telemetry/opentelemetry-demo.git .research/opentelemetry-demo
python3 experiments/otel-pilot/configure.py
docker compose -f .research/otel-pilot/compose.json up -d --no-build
python3 experiments/otel-pilot/prepare_client.py
python3 experiments/otel-pilot/run_order.py
```

After telemetry has flushed, pass the returned run directory to:

```sh
python3 experiments/otel-pilot/inspect_run.py /absolute/path/to/run-directory
```

Inspect the checkout response, accounting process log, accounting OTLP logs, and filtered `order-trace.otlp.json`. The inspection gate checks order correlation and processing evidence; it does not assert completeness or return a research-verifier verdict. The collector's raw `data/*.jsonl` files contain multiple OTLP batches; the inspection script produces one ordinary OTLP JSON object for the selected trace.

Shipping additionally calls quote, even though the upstream shipping Compose dependencies do not list it. The pilot explicitly includes quote. All published host ports and fixed upstream container names are removed. The isolated project/network is `porv-otel-pilot`; other projects are unaffected.

Stop this pilot with:

```sh
docker compose -f .research/otel-pilot/compose.json down
```

For a fresh experiment, run `python3 experiments/otel-pilot/reset.py`, then start the pilot again. This removes only the pilot containers and their volumes and archives exported telemetry before creating a fresh `data` directory. Inspect each run before resetting. `run_order.py` creates a unique user/cart per run but does not reset the broker. Repeated runs are pilot observations, not a frozen official corpus.

Before formal experiments, record image digests, verify message attribution and the meaning of producer results, add business-completion instrumentation as needed, independently reconcile actions, and freeze the model and completeness contract. Versioned images identify the release but have not been rebuilt from source or independently proven bit-for-bit equivalent to the inspected checkout.

## Business-checkpoint pilot

The separate `business-checkpoints.patch` adds application observations. Read [the pilot contract](../../docs/OTEL-OBSERVATION-CONTRACT.md) for their meaning and scope. The checkout build uses a local Go toolchain and the accounting build uses an isolated SDK container; no system .NET installation is required.

```sh
python3 experiments/otel-pilot/apply_checkpoints.py
CGO_ENABLED=0 go -C .research/opentelemetry-demo/src/checkout build -o ../../../otel-pilot/tools/checkout .
docker build -f experiments/otel-pilot/Dockerfile.checkout -t porv-pilot-checkout:checkpoints-v3 .research/otel-pilot/tools
docker build -f experiments/otel-pilot/Dockerfile.accounting -t porv-pilot-accounting:checkpoints-v3 .research/opentelemetry-demo
python3 experiments/otel-pilot/reset.py
python3 experiments/otel-pilot/configure_instrumented.py
docker compose -f .research/otel-pilot/compose.instrumented.json up -d --no-build
python3 experiments/otel-pilot/run_order.py
```

Wait until checkout/accounting are running before submitting an order. After export flush, run `inspect_run.py` and then `check_business_events.py` with the returned run directory. The latter checks order/message identity, topic/partition and the processing predecessor, and records the actual consumer offset. Producer offsets in upstream `NoResponse` mode are omitted from the business projection. It writes an explicitly incomplete projection; it does not produce a research-conformance verdict.

Use the instrumented Compose file when stopping these services. `reset.py` targets the shared pilot project and archives data from either profile. Preserve both the unmodified native baseline and instrumented datasets for comparison.

Run `python3 experiments/otel-pilot/validate_controls.py /absolute/path/to/run-directory` after the checkpoint gate passes to check identity/reference mismatches, known evidence loss and timestamp independence. These are derived observation controls, not additional application executions or formal verifier evaluations.

## Controlled completeness (v3)

Start from `reset.py` and submit exactly one order. The v3 image override enables separate synced action journals and an accounting operation-phase marker. Then run:

```sh
python3 experiments/otel-pilot/close_run.py /absolute/path/to/run-directory
python3 experiments/otel-pilot/validate_completeness_controls.py /absolute/path/to/run-directory
```

The closure runner freezes checkout/accounting and stops the collector. It checks the frozen journals against exported checkpoints and fresh Kafka offsets. It can establish completeness only for the three-checkpoint normal-run scope in the contract. A missing checkpoint or unsupported epoch stays inconclusive. The sources remain paused for inspection. To remove the pilot after preserving results:

```sh
docker compose -f .research/otel-pilot/compose.instrumented.json unpause checkout accounting
docker compose -f .research/otel-pilot/compose.instrumented.json down
```

The recorded freeze is the end of the observation interval; actions after unpausing are outside it. Never run the older checkpoint gate after closure and assume completeness is retained: that gate deliberately resets the projection to incomplete. `check_completeness.py` rechecks a saved closure without Docker. Its evidence-loss controls are derived files, not injected application faults or formal conformance results.
