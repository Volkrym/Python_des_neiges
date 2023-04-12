"""
Jeu du labyrinthe en turtle
Auteur: Clément Bastian
Date : 12 avril 2023
Labyrinthe fait avec turtle python sur base d'un fichier texte transformer en matrice
avec indices à collecter pour aider à ouvrir des portes bloquer par des énigmes.
"""



import turtle
from CONFIGS import *


def lire_matrice(fichier):
    """
    créer une matrice à partir d'un fichier plan
    :param fichier: utilise le fichier plan_chateau.txt
    :return: matrice du fichier plan
    """
    matrice = []
    with open(fichier, 'r') as f:
        for ligne in f:
            matrice.append([int(x) for x in ligne.strip().split()])
    return matrice


def calculer_pas(matrice):
    """
    renvoie la taille des cases par rapport à un zone donnée pour pouvoir rentrer tout le plan dedans
    :param matrice:
    :return: taille d'une case
    """
    width_window = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]
    height_window = ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]
    nb_lines = len(matrice)
    nb_columns = len(matrice[0])
    length_width = width_window // nb_columns
    length_height = height_window // nb_lines
    pas = min(length_width, length_height)
    return pas




def coordonnees(case, pas):
    """
    calcul la coordonnée du coin inférieur gauche d'une case en pixel turtle
    :param case: case qui sera transformé
    :param pas: pas
    :return: coordonnée turtle du coin inférieur gauche
    """
    x_config_min, y_config_min = ZONE_PLAN_MINI
    x_config_max, y_config_max = ZONE_PLAN_MAXI
    x, y = case
    x_turtle = x_config_min + (x * pas)
    y_turtle = y_config_max - (y + 1) * pas
    coord = (x_turtle, y_turtle)
    return coord


def tracer_carre(dimension):
    """
    permet de faire un carré avec turtle
    :param dimension: donne la taille du carré
    :return: rien
    """
    turtle.up()
    turtle.down()
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)
    turtle.end_fill()
    turtle.up()


def tracer_case(case, couleur, pas):
    """
    donne l'emplacement où commencer le carré
    :param case: endroit où dessiner le carré
    :param couleur: couleur de celui-ci
    :param pas: taille du carré
    :return: rien
    """
    depart = coordonnees(case, pas)
    turtle.up()
    turtle.color("white", couleur)
    turtle.goto(depart)
    tracer_carre(pas)


def afficher_plan(matrice):
    """
    affiche le plan du chateau de départ
    :param matrice: utiliser pour dessiner le plan
    :return: rien
    """
    turtle.tracer(False)
    pas = calculer_pas(matrice)
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.down()
    turtle.color("black")
    turtle.write("Inventaire :", font=('Arial', 15, "bold"))
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.write("Vous devez mener le point rouge à la sortie jaune", font=('Arial',15,"bold"))

    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            case = (j, i)
            if matrice[i][j] == 0:
                pass
            else:
                couleur = COULEURS[matrice[i][j]]
                tracer_case(case, couleur, pas)
    turtle.hideturtle()



########################################################################################################################
##############################################     Partie  2    ########################################################
########################################################################################################################

def create_character(position):
    """
    permet de créer le personnage (petit rond rouge)
    :param position: défini la position du personnage
    :return: rien
    """
    turtle.up()
    turtle.goto(coordonnees(position, pas_global)[0] + pas_global / 2,
                coordonnees(position, pas_global)[1] + pas_global / 2)
    turtle.down()
    turtle.dot(pas_global * RATIO_PERSONNAGE, COULEUR_PERSONNAGE)

def deplacer(matrice, position, mouvement):
    """
    permet le déplacement du personnage d'une case à l'autre
    :param matrice: matrice
    :param position: position précédente du personnage
    :param mouvement: mouvement devant être effectué par le personnage
    :return: rien
    """
    global position_globale, correct
    new_position = (position[0] + mouvement[0], position[1] + mouvement[1])
    if matrice[new_position[1]][new_position[0]] == 3:
        correct = False
        poser_question(matrice_global,position_globale, mouvement)
        turtle.listen()
        if correct == True:
            tracer_case(position, "wheat", pas_global)
            create_character(new_position)
            position_globale = new_position


    elif matrice[new_position[1]][new_position[0]] != 1:
        tracer_case(position, "wheat", pas_global)
        create_character(new_position)
        position_globale = new_position
        if matrice[new_position[1]][new_position[0]] == 4:
            ramasser_objet()
            matrice[new_position[1]][new_position[0]] = 0
        if matrice[new_position[1]][new_position[0]] == 2:
            win()  #déclenche la victoire une fois sur la case jaune (2)


def deplacer_gauche():
    """
    déplace le personnage vers la gauche
    :return: rien
    """
    global matrice_global, position_globale
    turtle.onkeypress(None, "Left")
    deplacer(matrice_global, position_globale, (-1, 0))
    turtle.onkeypress(deplacer_gauche, "Left")

def deplacer_droite():
    """
        déplace le personnage vers la droite
        :return: rien
        """
    global matrice_global, position_globale
    turtle.onkeypress(None, "Right")
    deplacer(matrice_global, position_globale, (1, 0))
    turtle.onkeypress(deplacer_droite, "Right")

def deplacer_haut():
    """
        déplace le personnage vers le haut
        :return: rien
        """
    global matrice_global, position_globale
    turtle.onkeypress(None, "Up")
    deplacer(matrice_global, position_globale, (0, -1))
    turtle.onkeypress(deplacer_haut, "Up")

def deplacer_bas():
    """
        déplace le personnage vers le bas
        :return: rien
        """
    global matrice_global, position_globale
    turtle.onkeypress(None, "Down")
    deplacer(matrice_global, position_globale, (0, 1))
    turtle.onkeypress(deplacer_bas, "Down")


########################################################################################################################
##############################################     Partie  3    ########################################################
########################################################################################################################

def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    créer un dictionnaire à partir de fichiers
    :param fichier_des_objets: le fichier en question
    :return: le dictionnaire
    """
    dico = {}
    with open(fichier_des_objets, encoding="utf-8") as item:
        for line in item:
            x, y = eval(line)
            dico[x] = y
    return dico


def erase_event():
    """
    permet d'effacer le message d'évènement précédent
    :return:rien
    """
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.color(COULEUR_CASES)
    turtle.down()
    turtle.begin_fill()
    turtle.setheading(0)
    for i in range(2):
        turtle.forward(500)
        turtle.left(90)
        turtle.forward(50)
        turtle.left(90)
    turtle.end_fill()
    turtle.up()



def ramasser_objet():
    """
    permet d'ajouter un indice/objet à l'inventaire
    :return: rien
    """
    global item_dico, pas_global, new_object
    x, y = position_globale
    new_position_globale = (y, x)
    erase_event()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.down()
    turtle.color("black")
    turtle.write("Vous avez trouvé : " + item_dico[new_position_globale], font=('Arial', 15, "bold"))
    turtle.up()
    new_object += 1
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - new_object * 2 *pas_global)
    turtle.write("n°" + str(new_object) + " : " + item_dico[new_position_globale], font=('Arial', 12, "bold"))


########################################################################################################################
##############################################     Partie  4    ########################################################
########################################################################################################################




def poser_question(matrice, case, mouvement):
    """
    permet de poser une question une fois que l'on fait face à une porte
    :param matrice: matrice
    :param case: case précédent la porte
    :param mouvement: mouvement menant sur la porte
    :return: rien
    """
    global correct
    emplacement = (case[1] + mouvement[1], case[0] + mouvement[0])
    erase_event()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.color("black")
    turtle.down()
    turtle.write("Cette porte est fermée.", font=('Arial', 12, "bold"))
    answer = turtle.textinput("Question :", quiz_dico[emplacement][0])
    if answer == quiz_dico[emplacement][1]:
        matrice[emplacement[0]][emplacement[1]] = 0
        correct = True
        erase_event()
        turtle.goto(POINT_AFFICHAGE_ANNONCES)
        turtle.color("black")
        turtle.down()
        turtle.write("Bonne réponse, La porte s'ouvre.", font=('Arial', 12, "bold"))
    else:
        erase_event()
        turtle.goto(POINT_AFFICHAGE_ANNONCES)
        turtle.color("black")
        turtle.down()
        turtle.write("Mauvaise Réponse, La porte reste fermée.", font=('Arial', 12, "bold"))


def win():
    """
    provoque la victoire au moment d'atteindre l'arrivée
    :return: rien
    """
    turtle.onkeypress(None, "Up")    #désactive la possibilitée de se mouvoir une fois la sortie atteinte
    turtle.onkeypress(None, "Down")
    turtle.onkeypress(None, "Right")
    turtle.onkeypress(None, "Left")
    erase_event()
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.color("black")
    turtle.down()
    turtle.write("Victoire !", font=('Arial', 20, "bold"))
    turtle.done()





###############################################Variable Globale#########################################################


matrice_global = lire_matrice(fichier_plan)
afficher_plan(matrice_global)
pas_global = calculer_pas(matrice_global)
position_globale = (1, 0)
correct = False               #devient True si la réponse à la question est correct
new_object = 0                #la valeur augmente au fur et à mesure que de nouveaux objets sont trouvés
item_dico = creer_dictionnaire_des_objets(fichier_objets)
quiz_dico = creer_dictionnaire_des_objets(fichier_questions)
create_character(position_globale)

turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")     # Associe à la touche Right une fonction appelée deplacer_droite
turtle.onkeypress(deplacer_haut, "Up")       # Associe à la touche Up une fonction appelée deplacer_haut
turtle.onkeypress(deplacer_bas, "Down")     # Associe à la touche Down une fonction appelée deplacer_bas
turtle.mainloop()    # Place le programme en position d’attente d’une action du joueur
