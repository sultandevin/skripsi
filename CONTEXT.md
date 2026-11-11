# Workflow conformance research

This research examines whether observed asynchronous service interactions conform to developer-defined workflows while preserving causal ordering.

## Language

**Allowed workflow sequence**:
A sequence of business events accepted by the developer-defined workflow specification, including any alternatives or repetition that the specification permits.
_Avoid_: Timestamp order as a synonym for allowed behavior.

**Workflow conformance**:
Compatibility of an observation with the allowed workflow behavior: at least one sequence preserving the known causal ordering is allowed. It does not establish that every compatible sequence is allowed or that the actual application enforced each business dependency.
_Avoid_: Causal prerequisite checking as a synonym for the entire research scope.

**Model-compatible observation**:
A complete workflow observation with at least one causally compatible sequence accepted by its specification.
_Avoid_: Proven-safe execution, guaranteed correct application.

**Model-incompatible observation**:
A complete workflow observation for which no causally compatible sequence is accepted by its specification.
_Avoid_: One rejected ordering as sufficient proof.

**Recorded causal dependency**:
An ordering relationship supported by the declared observation contract. A compatible workflow sequence must preserve it; ordering an otherwise unordered pair does not establish an actual causal dependency.
_Avoid_: Physical timestamp order as proof of causality.

**Application fault**:
A violation of the application's business requirements established independently from its observations. An observation of a faulty application can remain compatible with the workflow model when recorded dependencies permit an allowed explanation.
_Avoid_: Model-incompatible observation as a synonym for every application fault.

**Inconclusive observation**:
An observation for which compatibility cannot be decided because evidence is insufficient or the search did not complete within its resource limits.
_Avoid_: Insufficient evidence as a synonym for every search cutoff.

**PORV attributes**:
Application-defined observation metadata for the research prototype PORV. The `porv` namespace retains the implementation tool and repository name. These attributes are carried by OpenTelemetry but are not standard OpenTelemetry fields.
_Avoid_: Automatic business causality supplied by tracing.

## Required evaluation distinctions — 7 October 2026

- Compare existential search with raw timestamp sorting, conservative timestamp sorting under explicit clock-error bounds, and deterministic topological sorting of the same causal graph. Timestamp uncertainty may cause abstention; report its coverage.
- Test both swap-invariant models and graphs with accepted/rejected linear extensions. Separate benefits of causal information from benefits of alternative-order search.
- Retain bounded prerequisite reachability for explicit causal-dependency rules. Supported/unsupported paths use their own oracle; they are neither general DFA conformance nor independent proof of a business fault.
- Report reliable-clock S7 cases where timestamp sorting detects early action while existential checking accepts. A shared time reference across distinct processes does not itself add a causal edge.
- The three-event external path is bounded integration evidence. Both normal linear extensions are accepted; it cannot establish search benefit. Business-fault detection is required on the controlled application, and external fault claims require demonstrated independent business facts.

## Prospective statistics and targets — 7 October 2026

See docs/EVALUATION-PROTOCOL.md. Operational targets are now fixed before calibration: complete main graphs n=4–20, w<=4, DFA 2–16 states; 10 seconds/1,000,000 configurations; >=95% existential coverage and <=5% resource cutoffs. Numerical targets supersede the earlier calibration-selected target plan. A pre-calibration design manifest and pre-generation final manifest remain required.

Independent units are base graphs or fresh application executions; derived controls remain clustered. Statistics include paired bootstrap intervals, exact McNemar application comparisons with Holm correction and exact binomial FPR/FNR intervals on independent base observations. Poset width is controlled; fixed-width polynomial complexity follows the ideal/configuration bound, while general constrained topological sorting is hard. Offline runtime verification is the thesis's use of runtime.
