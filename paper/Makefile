all: tcp-congestion.tex tcp-body.tex tcp-congestion.bib
	pdflatex tcp-congestion.tex	

spelling:
	aspell -c -t tcp-congestion.tex
	aspell -c -t tcp-body.tex

references:
	pdflatex tcp-congestion.tex
	bibtex tcp-congestion.aux
	pdflatex tcp-congestion.tex
	pdflatex tcp-congestion.tex

clean:
	rm -f *.aux *.log
