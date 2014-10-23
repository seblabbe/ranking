Ultimate team ranking algorithm
===============================

Create the Ranking of USAU Open team from 2013 season. This was used in the
text in `Ranking Algorithms for Competitive Ultimate`__ published on Skyd
Magazine::

    cd 2013_USAU 
    python ../ranking.py -t 3 -p parameters.txt *.csv

__ http://skydmagazine.com/2014/04/ranking-algorithms-competitive-ultimate/

Création du classement de la saison 2011-2012::

    cd 2011-12-CQU4 
    python ../ranking.py -t 3 -p parameters_2011.txt *.csv

Création du classement de la saison 2011-2012 avec les nouveaux paramètres de
2014::

    cd 2011-12-CQU4 
    python ../ranking.py -t 3 -p parameters_2014.txt *.csv

Création du classement de la saison 2011-2012 avec les nouveaux paramètres de
2014 en comptant seulement la somme des deux meilleurs résultats::

    cd 2011-12-CQU4   
    python ../ranking.py -t 2 -p parameters_2014.txt *.csv
