from enums import Carte, TypeCombinaison
from random import choice, shuffle


class Combinaison:
    """Représente la combinaison d'un joueur

    Attributes:
        des (list): Liste des dés lancés.
        nb_lancers (int): Le nombre de lancés réalisés.
        types_cartes (list): Les différents types de cartes.
    """
    types_cartes = [
        Carte.AS, Carte.ROI, Carte.DAME, Carte.VALET, Carte.DIX, Carte.NEUF
    ]

    def __init__(self, des = None):
        """Initialise une combinaison"""
        self.nb_lancers = 1
        if des is None:
            self.des = self._lancer_des(5)
        else:
            self.des = des

    def relancer_des(self, index_a_relancer):
        """Relance les dés spécifiés
        Args:
            index_a_relancer (list): Liste des index des dés à relancer.
        """
        if len(index_a_relancer) > 0:
            nouveaux_des = self._lancer_des(len(index_a_relancer))
            for i in range(0, len(index_a_relancer)):
                self.des[index_a_relancer[i]] = nouveaux_des[i]

            self.nb_lancers += 1

    def determiner_type_combinaison(self):
        """Détermine le type de la combinaison.

        Return (TypeCombinaison): Le type de la combinaison.
        """
        valeurs = []
        for elem in self.des:
            valeurs.append(elem.value)
        valeurs.sort()

        nb_identiques = []
        precedent = -1
        sequence = True
        nb_as = 0
        as_utilises_sequence = 0

        for elem in valeurs:
            if elem == Carte.AS.value:
                nb_as += 1
            elif precedent == elem:
                nb_identiques[-1] += 1
                sequence = False
            else:
                nb_identiques.append(1)
                if not (precedent == -1 or precedent == elem - 1):
                    if as_utilises_sequence >= nb_as:
                        sequence = False
                    else:
                        as_utilises_sequence += 1
            if elem != Carte.AS.value:
                precedent = elem

        nb_identiques.sort(reverse=True)

        if nb_as == 5 or nb_identiques[0] + nb_as == 5:
            return TypeCombinaison.QUINTON
        if nb_identiques[0] + nb_as == 4:
            return TypeCombinaison.CARRE
        if nb_identiques[0] + nb_as == 3 and nb_identiques[1] == 2:
            return TypeCombinaison.FULL
        if nb_identiques[0] + nb_as == 3:
            return TypeCombinaison.BRELAN
        if sequence:
            return TypeCombinaison.SEQUENCE
        if nb_identiques[0] == 2 and nb_identiques[1] == 2:
            return TypeCombinaison.DEUX_PAIRES
        if nb_identiques[0] + nb_as == 2:
            return TypeCombinaison.UNE_PAIRE

        return TypeCombinaison.AUTRE

    @staticmethod
    def determiner_meilleur_combinaison(combinaisons):
        """
        Méthode statique qui détermine la meilleure combinaison (et donc le meilleur joueur) parmi une liste.
        Args:
            combinaisons (list): Liste de combinaisons sous forme de liste de tuples (Joueur, Combinaison)

        Returns (tuple): Un tuple (Joueur, Combinaison) du meilleur joueur et de la meilleur combinaison ou (None, None)
                         en cas d'égalité. Il est à noter que le premier élément du tuple n'est pas nécessairement de
                         type Joueur. Ce peut être un object quelconque (Joueur, entier, string, etc.), selon
                         l'utilisation souhaitée.

        """
        meilleur_valeur = -1
        meilleur_tuple = None
        egalite = False

        for joueur, combinaison in combinaisons:
            type = combinaison.determiner_type_combinaison()
            if type.value == meilleur_valeur:
                egalite = True
            elif type.value > meilleur_valeur:
                egalite = False
                meilleur_tuple = joueur, combinaison
                meilleur_valeur = type.value

        if egalite:
            return None, None
        return meilleur_tuple


    def _lancer_des(self, n):
        """Lance n dés.

        Args:
            n (int): Le nombre de dés à lancer.
        """
        resultats = []
        for _ in range(0, n):
            resultats.append(choice(self.types_cartes))
        return resultats

    def __str__(self):
        '''
        a vous de voir comment definir et utiliser
        :return: a definir selon vos besoins
        '''
        chaine = "Dés:    "
        for i in range(0, len(self.des)):
            chaine += "{:^3d}".format(i + 1)
        chaine += "\nValeur: "
        for elem in self.des:
            chaine += "{:^3s}".format(elem)
        return chaine + "\n"


if __name__ == "__main__":
    combinaison = Combinaison()

    # Test de init
    assert len(combinaison.des) == 5
    assert combinaison.nb_lancers == 1

    # Test de relancer_des
    combinaison.relancer_des([])
    assert combinaison.nb_lancers == 1
    anciens_des = list(combinaison.des)
    combinaison.relancer_des([3, 4])
    assert combinaison.nb_lancers == 2
    assert combinaison.des[0:2] == anciens_des[0:2]

    # Test de _lancer_des
    assert len(combinaison._lancer_des(5)) == 5
    assert len(combinaison._lancer_des(0)) == 0
    des = combinaison._lancer_des(5)
    for elem in des:
        assert isinstance(elem, Carte)

    # Test de str()
    combinaison.des = combinaison.types_cartes[0:5]
    assert "Dés:     1  2  3  4  5" in str(combinaison)
    assert "Valeur:  A  R  D  V  X" in str(combinaison)

    combinaisons = [
             # Combinaisons avec As
            ([Carte.AS, Carte.AS, Carte.AS, Carte.AS, Carte.AS],
             TypeCombinaison.QUINTON),
             ([Carte.ROI, Carte.AS, Carte.VALET, Carte.DIX, Carte.NEUF],
              TypeCombinaison.SEQUENCE),
             ([Carte.VALET] * 4 + [Carte.AS], TypeCombinaison.QUINTON),
             ([Carte.VALET] * 3 + [Carte.AS, Carte.ROI], TypeCombinaison.CARRE),
             ([Carte.VALET] * 2 + [Carte.ROI, Carte.AS, Carte.ROI],
              TypeCombinaison.FULL),
             ([Carte.VALET] * 2 + [Carte.ROI, Carte.AS, Carte.DAME],
              TypeCombinaison.BRELAN),
             ([Carte.ROI, Carte.DAME, Carte.AS, Carte.DIX, Carte.NEUF],
              TypeCombinaison.SEQUENCE),
             # Combinaisons sans As
             ([Carte.VALET] * 5, TypeCombinaison.QUINTON),
             ([Carte.VALET] * 4 + [Carte.ROI], TypeCombinaison.CARRE),
             ([Carte.VALET] * 3 + [Carte.ROI] * 2, TypeCombinaison.FULL),
             ([Carte.VALET] * 3 + [Carte.ROI, Carte.DAME], TypeCombinaison.BRELAN),
             ([Carte.AS, Carte.ROI, Carte.DAME, Carte.VALET, Carte.DIX],
              TypeCombinaison.SEQUENCE),
             ([Carte.ROI, Carte.DAME, Carte.VALET, Carte.DIX, Carte.NEUF],
              TypeCombinaison.SEQUENCE),
             ([Carte.ROI, Carte.ROI, Carte.VALET, Carte.VALET, Carte.NEUF],
              TypeCombinaison.DEUX_PAIRES),
             ([Carte.ROI, Carte.ROI, Carte.DIX, Carte.VALET, Carte.NEUF],
              TypeCombinaison.UNE_PAIRE)
             ]

    for des, vrai_type in combinaisons:
        shuffle(des)
        combinaison.des = des
        type = combinaison.determiner_type_combinaison()
        assert type == vrai_type
