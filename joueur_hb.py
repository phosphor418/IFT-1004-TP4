from combinaison import Combinaison


class Joueur:
    """Classe représentant un joueur.

    Attributes:
        nom (str): Le nom du joueur
        nb_victoires (int): Le nombre de parties remportées.
        nb_parties_jouees (int): Le nombre de parties jouées.
    """
    def __init__(self, nom):
        """
        Initialise un nouveau joueur avec son nom.

        Args:
            nom (str): Le nom du joueur.
        """
        self.nom = nom
        self.nb_victoires = 0
        self.nb_parties_jouees = 0

    def jouer_tour(self, limite_lancers):
        """
        Joue le tour d'un joueur.
        Args:
            limite_lancers (int): Le nombre de lancers maximums.

        Returns (Combinaison): La combinaison obtenue

        """
        combinaison = Combinaison()
        termine = False

        while combinaison.nb_lancers < limite_lancers and not termine:
            print("Voici votre combinaison:")
            print(str(combinaison))
            relance = input("Quel(s) dé(s) voulez-vous rejouer (0 pour aucun), entrez la liste (ex. 1,5): ").strip()

            if relance == "0":
                termine = True
            else:
                des_a_relancer = []
                for de in relance.split(","):
                    des_a_relancer.append(int(de)-1)
                combinaison.relancer_des(des_a_relancer)

        print("Voici votre combinaison:")
        print(str(combinaison))
        return combinaison, combinaison.nb_lancers

    def __str__(self):
        """
        Converti le joueur en une chaîne de caractères le représentant (le nom du joueur).
        Returns (str): La chaîne de caractères représentant le joueur.

        """
        return self.nom
