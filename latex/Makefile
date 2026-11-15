TARGET = TCC_FCTE.pdf

XELATEX = xelatex
BIBTEX = bibtex

VERSION = 0.1.0

FIXOS_DIR = fixos
FIXOS_SOURCES = informacoes.tex fichaCatalografica.tex \
		folhaDeAprovacao.tex pacotes.tex comandos.tex setup.tex	\
		listasAutomaticas.tex indiceAutomatico.tex

FIXOS_FILES = $(addprefix $(FIXOS_DIR)/, $(FIXOS_SOURCES))

EDITAVEIS_DIR = editaveis
EDITAVEIS_SOURCES = informacoes.tex resumo.tex abstract.tex estrutura-revisao.tex \
					listaapendices.tex abreviaturas.tex introducao.tex \
					referencialteorico.tex metodologia.tex desenvolvimento.tex consideracoes.tex textoepostexto.tex \
					elementosdotexto.tex elementosdopostexto.tex \
					apendices.tex anexos.tex

EDITAVEIS_FILES = $(addprefix $(EDITAVEIS_DIR)/, $(EDITAVEIS_SOURCES))

MAIN_FILE = tcc.tex
AUX_FILE  = $(addsuffix .aux, $(basename $(MAIN_FILE)))
PDF_FILE  = $(addsuffix .pdf, $(basename $(MAIN_FILE)))

SOURCES = $(FIXOS_FILES) $(EDITAVEIS_FILES)
FIGURAS = $(wildcard figuras/*.eps)

.PHONY: all clean dist-clean

all: 
	@make $(TARGET)
     
$(TARGET): $(MAIN_FILE) $(SOURCES) fixos/customizacoes.sty bibliografia.bib $(FIGURAS)
	$(XELATEX) -interaction=nonstopmode -halt-on-error $(MAIN_FILE)
	$(BIBTEX) $(AUX_FILE)
	$(XELATEX) -interaction=nonstopmode -halt-on-error $(MAIN_FILE)
	$(XELATEX) -interaction=nonstopmode -halt-on-error $(MAIN_FILE)
	@cp $(PDF_FILE) $(TARGET)

clean:
	rm -f *~ *.xdv *.backup *.aux *.log
	rm -f *.lof *.loq *.lot *.bbl *.blg *.brf *.toc *.out *.idx
	rm -f *.pdf
	
dist: clean
	tar vczf tcc-fga-latex-$(VERSION).tar.gz *

dist-clean: clean
	rm -f $(PDF_FILE) $(TARGET)
