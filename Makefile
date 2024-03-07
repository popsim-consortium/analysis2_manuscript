all: analysis2_manuscript.pdf

analysis2_manuscript.pdf: analysis2_manuscript.tex references.bib
	pdflatex analysis2_manuscript.tex
	bibtex analysis2_manuscript
	pdflatex analysis2_manuscript.tex
	pdflatex analysis2_manuscript.tex
	pdflatex analysis2_manuscript.tex

clean:
	rm -f analysis2_manuscript.pdf
	rm -f *.log *.dvi *.aux
	rm -f *.blg *.bbl