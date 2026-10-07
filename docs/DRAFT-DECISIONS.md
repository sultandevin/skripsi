# Proposal decisions and pending information

Recorded on 2 October 2026 (Asia/Jakarta). This file is an editorial record, not an instruction embedded in the uploaded document.

## Input and accessible context

- Primary input: `/mnt/c/Users/devino suyudi/Downloads/draft penelitian okt 26.pdf`, five pages. Its PDF metadata reports creation on 14 September 2026; the supplied filename is preserved in this record.
- The Thesis project was accessible. **Create Bab I II Latex PDF** confirms the Indonesian/English title and the prior draft direction, and points to a previous standalone Bab I–II draft. That older PDF/source was not retrieved or copied into this proposal.
- **Explain RPRC and DPIs** supports the distinction between application interactions and consensus protocol implementations. Only relevant readable messages were used; opaque content-reference placeholders were not treated as retrieved content.
- Local supporting context: `/home/molly/university/pornv/README.md`, `docs/decisions.md`, and demo/evaluation documentation. Those files were read without changes. They describe an existing causal verifier and a controlled demo, not completed thesis evidence or a timestamp comparison.
- The reference class, chapter order, and layout were studied previously. Its other author's research content was not reused.

## Research choices in this draft

| Choice | Rationale and scope |
| --- | --- |
| Keep the supplied title | It states the method, application interaction target, and observation source. |
| Accept an observation if an allowed compatible sequence exists | User confirmed existential workflow conformance on 2 October: at least one topological ordering must be accepted by the developer-defined state machine. This follows Section E, step 5 of the idea draft and supersedes the first proposal's causal-prerequisite interpretation. Acceptance is consistency, not proof of actual causal enforcement or universal safety. |
| Add an inconclusive outcome | Missing telemetry or an ambiguous link cannot by itself establish an application violation. Completeness is an explicit controlled observation contract. |
| Treat business events as points | A span start must not be mislabeled as business completion. Parentage does not imply parent completion before a child. |
| Make additional instrumentation explicit | `pornv.predecessors`, `pornv.causal`, and completeness markers are application contracts rather than standard OpenTelemetry semantics. |
| Start with offline verification | Runtime data are collected during execution; a streaming monitor is not promised. |
| Use the same normalized inputs for both approaches | Only the relation used by ordering rules differs; count rules and evidence-quality checks are shared. |
| Keep the timestamp comparison honest | Independent concurrency alone need not cause false positives. Clock offsets and missing required causality are separate test conditions. |
| Require independent labels | Independent enumeration/model checking or known constructions label observation consistency; application facts separately label actual business faults. Neither label comes from the evaluated verifier. |
| Distinguish independent runs and repeated timings | Timing repetition does not increase the number of independent accuracy observations. |
| Avoid global minimality claims | A displayed failed sequence cannot establish existential rejection. Exhaustive search on the full graph provides the conclusion; event slices provide context, with full-graph fallback if needed. |
| Test SDK interoperability | The local demo emits explicit OTLP-shaped JSON; the proposal plans at least one real SDK-export path rather than claiming this already exists. |

## Pending academic metadata and experimental choices

| Item | Current treatment |
| --- | --- |
| Supervisor and examiners | `Belum ditetapkan` in `content/proposal/main.tex`; no names inferred from the reference. |
| Seminar date | `Belum ditetapkan`; draft wording avoids claiming a completed defense. |
| Research start and duration | Provisional B1–B6 schedule, without invented calendar dates. |
| Main rule interpretation | Resolved by the user: accept if at least one compatible sequence is allowed. State-machine syntax, application-specific models, and search limits remain implementation choices to calibrate. |
| Experimental machine and final SDK/runtime versions | To be selected and recorded before official collection. |
| Replication count, size matrix, clock offsets | Explicit initial design choices for calibration, not supplied facts or finished results. |
| Official UGM guide | Not present in the reference checkout; layout follows the source template pending reconciliation with a supplied guide. |

No results, measured performance values, supervisor approvals, or completed experiments are fabricated. The current document is a proposal for review.

## Recheck against the supplied idea draft

Section E (page 3) explicitly proposes checking whether an execution exists that is consistent with both the partial order and protocol rules, and permits small state machines as well as simple dependencies. This supports workflow-sequence conformance as the intended direction. Its adjacent example instead requires an observed causal predecessor; the two statements can disagree when payment and shipping are unordered in the observed graph.

Section F (page 3) originally lists detection correctness (including false positives and false negatives), verification time, and counterexample size. Decision coverage and instrumentation effort were later recommendations, not original draft metrics. The user has now confirmed existential acceptance, and the LaTeX proposal describes the corresponding state-machine search. That verifier has not yet been implemented. External application selection and instrumentation remain pending; the evaluation now includes independent open-source applications alongside the controlled demo and synthetic graphs.

## Review revisions agreed on 5 October 2026

- Workflow conformance remains the primary objective; application-fault detection is a required separate practical evaluation. Acceptance respects every recorded causal dependency and does not establish actual enforcement of every prerequisite.
- S3 is a design-invariance check. The paired experiment measures changes in baseline decisions against the independent oracle, rather than claiming timestamp invariance proves better application-fault detection.
- Correctness gates require 100% agreement without abstain on the predefined complete small-graph suite, expected evidence-failure/cutoff outcomes, deterministic canonical outputs, one real SDK export path, and one external workflow. Operational targets are set in calibration and frozen before official collection; no invented timeout threshold or universal superiority requirement.
- One external application is required. Named target: OpenTelemetry Demo 2.0.2, commit `63649d6d6a59de88fb421b88c3c3a6185b6d21ad`, Apache-2.0; checkout publishes orders through Kafka and accounting consumes/logs them in this revision. Static source review is complete; execution, correlation, instrumentation, and independent fault labeling remain feasibility work. Current documentation's PostgreSQL behavior is not assumed for this older revision.
- An external replacement must be documented and frozen before experiments if the target is infeasible. A second application is optional. Cut optional second-app work, expanded large stress tests, and extra timing variations in that order. No full Cartesian product of experimental factors is promised.
- Added applicable table/figure/listing lists and aligned the seven stages. Local bibliography wording follows the Indonesian document while retaining original source titles and metadata.
- Official front-matter verification remains incomplete: the department's academic-documents page links the guide/template to an ownCloud share that was inaccessible during review. No originality declaration or removal of the separate cover/title page is justified from retrieved program guidance. Academic names and seminar date remain pending.

## Clarity pass agreed on 5 October 2026

- Shortened both abstracts to the core research story and reduced the research questions to three. Explanation work remains an objective and part of evaluation rather than a fourth compound question.
- Indonesian prose uses alur kerja, urutan parsial, mesin keadaan/keadaan, peristiwa, and kesalahan aplikasi. English equivalents are introduced where useful; standard OpenTelemetry and formal notation identifiers remain intact.
- Verifier outcomes are now **Kompatibel dengan model / Tidak kompatibel dengan model / Tidak dapat disimpulkan**. The third label is retained because resource cutoffs do not necessarily mean evidence is insufficient. Labels changed; existential acceptance and all evidence/search gates did not.
- The researcher-defined attribute namespace is **pornv**, following the user-supplied project name **PORnV**. `pornv.predecessors` carries predecessor event IDs; `pornv.causal` marks explicitly contracted causal links. This supersedes the proposal's `porv.*` examples, not the separate prototype implementation. Final serialization remains an implementation/calibration choice.
- Added a concise standard OTel/business-instrumentation/extra-causal-metadata boundary; introduced offline runtime verification earlier; defined formal-language “kata”; renamed S5 and S7.
- Timestamp sorting is explicitly a controlled comparison, not a state-of-the-art claim. A single deterministic topological ordering is discussed as an optional comparator only; no extra mandatory experiment or algorithm is added.
- Oracle agreement remains implementation validation. Empirical conclusions focus on decision changes, costs, evidence quality, and independently labeled application faults. Removed redundant acceptance caveats outside the designated interpretation sections.

## Proposal aligned with the execution pilot — 7 October 2026

- The verifier implementation plan uses Go to extend the actual preliminary prototype. The prior TypeScript/Bun plan is superseded; existential DFA search remains unimplemented.
- OpenTelemetry Demo 2.0.2 is the initial external target. SDK collection, identities and bounded normal-run completeness have been exercised. Business-fault feasibility is still unresolved, so the documented replacement procedure remains applicable before official collection.
- The normal external model accepts `acp` and `apc`: attempted publication precedes client-reported success and accounting processing, while the two successors are unordered. Client success under `sarama.NoResponse` is not a broker acknowledgement. A repeated delivery is not inherently a business fault.
- Completeness covers only declared event types, one order, and a recorded collection boundary. Separate synced action journals, the accounting phase marker, source state, broker offsets and closed exporter snapshots support the pilot collection gate. Journals share trusted action instrumentation with the telemetry points and are not independent business-state oracles.
- Missing/extra business-action scenarios require separate closure profiles. Collection completeness must not require DFA acceptance or the expected normal action count. Unsupported closure stays inconclusive.
- Preliminary execution results are feasibility evidence. They neither satisfy the end-to-end SDK/verifier acceptance criterion nor supply a formal comparison or independently verified application-fault verdict. Detailed run results stay outside the proposal.
