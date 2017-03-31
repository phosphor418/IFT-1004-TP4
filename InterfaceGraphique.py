"""Un module d'interface pour la banque.

"""
from tkinter import Tk, Toplevel, Label, Listbox, Frame, Entry, Button, END, NORMAL, E, DISABLED, messagebox



class InterfaceGraphique(Tk):
    """Classe principale de l'interface de la banque. Nous héritons de "Tk", la classe représentant la fenêtre principale
    d'une application tkinter.

    Attributes:
        banque (Banque): La banque liée à l'interface
        compte_selectionne (Compte): Référence vers le compte actuellement sélectionnée dans l'interface.

    """
    def __init__(self):

        super().__init__()

        self.title("Poker d'As")
        self.geometry("800x500")
        Label(self, text="Bienvenue dans le jeu Poker d'As!").grid(row=0, column=1, padx=290, pady=150)

        cadre_boutons = Frame(self)
        cadre_boutons.grid(row=1, column=1, padx = 10, pady=10)

        self.bouton_jouer = Button(cadre_boutons, text="Jouer", command=self.selection_joueur)
        self.bouton_jouer.grid(row=0, column=1)


        self.bouton_quitter = Button(cadre_boutons, text="Quitter", command=self.confirmation_quitter)
        self.bouton_quitter.grid(row=1, column=1)


    def selection_joueur (self) :
        FenetreJouer()
        InterfaceGraphique.destroy(self)

    def confirmation_quitter(self):
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
            self.destroy()



class FenetreJouer (Tk) :
    def __init__(self):

        super().__init__()

        self.title("Poker d'As")

        Label(self, text="Sélectioner le nombre de joueur : ").grid(row=0, column=1, padx=10, pady=10)



        cadre_boutons = Frame(self)
        cadre_boutons.grid(row=1, column=1, padx=10, pady=10)

        self.entree_numero = Entry(cadre_boutons)
        self.entree_numero.grid(padx = 10, pady =20 )

        self.bouton_ok = Button(cadre_boutons, text="Ok", command=self.ok)
        self.bouton_ok.grid(padx = 10, pady = 30)

    def ok (self):
        FenetreJeu ()
        FenetreJouer.destroy(self)


class FenetreJeu (Tk) :
    def __init__(self):
        super().__init__()


        #Frame(FenetreJeu()).size(300,300) #Broke ton portable avec cette ligne de code le jeune


        self.title("Poker d'As")

        Label(self, text=" Jeu : ").grid(row=0, column=1, padx=10, pady=10)




if __name__ == '__main__':
    # Instanciation de la fenêtre et démarrage de sa boucle principale.
    fenetre = InterfaceGraphique()
    fenetre.mainloop()
