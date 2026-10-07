# Review actions — 5 October 2026

| Review item | Action and status |
| --- | --- |
| Circularity / headline claim | Revised: conformance is primary; oracle independence stated; S3 is design invariance, paired baseline changes measured, application faults evaluated separately. |
| S7 detection gap | Revised: an actual prerequisite violation must be established independently; consistent observations on faulty executions count as missed faults in the application matrix. |
| External application count and identity | Revised: one required external workflow, OpenTelemetry Demo 2.0.2 at commit 63649d6d6a59de88fb421b88c3c3a6185b6d21ad. Subsequent 7 October pilot established execution, SDK checkpoint correlation and bounded normal-run collection completeness. Independent business-fault cases, broader closure profiles and formal evaluation remain B2–B3 work. Replacement procedure explicit. |
| Success criteria | Revised: 100% small-graph suite agreement without abstain, evidence/cutoff cases, canonical determinism, SDK and external-workflow deliverables. Workload, timeout, coverage and timeout-rate targets are calibrated and frozen before official experiments. |
| Six-month scope | Revised: no full factorial design; external second app and 1,000–5,000-event extensions optional; explicit cut order. Core correctness, external workflow and SDK retained. |
| Literature | Added Fidge, Mattern, Chase–Garg, Leucker–Schallhart, and Omer et al.; scope differences stated, no new algorithm claim. Added pinned application source. Full Fidge scan retrieval failed; source notes disclose verification limits. |
| Front matter lists | Added tables, figures and listings, including contents entries. |
| Approval metadata | Still pending: supervisor, examiners and seminar date require actual academic information. |
| Originality declaration / near-duplicate title pages | Verification pending: official departmental guide link located, but share contents inaccessible (HTTP 401 on public WebDAV). Separate inherited cover/title page preserved; no declaration or signature fabricated. |
| Revision-history wording | Removed specified leftovers; substantive semantic distinctions retained. |
| Seven stages | Figure and prose use matching grouping. |
| Metrics | Abstracts and methodology consistently use accuracy, coverage, verification time and explanation size; application-fault metrics separate. |
| Language and citations | Clarified heading, topological search and instrumentation wording; italicized technical terms in Indonesian prose. Local plainnat adaptation uses dan/dkk./Dalam/hlm.; original titles retained. Official style conformity remains unverified. |
| Verification | Full multi-file proposal and diagram build passed; 45 pages, 18 resolved bibliography entries, no LaTeX warnings or overfull boxes. Representative list, diagram, external target and criteria pages visually inspected. |

The proposal remains for supervisor review. Formal evaluation results, full external fault feasibility, calibrated operational values and program-specific front-matter compliance are not claimed. Preliminary collection results are reported separately from formal evaluation.

## Subsequent clarity review — 5 October 2026

Applied priority items 1–8 and 12–16: one-page Indonesian/English abstracts; three research questions; explicit model-compatibility outcomes with inconclusive retained for evidence and resource limits; early S7 example and offline explanation; standard/custom instrumentation separation; PORnV namespace definitions; controlled-baseline framing; descriptive S5/S7 names; consistent Indonesian terminology; definition of formal-language words; reduced duplicate caveats.

Item 9 is discussion only: a deterministic single topological ordering remains an optional comparator. Items 10–11 and 17–23 are preserved: independent oracle validation, separate application labels, unchanged existential DFA semantics, completeness contract, honest novelty, inconclusive cutoffs, and deterministic explanations with full-graph fallback. No new formalism or required experiments were added.

Final proofreading and full build cover references, equations, captions, terminology, and representative PDF pages. Existing metadata/template/feasibility/calibration tasks remain pending.

## Pilot-aligned methodology update — 7 October 2026

Chapter I distinguishes the initial external target from final fault feasibility. Chapter III specifies the three SDK checkpoints, the `NoResponse` producer interpretation, explicit predecessor edges, both normal event orders, separate action-ledger reconciliation, phase-aware source freezing, broker offset evidence, and graceful collector closure. Completeness is limited to the declared business-event scope; the normal three-action gate is explicitly not a closure policy for missing/extra-action fault scenarios. Trusted action journals are not substituted for an independent business-fault oracle.

The implementation plan now follows the existing Go prototype. The schedule distinguishes preliminary collection work from the pending DFA implementation, independent labels, fault profiles and formal experiments. Detailed runs and controls remain in the pilot notes; the proposal includes only a short feasibility status. Pending academic names, seminar date and official template verification are preserved.

Verification: the full proposal compiled to 50 A4 pages with all 18 bibliography entries and cross-references resolved. The final log contains no warnings, overfull boxes or underfull boxes. The new checkpoint table/listing, closure procedure and feasibility pages were rendered and visually checked. Long table columns were adjusted for readable wrapping without changing research semantics.
