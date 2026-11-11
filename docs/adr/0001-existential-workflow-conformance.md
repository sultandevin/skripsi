# Accept one allowed causally compatible workflow sequence

On 2 October 2026 the user chose existential workflow conformance: a complete observation is consistent if at least one topological ordering is accepted by the developer-defined state machine. This follows the original idea draft and replaces the first proposal's causal-prerequisite checks; requiring every ordering to be accepted would answer a stronger question. Acceptance does not establish actual causal enforcement, while rejection requires exhausting the compatible search space; incomplete evidence and resource cutoffs remain inconclusive.

## Evaluation amendment — 7 October 2026

Existential DFA conformance remains the primary semantics. Following the user's review approval, retain causal-prerequisite reachability as a required, bounded second analysis for explicitly declared dependency rules, initially without repetition. Its outcomes concern supported prerequisites, not existential compatibility or arbitrary-DFA universal acceptance. Validate paths independently and evaluate application alarms against separate business-fault facts; missing a path alone does not establish early execution.

Required conformance comparators now include raw timestamps, a deterministic single topological ordering, and a conservative bounded-clock-error variant. The clock variant checks the DFA only when all projected event intervals establish a unique strict total order; overlapping intervals cause an inconclusive result. Clock bounds are declared before measurement and assumption violations are reported separately. Oracle agreement and clock invariance validate implementation; practical benefit requires separate application-fault evidence and search-sensitive cases.
