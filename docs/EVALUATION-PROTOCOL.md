# Prospective evaluation protocol — 7 October 2026

This records design choices adopted before formal corpus generation, not completed experiments or an external preregistration. Chapters II–IV describe the same plan. Existential compatibility remains primary; prerequisite reachability is a bounded diagnostic for explicit dependency rules without repetition.

## Fixed targets

| Field | Requirement |
| --- | --- |
| Supported complete-graph profile | Full graph n in {4, 8, 12, 16, 20}, actual poset width w in {1, 2, 4}, explicit DFA with 2–16 states |
| Core search deadline | 10 seconds per workflow |
| Configuration cap | 1,000,000 configurations; stop at the first resource limit reached |
| Existential decision coverage | At least 95% on the selected complete-input main profile |
| Resource-cutoff rate | At most 5% on that profile |
| Small-graph implementation gate | 100% independent-oracle agreement without abstention on the predefined complete suite |
| Comparator coverage | Report as an outcome; the interval comparator has no 95% coverage requirement |

These are prospective offline-workflow targets, not measured performance. Slow selected cells remain eligible and may fail. Width is the maximum antichain of the full causal poset, verified from reachability and a minimum chain partition, not a count of service branches.

## Freeze sequence

1. Before calibration: save generator definitions, selected cells, sample counts, primary contrast/profile, label construction, clock bounds, fixed targets, analysis choices, identity ordering and timing procedure in a versioned pre-calibration manifest. Select and record the experimental machine.
2. Use separate pilot and calibration executions/seeds to validate implementation, oracle, structural feasibility and measurement tools. Record structurally impossible cells; do not remove cells because they are slow.
3. Freeze final manifest, machine, software and instrumentation versions before generating the official corpus with fresh seeds. Save normalized and raw cases before measurement.
4. Run every planned independent unit, including failures, abstentions and cutoffs. Do not stop or expand based on significance. Amendments create a new protocol version with reasons and preserve earlier results.

The complete generator/cell manifest is an implementation deliverable. Its absence means formal evaluation has not started. Operational numerical targets above are already chosen and are not selected from calibration performance.

## Sampling and statistics

- At least 30 independent base units per selected cell. A base unit is a generated graph or a fresh-state application execution. A seed alone does not establish independence if it reuses the same underlying execution.
- Derived clock shifts, evidence-loss variants and repeated timings stay in their base unit's cluster. Summarize timing repetitions by a per-unit median.
- Prespecified application comparisons: existential versus raw time, interval time, one topological order, and prerequisite analysis where applicable. Compare correctness separately on normal and faulty application labels: eight planned two-sided exact McNemar tests, with Holm familywise alpha 0.05. Keep the originally planned family size when some tests are unavailable.
- One base observation per independent unit enters the primary test; the main application profile and any mixture weights must be specified before corpus generation. Derived-offset and scenario-specific additional tests are exploratory.
- Use jointly determinate binary pairs for McNemar. Report eligible/excluded counts and whole-input coverage. Zero discordances give p=1; zero eligible pairs give an undefined test. Do not encode abstention as an ordinary accepted/rejected verdict.
- Paired, stratified cluster bootstrap: 10,000 replicates, fixed seed, percentile 95% CIs for error/coverage differences and the median paired time difference. Keep all method outcomes and derived variants together. Freeze stratum weights before measurement.
- For independent base-observation FPR/FNR within a stratum, report numerator/denominator and exact Clopper–Pearson 95% intervals, including zero errors. Do not apply binomial intervals to pooled correlated variants. Report undefined denominators and degenerate bootstrap intervals.
- Statistical uncertainty concerns the declared generator/execution profile. Designed correctness fixtures and external feasibility controls are descriptive. A small sample or zero observed errors does not establish universal accuracy.

## Scaling and abstention

- Compare both swap-invariant models and graphs with accepted/rejected extensions. Width-one graphs have a single extension, so mixed acceptance is inapplicable.
- Plot core time, explored configurations and cutoff proportion against event count, grouped by verified width. Hold model and acceptance class constant within a series.
- Report completed-time quantiles as conditional on completion; resource-limited timings are censored at their limit and accompanied by cutoff counts.
- Interval risk–coverage sweep uses clock-bound multipliers {0, 0.5, 1, 2}; multiplier 1 is primary. Flag assumption-violating points. Preserve the same inputs at every point. Other checkers are fixed-budget points, not invented confidence-score curves.
- Risk is error conditional on a decision, separately for existential and application labels. With no decisions risk is undefined. Report FPR/FNR, coverage and correct decisions over all labeled inputs together.

## Scope reductions

Cut optional external business-fault patches and additional external closure profiles first, then a second app and large stress tests or extra timing variants. Retain normal bounded external integration, minimum evidence gates, independent correctness/fault oracles, three comparators, bounded prerequisite diagnostics, S7 baseline-win cases and controlled-width scaling. Full-graph explanations satisfy the deliverable; slice optimization is optional. Search-benefit evidence comes from controlled and synthetic cases.
