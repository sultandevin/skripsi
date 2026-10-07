# UGM proposal workspace

> Can partial-order analysis of OpenTelemetry data reliably determine whether an asynchronous application execution is consistent with developer-defined workflow constraints, without relying on synchronized physical clocks across services, and under what conditions does it outperform timestamp-based verification?

LaTeX proposal for Sultan Devino Suyudi (23/521686/PA/22442): **Verifikasi Runtime Berbasis Partial Order pada Interaksi Layanan Asinkron Menggunakan OpenTelemetry**.

The research now checks whether at least one causally compatible event sequence is accepted by a developer-defined workflow state machine. Acceptance means consistency with that model. The existing Go causal-prerequisite prototype has not yet been extended to implement this search. Evaluation includes controlled cases, one external workflow from OpenTelemetry Demo 2.0.2, and synthetic graphs. Preliminary external runs established SDK checkpoint collection and bounded normal-run completeness; independent business-fault cases and formal verifier evaluation remain outstanding. Application-fault detection uses separate independent labels. See [CONTEXT.md](CONTEXT.md), [the acceptance decision](docs/adr/0001-existential-workflow-conformance.md), and [pilot results](docs/OTEL-PILOT-RESULTS.md).

The draft follows the reference's `content/proposal/` organization and four chapters. Supervisor, examiners, seminar date, and calendar schedule are still pending. The current schedule uses six relative months. See [docs/DRAFT-DECISIONS.md](docs/DRAFT-DECISIONS.md) for provisional research choices and [CHANGELOG.md](CHANGELOG.md) for major changes.

The studied reference is kept separately in `.reference/skripsi/`. See [REFERENCE-NOTES.md](REFERENCE-NOTES.md) for its structure, formatting, source organization, and the snapshot commit.

## WSL LaTeX setup

TeX Live 2026 is installed for this user at:

```text
/home/molly/.local/share/texlive/2026
```

Installed tools include pdfLaTeX, BibTeX, latexmk 4.88, XeLaTeX, LuaLaTeX, and MakeIndex. The proposal uses pdfLaTeX + BibTeX; latexmk handles repeated compilation automatically. Packages include Indonesian Babel support and hyphenation patterns, Times/Courier/Helvetica fonts, natbib, nomencl, tables, listings, hyperlinks, URL wrapping, enumitem, TikZ, standalone, and KOMA-Script's support for nomencl.

New interactive zsh sessions load the installation through `~/.config/texlive/env.sh`, sourced from `~/.zshrc`. `~/.profile` also loads it for shells that use that file. For an already-open terminal:

```sh
. "$HOME/.config/texlive/env.sh"
```

The Makefile also sets the TeX Live path directly, so builds do not depend on restarting the terminal. No administrator privileges or system package changes were required.

## Build and preview

Run these commands from this workspace:

```sh
make reference   # Compile the separate reference document
make proposal    # Compile diagrams, bibliography, and the full proposal
make proposal-diagrams # Regenerate diagram PDFs independently
make watch       # Rebuild our proposal as source files change; Ctrl+C to stop
make clean       # Remove auxiliary compilation files, retaining PDFs
```

Output paths:

- Reference PDF: `build/reference/main.pdf`.
- Proposal PDF: `content/proposal/main.pdf` (reviewable copy included in Git).
- Build PDF and auxiliary files: `build/proposal/` (ignored by Git).

The source layout mirrors the reference:

```text
content/proposal/
  main.tex
  main.pdf
  ugmskripsi.cls
  references.bib
  ugmplainnat.bst
  chapters/
    bab1-pendahuluan.tex
    bab2-penelitian-terkait.tex
    bab3-metodologi.tex
    bab4-jadwal-penelitian.tex
  figures/logougm.png
  diagrams/
    partial-order.tex / .pdf
    architecture-overview.tex / .pdf
    experiment-flow.tex / .pdf
```

Open the generated PDF in Codex or your usual PDF viewer. PDF rendering/text extraction tools (`pdftoppm`, `pdftotext`, and `pdfinfo`) already exist in WSL. SyncTeX files are generated to support editor/PDF navigation.

Use the WSL build for this project with chapter files, a custom class, bibliography, and images. `make watch` updates the PDF inside `build/proposal/`; run `make proposal` to refresh the committed review copy in `content/proposal/`. After editing a diagram's `.tex` source, run `make proposal-diagrams` to regenerate the PDF used by the main document.

## Recreate the local reference checkout

The reference is excluded from our own version history. To recreate the exact studied source:

```sh
mkdir -p .reference
git clone https://github.com/vityasyyy/skripsi.git .reference/skripsi
git -C .reference/skripsi checkout 1d4be15f23b5ba4e60425de5a0795f6452c1b6c0
make reference
```

## Add a LaTeX package later

```sh
tlmgr install package-name
```

Installation documentation: https://tug.org/texlive/quickinstall.html

Use `tlmgr` for this user-local installation rather than installing a second TeX distribution through the operating system.

## Verified on 2 October 2026

- Our revised proposal compiled successfully to 37 A4 pages, with all citations and cross-references resolved and no package warnings or overfull boxes.
- All three new diagrams compiled from their tracked standalone TikZ sources.
- Full reference compiled successfully: 55 A4 pages, with BibTeX references and cross-references resolved.
- All three standalone proposal diagrams compiled successfully from their TikZ sources into `build/reference-diagrams/`.
- PDF cover and table of contents were rendered and visually inspected.
- Indonesian hyphenation patterns are installed and enabled; no LaTeX package warnings or overfull boxes remained in the final reference log. Twelve underfull-box notices remain from the reference's paragraph layout.
- A second `make reference` reported the PDF up to date.
- New interactive zsh sessions find the installed tools.
- The reference checkout has no source changes.

## Template provenance

The UGM class and logo are copied from the reference snapshot recorded in `REFERENCE-NOTES.md`; the original class author attribution is retained. The approval-page wording is adapted for a draft with a pending seminar date. Main document content, diagrams, and bibliography are written for this topic. Hyperlink borders are hidden, and the bibliography is included in the contents. These changes do not certify compliance with an official guide absent from the reference repository.

## Review revisions verified on 5 October 2026

The revised proposal builds to 45 A4 pages with 18 resolved bibliography entries. The lists, matching methodology diagram, external-target section, and acceptance criteria were visually inspected. No LaTeX warnings, unresolved references, or overfull boxes remained. See [review actions](docs/REVIEW-ACTIONS.md) for completed changes and remaining metadata, template, feasibility, and calibration work. This is a revised proposal, not evidence that the proposed experiments have been completed.

## Clarity pass verified on 5 October 2026

Both abstracts now fit one page, with three research questions and model-compatibility outcome labels. Standard OTel context, business instrumentation, and PORnV-specific causal attributes are separated explicitly. Required experiments and existential DFA semantics are unchanged; the optional topological comparator is discussion only. The revised abstracts, namespace description, outcome table, and scenario table were visually checked.

## Pilot-aligned proposal verified on 7 October 2026

The proposal now describes the three external checkpoints, client success without broker acknowledgement, the two permitted normal event orders, and a bounded completeness procedure using separate action records, source phases, broker offsets and a closed collector snapshot. It distinguishes preliminary SDK collection from pending DFA verification and independent business-fault evaluation. The implementation plan follows the existing Go prototype.

The full proposal compiled to 50 A4 pages with 18 resolved bibliography entries, no LaTeX warnings, no unresolved references, and no overfull or underfull boxes. The new checkpoint table/listing, collection procedure and feasibility-status pages were visually inspected. Academic metadata and official template verification remain pending. The review copy is `content/proposal/main.pdf`.
