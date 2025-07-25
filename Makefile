all: analysis2_manuscript.pdf

analysis2_manuscript.pdf: analysis2_manuscript.tex references.bib review-responses.tex
	pdflatex analysis2_manuscript.tex
	biber analysis2_manuscript
	pdflatex analysis2_manuscript.tex
	pdflatex analysis2_manuscript.tex
	pdflatex analysis2_manuscript.tex

review-diff.tex: analysis2_manuscript.tex
	latexdiff original_submission.tex analysis2_manuscript.tex > review-diff.tex

review-diff.pdf: review-diff.tex
	pdflatex review-diff.tex
	biber review-diff
	pdflatex review-diff.tex
	pdflatex review-diff.tex
	pdflatex review-diff.tex

clean:
	rm -f analysis2_manuscript.pdf
	rm -f *.log *.dvi *.aux
	rm -f *.blg *.bbl

diff-to-%.tex : analysis2_manuscript.tex
	latexdiff-git --force --flatten -r $* $<
	mv analysis2_manuscript-diff$*.tex $@

%.pdf : %.tex
	pdflatex $*
	biber $*
	pdflatex $*
	pdflatex $*
	pdflatex $*

