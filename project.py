import turtle
from CONFIGS import *


def lire_matrice(fichier):
    """
    Permet de transformer le fichier texte en une matrice
    """
    matrice = []
    with open(fichier, 'r') as f:
        for ligne in f:
            matrice.append([int(x) for x in ligne.strip().split()])
    return matrice

matrice_global = lire_matrice("plan_chateau.txt")

def calculer_pas(matrice):
    width_window = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]
    height_window = ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]
    nb_lines = len(matrice)
    nb_columns = len(matrice[0])
    length_width = width_window // nb_columns
    length_height = height_window // nb_lines
    pas = min(length_width, length_height)
    return pas

pas_global = calculer_pas(matrice_global)


def coordonnees(case, pas):
    x_config_min, y_config_min = ZONE_PLAN_MINI
    x_config_max, y_config_max = ZONE_PLAN_MAXI
    x, y = case
    x_turtle = x_config_min + (x * pas)
    y_turtle = y_config_max - (y + 1) * pas
    coord = (x_turtle, y_turtle)
    return coord


def tracer_carre(dimension):
    turtle.up()
    turtle.down()
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)
    turtle.end_fill()
    turtle.up()


def tracer_case(case, couleur, pas):
    depart = coordonnees(case, pas)
    turtle.up()
    turtle.color("white", couleur)
    turtle.goto(depart)
    tracer_carre(pas)


def afficher_plan(matrice):
    turtle.tracer(False)
    pas = calculer_pas(matrice)
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.down()
    turtle.color("black")
    turtle.write("Inventaire :", font=('Calibri', 15, "bold"))
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.write("Vous devez mener le point rouge à la sortie jaune", font=('Calibri',15,"bold"))

    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            case = (j, i)
            if matrice[i][j] == 0:
                pass
            else:
                couleur = COULEURS[matrice[i][j]]
                tracer_case(case, couleur, pas)
    turtle.hideturtle()


afficher_plan(matrice_global)




########################################################################################################################
##############################################     Partie  2    ########################################################
########################################################################################################################

def create_character(position):
    turtle.up()
    turtle.goto(coordonnees(position, pas_global)[0] + pas_global / 2, coordonnees(position, pas_global)[1] + pas_global /2)
    turtle.down()
    turtle.dot(pas_global * RATIO_PERSONNAGE, COULEUR_PERSONNAGE)

position_globale = (1, 0)

def deplacer(matrice, position, mouvement):
    global position_globale
    new_position = (position[0] + mouvement[0], position[1] + mouvement[1])
    if matrice[new_position[1]][new_position[0]] != 1:
        tracer_case(position, "wheat", pas_global)
        create_character(new_position)
        position_globale = new_position
        if matrice[new_position[1]][new_position[0]] == 4:
            ramasser_objet()



def deplacer_gauche():
    global matrice_global, position_globale
    turtle.onkeypress(None, "Left")
    deplacer(matrice_global, position_globale, (-1, 0))
    turtle.onkeypress(deplacer_gauche, "Left")

def deplacer_droite():
    global matrice_global, position_globale
    turtle.onkeypress(None, "Right")
    deplacer(matrice_global, position_globale, (1, 0))
    turtle.onkeypress(deplacer_droite, "Right")

def deplacer_haut():
    global matrice_global, position_globale
    turtle.onkeypress(None, "Up")
    deplacer(matrice_global, position_globale, (0, -1))
    turtle.onkeypress(deplacer_haut, "Up")

def deplacer_bas():
    global matrice_global, position_globale
    turtle.onkeypress(None, "Down")
    deplacer(matrice_global, position_globale, (0, 1))
    turtle.onkeypress(deplacer_bas, "Down")


########################################################################################################################
##############################################     Partie  3    ########################################################
########################################################################################################################

def creer_dictionnaire_des_objets(fichier_des_objets):
    dico = {}
    with open(fichier_des_objets, encoding="utf-8") as item:
        for line in item:
            x, y = eval(line)
            dico[x] = y
    return dico

item_dico = creer_dictionnaire_des_objets(fichier_objets)



def erase_event():
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

new_object = 0

def ramasser_objet():
    global item_dico, pas_global, new_object
    x, y = position_globale
    new_position_globale = (y, x)
    erase_event()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.down()
    turtle.color("black")
    turtle.write("Vous avez trouvé : " + item_dico[new_position_globale], font=('Calibri', 15, "bold"))
    turtle.up()
    new_object += 1
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE[0], POINT_AFFICHAGE_INVENTAIRE[1] - new_object * 2 *pas_global)
    turtle.write("n°" + str(new_object) + " : " +item_dico[new_position_globale], font=('Calibri', 12, "bold"))


turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()    # Place le programme en position d’attente d’une action du joueur