all: maj

USAU2013:
	cd 2013_USAU && sage -python ../ranking.py -t 3 -p parameters.txt *.csv

cqu42011:
	cd 2011-12-CQU4 && sage -python ../ranking.py -t 3 -p parameters_2011.txt *.csv

cqu42014:
	cd 2011-12-CQU4 && sage -python ../ranking.py -t 2 -p parameters_2014.txt *.csv
	cd 2011-12-CQU4 && sage -python ../ranking.py -t 3 -p parameters_2014.txt *.csv

csv:
	sage-4.8 -python ranking.py --csv

html:
	rst2html.py classement.rst classement.html 

brute:
	rst2html.py brute.rst brute.html

text:
	rst2latex.py text.rst text.tex
	pdflatex text.tex
