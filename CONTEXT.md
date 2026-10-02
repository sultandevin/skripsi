# Workflow conformance research

This research examines whether observed asynchronous service interactions conform to developer-defined workflows while preserving causal ordering.

## Language

**Allowed workflow sequence**:
A sequence of business events accepted by the developer-defined workflow specification, including any alternatives or repetition that the specification permits.
_Avoid_: Timestamp order as a synonym for allowed behavior.

**Workflow conformance**:
Consistency of an observed execution with the allowed workflow behavior: at least one sequence preserving the known causal ordering is allowed. It does not establish that every compatible sequence is allowed or that the actual application enforced each business dependency.
_Avoid_: Causal prerequisite checking as a synonym for the entire research scope.

**Consistent observation**:
A complete workflow observation with at least one causally compatible sequence accepted by its specification.
_Avoid_: Proven-safe execution, guaranteed correct application.

**Inconsistent observation**:
A complete workflow observation for which no causally compatible sequence is accepted by its specification.
_Avoid_: One rejected ordering as sufficient proof.
