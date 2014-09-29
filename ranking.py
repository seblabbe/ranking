#!/opt/local/bin/python2.6
# coding=utf-8
r"""
AUTHOR: Sébastien Labbé, Fall 2011
"""

from copy import deepcopy
from collections import defaultdict
import csv
from itertools import izip, izip_longest, count
import heapq

import locale
locale.setlocale(locale.LC_ALL, 'fr_FR')
import datetime
today = datetime.datetime.today()

from table import table


#TOURNOIS = ["Oktober Disk","Movember","Fun-E-Nuf","Bye Bye","Bonne année", "La Flotte","Coup de Foudre","La Virée","Mars Attaque", "Tournoi FUL"]
TOURNOIS = ["Oktober Disk","Movember","Fun-E-Nuf","Bye Bye","Bonne année", "La Flotte","Coup de Foudre","La Virée","Mars Attaque"]

######################
# Systeme
######################
class Systeme(object):
    def __init__(self):
        self._scale = {}

        #CQU4 2011
        self._scale[(1000,50)] = [0, 1000, 938, 884, 835, 791, 750, 711, 675, 641, 609, 578, 549, 521, 494, 469, 444, 421, 399, 377, 356, 336, 317, 299, 281, 264, 248, 232, 217, 202, 188, 174, 161, 149, 137, 125, 114, 103, 93, 83, 74, 65, 57, 48, 41, 33, 26, 19, 13, 7, 1]
        self._scale[(400,24)] = [0, 400, 355, 317, 285, 256, 230, 206, 184, 164, 146, 129, 114, 99, 86, 74, 63, 52, 43, 34, 26, 19, 12, 6, 1]
        self._scale[(800,32)] = [0, 800, 728, 668, 614, 566, 522, 482, 444, 409, 377, 346, 317, 291, 265, 242, 219, 198, 178, 160, 142, 126, 110, 95, 82, 69, 57, 46, 35, 26, 17, 9, 1]
        self._scale[(1000,105)] = [0, 1000, 938, 884, 835, 791, 750, 711, 675, 641, 609, 578, 549, 521, 494, 469, 444, 421, 399, 377, 356, 336, 317, 299, 281, 264, 248, 232, 217, 202, 188, 174, 161, 149, 137, 125, 114, 103, 93, 83, 74, 73, 72, 71, 69, 68, 67, 66, 65, 64, 63, 61, 60, 59, 58, 57, 56, 55, 53, 52, 51, 50, 49, 48, 47, 45, 44, 43, 42, 41, 40, 39, 38, 36, 35, 34, 33, 32, 31, 30, 28, 27, 26, 25, 24, 23, 22, 20, 19, 18, 17, 16, 15, 14, 12, 11, 10, 9, 8, 7, 6, 4, 3, 2, 1]

        # USAU 2013
        self._scale[(1500,32)] = [0, 1500, 1366, 1252, 1152, 1061, 979, 903, 832, 767, 706, 648, 595, 544, 497, 452, 410, 371, 334, 299, 266, 235, 206, 178, 152, 128, 106, 85, 66, 47, 31, 15, 1]
        self._scale[(1000,32)] = [0, 1000, 911, 835, 768, 708, 653, 602, 555, 511, 471, 432, 397, 363, 332, 302, 274, 248, 223, 199, 177, 157, 137, 119, 102, 86, 71, 57, 44, 32, 21, 10, 1]
        self._scale[(500,32)] = [0, 500, 455, 417, 384, 354, 326, 301, 278, 256, 236, 217, 199, 182, 166, 151, 137, 124, 112, 100, 89, 79, 69, 60, 51, 43, 36, 29, 22, 16, 11, 6, 1]
        self._scale[(250,32)] = [0, 250, 228, 209, 192, 177, 163, 151, 139, 128, 118, 109, 100, 91, 83, 76, 69, 62, 56, 50, 45, 40, 35, 30, 26, 22, 18, 15, 12, 9, 6, 3, 1] 
        self._scale[(0,32)] = [0]*33

        #CQU4 2014
        self._scale[(1000,100)] = [0, 1000, 955, 916, 881, 848, 817, 788,
                761, 735, 710, 686, 663, 641, 620, 599, 580, 561, 542, 524,
                507, 490, 474, 458, 443, 428, 413, 399, 386, 372, 360, 347,
                335, 323, 311, 300, 289, 278, 268, 258, 248, 239, 229, 220,
                211, 203, 194, 186, 178, 171, 163, 156, 149, 142, 136, 129,
                123, 117, 111, 105, 100, 95, 89, 85, 80, 75, 71, 66, 62,
                58, 54, 51, 47, 44, 40, 37, 34, 31, 29, 26, 24, 21, 19, 17,
                15, 14, 12, 10, 9, 8, 6, 5, 4, 4, 3, 2, 2, 1, 1, 1, 1], 
        self._scale[(666,50)] = [0, 666, 614, 570, 530, 495, 462, 432, 404,
                378, 354, 331, 309, 288, 269, 251, 234, 217, 202, 187, 173,
                160, 148, 136, 125, 114, 104, 95, 86, 78, 70, 63, 56, 49,
                44, 38, 33, 28, 24, 20, 17, 14, 11, 9, 7, 5, 3, 2, 2, 1,
                1], 
        self._scale[(333,24)] = [0, 333, 286, 248, 216, 188, 163, 141, 122,
                104, 89, 75, 63, 52, 42, 34, 26, 20, 15, 10, 7, 4, 2, 1,
                1])

        self._division = ['AAA', 'AA', 'BB', 'CC', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def show(self):
        R = 2
        K = 1
        color = 'green'
        G = Graphics()
        G += list_plot(self._M1000_N105, color="blue")
        G += list_plot(self._M1000_N50, color=color)
        G += list_plot(self._M800_N32, color=color)
        G += list_plot(self._M400_N24, color=color)
        #G += plot(curve(50, 100, K=1, R=2, base=e), 1, 50, color=color)
        G += text("Mars Attaque", (50, 160), fontsize=15, color='blue')
        G += text("$G_{1000, 50}(p)$ \n Grand Chelem", (10, 800), fontsize=15, color=color)
        G += text("$G_{800, 32}(p)$ \n La Flotte", (8, 440), fontsize=15, color=color)
        G += text("$G_{400, 16}(p)$ \n Petit Chelem", (5, 160), fontsize=15, color=color)
        G += text(u"Systeme 2011-2012", (30, 1000), fontsize=15, color=color)
        return G

    def create_and_save_image(self):
        filename = 'systeme_cqu4_2011_2012.png' 
        G = self.show()
        G.axes_labels(['Position','Points'])
        G.xmax(60)
        G.save(filename,figsize=10)
        print "Creation de %s " % filename

    def print_table(self):
        A = self._M1000_N50
        B = self._M800_N32
        C = self._M400_N24
        for i,a,b,c in izip_longest(range(66), A, B, C, fillvalue=0): 
            print "%3s  %3s %3s %3s" % (i,a,b,c)
    def latex_table(self):
        s = ''
        s += "\\begin{tabular}{c|c|c|c|c}\n" 
        s += "Position & Série A & Mars Attaque & La Flotte & Série B \\\\ \n"
        s += " $p$ & $F_{1000,50}(p)$ & & $F_{800,32}(p)$ & $F_{400,16}(p)$ \\\\ \n"
        s += "\\hline \n"
        A = self._M1000_N50
        MA = self._M1000_N105
        B = self._M800_N32
        C = self._M400_N24
        it = izip_longest(range(89), A, MA, B, C, fillvalue=0)
        it.next() # consume the zero
        for i,a,ma,b,c in it: 
            s += "%s & %s & %s & %s & %s \\\\ \n" % (i,a,ma,b,c)
        s += "\\end{tabular}\n"
        return s


    def rst_table(self):
        s = ''
        s += "+----------+---------+--------------+-----------+---------+\n"
        s += "| Position | Série A | Mars Attaque | La Flotte | Série B |\n"
        s += "+----------+---------+--------------+-----------+---------+\n"

        A = self._M1000_N50
        MA = self._M1000_N105
        B = self._M800_N32
        C = self._M400_N24
        nn = max(map(len, (A, MA, B, C)))
        print nn

        lenghts = [8, 7, 12, 9, 7]

        it = izip_longest(range(nn), A, MA, B, C, fillvalue=0)
        it.next() # consume the zero
        for line in it: 
            t = ' | '.join(str(a).ljust(A) for a,A in zip(line, lenghts))
            s += "| %s |\n" % t
            s += "+----------+---------+--------------+-----------+---------+\n"
        return s
    def create_and_save_table(self):
        filename = 'cqu4_table_points.txt'
        f = open(filename, 'w')
        f.write(self.rst_table())
        f.close()
        print "Creation de %s " % filename

    def __repr__(self):
        s = "Systeme 2011\n"
        s += "SerieA: %s\n" % self._M1000_N50
        s += "Mars Attaque: %s\n" % self._M1000_N105
        s += "La Flotte: %s\n" % self._M800_N32
        s += "Serie B: %s\n" % self._M400_N24
        return s

    def score(self, M, N, position):
        if (M,N) not in self._scale:
            raise ValueError, "unknown tournoi parameters (M=%s, N=%s)" % (M, N)
        scale = self._scale[(M,N)]
        if position >= len(scale) :
            return 0
        else:
            return scale[position]

    def esprit_point(self):
        return 50
    def division(self, i):
        return self._division[(i-1) // 16]
######################
# Equipe
######################
class Equipe(object):
    def __init__(self, nom, provenance):
        r"""
        """
        self._nom = nom
        self._provenance = set()
        self._positions = defaultdict(str)
        self._esprit = defaultdict(str)
        self._points = defaultdict(str)
        self._resultats = defaultdict(int)
        self._systeme = Systeme()
        self.update_provenance(provenance)

    def update_provenance(self, provenance):
        self._provenance.update(p.strip() for p in provenance.split(','))
        if '' in self._provenance: self._provenance.remove('')

    def nom(self):
        return self._nom
    def provenance(self):
        s = ",".join(self._provenance)
        #s = s.replace('è','e')
        #s = s.replace('é','e')
        return s
    def __repr__(self):
        return "%22s %30s (%3s)  " % (self._nom, self.points(), self.total())

    def add_resultat(self, tournoi, position, provenance, esprit=False):
        position = int(position)
        error_msg = "tournoi(=%s) deja present pour l'equipe %s" % (tournoi, self.nom())
        assert tournoi not in self._positions, error_msg
        self._positions[tournoi] = position
        assert tournoi not in self._esprit, error_msg
        if esprit:
            assert esprit == "esprit sportif", "esprit sportif mal ecrit pour equipe %s" % self.nom()
            self._esprit[tournoi] = self._systeme.esprit_point()
        M = tournoi._max_points
        N = tournoi._size
        pts = self._systeme.score(M, N, position)
        assert tournoi not in self._points, error_msg
        self._points[tournoi] = pts
        assert tournoi not in self._resultats, error_msg
        self._resultats[tournoi] = pts
        if esprit:
            self._resultats[tournoi] += self._systeme.esprit_point()
        self.update_provenance(provenance)

    def positions(self):
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
        S = sum(L[:3])
        # S2 = sum(heapq.nlargest(3, L))
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
    def __init__(self, filename, long_name, max_points, size, date=None):
        r"""
        """
        self._filename = filename
        self._long_name = long_name
        self._max_points = int(max_points)
        self._size = int(size)

    def __repr__(self):
        return "Tournoi %s M=%s pts N=%s teams" % (self._long_name, self._max_points, self._size)

    def __hash__(self):
        return hash(self._filename)
    def __iter__(self):
        filename = self._filename
        with open(filename, 'r') as f:
            for row in csv.reader(f):
                yield row

    def short_name(self):
        assert self._filename.endswith('.csv')
        return self._filename[:-4]

    def long_name(self):
        return self._long_name
######################
# Classement
######################
class Classement(object):
    def __init__(self):
        r"""
        """
        self._systeme = Systeme()
        self._equipes = {}
        self._tournois = []

    def __repr__(self):
        s = "Classement de %s equipes\n" % len(self)
        s += "Systeme: %s " % self._systeme
        return s

    def __len__(self):
        return len(self._equipes)

    def __getitem__(self, name):
        return self._equipes[name]

    def ajout_equipe(self, nom, provenance=''):
        r"""
        """
        equipe = Equipe(nom, provenance)
        self._equipes[nom] = equipe
        return equipe

    def ajout_tournoi(self, tournoi):
        self._initial = deepcopy(self._equipes.values())
        self._tournois.append(tournoi)
        for row in tournoi:
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
            else:
                raise ValueError, "Longueur dune ligne (=%s) doit etre 2 ou 3 ou 4" % row
            if nom in self._equipes:
                equipe = self._equipes[nom]
            else:
                equipe = self.ajout_equipe(nom, provenance)
            equipe.add_resultat(tournoi, position, provenance, esprit=esprit)

    def get_position(self, equipe):
        L = sorted(self._equipes.values(), reverse=True)
        return L.index(equipe)
    def get_move(self, equipe):
        if equipe in self._initial:
            L = sorted(self._initial, reverse=True)
            diff = L.index(equipe) - self.get_position(equipe) 
            if diff > 0:
                return '+%s' % diff
            elif diff == 0:
                return ''
            else:
                return diff
        else:
            return ''

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
            print e, self.get_move(e)
    def print_equipe_alphabetiquement(self):
        L = self._equipes.keys()
        for nom in sorted(L):
            print nom.ljust(20), self._equipes[nom].provenance()

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
            s += "%s & %s & %s & %s \\\\ \n" % (i+1, e._nom, e.total(), self.get_move(e))
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
            s += "| %8s | %32s | %30s | %6s | %9s |\n" % (i+1, e._nom, e._positions, e.total(), self.get_move(e))
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
            s += "| %8s | %32s | %6s | %9s |\n" % (i+1, e._nom, e.total(), self.get_move(e))
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
        S = self._systeme
        title = ["Division", "Position", "Équipe", "Provenance"]
        title += ["Pos", "Pts", 'ES'] * len(self._tournois)
        title += ["Total", "Variation"]
        filename = 'classement.csv'
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(title)
            for i, e in enumerate(L):
                row = [S.division(i+1), i+1, e._nom, e.provenance()]
                row += e.pos_pts_es_ordonnes(self._tournois)
                row += [e.total(), self.get_move(e)]
                csv_writer.writerow(row)
            print "Creation de %s " % filename

    def save_csv_short_table(self):
        L = self._equipes.values()
        L.sort(reverse=True)
        S = self._systeme
        title = ["Division", "Position", "Équipe", "Provenance", "Total"]
        filename = today.strftime(u"resume_%Y_%m_%d.csv")
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(title)
            for i, e in enumerate(L):
                row = [S.division(i+1), i+1, e._nom, e.provenance(), e.total()]
                csv_writer.writerow(row)
            print "Creation de %s " % filename

    def sage_table(self):
        S = self._systeme
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
            rows.append( (T.long_name(), T._max_points, T._size, 
                          self.tournament_size(T), 
                          "5/%s and %s/20"%(self.strength5(T), self.strength20(T))))
        T2 = table(rows=rows,header_row=True)._repr_()

        #row_header = ["Pos", "Pts", "#Tourn", "Team name", "Region"]
        #row_header += ['Best', '2nd best', '3rd best', '4th best (does not count)']
        row_header = ["Pos", "Pts", "Team name", "Rg"]
        row_header += ['Best', '2nd best', '3rd best']
        rows = [row_header]
        for i, e in enumerate(L):
            row = [i+1]
            row.append(e.total())
            #row.append(e.nb_tournois_participes())
            row.append(e._nom)
            row.append(e.provenance())
            bests = ["%s (%s) %s" % b for b in e.four_best()]
            if len(bests) < 4:
                bests += [""] * (4-len(bests))
            row.extend(bests[:3])
            rows.append(row)
        T3 = table(rows=rows,header_row=True)._repr_()
        return "\n\n".join((T1, T2, T3))

    def txt_table_provincial(self):
        S = self._systeme
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
            line = [S.division(i+1), i%16 +1]
            line += [e.total(), self.get_move(e)]
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
            line += [e.total(), self.get_move(e)]
            line += [e._nom, e.provenance()]
            line += e.pos_pts_es_ordonnes(self._tournois)
            s += line_str(line, col_width, left=range(6))
        return s
    def save_txt_table_provincial(self):
        s = self.txt_table_provincial()
        filename = 'classement_provincial.txt'
        with open(filename, 'w') as f:
            f.write(s)
        print "Creation de %s " % filename

    def save_txt_table_provincial(self):
        #s = self.txt_table_provincial()
        s = self.sage_table()
        filename = 'classement_provincial.txt'
        with open(filename, 'w') as f:
            f.write(s)
        print "Creation de %s " % filename

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
    usage = u"""

        sage -python cqu4.py
        sage -python cqu4.py -csv

        sage -python -V
        Python 2.6.4

    Les autres versions de python fonctionnent mal avec les caractères
    accentués.
        """

    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--alphabetique",
                      action="store_true", dest="alphabetique",
                      help=u"Afficher les équipes alphabétiquement")
    parser.add_option("-c", "--csv",
                      action="store_true", dest="csv",
                      help=u"Créer le fichier csv global")
    parser.add_option("-n", "--nombre",
                      action="store_true", dest="nombre",
                      help=u"Afficher le nombre d'équipes")
    parser.add_option("-s", "--stat",
                      action="store_true", dest="stat",
                      help=u"Afficher statistiques sur la participation")
    #parser.add_option("-s", "--size", type="int", dest="size", default=0, help="size")
    #parser.add_option("-c", "--scale", type="float", dest="scale", default=1, help="scale")
    parser.add_option("-p", "--parameters",
                      action="store", type="string",
                      dest="parameters",
                      help=u"Tournaments parameters")
    (options, args) = parser.parse_args()

    #print options
    #print args

    parameters = {}
    with open(options.parameters, 'r') as f:
        for row in csv.reader(f):
            if len(row) == 0:
                continue
            elif len(row) == 4:
                M, N, filename, long_name = row
            else:
                raise ValueError, "Longueur dune ligne (=%s) doit etre 4 (fichier parameters)" % row
            T = Tournoi(filename, long_name, M, N)
            parameters[filename] = T

    #print parameters

    c = Classement()
    for filename in args:
        if filename not in parameters:
            raise ValueError("filename (=%s) not set in the parameters"%filename)
        T = parameters[filename]
        c.ajout_tournoi(T)

    if options.alphabetique:
        c.print_equipe_alphabetiquement()
    elif options.csv:
        c.save_csv_short_table()
    elif options.nombre:
        print len(c)
    elif options.stat:
        print c.statistiques_participation()
    else:
        c.save_txt_table_provincial()
        #c.save_txt_table_partiel(['Bretzels'], 'Junior')
        #c.save_txt_table_partiel(['Morues'], 'Est')
        filename = today.strftime(u"classement_%Y_%m_%d.html")
        if os.system("rst2html.py classement.rst %s" % filename):
            print "erreur avec la commande rst2html"
        else:
            print "Création du fichier %s" % filename

