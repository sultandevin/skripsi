SHELL := /bin/sh
ROOT := $(abspath .)
TEXLIVE_BIN ?= $(HOME)/.local/share/texlive/2026/bin/x86_64-linux
export PATH := $(TEXLIVE_BIN):$(PATH)

.PHONY: help reference proposal proposal-diagrams watch clean

help:
	@echo 'make reference  Compile the separate reference proposal'
	@echo 'make proposal   Compile our proposal once proposal/main.tex exists'
	@echo 'make proposal-diagrams  Regenerate the proposal diagrams'
	@echo 'make watch      Rebuild our proposal whenever its sources change'
	@echo 'make clean      Remove generated LaTeX files while keeping PDFs'

reference:
	@test -f .reference/skripsi/content/proposal/main.tex || { echo 'Reference checkout is missing; see README.md.'; exit 1; }
	mkdir -p build/reference/chapters
	latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -outdir="$(ROOT)/build/reference" .reference/skripsi/content/proposal/main.tex

proposal: proposal-diagrams
	@test -f content/proposal/main.tex || { echo 'Proposal source is missing.'; exit 1; }
	mkdir -p build/proposal/chapters
	latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -outdir="$(ROOT)/build/proposal" content/proposal/main.tex
	cp build/proposal/main.pdf content/proposal/main.pdf

proposal-diagrams:
	mkdir -p build/proposal-diagrams
	@for diagram in partial-order architecture-overview experiment-flow; do \
		latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -outdir="$(ROOT)/build/proposal-diagrams" "content/proposal/diagrams/$$diagram.tex" || exit 1; \
		cp "build/proposal-diagrams/$$diagram.pdf" "content/proposal/diagrams/$$diagram.pdf" || exit 1; \
	done

watch: proposal-diagrams
	@test -f content/proposal/main.tex || { echo 'Proposal source is missing.'; exit 1; }
	mkdir -p build/proposal/chapters
	latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -pvc -view=none -outdir="$(ROOT)/build/proposal" content/proposal/main.tex

clean:
	@if test -f .reference/skripsi/content/proposal/main.tex; then latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -c -outdir="$(ROOT)/build/reference" .reference/skripsi/content/proposal/main.tex; fi
	@if test -f content/proposal/main.tex; then latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -c -outdir="$(ROOT)/build/proposal" content/proposal/main.tex; fi
	@for diagram in partial-order architecture-overview experiment-flow; do \
		latexmk -norc -r "$(ROOT)/.latexmkrc" -cd -c -outdir="$(ROOT)/build/proposal-diagrams" "content/proposal/diagrams/$$diagram.tex" || exit 1; \
	done
