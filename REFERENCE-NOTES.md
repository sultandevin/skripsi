# Proposal reference study

Studied on 2 October 2026. The user confirmed that our proposal will use the same UGM Computer Science format.

Source: https://github.com/vityasyyy/skripsi
Entry point: `content/proposal/main.tex`
Snapshot commit: `1d4be15f23b5ba4e60425de5a0795f6452c1b6c0`
Local reference checkout: `.reference/skripsi/` (excluded from our future Git history).

## Document order

1. Cover (`\cover`).
2. Indonesian title page (`\titlepageind`).
3. Approval page (`\approvalpage`).
4. Table of contents (`\tableofcontents`).
5. Indonesian abstract, followed by keywords (`\abstractind` / `\endabstractind`).
6. English abstract, followed by keywords (`\abstracteng` / `\endabstracteng`).
7. BAB I — PENDAHULUAN.
8. BAB II — PENELITIAN TERKAIT.
9. BAB III — METODE DAN RANCANGAN PENELITIAN.
10. BAB IV — JADWAL PENELITIAN.
11. DAFTAR PUSTAKA.

The actual proposal has no declaration, dedication, preface, lists of figures or tables, results chapter, conclusion chapter, or appendices. It includes both abstracts; this is relevant because the reference's guidance distinguishes examples from institutional requirements.

## Chapter structure and writing approach

BAB I contains Latar Belakang, Rumusan Masalah, Batasan Masalah, Tujuan Penelitian, Manfaat Penelitian, and Sistematika Penulisan. The background develops context, a practical problem, evidence from previous studies, a research gap, and the proposed investigation. The problem, boundaries, objectives, and benefits should agree with one another.

BAB II moves from key concepts and terminology to relevant prior studies, a comparison of their limitations, methodological background, and an explicit research gap. It contains a literature comparison table. Section names inside this chapter depend on our topic.

BAB III contains the general research description, methodology and flowchart, design/architecture, variables, materials/environment/data, procedures, evaluation, analysis, and validity/reliability considerations. The reference is a controlled empirical comparison of manual deployment and GitOps, so its interventions, repetitions, metrics, operator controls, and statistics belong to that research design. Our own method and subsections must follow our topic rather than inherit those choices automatically.

BAB IV uses a monthly Gantt-style table and explanations of each activity. The reference has a six-month schedule; our dates and duration remain to be supplied.

## Class and formatting

- Class: `\documentclass[proposal,indonesia]{ugmskripsi}`.
- Base class: `report`, A4 paper, 12-point text.
- Fonts: `times` with T1 encoding; body uses 1.5 spacing by default, abstracts use single spacing.
- Text block: 14.3 cm wide by 22 cm high, with a 4 cm left margin. Other page offsets are set directly in the class, rather than through `geometry`.
- Chapters use Roman numerals; sections use decimal chapter/section numbering, such as `1.1` and `1.1.1`.
- Preliminary pages use Roman page numbers; Arabic numbering starts after the English abstract.
- Figures, tables, and equations use chapter-based numbering.
- Class provides Indonesian headings and switches language for the English abstract.
- Cover requires `figures/logougm.png` in this reference, despite README examples mentioning a PDF logo.
- Default institutional text is Universitas Gadjah Mada, Fakultas Matematika dan Ilmu Pengetahuan Alam, Yogyakarta.

Metadata in `main.tex`: Indonesian and English titles, full name, NIM, degree, degree abbreviation, submission year, program, department, supervisor, two examiners, and examination date. Those values remain pending for our proposal.

## Source organization and compilation

`main.tex` holds metadata, packages, preliminary pages, both abstracts, chapter includes, and bibliography declaration. Each chapter is a separate file under `chapters/`. References belong in `references.bib`; illustrations belong in `figures/` and `diagrams/`; the UGM class sits next to `main.tex`.

Bibliography uses BibTeX, `natbib` with author–year citations, and `plainnat`. Use `\citep{key}` for parenthetical citations and `\citet{key}` for narrative citations. This proposal does not require Biber.

The original build sequence is pdfLaTeX → BibTeX → pdfLaTeX → pdfLaTeX. Our `latexmk` setup automates the necessary passes and creates SyncTeX data for source/PDF navigation.

Packages cover Indonesian/English language, mathematics, tables, listings, links, wrapping long URLs, lists, and TikZ diagrams. The three proposal diagrams are separate `standalone` sources whose PDFs are already tracked and are embedded in Chapter III. They can be regenerated separately.

## Reference limitations

The reference's AGENTS.md names `examples/pedoman_ta.pdf`, `contoh_proposal.pdf`, and `contoh_skripsi.pdf`, but those files are excluded from Git and absent from this checkout. The notes above describe the actual class and proposal sources; they do not certify compliance with a current official UGM guide. If an updated guide is supplied later, reconcile it with this template before submission.

The previous author's identity, topic, citations, dates, diagrams, and methodological claims are reference material. Our proposal content will be written after the user supplies the topic.

The reference uses the default visible hyperlink borders in its table of contents and citations. Its class also adds no bibliography entry to the table of contents. These are source behaviors to consider when preparing our own draft, rather than compilation failures.
