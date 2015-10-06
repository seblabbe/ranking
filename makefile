all: maj

USAU2013:
	sage -python ranking.py -p parameters_USAU_2013.json -o 2013_USAU-output

cqu42011:
	sage -python ranking.py -p parameters_2011.json -o 2011-12-CQU4-output

cqu42014:
	sage -python ranking.py -p parameters_2014.json -o 2014-15-CQU4-output

cqu42015:
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2014.json
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015_v1.json
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015_v2.json
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015_v3.json
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015_v4.json
	cd 2011-12-CQU4 && sage -python ../ranking.py -p parameters_2015_v5.json

csv:
	sage-4.8 -python ranking.py --csv

html:
	rst2html.py classement.rst classement.html 

brute:
	rst2html.py brute.rst brute.html

text:
	rst2latex.py text.rst text.tex
	pdflatex text.tex
