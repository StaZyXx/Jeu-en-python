from tkinter import *
from tkinter import messagebox as mb


class Case:

    def __init__(self):
        self.__nbr_pion = 0
        self.__joueur = 0

    def get_nbr_pion(self):
        return self.__nbr_pion

    def get_joueur(self):
        return self.__joueur
    
    def change_joueur_case(self,new_joueur):
        self.__joueur = new_joueur
        
    def change_nombre_pion(self):
        self.__nbr_pion += 1
    
    def reset_case(self):
        self.__nbr_pion = 0
        


class Jeu:

    def __init__(self, x, y, nbr_joueur):
        self.__tableau = []  # notre plateau de jeu en tableau
        for i in range(x):
            self.__tableau.append([])
            for j in range(y):
                self.__tableau[i].append(Case())
        self.__joueur_demander = 0  # je reprends la valeur du nombre de joueur demander
        self.__player = 1  # le joueur a qui c'est le tour de jouer
        self.__joueur_elimine = []  # liste des joueurs plus présent
        self.__nombre_de_tour = 0  # nombre de tour effectué afin de ne pas éxecuter le tri des joueurs sur le plateau vide

    #def get_tableau(self):
    #   return self.tableau[0][0].nbr_pion
    
    
    def get_tableau(self):
        return self.__tableau
    
    def get_tableau_x(self,x):
        return self.__tableau[x]
        
    def get_tableau_x_y(self,x,y):
        return self.__tableau[x][y]
    
    def nbr_player_in_game(self,nbr):
        self.__joueur_demander = nbr
        
    def get_joueur_elimine(self):
        return self.__joueur_elimine

    def get_player(self):
        return self.__player

    def get_nbr_tour(self):
        return self.__nombre_de_tour

    # ----------------------------- fonction qui place le pion du joueur -----------------------------

    def place_joueur(self, y, x):
        if self.__tableau[x][y].get_joueur() == self.__player or self.__tableau[x][y].get_joueur() == 0:
            self.__tableau[x][y].change_nombre_pion()
            self.__tableau[x][y].change_joueur_case(self.__player)
            self.case_full(x, y, self.__player)
            if self.__nombre_de_tour > 0:
                self.joueur_liste_ou_pas()
            self.change_joueur()
        else:
            pass

    # ----------------------------- fonction qui permet de définir le tour a qui c'est de jouer -----------------------------

    def change_joueur(self):
        print(self.__joueur_elimine)
        print(self.__player)
        self.__player += 1
        # ce while permet de remplir les 2 conditions pour le joueur : il ne doit pas etre éliminé et ca ne doit pas être un joueur qui n'existe pas
        # il ne doit donc pas etre supérieure au nombre de joueur
        while self.__player in self.__joueur_elimine or self.__player > self.__joueur_demander:
            if self.__player in self.__joueur_elimine:
                self.__player += 1
            if self.__player > self.__joueur_demander:
                self.__player = 1
                self.__nombre_de_tour += 1

        print(self.__player)

    # ----------------------------- fonction qui permet parcourir tt les joueurs afin de vérifier les joueurs en liste -----------------------------

    def joueur_liste_ou_pas(self):
        joueur = 1
        for k in range(self.__joueur_demander):
            if self.test_joueur_en_liste(joueur) == False:
                if joueur not in self.__joueur_elimine:
                    self.__joueur_elimine.append(joueur)
            else:
                pass
            joueur += 1

    # ----------------------------- fonction qui permet parcourir tt le tableau pour voir si il a encore des pions -----------------------------
    def test_joueur_en_liste(self, joueur):
        for i in self.__tableau:
            for j in i:
                if j.get_joueur() == joueur:
                    return True
                else:
                    pass
        return False

    # ----------------------------- fonction qui permet la distribution après une case complète -----------------------------

    def check_case(self, i, j):
        if (i == 0 and j == 0) or (i == len(self.__tableau) - 1 and j == 0) or (
                j == len(self.__tableau) - 1 and i == 0) or (
                i == len(self.__tableau) - 1 and j == len(self.__tableau) - 1):
            return 2
        elif (i == 0) or (i == len(self.__tableau) - 1) or (j == 0) or (j == len(self.__tableau) - 1):
            return 3
        elif (i != 0) and (i != len(self.__tableau) - 1) and (j != 0) and (j != len(self.__tableau) - 1):
            return 4

    def case_full(self, i, j, joueur):
        position_case = self.check_case(i, j)  # point nécessaire
        if self.__tableau[i][j].get_nbr_pion() == position_case:
            if i - 1 >= 0:
                self.__tableau[i - 1][j].change_nombre_pion()
                self.__tableau[i - 1][j].change_joueur_case(joueur)
                self.case_full(i - 1, j, joueur)
            if j - 1 >= 0:
                self.__tableau[i][j - 1].change_nombre_pion()
                self.__tableau[i][j - 1].change_joueur_case(joueur)
                self.case_full(i, j - 1, joueur)
            if i + 1 < len(self.__tableau):
                self.__tableau[i + 1][j].change_nombre_pion()
                self.__tableau[i + 1][j].change_joueur_case(joueur)
                self.case_full(i + 1, j, joueur)
            if j + 1 < len(self.__tableau):
                self.__tableau[i][j + 1].change_nombre_pion()
                self.__tableau[i][j + 1].change_joueur_case(joueur)
                self.case_full(i, j + 1, joueur)
            self.__tableau[i][j].reset_case()
            self.__tableau[i][j].change_joueur_case(0)


class Affichage:
    def __init__(self):
        # ----------------------------- 1 ère page -----------------------------
        self.__page = Tk()
        self.__page.title("Paramètre")
        self.__page.config(width=400, height=400)
        self.__page.grid()
        self.__x = 0
        self.__y = 0
        self.__nbr_joueur = 0

        self.plateau = 0
        
        self.__label1 = Label(text="Nombres de colonnes:")
        self.__label1.pack()
        self.__barre_texte = Entry(self.__page, width=50)
        self.__barre_texte.insert(0, "6")  # c'est y
        self.__barre_texte.pack(pady=10)  # c'est x

        self.__label2 = Label(text="Nombres de Lignes:")
        self.__label2.pack()
        self.__barre_texte1 = Entry(self.__page, width=50)
        self.__barre_texte1.insert(0, "6")
        self.__barre_texte1.pack(pady=10)

        self.__label3 = Label(text="Nombres de joueurs:")
        self.__label3.pack()
        self.__barre_texte_joueur = Entry(self.__page, width=50)
        self.__barre_texte_joueur.insert(0, "2")
        self.__barre_texte_joueur.pack(pady=10)

        self.__bouton = Button(self.__page, height=1, width=10, text="Start", command=self.get_entry)
        self.__bouton.pack()
        self.__page.mainloop()

        # ----------------------------- 2 ème page -----------------------------

        self.__root = Tk()
        self.__root.title("Page de jeu")

        self.__frame1 = Frame(self.__root)
        self.__frame1.grid(row=0, column=0, rowspan=2)
        self.__frame1.config(bg="white")

        self.__canvas = Canvas(self.__frame1)
        self.__canvas.config(width=self.__y * 71, height=self.__x * 71, highlightthickness=0, bd=0, bg="white")
        self.__canvas.pack()
        self.__canvas.bind('<Button-1>', self.clic)

        self.show_board()

        self.carre = 0
        # --------------------------------------3e page-------------------------
        self.__frame3 = Frame(self.__root)
        self.__frame3.grid(row=0, column=1)
        self.__frame3.config(width=150, height=150, highlightthickness=0, bd=0)
        self.__button2 = Button(self.__frame3, text="Recommencer une partie", command=self.reset_game)
        self.__button2.grid(row=2)

        self.show_next_player()
        self.__root.mainloop()

    # ----------------------------- fin init -----------------------------

    def show_next_player(self):
        print(self.plateau.get_player())
        self.__label = Label(self.__frame3, text="Au tour du joueur " + str(self.plateau.get_player()) + " de jouer", bg="red")
        self.__label.grid(row=0, column=0)

    def show_winner(self):
        if self.plateau.get_nbr_tour() > 1:
            if len(self.plateau.get_joueur_elimine()) == self.__nbr_joueur - 1:
                mb.showinfo("Gagnant", "le joueur " + str(self.plateau.get_player()) + " a gagner !")

    # ----------------------------- les programmes pour les pages -----------------------------

    # ----------------------------- 1 ère page -----------------------------

    def get_entry(self):
        x = int(self.__barre_texte1.get())  # c'est x
        y = int(self.__barre_texte.get())  # c'est y
        nb_joueur = int(self.__barre_texte_joueur.get())

        if x >= 3 and x <= 10:
            if y >= 3 and y <= 12:
                if nb_joueur >= 2 and nb_joueur <= 8:
                    self.__x = x
                    self.__y = y
                    self.__nbr_joueur = nb_joueur
                    self.plateau = Jeu(x, y, nb_joueur)
                    self.plateau.nbr_player_in_game(nb_joueur)
                    self.__page.destroy()
                    self.__page = None

    # ----------------------------- 2 ème page -----------------------------

    def get_x(self):
        return self.__x

    def show_board(self):
        y = -71
        for i in range(len(self.plateau.get_tableau())):
            x = 0
            y += 71
            for j in range(len(self.plateau.get_tableau_x(i))):
                couleur = "white"
                if self.plateau.get_tableau_x_y(i,j).get_joueur() == 0:
                    couleur = "white"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 1:
                    couleur = "yellow"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 2:
                    couleur = "blue"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 3:
                    couleur = "green"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 4:
                    couleur = "red"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 5:
                    couleur = "orange"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 6:
                    couleur = "purple"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 7:
                    couleur = "pink"
                elif self.plateau.get_tableau_x_y(i,j).get_joueur() == 8:
                    couleur = "brown"
                self.carre = self.__canvas.create_rectangle(x, y, x + 70, y + 70, fill="black", outline=couleur)
                if self.plateau.get_tableau_x_y(i,j).get_nbr_pion() == 1:
                    self.carre = self.__canvas.create_oval(x + 30, y + 30, x + 40, y + 40, fill=couleur, width=4, outline=couleur)
                if self.plateau.get_tableau_x_y(i,j).get_nbr_pion() == 2:
                    self.carre = self.__canvas.create_oval(x + 20, y + 20, x + 30, y + 30, fill=couleur, width=4, outline=couleur)
                    self.carre = self.__canvas.create_oval(x + 50, y + 50, x + 40, y + 40, fill=couleur, width=4, outline=couleur)
                if self.plateau.get_tableau_x_y(i,j).get_nbr_pion() == 3:
                    self.carre = self.__canvas.create_oval(x + 10, y + 10, x + 20, y + 20, fill=couleur, width=4, outline=couleur)
                    self.carre = self.__canvas.create_oval(x + 30, y + 30, x + 40, y + 40, fill=couleur, width=4, outline=couleur)
                    self.carre = self.__canvas.create_oval(x + 50, y + 50, x + 60, y + 60, fill=couleur, width=4, outline=couleur)
                x += 71
        # self.__root.mainloop()
    def reset_game(self):
        self.__root.destroy()
        Affichage()


    def clic(self, event):
        x = event.x
        x = x * self.__x // (71 * self.__x)
        y = event.y
        y = event.y * self.__y // (71 * self.__y)
        self.plateau.place_joueur(x, y)
        self.show_board()
        self.show_next_player()
        self.show_winner()


page = Affichage()
