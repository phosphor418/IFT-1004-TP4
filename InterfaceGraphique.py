
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from random import randint, shuffle
from combinaison import Combinaison
from partie import Partie
from enums import *


NB_MAX_JOUEURS = 3
NB_MAX_LANCERS = 3
NOMBRE_DES_DU_JEU = 5






#*****************************************************************************
class Parametres_partie(Toplevel):

    def __init__(self, parent):

#   Différents paramètres de la fenêtre popup proposant les différentes options de jeu au joueur

        super().__init__(parent)
        self.title("Info partie...")
        self.parent = parent
        self.transient(parent)
        self.grab_set()

        self.nombre_joueurs = 0

        self.as_joker = None
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
        self.var_As_joker = Combobox(self, textvariable=self.var_As_joker, values=["non", "oui"])
        self.var_As_joker.grid(row=1, column=1, padx=5, pady=5)



#   On demande le nom de chacun des joueurs

        self.instruction_nom_joueurs = Label(self, text="Entrez le nom des joueurs :")
        self.list_labels_nom_joueurs = []
        self.list_entrees_nom_joueurs = []
        self.list_vars_nom_joueurs = []


        self.file = open('testfile.txt','w')

        self.file.write('test ecriture\n')

        self.file.write('test\n')


        self.file.write('test\n')

        self.file.close()



        self.file_1 = open('testfile.txt','r')

        for line in self.file_1 :
            print(line,end='')

        for i in range(NB_MAX_JOUEURS):
            self.list_vars_nom_joueurs.append(StringVar(value='Joueur {}'.format(i + 1)))
            self.list_labels_nom_joueurs.append(Label(self, text="Nom du joueur{}".format(i + 1)))
            self.list_entrees_nom_joueurs.append(Entry(self, width=10,
                                                       textvariable=self.list_vars_nom_joueurs[i]))
        self.erreur_nom_joueurs = Label(self, text="Erreur! Vous devez entrez un nom pour "
                                                   "chacun des joueurs avant de poursuivre.")


        self.bouton_commencer_partie = Button(self, text="Commencer", command=self.valider)

        self.box_nb_joueurs.current(0)
        self.protocol("WM_DELETE_WINDOW", self.valider)
        self.wait_window()


    def valider(self):
        valide = False
        try:
            self.nombre_joueurs = self.var_nb_joueurs.get()
            self.nom_joueurs = [self.list_vars_nom_joueurs[i].get()
                                for i in range(self.nombre_joueurs)]

            self.as_joker = self.var_As_joker.get()



#   Message d'erreur concernant le nombre de joueurs nécessaire

            if not (2 <= self.nombre_joueurs <= 3):
                messagebox.showerror("Erreur",
                                     "Le nombre de joueur de la partie incluant l'ordinateur doit être entre 2 et 3")

#   Message d'erreur sur l'obligation de choisir si le joueur veut utiliser les as

            if not (self.as_joker == "oui" or self.as_joker == "non" ):
                messagebox.showerror("Erreur",
                                     "Vous devez entrer une reponse au as étant joker ou non")
            else:
                valide = True


        except:
            messagebox.showerror("Erreur",
                                 "Le nombre de joueur de la partie incluant l'ordinateur doit être entre 2 et 4")

        if valide:
#   On redonne le controle à la fenêtre parent et on ferme la fenêtre.
            self.grab_release()
            self.parent.focus_set()
            self.destroy()

    def selection_nb_joueur(self, index, value, op):

        for i in range(NB_MAX_JOUEURS):

            self.list_labels_nom_joueurs[i].grid_forget()
            self.list_entrees_nom_joueurs[i].grid_forget()

        for i in range(self.var_nb_joueurs.get()):

            self.list_labels_nom_joueurs[i].grid(row=2+i, column=0, padx=5, pady=5)
            self.list_entrees_nom_joueurs[i].grid(row=2+i, column=1, padx=5, pady=5)

        self.bouton_commencer_partie.grid_forget()
        self.bouton_commencer_partie.grid(row=3+i, column=1, padx=5, pady=5)

    def get_values_saved(self):

        return self.nombre_joueurs, self.as_joker, self.nom_joueurs,

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

#   On initialise la fenêtre où se déroulera le jeu

        super().__init__()
        self.title("Simulateur")
        self.geometry("800x500")
        self.protocol("WM_DELETE_WINDOW", self.confirmation_quitter)

#   Menu déroulant des options disponibles pour l'utilisateur

        self.menubar = Menu(self)
        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Nouvelle partie", command=self.definir_partie)
        menu1.add_command(label="Charger", command=self.definir_partie_charger)

        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.confirmation_quitter)
        self.menubar.add_cascade(label="Menu", menu=menu1)
        menu3 = Menu(self.menubar, tearoff=0)
        menu3.add_command(label="Instructions", command=self.instructions)
        self.menubar.add_cascade(label="Règles du jeu", menu=menu3)
        self.config(menu=self.menubar)

#   Premier stade du jeu soit l'accueil (nouvelle partie, charger partie, quitter)

        self.title_princ_jeu = Label(self, text="Poker d'as", font=("DejaVu Sans", 26),
                                        width=30, height=3)
        self.title_princ_jeu['background'] = 'green'
        self.bouton_princ_jouer = Button(self, text="Nouvelle partie",  command=self.definir_partie,
                                         width=20, height=3, bg="yellow")
        self.bouton_princ_charger = Button(self, text="Charger", command=self.definir_partie_charger,
                                            width=20, height=3, bg="yellow")
        self.bouton_princ_quitter = Button(self, text="Quitter", command=self.confirmation_quitter,
                                           width=20, height=3, bg="red")

#   Différentes zones de disposition des éléments dans la deuxième fenêtre de jeu

        # ----- Elements de la partie -----
        self.frame_bouton= Frame(self)
        self.frame_de_gauche = Frame(self)
        self.frame_de_bas = Frame(self)
        self.frame_resultat = Frame (self)

        self.recap_canvas = Canvas(self.frame_de_gauche)
        self.bas_canvas = Canvas(self.frame_de_bas)


        self.boutonframe = Frame(self.frame_bouton)

#   Initialisation des différents compteurs nécessaires au déroulement du jeu

        self.nb_lancer = 0
        self.nb_lancer_1 = 0
        self.nb_lancer_2 = 0
        self.nb_lancer_autre = 0
        self.nb_lancer_autre_1 = 0
        self.nb_lancer_autre_2 = 0
        self.max_lancer = 3
        self.zero = 0

        self.joueur_liste=[]



        self.passer = 0
        self.joueur_1 = []
        self.joueur_2 = []
        self.joueur_3 = []
        self.joueur_1_lancer = None
        self.joueur_2_lancer = None
        self.joueur_3_lancer = None

        self.commencer_1 = False
        self.commencer_2 = False
        self.commencer_3 = False
        self.commencer = True

        self.bool_passer = True
        self.bool_compteur_lancer_1 = True
        self.bool_lancer_1 = True
        self.bool_lancer_2 = False
        self.bool_lancer_3 = False

        self.lol_1 = False
        self.lol_2 = False
        self.lol_3 = False

        self.tour_joueur_1 = 1
        self.tour_joueur_2 = 1
        self.tour_joueur_3 = 1
        self.test= None
        self.lolxd = None
        self.lancer = None
        self.combinaison_1 = None
        self.combinaison_2 = None
        self.combinaison_3 = None

#   On fait apparaître les différents bouttons utiles pour jouer une partie ("Commencer", "Lancer" et "Passer")

        self.bouton_commencer = Button(self.boutonframe, text="Commencer", command=self.commencer_tour)
        self.bouton_commencer.grid(column=0, row=0, rowspan=1, columnspan=1)

        self.bouton_lancer = Button(self.boutonframe, text="Lancer", command= self.update)
        self.bouton_lancer.grid(column=1, row=0, rowspan=1, columnspan=1)

        self.bouton_passer = Button(self.boutonframe, text="Passer", command=self.update_passer)
        self.bouton_passer.grid(column=2, row=0, rowspan=1, columnspan=1)

#   Label indiquant l'ordre des joueurs pour la partie en cours

        self.ordre_joueur_label = Label(self.frame_de_gauche, text=" Ordre des joueurs : ", font='Arial 20 italic')
        self.ordre_joueur_label.grid(row=0, column=0, padx=0, pady=0)
        self.ordre_joueur_label['background'] = 'blue'



#   Zone du tableau des résultats

        self.nom_joueur_1 = Label (self.frame_de_bas, text = "Joueur 1")
        self.nom_joueur_1.grid (row = 0, column = 0, padx = 0, pady = 0 )
        self.nom_joueur_1_resultat = Label(self.frame_de_bas, text="Resultat :")
        self.nom_joueur_1_resultat.grid(row=1, column=0, padx=0, pady=0)
        self.var_joueur_1_resultat = Label (self.frame_de_bas, text = "X")
        self.var_joueur_1_resultat.grid(row=1, column=1, padx=0, pady=0)
        self.var_joueur_1_sequence = Label(self.frame_de_bas, text = "X")
        self.var_joueur_1_sequence.grid(row=1, column=2, padx=0, pady=0)

        self.nom_joueur_2 = Label(self.frame_de_bas, text="Joueur 2")
        self.nom_joueur_2.grid(row=2, column=0, padx=0, pady=0)
        self.nom_joueur_2_resultat = Label(self.frame_de_bas, text="Resultat :")
        self.nom_joueur_2_resultat.grid(row=3, column=0, padx=0, pady=0)
        self.var_joueur_2_resultat = Label(self.frame_de_bas, text="X")
        self.var_joueur_2_resultat.grid(row=3, column=1, padx=0, pady=0)
        self.var_joueur_2_sequence = Label(self.frame_de_bas, text="X")
        self.var_joueur_2_sequence.grid(row=3, column=2, padx=0, pady=0)

        self.nom_joueur_3 = Label(self.frame_de_bas, text="Joueur 3")
        self.nom_joueur_3.grid(row=4, column=0, padx=0, pady=0)
        self.nom_joueur_3_resultat = Label(self.frame_de_bas, text="Resultat :")
        self.nom_joueur_3_resultat.grid(row=5, column=0, padx=0, pady=0)
        self.var_joueur_3_resultat = Label(self.frame_de_bas, text="X")
        self.var_joueur_3_resultat.grid(row=5, column=1, padx=0, pady=0)
        self.var_joueur_3_sequence = Label(self.frame_de_bas, text="X")
        self.var_joueur_3_sequence.grid(row=5, column=2, padx=0, pady=0)

        self.nom_joueur_courant = Label(self.frame_de_bas, text="Joueur courant")
        self.nom_joueur_courant.grid(row=7, column=0, padx=0, pady=0)

        self.num_lancer = Label(self.frame_de_bas, text="Lancer actuel")
        self.num_lancer.grid(row=7, column=3, padx=0, pady=0)

        self.nbr_max_lancer = Label(self.frame_de_bas, text="Nombre maximal de lancer(s)")
        self.nbr_max_lancer.grid(row=7, column=5, padx=0, pady=0)



        self.var_nom_joueur_courant = Label(self.frame_de_bas, text="XXXXX")
        self.var_nom_joueur_courant.grid(row=8, column=0, padx=0, pady=0)

        self.var_num_lancer = Label(self.frame_de_bas, text="XXXXX")
        self.var_num_lancer.grid(row=8, column=3, padx=20, pady=20)

        self.var_nbr_max_lancer = Label(self.frame_de_bas, text="XXXXX")
        self.var_nbr_max_lancer.grid(row=8, column=5, padx=0, pady=20)





        self.jeu_courant_label = Label(self.frame_de_bas, text="Voici le jeu courant ")
        self.jeu_courant_label.grid(row=9, column = 0, padx=0, pady=0)
        self.jeu_courant_label['background'] = 'blue'

        self.espace= Label(self.frame_de_bas, text="                            ")
        self.espace.grid(row=9, column=1, padx=0, pady=0)
        self.espace1 = Label(self.frame_de_bas, text="                         ")
        self.espace1.grid(row=9, column=2, padx=0, pady=0)
        self.espace2 = Label(self.frame_de_bas, text="                         ")
        self.espace2.grid(row=9, column=3, padx=0, pady=0)
        self.espace3 = Label(self.frame_de_bas, text="                         ")
        self.espace3.grid(row=9, column=4, padx=0, pady=0)


        self.valeurs_obtenues = Combinaison()

        self.var_1 = IntVar()
        self.var_2 = IntVar()
        self.var_3 = IntVar()
        self.var_4 = IntVar()
        self.var_5 = IntVar()



        self.afficher_menu_principal()


#   Gestion des l'affichage

    def afficher_menu_principal(self):

        self.title_princ_jeu.place(relx=0.5, rely=0.33, anchor=CENTER)
        self.bouton_princ_jouer.place(relx=0.5, rely=0.68, anchor=CENTER)
        self.bouton_princ_charger.place(relx=0.5, rely=0.79, anchor=CENTER)
        self.bouton_princ_quitter.place(relx=0.5, rely=0.90, anchor=CENTER)

    def cacher_menu_principal(self):

        self.title_princ_jeu.place_forget()
        self.bouton_princ_jouer.place_forget()
        self.bouton_princ_quitter.place_forget()
        self.bouton_princ_charger.place_forget()

    def confirmation_quitter(self):

        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
            self.destroy()

    def instructions(self):

        messagebox.showinfo("Instructions", "Voici les règles du jeu:\n"
                                            "\n"
                                            "   1.  Le fonctionnement est basé sur les règlements officiels"
                                            "       du jeu de poker d'as\n"
                                            "\n"
                                            "   2.  Le simulateur accepte un, deux ou trois joueurs\n"
                                            "\n"
                                            "   3.  Il est obligatoire de sélectionner l'option où l'on"
                                            "       joue avec ou sans les as\n"
                                            "\n"
                                            "   4.  La partie débute lorsque le premier joueur appuie sur le"
                                            "       bouton lancer\n"
                                            "\n"
                                            "   5.  L'ordre de jeu est sélectionné de manière aléatoire\n"
                                            "\n "
                                            "   6.  La sauvegarde du jeu ne peut s'effectuer que si le premier"
                                            "       joueur a terminé son tour\n"
                                            "\n"
                                            "   7.  On peut charger une partie lorsque le premier joueur a terminé"
                                            "       son tour(à deux joueurs) et lorque le premier ou le deuxième"
                                            "       joueur a terminé (à trois joueurs)\n"
                                            "\n")

    def definir_partie_charger(self):

        self.indice_joueur_courant = None
        self.tour = 0
        self.lancer_passer_control_var = BooleanVar(value=False)
        self.choix = None
        self.value_checkbutton()

        #afficheur_doptions = Parametres_partie(self)
        #self.nombre_joueurs, self.as_joker, self.nom_joueurs = afficheur_doptions.get_values_saved()




        self.nombre_joueurs = None
        self.as_joker = None
        self.nom_joueurs = []



        # NOMBRE DE JOuEUUR :
       # nb_joueur = self.sauvegarde_read.readline(1)
        #print(nb_joueur)
       #  self.nombre_joueurs = int(nb_joueur)



        #AS JOKER :
       # as_joker = self.sauvegarde_read.readline(2)
       # print(str(as_joker))
        #self.as_joker = str(as_joker)



        self.sauvegarde_read = open('Sauvegarde.txt','r')
        sauvegarde_charactere = self.sauvegarde_read.readlines()


        # print(self.sauvegarde_read.readlines())
        liste = []
        liste1 = []
        liste_de_joueur=[]
        liste_ordre_joueur =[]
        liste_de_joueur1 = []
        liste_de_joueur2 = []
        liste_de_joueur3 = []
        liste_resultat_1 = []
        liste_resultat_2 = []
        liste_resultat_3 = []
        l_1 = []
        l_2 = []
        l_3 = []



        bool_lancer1 = False
        bool_lancer2 = False
        bool_lancer3 = False
        for line in sauvegarde_charactere:
            for c in line :
                    liste.append(c)


        for i in liste :
                liste1 = ''.join(liste)

        sauvegarde_liste = liste1.split('@')
        print(sauvegarde_liste)

        nombre_joueur = sauvegarde_liste[0]
        nombre_joueur_int = int(nombre_joueur)
        as_joker = sauvegarde_liste[1]

        if nombre_joueur_int == 2 :

            nom_joueur_1  = sauvegarde_liste[2]
            nom_joueur_2 = sauvegarde_liste [3]
            liste_de_joueur.append(nom_joueur_1)
            liste_de_joueur.append(nom_joueur_2)
            lancer_max = sauvegarde_liste[4]
            lancer_max_int = int(lancer_max)

            bool_lancer_1 = sauvegarde_liste[5]
            bool_lancer_2 = sauvegarde_liste[6]

            if bool_lancer_1 == "False" :
                bool_lancer1 = False
            elif bool_lancer_1 == "True" :
                bool_lancer1 = True
            if bool_lancer_2 == "False" :
                bool_lancer2 = False
            elif bool_lancer_2 == "True" :
                bool_lancer2 = True


            ordre_joueur = sauvegarde_liste[7]

            charactere_1 = ordre_joueur[1]
            charactere_2 = ordre_joueur[4]

            charactere_1_int = int(charactere_1)
            charactere_2_int = int(charactere_2)

            liste_ordre_joueur.append(charactere_1_int)
            liste_ordre_joueur.append(charactere_2_int)

            self.nombre_joueurs = nombre_joueur_int

            self.as_joker = as_joker

            self.nb_lancer_1 = lancer_max_int

            self.nom_joueurs = liste_de_joueur



            self.bool_lancer_1 = bool_lancer1

            self.bool_lancer_2 = bool_lancer2


            self.ordre_joueur =  liste_ordre_joueur

            self.tour_joueur_1 = 1
            self.tour_joueur_2 = 1



            if bool_lancer_1 == "False" and bool_lancer_2 == "True" :
                joueur_1 = sauvegarde_liste[8]
                char1 = joueur_1[2]
                char2 =  joueur_1[7]
                char3 = joueur_1[12]
                char4 = joueur_1[17]
                char5 = joueur_1[22]
                liste_de_joueur1.append(char1)
                liste_de_joueur1.append(char2)
                liste_de_joueur1.append(char3)
                liste_de_joueur1.append(char4)
                liste_de_joueur1.append(char5)
                print(liste_de_joueur1)
                joueur_1_lancer = sauvegarde_liste[9]

                liste_resultat_1 = joueur_1_lancer.replace('[','')
                liste_resultat_1 = liste_resultat_1.replace(']', '')
                liste_resultat_1 = liste_resultat_1.replace('<','')
                liste_resultat_1 = liste_resultat_1.replace('>', '')
                liste_resultat_1 = liste_resultat_1.replace(' ', '')
                liste_resultat_1 = liste_resultat_1.replace(',', '')
                for i in liste_resultat_1 :
                    if i == '0' :
                        liste_resultat_1 = liste_resultat_1.replace('0', '')
                    if i == '1' :
                        liste_resultat_1 = liste_resultat_1.replace('1', '')
                    if i == '2' :
                        liste_resultat_1 = liste_resultat_1.replace('2', '')
                    if i == '3' :
                        liste_resultat_1 = liste_resultat_1.replace('3', '')
                    if i == '4' :
                        liste_resultat_1 = liste_resultat_1.replace('4', '')
                    if i == '5' :
                        liste_resultat_1 = liste_resultat_1.replace('5', '')


                liste_res_1 = liste_resultat_1.split(':')

                l_1.append(eval(liste_res_1[0]))
                l_1.append(eval(liste_res_1[1]))
                l_1.append(eval(liste_res_1[2]))
                l_1.append(eval(liste_res_1[3]))
                l_1.append(eval(liste_res_1[4]))


                print(eval(liste_res_1[0]))

                self.joueur_1 = liste_de_joueur1
                self.joueur_1_lancer = l_1



            elif bool_lancer_1 == "False" and bool_lancer_2 == "False":
                joueur_1 = sauvegarde_liste[8]
                char1 = joueur_1[2]
                char2 = joueur_1[7]
                char3 = joueur_1[12]
                char4 = joueur_1[17]
                char5 = joueur_1[22]
                liste_de_joueur1.append(char1)
                liste_de_joueur1.append(char2)
                liste_de_joueur1.append(char3)
                liste_de_joueur1.append(char4)
                liste_de_joueur1.append(char5)

                joueur_1_lancer = sauvegarde_liste[9]

                liste_resultat_1 = joueur_1_lancer.replace('[', '')
                liste_resultat_1 = liste_resultat_1.replace(']', '')
                liste_resultat_1 = liste_resultat_1.replace('<', '')
                liste_resultat_1 = liste_resultat_1.replace('>', '')
                liste_resultat_1 = liste_resultat_1.replace(' ', '')
                liste_resultat_1 = liste_resultat_1.replace(',', '')
                for i in liste_resultat_1:
                    if i == '0':
                        liste_resultat_1 = liste_resultat_1.replace('0', '')
                    if i == '1':
                        liste_resultat_1 = liste_resultat_1.replace('1', '')
                    if i == '2':
                        liste_resultat_1 = liste_resultat_1.replace('2', '')
                    if i == '3':
                        liste_resultat_1 = liste_resultat_1.replace('3', '')
                    if i == '4':
                        liste_resultat_1 = liste_resultat_1.replace('4', '')
                    if i == '5':
                        liste_resultat_1 = liste_resultat_1.replace('5', '')

                liste_res_1 = liste_resultat_1.split(':')



                joueur_1 = sauvegarde_liste[8]
                char1 = joueur_1[2]
                char2 = joueur_1[7]
                char3 = joueur_1[12]
                char4 = joueur_1[17]
                char5 = joueur_1[22]
                liste_de_joueur1.append(char1)
                liste_de_joueur1.append(char2)
                liste_de_joueur1.append(char3)
                liste_de_joueur1.append(char4)
                liste_de_joueur1.append(char5)
                print(liste_de_joueur1)
                joueur_1_lancer = sauvegarde_liste[9]

                liste_resultat_1 = joueur_1_lancer.replace('[', '')
                liste_resultat_1 = liste_resultat_1.replace(']', '')
                liste_resultat_1 = liste_resultat_1.replace('<', '')
                liste_resultat_1 = liste_resultat_1.replace('>', '')
                liste_resultat_1 = liste_resultat_1.replace(' ', '')
                liste_resultat_1 = liste_resultat_1.replace(',', '')
                for i in liste_resultat_1:
                    if i == '0':
                        liste_resultat_1 = liste_resultat_1.replace('0', '')
                    if i == '1':
                        liste_resultat_1 = liste_resultat_1.replace('1', '')
                    if i == '2':
                        liste_resultat_1 = liste_resultat_1.replace('2', '')
                    if i == '3':
                        liste_resultat_1 = liste_resultat_1.replace('3', '')
                    if i == '4':
                        liste_resultat_1 = liste_resultat_1.replace('4', '')
                    if i == '5':
                        liste_resultat_1 = liste_resultat_1.replace('5', '')

                l_1.append(eval(liste_res_1[0]))
                l_1.append(eval(liste_res_1[1]))
                l_1.append(eval(liste_res_1[2]))
                l_1.append(eval(liste_res_1[3]))
                l_1.append(eval(liste_res_1[4]))




                joueur_2 = sauvegarde_liste[10]

                char11 = joueur_2[2]
                char22 = joueur_2[7]
                char33 = joueur_2[12]
                char44 = joueur_2[17]
                char55 = joueur_2[22]
                liste_de_joueur2.append(char11)
                liste_de_joueur2.append(char22)
                liste_de_joueur2.append(char33)
                liste_de_joueur2.append(char44)
                liste_de_joueur2.append(char55)


                joueur_2_lancer = sauvegarde_liste[11]

                liste_resultat_2 = joueur_2_lancer.replace('[', '')
                liste_resultat_2 = liste_resultat_2.replace(']', '')
                liste_resultat_2 = liste_resultat_2.replace('<', '')
                liste_resultat_2 = liste_resultat_2.replace('>', '')
                liste_resultat_2 = liste_resultat_2.replace(' ', '')
                liste_resultat_2 = liste_resultat_2.replace(',', '')


                for i in liste_resultat_2:
                    if i == '0':
                        liste_resultat_2 = liste_resultat_2.replace('0', '')
                    if i == '1':
                        liste_resultat_2 = liste_resultat_2.replace('1', '')
                    if i == '2':
                        liste_resultat_2 = liste_resultat_2.replace('2', '')
                    if i == '3':
                        liste_resultat_2 = liste_resultat_2.replace('3', '')
                    if i == '4':
                        liste_resultat_2 = liste_resultat_2.replace('4', '')
                    if i == '5':
                        liste_resultat_2 = liste_resultat_2.replace('5', '')

                liste_res_2 = liste_resultat_1.split(':')


                l_2.append(eval(liste_res_2[0]))
                l_2.append(eval(liste_res_2[1]))
                l_2.append(eval(liste_res_2[2]))
                l_2.append(eval(liste_res_2[3]))
                l_2.append(eval(liste_res_2[4]))


                print(eval(liste_res_2[0]))

                self.joueur_1 = liste_de_joueur1
                self.joueur_1_lancer = l_1
                self.joueur_2 = liste_de_joueur2
                self.joueur_2_lancer = l_2


        elif nombre_joueur_int == 3 :
            nom_joueur_1 = sauvegarde_liste[2]
            nom_joueur_2 = sauvegarde_liste[3]
            nom_joueur_3 = sauvegarde_liste[4]
            liste_de_joueur.append(nom_joueur_1)
            liste_de_joueur.append(nom_joueur_2)
            liste_de_joueur.append(nom_joueur_3)


            lancer_max = sauvegarde_liste[5]
            lancer_max_int = int(lancer_max)


            bool_lancer_1 = sauvegarde_liste[6]
            bool_lancer_2 = sauvegarde_liste[7]
            bool_lancer_3 = sauvegarde_liste[8]

            if bool_lancer_1 == "False" :
                bool_lancer1 = False
            elif bool_lancer_1 == "True" :
                bool_lancer1 = True
            if bool_lancer_2 == "False" :
                bool_lancer2 = False
            elif bool_lancer_2 == "True" :
                bool_lancer2 = True
            if bool_lancer_3 == "False":
                bool_lancer3 = False
            elif bool_lancer_3 == "True":
                 bool_lancer3 = True



            ordre_joueur = sauvegarde_liste[9]

            charactere_1 = ordre_joueur[1]
            charactere_2 = ordre_joueur[4]
            charactere_3 = ordre_joueur[7]
            charactere_1_int = int(charactere_1)
            charactere_2_int = int(charactere_2)
            charactere_3_int = int(charactere_3)

            liste_ordre_joueur.append(charactere_1_int)
            liste_ordre_joueur.append(charactere_2_int)
            liste_ordre_joueur.append(charactere_3_int)

            self.nombre_joueurs = nombre_joueur_int

            self.as_joker = as_joker

            self.nb_lancer_1 = lancer_max_int

            self.nom_joueurs = liste_de_joueur

            self.bool_lancer_1 = bool_lancer1

            self.bool_lancer_2 = bool_lancer2
            self.bool_lancer_3 = bool_lancer3

            self.ordre_joueur = liste_ordre_joueur

            self.tour_joueur_1 = 1
            self.tour_joueur_2 = 1
            self.tour_joueur_3 = 1



            if bool_lancer_2 == "False" and bool_lancer_2 == "True" and bool_lancer_3 == "False":
                joueur_1 = sauvegarde_liste[10]
                char1 = joueur_1[2]
                char2 = joueur_1[7]
                char3 = joueur_1[12]
                char4 = joueur_1[17]
                char5 = joueur_1[22]
                liste_de_joueur1.append(char1)
                liste_de_joueur1.append(char2)
                liste_de_joueur1.append(char3)
                liste_de_joueur1.append(char4)
                liste_de_joueur1.append(char5)
                joueur_1_lancer = sauvegarde_liste[11]

                liste_resultat_1 = joueur_1_lancer.replace('[', '')
                liste_resultat_1 = liste_resultat_1.replace(']', '')
                liste_resultat_1 = liste_resultat_1.replace('<', '')
                liste_resultat_1 = liste_resultat_1.replace('>', '')
                liste_resultat_1 = liste_resultat_1.replace(' ', '')
                liste_resultat_1 = liste_resultat_1.replace(',', '')
                for i in liste_resultat_1:
                    if i == '0':
                        liste_resultat_1 = liste_resultat_1.replace('0', '')
                    if i == '1':
                        liste_resultat_1 = liste_resultat_1.replace('1', '')
                    if i == '2':
                        liste_resultat_1 = liste_resultat_1.replace('2', '')
                    if i == '3':
                        liste_resultat_1 = liste_resultat_1.replace('3', '')
                    if i == '4':
                        liste_resultat_1 = liste_resultat_1.replace('4', '')
                    if i == '5':
                        liste_resultat_1 = liste_resultat_1.replace('5', '')

                liste_res_1 = liste_resultat_1.split(':')

                l_1.append(eval(liste_res_1[0]))
                l_1.append(eval(liste_res_1[1]))
                l_1.append(eval(liste_res_1[2]))
                l_1.append(eval(liste_res_1[3]))
                l_1.append(eval(liste_res_1[4]))

                print(eval(liste_res_1[0]))

                self.joueur_1 = liste_de_joueur1
                self.joueur_1_lancer = l_1


            elif bool_lancer_2 == "False" and bool_lancer_2 == "False" and bool_lancer_3 == "True":
                joueur_1 = sauvegarde_liste[10]
                char1 = joueur_1[2]
                char2 = joueur_1[7]
                char3 = joueur_1[12]
                char4 = joueur_1[17]
                char5 = joueur_1[22]
                liste_de_joueur1.append(char1)
                liste_de_joueur1.append(char2)
                liste_de_joueur1.append(char3)
                liste_de_joueur1.append(char4)
                liste_de_joueur1.append(char5)
                joueur_1_lancer = sauvegarde_liste[11]

                liste_resultat_1 = joueur_1_lancer.replace('[', '')
                liste_resultat_1 = liste_resultat_1.replace(']', '')
                liste_resultat_1 = liste_resultat_1.replace('<', '')
                liste_resultat_1 = liste_resultat_1.replace('>', '')
                liste_resultat_1 = liste_resultat_1.replace(' ', '')
                liste_resultat_1 = liste_resultat_1.replace(',', '')
                for i in liste_resultat_1:
                    if i == '0':
                        liste_resultat_1 = liste_resultat_1.replace('0', '')
                    if i == '1':
                        liste_resultat_1 = liste_resultat_1.replace('1', '')
                    if i == '2':
                        liste_resultat_1 = liste_resultat_1.replace('2', '')
                    if i == '3':
                        liste_resultat_1 = liste_resultat_1.replace('3', '')
                    if i == '4':
                        liste_resultat_1 = liste_resultat_1.replace('4', '')
                    if i == '5':
                        liste_resultat_1 = liste_resultat_1.replace('5', '')

                liste_res_1 = liste_resultat_1.split(':')
                l_1.append(eval(liste_res_1[0]))
                l_1.append(eval(liste_res_1[1]))
                l_1.append(eval(liste_res_1[2]))
                l_1.append(eval(liste_res_1[3]))
                l_1.append(eval(liste_res_1[4]))

                joueur_2 = sauvegarde_liste[12]
                char11 = joueur_2[2]
                char22 = joueur_2[7]
                char33 = joueur_2[12]
                char44 = joueur_2[17]
                char55 = joueur_2[22]
                liste_de_joueur2.append(char11)
                liste_de_joueur2.append(char22)
                liste_de_joueur2.append(char33)
                liste_de_joueur2.append(char44)
                liste_de_joueur2.append(char55)

                joueur_2_lancer = sauvegarde_liste[13]

                liste_resultat_2 = joueur_2_lancer.replace('[', '')
                liste_resultat_2 = liste_resultat_2.replace(']', '')
                liste_resultat_2 = liste_resultat_2.replace('<', '')
                liste_resultat_2 = liste_resultat_2.replace('>', '')
                liste_resultat_2 = liste_resultat_2.replace(' ', '')
                liste_resultat_2 = liste_resultat_2.replace(',', '')

                for i in liste_resultat_2:
                    if i == '0':
                        liste_resultat_2 = liste_resultat_2.replace('0', '')
                    if i == '1':
                        liste_resultat_2 = liste_resultat_2.replace('1', '')
                    if i == '2':
                        liste_resultat_2 = liste_resultat_2.replace('2', '')
                    if i == '3':
                        liste_resultat_2 = liste_resultat_2.replace('3', '')
                    if i == '4':
                        liste_resultat_2 = liste_resultat_2.replace('4', '')
                    if i == '5':
                        liste_resultat_2 = liste_resultat_2.replace('5', '')

                liste_res_2 = liste_resultat_1.split(':')
                l_2.append(eval(liste_res_2[0]))
                l_2.append(eval(liste_res_2[1]))
                l_2.append(eval(liste_res_2[2]))
                l_2.append(eval(liste_res_2[3]))
                l_2.append(eval(liste_res_2[4]))

                self.joueur_1 = liste_de_joueur1
                self.joueur_1_lancer = l_1
                self.joueur_2 = liste_de_joueur2
                self.joueur_2_lancer = l_2

        """
        self.nombre_joueurs = 3

        self.nb_lancer_1 = 3

        self.as_joker = 'oui'

        self.nom_joueurs=['Lil','Xx','Lol']

        self.ordre_joueur=[1,0,3]

        self.bool_lancer_1 = False
        self.bool_lancer_2 = False
        self.bool_lancer_3 = True

        self.tour_joueur_1 = 1
        self.tour_joueur_2 = 1
        self.tour_joueur_3 = 1

        #self.joueur_1 = ['A', 'R', 'D', 'V', 'X']
        #self.joueur_2 = ['A', 'R', 'D', 'V', 'X']

        #self.joueur_1_lancer =  [Carte.AS, Carte.ROI, Carte.DAME, Carte.VALET, Carte.DIX]
       # self.joueur_2_lancer =  [Carte.AS, Carte.ROI, Carte.DAME, Carte.VALET, Carte.DIX]


        self.joueur_1 = ['X', 'X', 'X', 'X', 'X']
        self.joueur_2 = ['X', 'X', 'X', 'X', 'X']

        self.joueur_1_lancer =  [eval("Carte.DIX"), eval("Carte.DIX"),eval("Carte.DIX"), eval("Carte.DIX"), eval("Carte.DIX")]
        self.joueur_2_lancer =  [eval("Carte.DIX"), eval("Carte.DIX"),eval("Carte.DIX"), eval("Carte.DIX"), eval("Carte.DIX")]
        """
        self.afficher_partie()
        self.jouer_sauvegarde()




    def definir_partie(self):

        self.indice_joueur_courant = None
        self.phase = InterfaceGraphique.TROUVER_PREMIER
        self.tour = 0
        self.lancer_passer_control_var = BooleanVar(value=False)
        self.choix = None
        self.value_checkbutton()

        afficheur_doptions = Parametres_partie(self)
        self.nombre_joueurs, self.as_joker, self.nom_joueurs = afficheur_doptions.get_values_saved()



        self.nb_lancer = 0
        self.nb_lancer_1 = 0
        self.nb_lancer_2 = 0
        self.nb_lancer_autre = 0
        self.nb_lancer_autre_1 = 0
        self.nb_lancer_autre_2 = 0
        self.max_lancer = 3
        self.zero = 0

        self.joueur_liste = []

        self.passer = 0
        self.joueur_1 = []
        self.joueur_2 = []
        self.joueur_3 = []
        self.joueur_1_lancer = None
        self.joueur_2_lancer = None
        self.joueur_3_lancer = None

        self.commencer_1 = False
        self.commencer_2 = False
        self.commencer_3 = False
        self.commencer = True

        self.bool_passer = True
        self.bool_compteur_lancer_1 = True
        self.bool_lancer_1 = True
        self.bool_lancer_2 = False
        self.bool_lancer_3 = False


        self.combinaison_1 = None
        self.combinaison_2 = None
        self.combinaison_3 = None

        self.lol_1 = False
        self.lol_2 = False
        self.lol_3 = False

        self.tour_joueur_1 = 1
        self.tour_joueur_2 = 1
        self.tour_joueur_3 = 1
        self.test = None
        self.lolxd = None
        self.lancer = None

        self.afficher_partie()
        self.jouer()
       # self.sauvegarder()

#   Appel un nouveau tour de jeu
    def update(self):
        self.tour_jouer()

#   Appel un nouveau tour de jeu en modifiant les compteurs de la définition "passer_tour"
    def update_passer(self):
        self.passer_tour()

    def afficher_partie(self):
        self.cacher_menu_principal()
        self.frame_de_gauche.grid(row=0, column=0)
        self.frame_de_bas.grid(row=1,column=0)
        self.boutonframe.grid(row=2, column=0)
        self.frame_bouton.grid(row=3, column=0)

    def afficher_message(self, message):
        self.message.grid_forget()
        self.message['text'] = message
        self.message.grid(row=1, column=0)
        self.message.after(3000, self.message.grid_forget)

    def sauvegarder(self):
        if self.nombre_joueurs ==2 :
            self.sauvegarde = open('Sauvegarde.txt', 'w')


            self.sauvegarde.write(str(self.nombre_joueurs)+'@')
            self.sauvegarde.write((self.as_joker)+'@')

            if self.lol_1 == True :

                self.sauvegarde.write(str(self.nom_joueurs[0]) + '@')
                self.sauvegarde.write(str(self.nom_joueurs[1]) + '@')

                self.sauvegarde.write(str(self.nb_lancer_1) + '@')
                self.sauvegarde.write(str(self.bool_lancer_1) + '@')
                self.sauvegarde.write(str(self.bool_lancer_2) + '@')

                self.sauvegarde.write(str(self.ordre_joueur) + '@')
                self.sauvegarde.write(str(self.joueur_1) + '@')
                self.sauvegarde.write(str(self.joueur_1_lancer) + '@')

                self.sauvegarde.close()





            elif self.lol_2 == True :

                self.sauvegarde.write(str(self.nom_joueurs[0]) + '@')
                self.sauvegarde.write(str(self.nom_joueurs[1]) + '@')

                self.sauvegarde.write(str(self.nb_lancer_1) + '@')
                self.sauvegarde.write(str(self.bool_lancer_1) + '@')
                self.sauvegarde.write(str(self.bool_lancer_2) + '@')

                self.sauvegarde.write(str(self.ordre_joueur) + '@')
                self.sauvegarde.write(str(self.joueur_1) + '@')
                self.sauvegarde.write(str(self.joueur_1_lancer) + '@')
                self.sauvegarde.write(str(self.joueur_2) + '@')
                self.sauvegarde.write(str(self.joueur_2_lancer) + '@')
                self.sauvegarde.close()


            else :

                 self.sauvegarde.close()




        elif self.nombre_joueurs == 3 :

                self.sauvegarde = open('Sauvegarde.txt', 'w')

                self.sauvegarde.write(str(self.nombre_joueurs)+ '@')
                self.sauvegarde.write(str(self.as_joker)+ '@')


                if self.lol_1 == True:

                    self.sauvegarde.write(str(self.nom_joueurs[0]) + '@')
                    self.sauvegarde.write(str(self.nom_joueurs[1]) + '@')
                    self.sauvegarde.write(str(self.nom_joueurs[2]) + '@')
                    self.sauvegarde.write(str(self.nb_lancer_1) + '@')
                    self.sauvegarde.write(str(self.bool_lancer_1) + '@')
                    self.sauvegarde.write(str(self.bool_lancer_2) + '@')
                    self.sauvegarde.write(str(self.bool_lancer_3) + '@')
                    self.sauvegarde.write(str(self.ordre_joueur) + '@')
                    self.sauvegarde.write(str(self.joueur_1) + '@')
                    self.sauvegarde.write(str(self.joueur_1_lancer) + '@')
                    self.sauvegarde.close()



                elif self.lol_2 == True :

                     self.sauvegarde.write(str(self.nom_joueurs[0]) + '@')
                     self.sauvegarde.write(str(self.nom_joueurs[1]) + '@')
                     self.sauvegarde.write(str(self.nom_joueurs[2]) + '@')
                     self.sauvegarde.write(str(self.nb_lancer_1) + '@')
                     self.sauvegarde.write(str(self.bool_lancer_1) + '@')
                     self.sauvegarde.write(str(self.bool_lancer_2) + '@')
                     self.sauvegarde.write(str(self.bool_lancer_3) + '@')
                     self.sauvegarde.write(str(self.ordre_joueur) + '@')
                     self.sauvegarde.write(str(self.joueur_1) + '@')
                     self.sauvegarde.write(str(self.joueur_1_lancer) + '@')
                     self.sauvegarde.write(str(self.joueur_2) + '@')
                     self.sauvegarde.write(str(self.joueur_2_lancer) + '@')
                     self.sauvegarde.close()







                elif self.lol_3 == True :

                    self.sauvegarde.write(str(self.nom_joueurs[0]) + '@')
                    self.sauvegarde.write(str(self.nom_joueurs[1]) + '@')
                    self.sauvegarde.write(str(self.nom_joueurs[2]) + '@')
                    self.sauvegarde.write(str(self.nb_lancer_1) + '@')
                    self.sauvegarde.write(str(self.bool_lancer_1) + '@')
                    self.sauvegarde.write(str(self.bool_lancer_2) + '@')
                    self.sauvegarde.write(str(self.bool_lancer_3) + '@')
                    self.sauvegarde.write(str(self.ordre_joueur) + '@')
                    self.sauvegarde.write(str(self.joueur_1) + '@')
                    self.sauvegarde.write(str(self.joueur_1_lancer) + '@')
                    self.sauvegarde.write(str(self.joueur_2) + '@')
                    self.sauvegarde.write(str(self.joueur_2_lancer) + '@')
                    self.sauvegarde.write(str(self.joueur_3) + '@')
                    self.sauvegarde.write(str(self.joueur_3_lancer) + '@')
                    self.sauvegarde.close()

                else :
                    self.sauvegarde.close()


    def afficher_tableau(self):

        self.recap_canvas.delete()


        self.checkbutton_1 = Checkbutton(self.frame_de_bas, text="", variable=self.var_1)
        self.checkbutton_1.grid(row=11, column=0, padx=0, pady=10)

        self.checkbutton_2 = Checkbutton(self.frame_de_bas, text="", variable=self.var_2)
        self.checkbutton_2.grid(row=11, column=1, padx=0, pady=10)

        self.checkbutton_3 = Checkbutton(self.frame_de_bas, text="", variable=self.var_3)
        self.checkbutton_3.grid(row=11, column=2, padx=0, pady=10)

        self.checkbutton_4 = Checkbutton(self.frame_de_bas, text="", variable=self.var_4)
        self.checkbutton_4.grid(row=11, column=3, padx=0, pady=10)

        self.checkbutton_5 = Checkbutton(self.frame_de_bas, text="", variable=self.var_5)
        self.checkbutton_5.grid(row=11, column=4, padx=0, pady=10)

        self.valeurs_obtenues.relancer_des([])

        self.lancer = self.valeurs_obtenues.des
        self.liste = []


        list_checkbox = self.value_checkbutton()
        self.lol = self.valeurs_obtenues.relancer_des(list_checkbox)

        for elem in self.lancer:
                 # chaine += "{:^3s}".format(elem)
                self.liste += "{:s}".format(elem)



        self.carte_1 = Label(self.frame_de_bas,text=self.liste[0])
        self.carte_1.grid(row=10,column=0,padx=0,pady=10)

        self.carte_2 = Label(self.frame_de_bas,text=self.liste[1])
        self.carte_2.grid(row=10,column=1,padx=0,pady=10)

        self.carte_3 = Label(self.frame_de_bas, text=self.liste[2])
        self.carte_3.grid(row=10, column=2, padx=0, pady=10)

        self.carte_4 = Label(self.frame_de_bas, text=self.liste[3])
        self.carte_4.grid(row=10, column=3, padx=0, pady=10)

        self.carte_5 = Label(self.frame_de_bas, text=self.liste[4])
        self.carte_5.grid(row=10, column=4, padx=0, pady=10)


    def passer_tour (self):
        self.bool_passer = False
        self.bool_compteur_lancer_1 = False
        self.tour_jouer()

    def tour_jouer (self):

        if self.nombre_joueurs == 2 :


            if self.bool_compteur_lancer_1 == True :
                self.tour_joueur_1 += 1
                self.var_num_lancer.config(text=self.tour_joueur_1)
                self.var_nbr_max_lancer.config(text=NB_MAX_LANCERS)


            if self.bool_lancer_1 == True :

                self.lol_1 = True
                self.var_nom_joueur_courant.config(text= self.nom_joueurs[self.ordre_joueur[0]])



            if self.bool_lancer_2 == True :
                self.tour_joueur_2 +=1
                if self.tour_joueur_2 > self.nb_lancer_1:
                    self.tour_joueur_2 = self.nb_lancer_1

                self.var_num_lancer.config(text=self.tour_joueur_2)
                self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[1]])

                self.lol_1= False
                self.lol_2 = True



            if self.bool_passer == False:
                self.passer += 1



            elif self.bool_passer == True :

                self.afficher_tableau()


            self.bool_passer = True




            if self.lol_1 == True :
                if self.tour_joueur_1==NB_MAX_LANCERS or self.passer == 1 :

                    self.bool_lancer_1 = False
                    self.bool_lancer_2 = True

                    self.commencer_1 = True
                    self.combinaison_2= False



                    self.nb_lancer_1 = self.tour_joueur_1
                    self.joueur_1 = self.liste
                    self.joueur_1_lancer = self.lancer

                    self.joueur_liste.append(self.joueur_1)
                    self.passer = 2
                    self.sauvegarder()
                    #self.sauvegarde.close()
                    self.type_de_combin()
                    self.changer_tour()




            elif self.lol_2 == True :
                if self.tour_joueur_2 >=  self.nb_lancer_1 or self.passer == 3 :


                    self.bool_lancer_1 = False
                    self.bool_lancer_2 = True

                    self.commencer_1 = False
                    self.commencer_2 = True




                    self.joueur_2 = self.liste

                    self.joueur_2_lancer = self.lancer


                    self.joueur_liste.append(self.joueur_2)

                    self.sauvegarder()
                    #self.sauvegarde.close()

                    self.type_de_combin()
                    self.changer_tour()
                    self.commencer_disable()
                    self.arreter_jeur()
                    self.combin_gagnant()




        elif self.nombre_joueurs == 3:


            if self.bool_compteur_lancer_1 == True:
                self.tour_joueur_1 += 1
                self.var_num_lancer.config(text = self.tour_joueur_1)
                self.var_nbr_max_lancer.config(text=NB_MAX_LANCERS)



            if self.bool_lancer_1 == True:
                self.lol_1 = True
                self.lol_2 = False
                self.lol_3 = False
                self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[0]])



            if self.bool_lancer_2 == True:
                self.tour_joueur_2 += 1
                if self.tour_joueur_2 > self.nb_lancer_1:
                    self.tour_joueur_2 = self.nb_lancer_1

                self.var_num_lancer.config(text=self.tour_joueur_2)
                self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[1]])
                self.lol_1 = False
                self.lol_2 = True
                self.lol_3 = False

            if self.bool_lancer_3 == True:
                self.tour_joueur_3 += 1
                if self.tour_joueur_3 > self.nb_lancer_1:
                    self.tour_joueur_3 = self.nb_lancer_1
                self.var_num_lancer.config(text=self.tour_joueur_3)
                self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[2]])

                self.lol_1 = False
                self.lol_2 = False
                self.lol_3 = True

            if self.bool_passer == False:
                self.passer += 1


            elif self.bool_passer == True:

                self.afficher_tableau()

            self.bool_passer = True

            if self.lol_1 == True:
                if self.tour_joueur_1 == NB_MAX_LANCERS or self.passer == 1:
                    self.bool_lancer_2 = True
                    self.bool_lancer_1 = False
                    self.bool_lancer_3 = False
                    self.commencer_1 = True
                    self.commencer_2 = False
                    self.commencer_3 = False



                    self.nb_lancer_1 = self.tour_joueur_1

                    self.joueur_1 = self.liste
                    self.joueur_1_lancer = self.lancer

                    self.joueur_liste.append(self.joueur_1)
                    self.passer = 2

                    self.sauvegarder()
                    #self.sauvegarde.close()

                    self.type_de_combin()
                    self.changer_tour()






            elif self.lol_2 == True:
                if self.tour_joueur_2 == self.nb_lancer_1 or self.passer == 3:
                    self.bool_lancer_2 = False
                    self.bool_lancer_1 = False
                    self.bool_lancer_3 = True
                    self.commencer_1 = False
                    self.commencer_2 = True
                    self.commencer_3 = False

                    self.joueur_2 = self.liste
                    self.joueur_2_lancer = self.lancer
                    self.joueur_liste.append(self.joueur_1)
                    self.passer = 4


                    self.sauvegarder()
                    #self.sauvegarde.close()


                    self.type_de_combin()
                    self.changer_tour()





            elif self.lol_3 == True:
                if self.tour_joueur_3 == self.nb_lancer_1 or self.passer == 5:
                    self.bool_lancer_2 = False
                    self.bool_lancer_1 = False
                    self.bool_lancer_3 = True

                    self.passer = 5

                    self.commencer_1 = False
                    self.commencer_2 = False
                    self.commencer_3 = True


                    self.joueur_3 = self.liste
                    self.joueur_3_lancer = self.lancer
                    self.joueur_liste.append(self.joueur_3)

                    self.sauvegarder()
                    #self.sauvegarde.close()


                    self.type_de_combin()

                    self.changer_tour()
                    self.commencer_disable()
                    self.arreter_jeur()
                    self.combin_gagnant()







    def type_de_combin (self):

        if self.as_joker == "oui":

            if self.lol_1 == True :

                 self.test = Combinaison(self.joueur_1_lancer)
                 self.combinaison_1= self.test.determiner_type_combinaison()
                 self.var_joueur_1_resultat.config(text=self.combinaison_1)
                 self.var_joueur_1_sequence.config(text=self.joueur_1)

            if self.lol_2 == True :

                self.test1 = Combinaison(self.joueur_2_lancer)
                self.combinaison_2 = self.test1.determiner_type_combinaison()
                self.var_joueur_2_resultat.config(text=self.combinaison_2)
                self.var_joueur_2_sequence.config(text=self.joueur_2)

            if self.lol_3 == True :
                self.test1 = Combinaison(self.joueur_3_lancer)
                self.combinaison_3 = self.test1.determiner_type_combinaison()
                self.var_joueur_3_resultat.config(text=self.combinaison_3)
                self.var_joueur_3_sequence.config(text=self.joueur_3)


        else :

            if self.lol_1 == True:
                self.test = Combinaison(self.joueur_1_lancer)
                self.combinaison_1 = self.test.determiner_type_combinaison_sans_AS()
                self.var_joueur_1_resultat.config(text=self.combinaison_1)
                self.var_joueur_1_sequence.config(text=self.joueur_1)

            if self.lol_2 == True:
                self.test2 = Combinaison(self.joueur_2_lancer)
                self.combinaison_2 = self.test2.determiner_type_combinaison_sans_AS()
                self.var_joueur_2_resultat.config(text=self.combinaison_2)
                self.var_joueur_2_sequence.config(text=self.joueur_2)

            if self.lol_3 == True:
                self.test3 = Combinaison(self.joueur_3_lancer)
                self.combinaison_3 = self.test3.determiner_type_combinaison_sans_AS()
                self.var_joueur_3_resultat.config(text=self.combinaison_3)
                self.var_joueur_3_sequence.config(text=self.joueur_3)

    def combin_gagnant (self) :



        if self.nombre_joueurs == 2 :

            joueur_1 = self.combinaison_1.value
            joueur_2 = self.combinaison_2.value

            if joueur_1 < joueur_2 :
                messagebox.showinfo("Gagnant","{0} GAGNE".format(self.nom_joueurs[self.ordre_joueur[1]]))
            elif joueur_1 > joueur_2:
                messagebox.showinfo("Gagnant","{0} GAGNE".format(self.nom_joueurs[self.ordre_joueur[0]]))
            elif joueur_1 == joueur_2:
                messagebox.showinfo("Égalité","Le match est nul ")

        elif self.nombre_joueurs == 3 :

            joueur_1 = self.combinaison_1.value
            joueur_2 = self.combinaison_2.value
            joueur_3 = self.combinaison_3.value


            if joueur_1 > joueur_2 and joueur_1 > joueur_3:
                messagebox.showinfo("Gagnant","{0} GAGNE".format(self.nom_joueurs[self.ordre_joueur[0]]))

            elif joueur_2 > joueur_3 and joueur_2 > joueur_1:
                messagebox.showinfo("Gagnant","{0} GAGNE".format(self.nom_joueurs[self.ordre_joueur[1]]))

            elif joueur_3> joueur_1 and joueur_3 > joueur_2:
                messagebox.showinfo("Gagnant","{0} GAGNE".format(self.nom_joueurs[self.ordre_joueur[2]]))

            elif joueur_1 == joueur_2 and joueur_1 == joueur_3:
                messagebox.showinfo("Égalité","Le match est nul ")


    def txt_utilisateur (self, string):

        return self.string


    def lancer_des(self):

        self.lancer_passer_control_var.set(True)
        self.choix = "L"

    def empecher_lancer(self):

        self.bouton_lancer.config(state=DISABLED)

    def permettre_lancer(self):

        self.bouton_lancer.config(state=NORMAL)

    def empecher_passer(self):

        self.bouton_passer.config(state=DISABLED)

    def permettre_passer(self):

        self.bouton_passer.config(state=NORMAL)

    def commencer_disable(self):

        self.bouton_commencer.config(state=DISABLED)

    def commencer_enable(self):

        self.bouton_commencer.config(state=NORMAL)

    def passer_au_suivant(self):

        self.lancer_passer_control_var.set(True)
        self.choix = "P"

        self.passer += 1

        if self.passer == 1:
            print("JOUEUR 1")
            self.joueur_1 = self.liste
            print(self.joueur_1)
        elif self.passer == 2 :
            print("JOEUR2")
            self.joueur_2 = self.liste
            print(self.joueur_2)

        elif self.passer ==3 :
            print("joueur 3")
            self.joueur_3 = self.liste
            print(self.joueur_3)


#   Indique que le tour d'un joueur est terminé et que s'il y a un prochain joueur, c'est à son tour
    def changer_tour (self):

            self.commencer_enable()
            self.arreter_jeur()
            messagebox._show("Tour terminé","Le joueur a terminé son tour. C'est maintenant au prochain joueur.")

#   Empêche la sélection du bouton "Commencer" et permet la sélection du bouton "Lancer"
    def commencer_tour(self):

        self.permettre_lancer()
        self.commencer_disable()

        if self.commencer == True :

            self.afficher_tableau()
            self.checkbutton_1.select()
            self.checkbutton_2.select()
            self.checkbutton_3.select()
            self.checkbutton_4.select()
            self.checkbutton_5.select()
            self.afficher_tableau()
            self.permettre_passer()
            self.commencer = False

            self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[0]])
            self.joueur_1_lancer = 1
            self.var_num_lancer.config(text=self.joueur_1_lancer)
            self.var_nbr_max_lancer.config(text=NB_MAX_LANCERS)


        if self.commencer_1 == True :

            self.checkbutton_1.select()
            self.checkbutton_2.select()
            self.checkbutton_3.select()
            self.checkbutton_4.select()
            self.checkbutton_5.select()
            self.afficher_tableau()
            self.permettre_passer()




            self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[1]])
            self.joueur_2_lancer = 1
            self.var_num_lancer.config(text=self.joueur_2_lancer)
            self.var_nbr_max_lancer.config(text=self.nb_lancer_1)
        elif self.commencer_2 == True :
            self.checkbutton_1.select()
            self.checkbutton_2.select()
            self.checkbutton_3.select()
            self.checkbutton_4.select()
            self.checkbutton_5.select()
            self.afficher_tableau()
            self.permettre_passer()

            self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[2]])
            self.joueur_3_lancer = 1
            self.var_num_lancer.config(text=self.joueur_3_lancer)
            self.var_nbr_max_lancer.config(text=self.nb_lancer_1)

        elif self.commencer_3 == True :
            self.checkbutton_1.select()
            self.checkbutton_2.select()
            self.checkbutton_3.select()
            self.checkbutton_4.select()
            self.checkbutton_5.select()
            self.afficher_tableau()

            self.var_nom_joueur_courant.config(text=self.nom_joueurs[self.ordre_joueur[2]])
            self.joueur_3_lancer = 1
            self.var_num_lancer.config(text=self.joueur_3_lancer)
            self.var_nbr_max_lancer.config(text=self.nb_lancer_1)

#   Empêche le joueur de sélectionner les boutons "Passer" et "Lancer"
    def arreter_jeur(self):

        self.empecher_passer()
        self.empecher_lancer()

#   Crée une liste d'ordre aléatoire des joueurs de la partie et permet d'utiliser le bouton "Commencer"
    def determiner_premier_lanceur(self):

        partie = Partie(self.nom_joueurs)
        self.ordre_joueur = partie._determiner_ordre()
        self.commencer_enable()


        for i in range(0, len(self.ordre_joueur)):
            joueur = self.nom_joueurs[self.ordre_joueur[i]]
            self.ordre_joueur_label1 = Label(self.frame_de_gauche, text="Le joueur {} est {}".format(i + 1, joueur))
            self.ordre_joueur_label1.grid(row=i + 1, column=0, padx=0, pady=0)

#   Initialisation des valeurs par défaut contenues dans le tableau des résultats (pour deux joueurs)
        if  self.nombre_joueurs == 2 :

            self.commencer_enable()
            self.nom_joueur_1.config(text=self.nom_joueurs[self.ordre_joueur[0]])
            self.nom_joueur_2.config(text=self.nom_joueurs[self.ordre_joueur[1]])
            self.nom_joueur_3.config(text="")
            self.nom_joueur_3_resultat.config(text="")
            self.var_joueur_3_resultat.config (text="")
            self.var_joueur_3_sequence.config(text="")
            self.var_num_lancer.config(text="XXXXX")
            self.var_joueur_1_resultat.config(text="X")
            self.var_joueur_2_resultat.config(text="X")
            self.var_joueur_3_resultat.config(text="")
            self.var_joueur_1_sequence.config(text="X")
            self.var_joueur_2_sequence.config(text="X")
            self.var_joueur_3_sequence.config(text="")

#   Initialisation des valeurs par défaut contenues dans le tableau des résultats (pour deux joueurs)
        elif self.nombre_joueurs == 3 :
            self.nom_joueur_1.config(text=self.nom_joueurs[self.ordre_joueur[0]])
            self.nom_joueur_2.config(text=self.nom_joueurs[self.ordre_joueur[1]])
            self.nom_joueur_3.config(text=self.nom_joueurs[self.ordre_joueur[2]])
            self.var_num_lancer.config(text="XXXXX")
            self.var_joueur_1_resultat.config(text="X")
            self.var_joueur_2_resultat.config(text="X")
            self.var_joueur_3_resultat.config(text="X")
            self.var_joueur_1_sequence.config(text="X")
            self.var_joueur_2_sequence.config(text="X")
            self.var_joueur_3_sequence.config(text="X")


        concernes = list(range(self.nombre_joueurs))
        self.premier = concernes[0]


    def jouer_tour_premiere_phase(self):

        self.tour += 1
        self.empecher_lancer()
        self.empecher_passer()

        for i in range(self.nombre_joueurs):
            pos = (self.premier+i) % self.nombre_joueurs

            self.indice_joueur_courant = pos

        return -1, -1

#   Prend la valeur inscrite dans chaque bouton (1 ou 0) et retourne une liste (Ex.: [0,1,0,0,0] si seulement le
#   deuxième dé est activé pour la relance)
    def value_checkbutton(self):

        value = []
        value.clear()

        if self.var_1.get():
            value.append(0)

        if self.var_2.get():
            value.append(1)

        if self.var_3.get():
            value.append(2)

        if self.var_4.get():
            value.append(3)

        if self.var_5.get():
            value.append(4)

        return value

#   Place le compteur "self.tour" à zéro et appel les définitions "determiner_premier_lanceur" et "jouer_tour_premiere_phase"
    def jouer(self):

        self.tour = 0
        self.determiner_premier_lanceur()
        self.jouer_tour_premiere_phase()

#   Appel les définitions de sauvegarde pour la reprise d'un jeu
    def jouer_sauvegarde(self):

        self.tour = 0
        self.determiner_premier_lanceur_sauvegarde()
        self.jouer_tour_premiere_phase_sauvegarde()

    def determiner_premier_lanceur_sauvegarde (self):



            self.commencer_enable()

            for i in range(0, len(self.ordre_joueur)):

                joueur = self.nom_joueurs[self.ordre_joueur[i]]
                self.ordre_joueur_label1 = Label(self.frame_de_gauche, text="Le joueur {} est {}".format(i + 1, joueur))
                self.ordre_joueur_label1.grid(row=i + 1, column=0, padx=0, pady=0)

            if self.nombre_joueurs == 2:

                self.commencer_enable()
                self.nom_joueur_1.config(text=self.nom_joueurs[self.ordre_joueur[0]])
                self.nom_joueur_2.config(text=self.nom_joueurs[self.ordre_joueur[1]])
                self.nom_joueur_3.config(text="")
                self.nom_joueur_3_resultat.config(text="")
                self.var_joueur_3_resultat.config(text="")
                self.var_joueur_3_sequence.config(text="")
                self.var_joueur_3_resultat.config(text="")

                self.var_joueur_3_sequence.config(text="")

                print(self.bool_lancer_1)

                print(self.bool_lancer_2)
                print(self.joueur_1_lancer)
                print(self.joueur_1)
                if self.bool_lancer_1 == False and self.bool_lancer_2 == True :
                    print("lol")
                    self.test = Combinaison(self.joueur_1_lancer)
                    self.combinaison_1 = self.test.determiner_type_combinaison()
                    self.var_joueur_1_resultat.config(text=self.combinaison_1)
                    self.var_joueur_1_sequence.config(text=self.joueur_1)







            elif self.nombre_joueurs == 3:

                self.nom_joueur_1.config(text=self.nom_joueurs[self.ordre_joueur[0]])
                self.nom_joueur_2.config(text=self.nom_joueurs[self.ordre_joueur[1]])
                self.nom_joueur_3.config(text=self.nom_joueurs[self.ordre_joueur[2]])

                if self.bool_lancer_1 == False and self.bool_lancer_2 == True and self.bool_lancer_3 == False:


                    self.test = Combinaison(self.joueur_1_lancer)
                    self.combinaison_1 = self.test.determiner_type_combinaison()
                    self.var_joueur_1_resultat.config(text=self.combinaison_1)
                    self.var_joueur_1_sequence.config(text=self.joueur_1)

                elif  self.bool_lancer_1 == False and self.bool_lancer_2 == False and self.bool_lancer_3 == True:

                    self.test = Combinaison(self.joueur_1_lancer)
                    self.combinaison_1 = self.test.determiner_type_combinaison()
                    self.var_joueur_1_resultat.config(text=self.combinaison_1)
                    self.var_joueur_1_sequence.config(text=self.joueur_1)
                    self.test = Combinaison(self.joueur_2_lancer)
                    self.combinaison_2 = self.test.determiner_type_combinaison()
                    self.var_joueur_2_resultat.config(text=self.combinaison_2)
                    self.var_joueur_2_sequence.config(text=self.joueur_2)




                #  self.empecher_passer()
            concernes = list(range(self.nombre_joueurs))
            self.premier = concernes[0]

    def jouer_tour_premiere_phase_sauvegarde (self):

        self.tour += 1
        self.empecher_lancer()
        self.empecher_passer()

        for i in range(self.nombre_joueurs):
            pos = (self.premier + i) % self.nombre_joueurs

            self.indice_joueur_courant = pos

#*****************************************************************************

