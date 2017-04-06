
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from random import randint, shuffle
from combinaison import Combinaison
from partie import Partie


NB_MAX_JOUEURS = 3
NB_MAX_LANCERS = 3
NOMBRE_DES_DU_JEU = 5
GROS_LOT = 1




#*****************************************************************************

class Parametres_partie(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Info partie...")
        # self.geometry("600x200")
        #tst
        # On prend le contrôle
        self.parent = parent
        self.transient(parent)
        self.grab_set()

        self.nombre_joueurs = 0
        self.inclure_ordi = False

        self.nom_joueurs = []

        self.instruction_nb_joueurs = Label(self, text="Nombre de joueur")
        self.instruction_nb_joueurs.grid(row=0, column=0, padx=5, pady=5)
        self.var_nb_joueurs = IntVar()
        self.var_nb_joueurs.trace('w', self.selection_nb_joueur)
        self.box_nb_joueurs = Combobox(self, textvariable=self.var_nb_joueurs, values=[2, 3])

        self.box_nb_joueurs.grid(row=0, column=1, padx=5, pady=5)

        self.instruction_nb_joueurs = Label(self, text="Inclure l'ordinateur")
        self.instruction_nb_joueurs = Label(self, text="Les As sont des Joker?")
        self.instruction_nb_joueurs.grid(row=1, column=0, padx=5, pady=5)
        self.var_As_joker = StringVar()
        self.var_As_joker.trace('w', self.selection_nb_joueur)
        self.var_As_joker = Combobox(self, textvariable=self.var_As_joker, values=["Non", "Oui"])
        self.var_As_joker.grid(row=1, column=1, padx=5, pady=5)



        # ----- Entrer le nom des joueurs -----
        self.instruction_nom_joueurs = Label(self, text="Entrez le nom des joueurs :")
        self.list_labels_nom_joueurs = []
        self.list_entrees_nom_joueurs = []
        self.list_vars_nom_joueurs = []


        for i in range(NB_MAX_JOUEURS):
            self.list_vars_nom_joueurs.append(StringVar(value='Joueur {}'.format(i + 1)))
            self.list_labels_nom_joueurs.append(Label(self, text="Nom du joueur{}".format(i + 1)))
            self.list_entrees_nom_joueurs.append(Entry(self, width=10,
                                                       textvariable=self.list_vars_nom_joueurs[i]))
        self.erreur_nom_joueurs = Label(self, text="Erreur! Vous devez entrez un nom pour "
                                                   "chacun des joueurs avant de poursuivre.")


        self.bouton_commencer_partie = Button(self, text="Commencer", command=self.valider)

        #self.box_ajout_ordi.current(0)
        self.box_nb_joueurs.current(0)
        self.protocol("WM_DELETE_WINDOW", self.valider)
        self.wait_window()

    def valider(self):
        valide = False
        try:
            self.nombre_joueurs = self.var_nb_joueurs.get()  #INT NOMBRE DE JOUEUR
           # self.inclure_ordi = self.var_ajout_ordi.get() == "Oui"
            self.nom_joueurs = [self.list_vars_nom_joueurs[i].get()  #LISTE NOM DE JOUEUR
                                for i in range(self.nombre_joueurs)]



          #  print(self.ordre_joueur)
            print(self.nom_joueurs)
            if not (2 <= self.nombre_joueurs <= 3):
                messagebox.showerror("Erreur",
                                     "Le nombre de joueur de la partie incluant l'ordinateur doit être entre 2 et 3")
            else:
                valide = True


        except:
            messagebox.showerror("Erreur",
                                 "Le nombre de joueur de la partie incluant l'ordinateur doit être entre 2 et 4")

        if valide:
            # On redonne le contole à la fenêtre parent et on ferme la fenêtre.
            self.grab_release()
            self.parent.focus_set()
            self.destroy()

    def selection_nb_joueur(self, index, value, op):
        #t = int(self.var_ajout_ordi.get() == "Oui")
        for i in range(NB_MAX_JOUEURS):
            self.list_labels_nom_joueurs[i].grid_forget()
            self.list_entrees_nom_joueurs[i].grid_forget()
        for i in range(self.var_nb_joueurs.get()):
            self.list_labels_nom_joueurs[i].grid(row=2+i, column=0, padx=5, pady=5)
            self.list_entrees_nom_joueurs[i].grid(row=2+i, column=1, padx=5, pady=5)
        self.bouton_commencer_partie.grid_forget()
        self.bouton_commencer_partie.grid(row=3+i, column=1, padx=5, pady=5)

    def get_values_saved(self):
        return self.nombre_joueurs, self.inclure_ordi, self.nom_joueurs

#*****************************************************************************








class JoueurInterface(LabelFrame):

    def __init__(self, master, nom, images_des, **kw):
        super().__init__(master, borderwidth=1, relief=RIDGE, )
        self.nom = nom
        self.nb_jetons = 0
        self.combinaison_actuelle = None

        self.images_des = images_des
        self.nb_pixels_img = max(self.images_des[0].width(), self.images_des[0].height())
        self.nb_cases = 7
        self.table_de_jeu = Canvas(self, width=self.nb_pixels_img*self.nb_cases,
                                   height=self.nb_pixels_img*self.nb_cases, bg='ivory')
        self.table_de_jeu.grid()

        self.des_sur_canvas = {}

        # On lie un clic sur le Canvas à une méthode.
        self.table_de_jeu.bind('<Button-1>', self.selectionner_des)
        self.resultat_lancer = None
        self.tour = 0

    def is_algo(self):
        return False

    def lancer_des(self):

        nombre_des = self.nb_des_a_lancer
        self.lancer_1 = [0] *5

        valeurs_obtenues = Combinaison()




      #  premier = valeurs_obtenues._lancer_des(5)
      #  print (premier)


       # print(valeurs_obtenues)

       # print(Combinaison.des)



        for k in range(7):
            shuffle(self.positions_libres)
            pos = self.positions_libres[:nombre_des]

            for gif in self.images_des:
                ids = []
                for i in range(nombre_des):
                    x = (pos[i][0] * self.nb_pixels_img) + (self.nb_pixels_img // 2)
                    y = (pos[i][1] * self.nb_pixels_img) + (self.nb_pixels_img // 2)
                    id = self.table_de_jeu.create_image(x, y, image=gif)
                    ids += [id]
                self.table_de_jeu.update()
                self.after(100)
                self.table_de_jeu.delete(*ids)

        shuffle(self.positions_libres)
        pos = self.positions_libres[:nombre_des]
        for i, v in enumerate(valeurs_obtenues):
            x = pos[i][0] * self.nb_pixels_img + self.nb_pixels_img // 2
            y = pos[i][1] * self.nb_pixels_img + self.nb_pixels_img // 2
            id = self.table_de_jeu.create_image(x, y, image=self.images_des[v-1])
            self.table_de_jeu.update()
            self.des_sur_canvas[pos[i]] = (v, id)

        self.resultat_lancer += valeurs_obtenues
        #
        self.combinaison_actuelle = Combinaison(self.resultat_lancer)
        print(self.combinaison_actuelle)


        self.after(1000)
        self.num_lancer += 1
        self.des_a_relancer = []
        self.nb_des_a_lancer = 0
        return valeurs_obtenues

    def jouer_tour(self, nb_des_a_lancer=NOMBRE_DES_DU_JEU, nb_maximum_lancer=NB_MAX_LANCERS):
        self.nb_des_a_lancer = nb_des_a_lancer
        self.nb_maximum_lancer = nb_maximum_lancer
        self.num_lancer = 0
        self.des_sur_canvas = {}
        self.positions_libres = [(i, j) for i in range(self.nb_cases) for j in range(self.nb_cases)]

        self.resultat_lancer = []


    def selectionner_des(self, event):
        pass


    def clear_table(self):
        self.table_de_jeu.delete('all')
        self.update()


    def asg_tour(self, v):
        self.tour = v











#*****************************************************************************

class JoueurAlgoInterface(JoueurInterface):

    def __init__(self, master, images_des, **kw):
        super().__init__(master, "R2D2", images_des, **kw)

    def is_algo(self):
        return True


#*****************************************************************************












class InterfaceGraphique(Tk):
    TROUVER_PREMIER = 0
    JOUER = 1
#    DECHARGE = 2


    def __init__(self):
        super().__init__()
        self.title("hb H17 aide TP4")
        self.geometry("1080x600")
        self.protocol("WM_DELETE_WINDOW", self.confirmation_quitter)

        # menu
        self.menubar = Menu(self)
        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Nouvelle partie", command=self.definir_partie)
        menu1.add_command(label="Poursuivre...", command=None)
        menu1.add_command(label="Enregistrer...", command=None)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.confirmation_quitter)
        self.menubar.add_cascade(label="Menu 1", menu=menu1)
        menu3 = Menu(self.menubar, tearoff=0)
        menu3.add_command(label="A venir...", command=None)
        self.menubar.add_cascade(label="Règles du jeu", menu=menu3)
        self.config(menu=self.menubar)

        # ----- Menu principal -----
        self.title_princ_jeu = Label(self, text="Jeu de dés....", font=("DejaVu Sans", 26),
                                        width=30, height=3)
        self.title_princ_jeu['background'] = 'green'
        self.bouton_princ_jouer = Button(self, text="Nouvelle partie",  command=self.definir_partie,
                                         width=20, height=3, bg="yellow")
        self.bouton_princ_quitter = Button(self, text="Quitter", command=self.confirmation_quitter,
                                           width=20, height=3, bg="red")

        # images des dés
        self.images_des = [PhotoImage(file="ressources/dice_1.gif"), PhotoImage(file="ressources/dice_2.gif"),
                           PhotoImage(file="ressources/dice_3.gif"), PhotoImage(file="ressources/dice_4.gif"),
                           PhotoImage(file="ressources/dice_5.gif"), PhotoImage(file="ressources/dice_6.gif")]

        # ----- Elements de la partie -----
        self.frame_de_droit = Frame(self)
        self.frame_de_gauche = Frame(self)
        self.frame_de_bas = Frame(self)

        self.recap_canvas = Canvas(self.frame_de_gauche)

        self.boutonframe = Frame(self.frame_de_droit)


        self.bouton_lancer = Button(self.boutonframe, text="Lancer", command=self.value_checkbutton)
        self.bouton_lancer.grid(column=0, row=0, rowspan=1, columnspan=1)

        self.bouton_passer = Button(self.boutonframe, text="Passer", command=self.passer_au_suivant)
        self.bouton_passer.grid(column=1, row=0, rowspan=1, columnspan=1)

        self.phase_label = Label(self.frame_de_droit, text="", font="Arial 20 italic")
        self.message = Label(self.frame_de_droit, text="", font="Arial 14 italic", foreground="blue")

        self.ordre_joueur_label = Label(self.frame_de_gauche, text=" Ordre de joueur de la partie : ")
        self.ordre_joueur_label.grid(row=0, column=0, padx=40, pady=0)

        self.jeu_courant_label= Label (self.frame_de_bas,text="Voici le jeu courant ")
        self.jeu_courant_label.grid(padx=0,pady=0)

        valeurs_obtenues = Combinaison()
        premier_lancer = valeurs_obtenues.des
        self.liste = []
        for elem in premier_lancer:
            # chaine += "{:^3s}".format(elem)
            self.liste += "{:s}".format(elem)
        print(self.liste)

        str_1 = self.liste [0]
        print(str_1)


        self.carte_1 = Label(self.frame_de_bas,text=self.liste[0])
        self.carte_1.grid(row=1,column=0,padx=0,pady=10)

        self.carte_2 = Label(self.frame_de_bas,text=self.liste[1])
        self.carte_2.grid(row=1,column=1,padx=40,pady=10)

        self.carte_3 = Label(self.frame_de_bas, text=self.liste[2])
        self.carte_3.grid(row=1, column=2, padx=40, pady=10)

        self.carte_4 = Label(self.frame_de_bas, text=self.liste[3])
        self.carte_4.grid(row=1, column=3, padx=40, pady=10)

        self.carte_5 = Label(self.frame_de_bas, text=self.liste[4])
        self.carte_5.grid(row=1, column=4, padx=40, pady=10)


        self.var_1 = IntVar()
        self.var_2 = IntVar()
        self.var_3 = IntVar()
        self.var_4 = IntVar()
        self.var_5 = IntVar()


        self.checkbutton_1 = Checkbutton(self.frame_de_bas,text="",variable = self.var_1)
        self.checkbutton_1.grid(row=2,column=0,padx=0,pady=10)

        self.checkbutton_2 = Checkbutton(self.frame_de_bas,text="",variable = self.var_2)
        self.checkbutton_2.grid(row=2,column=1,padx=40,pady=10)


        self.checkbutton_3 = Checkbutton(self.frame_de_bas,text="",variable = self.var_3)
        self.checkbutton_3.grid(row=2,column=2,padx=40,pady=10)


        self.checkbutton_4 = Checkbutton(self.frame_de_bas,text="",variable = self.var_4)
        self.checkbutton_4.grid(row=2,column=3,padx=40,pady=10)

        self.checkbutton_5 = Checkbutton(self.frame_de_bas,text="",variable = self.var_5)
        self.checkbutton_5.grid(row=2,column=4,padx=40,pady=10)

        self.checkbutton_1.select()
        self.checkbutton_2.select()
        self.checkbutton_3.select()
        self.checkbutton_4.select()
        self.checkbutton_5.select()


        self.afficher_menu_principal()

    # ----- Gestion des l'affichage -----
    def afficher_menu_principal(self):
        self.title_princ_jeu.place(relx=0.5, rely=0.33, anchor=CENTER)
        self.bouton_princ_jouer.place(relx=0.5, rely=0.68, anchor=CENTER)
        self.bouton_princ_quitter.place(relx=0.5, rely=0.79, anchor=CENTER)

    def cacher_menu_principal(self):
        self.title_princ_jeu.place_forget()
        self.bouton_princ_jouer.place_forget()
        self.bouton_princ_quitter.place_forget()

    def confirmation_quitter(self):
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
            self.destroy()

    def definir_partie(self):
        self.gros_lot = GROS_LOT
        self.indice_joueur_courant = None
        self.phase = InterfaceGraphique.TROUVER_PREMIER
        self.tour = 0
        self.lancer_passer_control_var = BooleanVar(value=False)
        self.choix = None
        self.value_checkbutton()
        
        afficheur_doptions = Parametres_partie(self)
        self.nombre_joueurs, self.inclure_ordi, self.nom_joueurs = afficheur_doptions.get_values_saved()
        self.joueurs = [JoueurInterface(self.frame_de_droit, nom, self.images_des) for nom in self.nom_joueurs]

       # if self.inclure_ordi:
       #     self.joueurs += [JoueurAlgoInterface(self.frame_de_droit, self.images_des)]


        self.afficher_partie()
        self.jouer()







    def afficher_partie(self):
        self.cacher_menu_principal()
        self.frame_de_gauche.grid(row=0, column=0)
        self.frame_de_droit.grid(row=0, column=1)
        self.afficher_espace_joueur_courant()
        self.boutonframe.grid(row=3, column=0, columnspan=2)
        self.frame_de_bas.grid(row=5,column=0)

    def afficher_phase(self):
        self.phase_label.grid_forget()
        if self.phase == InterfaceGraphique.TROUVER_PREMIER:
            self.phase_label['text'] = 'Détermination du premier joueur'
        elif self.phase == InterfaceGraphique.JOUER:
            self.phase_label['text'] = 'On joue....'

        self.phase_label.grid(row=0, column=0)

    def afficher_message(self, message):
        self.message.grid_forget()
        self.message['text'] = message
        self.message.grid(row=1, column=0)
        self.message.after(3000, self.message.grid_forget)

    def afficher_tableau_recapitulatif(self):
        self.recap_canvas.delete('all')
        h, l = 100, 300

        for position, joueur in enumerate(self.joueurs):
            color = "black" if position != self.indice_joueur_courant else "red"
            self.recap_canvas.create_rectangle(1, 1 + (h * position), l, 1 + (h * (position+1)))
            self.recap_canvas.create_text(15, 25 + (h * position), text=joueur.nom, font="Arial 16 italic", fill=color,
                                          justify="left", anchor=W)
            self.recap_canvas.create_text(50, 70 + (h * position), text=str(joueur.nb_jetons) + " mise",
                                          font="Arial 12 italic", fill=color, justify="left")

            if joueur.resultat_lancer is None:
                comb_str = ""
            elif joueur.tour == 0:
                comb_str = "Lancer : " + str(joueur.resultat_lancer)
            else:
                comb_str = ""

            self.recap_canvas.create_text(200, 70 + (h * position), text=comb_str, font="Arial 12 italic",
                                          fill=color, justify="left")
        self.recap_canvas.create_text(5, 25 + (h * self.nombre_joueurs),
                                      text="Gros lot: {} $".format(self.gros_lot),
                                      font="Arial 16 italic", fill="Blue", justify="left", anchor=W)
        self.recap_canvas.config(height=(h*self.nombre_joueurs+h), width=l+50)
        self.recap_canvas.grid(padx=5, pady=5)
        self.recap_canvas.update()

    def afficher_espace_joueur_courant(self, position=None):
        for joueur in self.joueurs:
            joueur.grid_forget()
        if self.indice_joueur_courant is None:
            self.indice_joueur_courant = 0
        if position is None:
            position = self.indice_joueur_courant
        self.joueurs[position].grid(row=2, column=0, padx=5, pady=5)

    def lancer_des(self):
        self.lancer_passer_control_var.set(True)
       # lancer =[]
       # Combinaison(lancer)
        print("BRAP")
        self.choix = "L"

    def empecher_lancer(self):
        self.bouton_lancer.config(state=DISABLED)

    def permettre_lancer(self):
        self.bouton_lancer.config(state=NORMAL)

    def empecher_passer(self):
        self.bouton_passer.config(state=DISABLED)

    def permettre_passer(self):
        self.bouton_passer.config(state=NORMAL)

    def passer_au_suivant(self):
        self.lancer_passer_control_var.set(True)
        self.choix = "P"



    def determiner_premier_lanceur(self):
        """
        ...
        """
        partie = Partie(self.nom_joueurs)
        self.ordre_joueur = partie._determiner_ordre()

        for i in range(0, len(self.ordre_joueur)):
            joueur = self.nom_joueurs[self.ordre_joueur[i]]
            print("Le joueur {} est {}".format(i + 1, joueur))
            self.ordre_joueur_label1 = Label(self.frame_de_gauche, text="Le joueur {} est {}".format(i + 1, joueur))
            self.ordre_joueur_label1.grid(row=i + 1, column=0, padx=0, pady=0)

        self.phase = InterfaceGraphique.TROUVER_PREMIER
        self.afficher_phase()
        self.empecher_passer()
        concernes = list(range(self.nombre_joueurs))
        self.premier = concernes[0]
        self.afficher_tableau_recapitulatif()


    def jouer_tour_premiere_phase(self):
        """
        ..........
        """
        self.tour += 1
        self.phase = InterfaceGraphique.JOUER
        self.afficher_phase()
        self.empecher_passer()

        for i in range(self.nombre_joueurs):
            pos = (self.premier+i) % self.nombre_joueurs
            self.permettre_lancer()
            self.indice_joueur_courant = pos

            self.afficher_espace_joueur_courant(pos)
            self.joueurs[pos].asg_tour(self.tour)
            self.joueurs[pos].jouer_tour(nb_des_a_lancer=NOMBRE_DES_DU_JEU, nb_maximum_lancer=1)
            self.joueurs[pos].lancer_des()

            self.joueurs[pos].clear_table()



        return -1, -1



    def value_checkbutton(self):

        value = []
        value.clear()

        if self.var_1.get():
            value.append(1)

        if self.var_2.get():
            value.append(2)

        if self.var_3.get():
            value.append(3)

        if self.var_4.get():
            value.append(4)

        if self.var_5.get():
            value.append(5)

        return value

    def jouer(self):
        """
        .......
        """

        self.tour = 0

        self.determiner_premier_lanceur()

        self.jouer_tour_premiere_phase()

      #  if messagebox.askokcancel("FIN", "...merci...."):
        #    print("lel")

            #self.destroy()


#*****************************************************************************

