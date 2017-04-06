# YO - h17
from partie import Partie
from joueur import Joueur

if __name__ == "__main__":
    print("Bienvenue au Poker d'As!")
    max_joueurs = 3
    min_joueurs = 1

    nb_joueurs = 0
    while nb_joueurs < min_joueurs or nb_joueurs > max_joueurs:
        nb_joueurs = int(input("Combien êtes-vous de joueurs? "))

    joueurs = []
    for i in range(0, nb_joueurs):
        nom = input("Entrez le nom du joueur {:d} ".format(i + 1))
        joueurs.append(Joueur(nom))

    continuer = True
    while continuer:
        partie = Partie(joueurs)
        partie.jouer_partie()
        refaire_partie = ""
        while not ("oui" in refaire_partie or "non" in refaire_partie):
            refaire_partie = input(
                "Voulez-vous refaire une partie? (oui/non) ").lower()
        continuer = "oui" in refaire_partie

    for joueur in joueurs:
        print("{} a gagné {:d} parties, soit {:.0f}%.".format(joueur,
                                                             joueur.nb_victoires,
                                                             joueur.nb_victoires / joueur.nb_parties_jouees * 100))
