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
| Use causal prerequisite rules as the main semantics | This matches the draft's example requiring payment to causally precede shipping and the existing verifier. Existence of an accepted linear extension is explained separately; it is not equivalent to proving a causal prerequisite. This choice is provisional pending the user's response or supervisor review. |
| Add an inconclusive outcome | Missing telemetry or an ambiguous link cannot by itself establish an application violation. Completeness is an explicit controlled observation contract. |
| Treat business events as points | A span start must not be mislabeled as business completion. Parentage does not imply parent completion before a child. |
| Make additional instrumentation explicit | `porv.predecessors`, `porv.causal`, and completeness markers are application contracts rather than standard OpenTelemetry semantics. |
| Start with offline verification | Runtime data are collected during execution; a streaming monitor is not promised. |
| Use the same normalized inputs for both approaches | Only the relation used by ordering rules differs; count rules and evidence-quality checks are shared. |
| Keep the timestamp comparison honest | Independent concurrency alone need not cause false positives. Clock offsets and missing required causality are separate test conditions. |
| Require independent labels | Application scenario/facts or independent synthetic construction provide the oracle, rather than the evaluated verifier. |
| Distinguish independent runs and repeated timings | Timing repetition does not increase the number of independent accuracy observations. |
| Avoid global minimality claims | A causal slice provides context. Checking non-reachability still requires the full workflow graph. |
| Test SDK interoperability | The local demo emits explicit OTLP-shaped JSON; the proposal plans at least one real SDK-export path rather than claiming this already exists. |

## Pending academic metadata and experimental choices

| Item | Current treatment |
| --- | --- |
| Supervisor and examiners | `Belum ditetapkan` in `content/proposal/main.tex`; no names inferred from the reference. |
| Seminar date | `Belum ditetapkan`; draft wording avoids claiming a completed defense. |
| Research start and duration | Provisional B1–B6 schedule, without invented calendar dates. |
| Main rule interpretation | Recommended causal prerequisite interpretation drafted; the optional clarification remains open. |
| Experimental machine and final SDK/runtime versions | To be selected and recorded before official collection. |
| Replication count, size matrix, clock offsets | Explicit initial design choices for calibration, not supplied facts or finished results. |
| Official UGM guide | Not present in the reference checkout; layout follows the source template pending reconciliation with a supplied guide. |

No results, measured performance values, supervisor approvals, or completed experiments are fabricated. The current document is a proposal for review.
