all: maj

USAU2013:
	cd 2013_USAU && sage -python ../ranking.py -p parameters.json

cqu42011:
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2011.json

cqu42014:
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2014.json

cqu42015:
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015.json
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015_v2.json

csv:
	sage-4.8 -python ranking.py --csv

html:
	rst2html.py classement.rst classement.html 

brute:
	rst2html.py brute.rst brute.html

text:
	rst2latex.py text.rst text.tex
	pdflatex text.tex
