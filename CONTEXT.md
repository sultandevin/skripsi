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

**PORnV attributes**:
Application-defined observation metadata in the `pornv` namespace, named after the research prototype PORnV. These attributes are carried by OpenTelemetry but are not standard OpenTelemetry fields.
_Avoid_: Automatic business causality supplied by tracing.
