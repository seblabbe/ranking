Ultimate team ranking algorithm
===============================

Create the Ranking of USAU Open team from 2013 season. This was used in the
text in `Ranking Algorithms for Competitive Ultimate`__ published on Skyd
Magazine::

	sage -python ranking.py -p parameters_USAU_2013.json -o 2013_USAU-output

__ http://skydmagazine.com/2014/04/ranking-algorithms-competitive-ultimate/

Création du classement de la saison 2011-2012::

	sage -python ranking.py -p parameters_2011.json -o 2011-12-CQU4-output

Création du classement de la saison 2014-2015::

	sage -python ranking.py -p parameters_2014.json -o 2014-15-CQU4-output
