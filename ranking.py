# coding=utf-8
r"""
AUTHOR: Sébastien Labbé, Fall 2011
"""
#*****************************************************************************
#       Copyright (C) 2010-2014 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from copy import deepcopy
from collections import defaultdict
import csv
from itertools import izip, izip_longest, count
import heapq

import locale
try:
    locale.setlocale(locale.LC_ALL, 'fr_CA.utf8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'fr_CA')

import datetime
today = datetime.datetime.today()

try:
    from sage.misc.table import table
except ImportError:
    from table import table

######################
# Should be in Sage
######################
def table_to_csv(self, filename, dialect='excel'):
    r"""
    """
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f, dialect=dialect)
        csv_writer.writerows(self._rows)
        print "Creation of file %s" % filename

######################
# Equipe
######################
class Equipe(object):
    def __init__(self, nom, provenance, counting_tournaments):
        r"""
        """
        self._nom = nom
        self._provenance = set()
        self.update_provenance(provenance)
        self._counting_tournaments = counting_tournaments
        self._positions = defaultdict(str)
        self._esprit = defaultdict(str)
        self._points = defaultdict(str)
        self._resultats = defaultdict(int)

    def update_provenance(self, provenance):
        r"""
        EXEMPLES::

            sage: e = Equipe("Berger", "Mtl", 2)
            sage: e.provenance()
            'Mtl'
            sage: e.update_provenance('Sherb,TR,Mtl')
            sage: e.provenance()
            'TR,Mtl,Sherb'
            sage: e.update_provenance('galaxie')
            sage: e.provenance()
            'galaxie,TR,Mtl,Sherb'
        """
        self._provenance.update(p.strip() for p in provenance.split(','))
        if '' in self._provenance: self._provenance.remove('')

    def nom(self):
        return self._nom
    def provenance(self):
        r"""
        EXEMPLES::

            sage: e = Equipe("Berger", "Mtl", 2)
            sage: e.provenance()
            'Mtl'
        """
        s = ",".join(self._provenance)
        #s = s.replace('è','e')
        #s = s.replace('é','e')
        return s
    def __repr__(self):
        r"""
        EXEMPLES::

            sage: e = Equipe("Berger", "Mtl", 2)
            sage: e
            Berger Pts:[] Tot:0
        """
        nom = self.nom()
        pts = sorted(self.points().values(), reverse=True)
        tot = self.total()
        return "{} Pts:{} Tot:{}".format(nom, pts, tot)

    def add_resultat(self, tournoi, position, points, esprit=0):
        r"""
        EXEMPLES::

            sage: e = Equipe("Berger", "Mtl", 2)
            sage: e.add_resultat('t1', 3, 35)
            sage: e.add_resultat('t2', 2, 20)
            sage: e.add_resultat('t3', 1, 100)
            sage: e
            Berger Pts:[100, 35, 20] Tot:135
        """
        nom = self.nom().decode('UTF-8')
        error_msg = u"tournoi(={}) deja present pour l'equipe {}".format(tournoi, nom)
        assert tournoi not in self._positions, error_msg
        assert tournoi not in self._esprit, error_msg
        assert tournoi not in self._points, error_msg
        assert tournoi not in self._resultats, error_msg
        self._positions[tournoi] = position
        self._points[tournoi] = points
        self._resultats[tournoi] = points
        if esprit:
            self._esprit[tournoi] = esprit
            self._resultats[tournoi] += esprit

    def positions(self):
        r"""
        EXEMPLES::

            sage: e = Equipe("Berger", "Mtl", 2)
            sage: e.add_resultat('t1', 3, 35)
            sage: e.add_resultat('t2', 2, 20)
            sage: e.add_resultat('t3', 1, 100)
            sage: e.positions()
            defaultdict(<type 'str'>, {'t2': 2, 't3': 1, 't1': 3})
        """
        return self._positions

    def points(self):
        return self._points

    def nb_tournois_participes(self):
        return len(self._positions)
    def pos_pts_es_ordonnes(self, tournois_ordered):
        rep = []
        for t in tournois_ordered:
            rep.append(self._positions[t])
            rep.append(self._points[t])
            rep.append(self._esprit[t])
        return rep

    def pts_ordonnes(self, tournois_ordered):
        rep = []
        for t in tournois_ordered:
            rep.append(self._points[t])
        return rep

    def __eq__(self, other):
        if not isinstance(other, Equipe):
            return False
        return self._nom == other._nom

    def total(self):
        L = self._resultats.values()
        L.sort(reverse=True)
        counting_tournaments = self._counting_tournaments
        S = sum(L[:counting_tournaments])
        # S2 = sum(heapq.nlargest(counting_tournaments, L))
        # assert S == S2, "erreur heapq.nlargest"
        return S

    def four_best(self):
        tournaments = self._resultats.keys()
        tournaments.sort(key=lambda a:self._resultats[a], reverse=True)
        L = []
        for t in tournaments:
            L.append((self._positions[t], self._resultats[t], t.long_name()))
        return L[:4]
        
    def __cmp__(self, other):
        return self.total() - other.total()

######################
# Tournoi
######################
class Tournoi(object):
    def __init__(self, filename, long_name, scale_id, date=None):
        r"""
        """
        self._filename = filename
        self._long_name = long_name
        self._scale_id = scale_id

    def __repr__(self):
        return "Tournoi %s" % self._long_name

    def __hash__(self):
        return hash(self._filename)
    def __iter__(self):
        filename = self._filename
        with open(filename, 'r') as f:
            for row in csv.reader(f):
                if len(row) == 0:
                    continue
                elif len(row) == 2:
                    position, nom = row
                    provenance = ""
                    esprit = False
                elif len(row) == 3:
                    position, nom, provenance = row
                    esprit = False
                elif len(row) == 4:
                    position, nom, provenance, esprit = row
                    error_msg = "esprit sportif mal ecrit pour %s" % self
                    assert esprit in ["", "esprit sportif"], error_msg
                else:
                    raise ValueError, "In file {}: Longueur dune ligne (={}) doit etre 2 ou 3 ou 4.".format(filename, row)
                yield int(position), nom, provenance, esprit

    def short_name(self):
        assert self._filename.endswith('.csv')
        return self._filename[:-4]

    def long_name(self):
        return self._long_name
######################
# Classement
######################
class Classement(object):
    def __init__(self, scales, counting_tournaments=3):
        r"""
        """
        self._counting_tournaments = counting_tournaments
        self._scales = scales
        self._equipes = {}
        self._tournois = []
        self._sorted_previous = []
        self._sorted_teams = []
        self._moves = {}
        self._division = ['AAA', 'AA', 'BB', 'CC', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    def __repr__(self):
        s = "Classement de %s equipes\n" % len(self)
        return s

    def __len__(self):
        return len(self._equipes)

    def __getitem__(self, name):
        return self._equipes[name]

    def division(self, i):
        return self._division[(i-1) // 16]

    def add_tournoi(self, tournoi):
        self._sorted_previous = self._sorted_teams
        self._tournois.append(tournoi)
        scale_id = tournoi._scale_id
        scale = self._scales[scale_id]
        for position, nom, provenance, esprit in tournoi:
            if nom in self._equipes:
                equipe = self._equipes[nom]
                equipe.update_provenance(provenance)
            else:
                equipe = Equipe(nom, provenance, self._counting_tournaments)
                self._equipes[nom] = equipe
            points = 0 if position >= len(scale) else scale[position]
            esprit_pts = 50 if esprit else 0
            equipe.add_resultat(tournoi, position, points, esprit_pts)
        self._sorted_teams = sorted(self._equipes.values(), reverse=True)
        self._moves[tournoi] = c.get_move_list()

    def get_previous_position(self, equipe):
        if equipe in self._sorted_previous:
            return self._sorted_previous.index(equipe)
        else:
            return None

    def get_position(self, equipe):
        return self._sorted_teams.index(equipe)

    def get_move(self, equipe):
        previous = self.get_previous_position(equipe)
        if previous is None:
            return None
        return previous - self.get_position(equipe) 

    def get_move_str(self, equipe):
        diff = self.get_move(equipe)
        if diff is None or diff == 0:
            return ''
        elif diff > 0:
            return '+{}'.format(diff)
        else:
            return '{}'.format(diff)

    def get_move_list(self):
        L = []
        for eq in c._sorted_teams:
            diff = c.get_move(eq)
            L.append(0 if diff is None else diff)
        return L

    def number_of_inversions(self, top=32):
        rows  = [("Tournoi", "Nombre d'inversions")]
        tot = 0
        for tournoi in self._tournois:
            move_list = self._moves[tournoi]
            #print tournoi, move_list[:top]
            moves = sum(abs(a) for a in move_list[:top])
            rows.append((tournoi, moves))
            tot += moves
        rows.append(('Total', tot))
        return table(rows=rows, header_row=True)._repr_()+"\n"

    def strength5(self, tournoi, best=5):
        r"""
        The best 5 teams of a tournaments finished in the top what overall?
        """
        L = sorted(self._equipes.values(), reverse=True)
        s = 0
        for i,e in enumerate(L):
            if tournoi in e._positions:
                s += 1
            if s == best:
                return i+1
    def strength20(self, tournoi, top=20):
        r"""
        How many of top 20 went to the tournament?
        """
        L = sorted(self._equipes.values(), reverse=True)
        return sum((1 for e in L[:top] if tournoi in e._positions))

    def tournament_size(self, tournoi):
        L = self._equipes.values()
        return sum((1 for e in L if tournoi in e._positions))

    def show(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        for e in L:
            print e, self.get_move_str(e)
    def print_equipe_alphabetiquement(self):
        L = self._equipes.keys()
        for nom in sorted(L):
            equipe = self._equipes[nom]
            print nom.ljust(40), equipe.provenance(), equipe._positions.keys()

    def statistiques_participation(self):
        L = [e.nb_tournois_participes() for e in self._equipes.values()]
        M = max(L)
        rows = [("Number of tournaments played", "Number of teams")]
        for i in range(1, M+1):
            rows.append( (i, L.count(i)) )
        return table(rows=rows, header_row=True)._repr_()+"\n"
    def latex_table(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        s = '\\begin{tabular}{c|c|c|c}\n'
        s += "Position & Équipe & Points & Variation \\\\ \n"
        s += "\\hline \n"
        for i, e in enumerate(L):
            s += "%s & %s & %s & %s \\\\ \n" % (i+1, e._nom, e.total(), self.get_move_str(e))
        s += '\\end{tabular}\n'
        return s

    def rst_table_avec_resultats(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        s = ""
        s += "+----------+----------------------------------+--------------------------------+--------+-----------+\n"
        s += "| Position | Équipe                           | Resultats                      | Points | Variation |\n"
        s += "+----------+----------------------------------+--------------------------------+--------+-----------+\n"
        for i, e in enumerate(L):
            s += "| %8s | %32s | %30s | %6s | %9s |\n" % (i+1, e._nom, e._positions, e.total(), self.get_move_str(e))
            s += "+----------+----------------------------------+--------------------------------+--------+-----------+\n"
        return s

    def rst_table(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        s = ""
        s += "+----------+----------------------------------+--------+-----------+\n"
        s += "| Position | Équipe                           | Points | Variation |\n"
        s += "+----------+----------------------------------+--------+-----------+\n"
        for i, e in enumerate(L):
            s += "| %8s | %32s | %6s | %9s |\n" % (i+1, e._nom, e.total(), self.get_move_str(e))
            s += "+----------+----------------------------------+--------+-----------+\n"
        return s

    def save_rst_table(self):
        filename = 'cqu4_classement_fictif.txt'
        f = open(filename, 'w')
        f.write(self.rst_table())
        f.close()
        print "Creation de %s " % filename

    def save_csv_table(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        title = ["Division", "Position", "Équipe", "Provenance"]
        title += ["Pos", "Pts", 'ES'] * len(self._tournois)
        title += ["Total", "Variation"]
        filename = 'classement.csv'
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(title)
            for i, e in enumerate(L):
                row = [self.division(i+1), i+1, e._nom, e.provenance()]
                row += e.pos_pts_es_ordonnes(self._tournois)
                row += [e.total(), self.get_move_str(e)]
                csv_writer.writerow(row)
            print "Creation de %s " % filename

    def save_csv_short_table(self, output_dir):
        L = self._equipes.values()
        L.sort(reverse=True)
        title = ["Division", "Position", "Équipe", "Provenance", "Total"]
        filename = today.strftime(u"resume_%Y_%m_%d.csv")
        with open(output_dir+"/"+filename, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(title)
            for i, e in enumerate(L):
                row = [self.division(i+1), i+1, e._nom, e.provenance(), e.total()]
                csv_writer.writerow(row)
            print "Creation de %s " % filename

    def sage_table(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        nb_tournois = len(self._tournois)

        T1 = ''
        T1 += "Mis à jour le %s.\n" % today.strftime(u"%d %B %Y")
        T1 += "\nNombre total d'équipes : %s\n\n" % len(c)
        T1 += self.statistiques_participation()

        rows = [("Tournaments considered", "Points for champion", "#teams getting points", 
                 "#teams", "Strength")]
        for T in self._tournois:
            scale = self._scales[T._scale_id]
            rows.append( (T.long_name(), scale[1], len(scale)-1, 
                          self.tournament_size(T), 
                          "5/%s and %s/20"%(self.strength5(T), self.strength20(T))))
        T2 = table(rows=rows,header_row=True)

        counting = self._counting_tournaments
        #row_header = ["Pos", "Pts", "#Tourn", "Team name", "Region"]
        #row_header += ['Best', '2nd best', '3rd best', '4th best (does not count)']
        row_header = ["Pos", "Pts", "Team name"]
        row_header += ['Best', '2nd best', '3rd best', '4th best'][:counting]
        row_header += ['Provenance']
        rows = [row_header]
        for i, e in enumerate(L):
            row = [i+1]
            row.append(e.total())
            #row.append(e.nb_tournois_participes())
            row.append(e._nom)
            bests = ["%s (%s) %s" % b for b in e.four_best()]
            if len(bests) < 4:
                bests += [""] * (4-len(bests))
            row.extend(bests[:counting])
            row.append(e.provenance())
            rows.append(row)
        T3 = table(rows=rows,header_row=True)
        #return "\n\n".join((T1, T2, T3))
        return (T1, T2, T3)

    def txt_table_provincial(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        nb_tournois = len(self._tournois)
        col_width       = [9, 9, 10, 6, 5, 23] + [4,6,4] * nb_tournois + [20]
        col_width_title = [9, 9, 10, 6, 5, 23] + [14]    * nb_tournois + [20]
        def line_str(line, col_width, left=[0,1,2,3], right=[]):
            L = []
            for i,t,w in zip(count(), line, col_width):
                t = str(t)
                if i in left:
                    L.append(t.ljust(w + nombre_car_accentues(t)))
                    #L.append(t.ljust(w))
                elif i in right:
                    L.append(t.rjust(w + nombre_car_accentues(t)))
                    #L.append(t.rjust(w))
                else:
                    L.append(t.center(w + nombre_car_accentues(t)))
                    #L.append(t.center(w))
            return "".join(L) + "\n"
        title = ["", "", "", "", "", ""]
        title += [T.long_name() for T in self._tournois]
        title += [""]
        s = ''
        s += "Mis à jour le %s.\n" % today.strftime(u"%d %B %Y")
        s += "\nStatistiques de participation :\n\n"
        s += self.statistiques_participation()
        s += "Nombre total d'équipes : %s\n" % len(c)
        souligne = ['-'*(i-1) for i in col_width_title]
        subtitle = ["Division", "Position"]
        subtitle += ["Points", "Var", "NbTP"]
        subtitle += ["Équipe"]
        subtitle += ['Pos', 'Pts', 'ES']  * nb_tournois
        subtitle += ["Provenance"]
        titre_str = ''
        titre_str += line_str(title, col_width_title,left=range(16))
        titre_str += line_str(souligne, col_width_title, left=range(16))
        titre_str += line_str(subtitle, col_width, left=range(7))
        titre_str += line_str(souligne, col_width_title, left=range(16))
        s += titre_str
        for i, e in enumerate(L):
            line = [self.division(i+1), i%16 +1]
            line += [e.total(), self.get_move_str(e)]
            line += [e.nb_tournois_participes()]
            line += [e._nom]
            line += e.pos_pts_es_ordonnes(self._tournois)
            line += [e.provenance()]
            if i > 0 and i % 16 == 0:
                s += "\n"
                #s += titre_str
            s += line_str(line, col_width, left=range(7))
        return s
    def txt_table_partiel(self, L, categorie_name):
        L = [self[nom] for nom in L]
        L.sort(reverse=True)
        nb_tournois = len(self._tournois)
        col_width       = [9, 9, 10, 6, 23, 28] + [4,6,4] * nb_tournois
        col_width_title = [9, 9, 10, 6, 23, 28] + [14]    * nb_tournois
        def line_str(line, col_width, left=[0,1,2,3], right=[]):
            L = []
            for i,t,w in zip(count(), line, col_width):
                t = str(t)
                if i in left:
                    #L.append(t.ljust(w + nombre_car_accentues(t)))
                    L.append(t.ljust(w))
                elif i in right:
                    #L.append(t.rjust(w + nombre_car_accentues(t)))
                    L.append(t.rjust(w))
                else:
                    #L.append(t.center(w + nombre_car_accentues(t)))
                    L.append(t.center(w))
            return "".join(L) + "\n"
        title = ["", "", "", "", "", ""]
        title += [T.long_name() for T in self._tournois]
        s = ''
        souligne = ['-'*(i-1) for i in col_width_title]
        subtitle = ["Division", "Position"] 
        subtitle += ["Points", "Var"]
        subtitle += ["Équipe", "Provenance"]
        subtitle += ['Pos', 'Pts', 'ES']  * nb_tournois
        titre_str = ''
        titre_str += line_str(title, col_width_title,left=range(16))
        titre_str += line_str(souligne, col_width_title, left=range(16))
        titre_str += line_str(subtitle, col_width, left=range(6))
        titre_str += line_str(souligne, col_width_title, left=range(16))
        s += titre_str
        for i, e in enumerate(L):
            line = [categorie_name, i+1] 
            line += [e.total(), self.get_move_str(e)]
            line += [e._nom, e.provenance()]
            line += e.pos_pts_es_ordonnes(self._tournois)
            s += line_str(line, col_width, left=range(6))
        return s
    def save_txt_table_provincial(self, filename):
        s = self.txt_table_provincial()
        with open(filename, 'w') as f:
            f.write(s)
        print "Creation de %s " % filename

    def save_sage_table(self, filename):
        (T1, T2, T3) = self.sage_table()
        s = "\n\n".join((T1, T2.__repr__(), T3.__repr__()))
        with open(filename, 'w') as f:
            f.write(s)
        print "Creation de %s " % filename

    def save_csv_summary(self, filename):
        (T1, T2, T3) = self.sage_table()
        table_to_csv(T3, filename)

    def save_txt_table_partiel(self, L, categorie_name):
        s = self.txt_table_partiel(L, categorie_name)
        filename = 'classement_%s.txt' % categorie_name
        with open(filename, 'w') as f:
            f.write(s)
        print "Creation de %s " % filename

################################
# Nombre de caracteres accentues
################################
def nombre_car_accentues(string):
    r"""
    EXEMPLES::

        sage: nombre_car_accentues("Montreal")
        0
        sage: nombre_car_accentues("Mont,re,a,l")
        0
    """
    i = 0
    for a in string:
        if not a.isalnum() and not a.isspace() and not a in "-/!?'+,*":
            i += 1
    #assert i % 2 == 0, "nombre pair daccents (%s)" % string
    return i# / 2

################################
# Script
################################
from optparse import OptionParser
import os

if __name__ == '__main__':

    # set the parser
    usage = u"""sage -python ranking.py -p parameters_2014.json"""

    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--alphabetique",
                      action="store_true", dest="alphabetique",
                      help=u"Afficher les équipes alphabétiquement")
    parser.add_option("-c", "--csv",
                      action="store_true", dest="csv",
                      help=u"Créer le fichier csv global")
    parser.add_option("-i", "--inversions",
                      action="store", type="int",
                      dest="inversions", default=0,
                      help=(u"Afficher le nombre d'inversions par tournois "
                      u"pour les équipes du top INVERSIONS"))
    parser.add_option("-n", "--nombre",
                      action="store_true", dest="nombre",
                      help=u"Afficher le nombre d'équipes")
    parser.add_option("-s", "--stat",
                      action="store_true", dest="stat",
                      help=u"Afficher statistiques sur la participation")
    parser.add_option("-p", "--parameters",
                      action="store", type="string",
                      dest="parameters",
                      help=u"Tournaments parameters (.json file)")
    parser.add_option("-o", "--output_dir",
                      action="store", type="string",
                      default="OUTPUT",
                      dest="output_dir",
                      help=u"The output directory")
    (options, args) = parser.parse_args()

    #print options
    #print args

    all_tournaments = {}
    with open(options.parameters, 'r') as f:
        import json
        D = json.load(f)

    scales = D['scales']
    counting_tournaments = D['counting_tournaments']
    c = Classement(scales, counting_tournaments)
    for T in D['tournaments']:
        filename = T['file']
        name = T['name']
        scale_id = T['scale_id']
        T = Tournoi(filename, name, scale_id)
        c.add_tournoi(T)

    if options.alphabetique:
        c.print_equipe_alphabetiquement()
    elif options.csv:
        c.save_csv_short_table(options.output_dir)
    elif options.nombre:
        print len(c)
    elif options.inversions:
        print c.number_of_inversions(top=options.inversions)
    elif options.stat:
        print c.statistiques_participation()
    else:
        assert options.parameters.endswith('.json'), "parameter file extension must be .json"
        param = options.parameters[:-5]
        output_dir = options.output_dir
        filename  = u"{}/classement_{}.csv".format(output_dir, param)
        c.save_csv_summary(filename)

