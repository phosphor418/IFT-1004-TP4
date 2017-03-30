from joueur import Joueur
from combinaison import Combinaison
from random import shuffle


class Partie:
    """Représente une partie du jeu de Poker d'As

    Attributes:
        joueurs (list): La liste des joueurs.
    """

    def __init__(self, joueurs):
        """Initialise une partie avec la liste de joueurs

        Args:
            joueurs (list): La liste des joueurs.
        """
        self.joueurs = joueurs

    def jouer_partie(self):
        """ Joue une partie entre tous les joueurs et détermine le gagnant.
        Le compteur du nombre de partie est incrémenté pour chacun des joueurs.
        Le compteur de victoires est incrémenté pour le joueur gagnant (si la partie n'est pas nulle).
        Le joueur gagnant est affiché à l'écran (ou un message indiquant que la partie est nulle, s'il y a lieu).
        """
        ordre = self._determiner_ordre()
        print("\n\nL'ordre est tiré au hasard.")
        for i in range(0, len(ordre)):
            joueur = self.joueurs[ordre[i]]
            print("Le joueur {} est {}".format(i+1, joueur))

        print()

        max_lancers = 3
        resultats = []

        for i in range(0, len(ordre)):
            index = ordre[i]
            joueur = self.joueurs[index]
            joueur.nb_parties_jouees += 1

            print("C'est au tour de {}\n".format(joueur))
            resultat, nb_tours = joueur.jouer_tour(max_lancers)
            if i == 0:
                max_lancers = nb_tours

            print("{} a eu {}\n\n".format(joueur, resultat.determiner_type_combinaison()))

            resultats.append((joueur, resultat))

        meilleur_joueur, _  = Combinaison.determiner_meilleur_combinaison(resultats)
        if meilleur_joueur is None:
            print("La partie est nulle.")
        else:
            print("{} a gagné".format(meilleur_joueur))
            meilleur_joueur.nb_victoires += 1

    def _determiner_ordre(self):
        """Détermine l'ordre dans lequel les joueurs vont jouer.
        Return (list): La liste des index des joueurs indiquant l'ordre.

        Exemple:
            [2, 1, 0] indique que joueur 3 joue, suivi du joueur 2, puis du
            joueur 1.
        """
        ordre = list(range(0, len(self.joueurs)))
        shuffle(ordre)
        return ordre


if __name__ == "__main__":
    joueurs = [Joueur("a"), Joueur("b"), Joueur("c")]

    partie = Partie(joueurs)

    # Teste que tous les joueurs vont jouer une et une seule fois
    ordre = partie._determiner_ordre()
    assert len(ordre) == 3
    assert 0 in ordre
    assert 1 in ordre
    assert 2 in ordre
