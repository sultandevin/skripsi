# Source verification

Reviewed on 2 October 2026. The uploaded idea draft was the substantive starting point; source titles, identifiers, and scope were checked against primary records where available.

| Source | Verification and use |
| --- | --- |
| Lamport (1978) | [Microsoft Research publication record](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/) confirms the paper, venue, year, and pages. Used for happened-before and partial ordering. |
| Sakai and Takahashi (2022) | Publisher-deposited DOI metadata confirms authors, title, pages 1–6, and complete DOI `10.1109/NOMS54207.2022.9789804`. The supplied draft's DOI was truncated. Publisher full-text access was unavailable; discussion is limited to the broad topic, without unsupported implementation or numerical claims. |
| Sun et al. (2024) | Publisher-deposited DOI metadata confirms the six authors, journal, volume 17(5), pages 2194–2209, and DOI `10.1109/TSC.2024.3399652`. Full-text access was unavailable. Discussion is limited to the paper's annotation-assisted, scenario-oriented inconsistency-checking focus. |
| Ding et al. (2025) | [USENIX publisher page and BibTeX](https://www.usenix.org/conference/nsdi25/presentation/ding) verify authors, paper scope, evaluation subjects, and pages. |
| Hackett and Beschastnikh (2025) | [Author-hosted published paper](https://fhackett.com/files/oopsla25-tracelink.pdf) verifies PGo/Modular PlusCal/TLA+/Go scope, Article 350, 33 pages, and DOI `10.1145/3763128`. |
| Weil-Kennedy et al. (2025) | [Author-submitted arXiv record](https://arxiv.org/abs/2511.00531) verifies four authors and clock-independent multitrace/automata focus. Added from the recent Thesis conversation and explicitly labeled a preprint. |
| OpenTelemetry traces | [Official concepts documentation](https://opentelemetry.io/docs/concepts/signals/traces/) supports trace/span/event terminology. |
| OpenTelemetry Tracing API | [Official specification](https://opentelemetry.io/docs/specs/otel/trace/api/) supports context/parent/link terminology. Proposal-specific causal interpretation is separately stated as a design contract. |
| Messaging conventions | [Official semantic conventions](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/) support producer/consumer context discussion. The document is marked development at review time, so experiment versions must be pinned. |
| Tracing SDK | [Official SDK specification](https://opentelemetry.io/docs/specs/otel/trace/sdk/) supports limitations associated with sampling and recording. |
| OTLP | [Official protocol specification](https://opentelemetry.io/docs/specs/otlp/) supports the choice of JSON export. Structural validity is distinguished from semantic completeness. |
| W3C Trace Context | [W3C Recommendation](https://www.w3.org/TR/trace-context/) supports propagating trace context; business workflow correlation remains an application requirement. |

For live documentation, `year = 2026` indicates the year accessed, not a claim about initial publication. All live-document bibliography entries include the access date. Prior conversations and local prototype documentation are context for the proposal, not peer-reviewed sources or experimental results.
