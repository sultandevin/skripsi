# Seminar proposal slides

Indonesian, 16:9 Beamer presentation of the current proposal in `content/proposal/`.
The main talk has a title slide and 20 content slides, followed by backup material
and selected references. The PDF is generated, not hand-edited.

## Build

From the repository root:

```sh
make presentation
```

- Source: `presentation/proposal/main.tex`
- Review PDF: `presentation/proposal/main.pdf`
- Auxiliary files: `build/presentation/`

Uses XeLaTeX, BibTeX, and latexmk. The presentation configuration is independent
of the proposal's pdfLaTeX configuration. On a minimal existing TeX Live setup,
install the additional template dependencies with:

```sh
tlmgr install beamer fontspec translator fancyvrb
```

Bibliography entries are read directly from `content/proposal/references.bib`.
The slide wording summarizes, rather than includes, the proposal chapters;
update it when the proposal's research decisions change. OpenTelemetry, trace,
span, and OTLP are introduced before the motivating example; partial order,
PORV, and DFA are explained when first used. Seminar date is omitted
because it is not yet confirmed. Targets and planned evaluation are not presented
as completed results; the preliminary external pilot is labeled separately.

## Template provenance

Reuses the **unofficial** UGM Beamer theme, Gama Sans fonts, and image assets from
`presentation/proposal/ugm-beamer-template/` in
<https://github.com/vityasyyy/skripsi> at commit
`1d4be15f23b5ba4e60425de5a0795f6452c1b6c0`, already available in the local
reference checkout. The upstream template is
<https://github.com/canggihpw/ugm-beamer-template>.
Its MIT license is retained in `LICENSE`; the vendored theme, fonts, and images
are unmodified. This is not a claim of official UGM template approval.

The deck adjusts title sizing, adds slide numbers, uses Latin Modern for math
and bibliography text, and substitutes Latin Modern dashes where Gama Sans lacks
the glyph. Assets are copied into this directory so the presentation does not
require the ignored `.reference/` checkout to build.
