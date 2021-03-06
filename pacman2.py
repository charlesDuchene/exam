###
### Author : Antoine Scherrer <antoine.scherrer@lecole-ldlc.com>
### License : GPL
###

# The game map, as a large string
# Be careful not to include useless spaces on the right when you modify the map !


game_map = """
#########
#C....o.#
#.#B#.#.#
#.#.#.#.#
#......X#
#########
"""

# Definition of each component of the map
PACMAN = 'C'
ENNEMY = 'X'
WALL = '#'
SUPERGUM = 'o'
GUM = '.'
EMPTY = ' '
BOMBE ='B'

# Compute width and height of the map
width = len(game_map.split('\n')[1])
# we need to subtract 2 because of the newline at beginning and the newline at the end of the string
height = len(game_map.split('\n')) - 2


# Generate a red colored text
def red_text(txt):
    return '\033[31;1m' + txt + '\033[0m'


# Generate a green colored text
def green_text(txt):
    return '\033[0;32m' + txt + '\033[0m'


# Generate a blue colored text
def blue_text(txt):
    return '\033[34;1m' + txt + '\033[0m'


# Generate a pink colored text
def pink_text(txt):
    return '\033[35;1m' + txt + '\033[0m'


# changement de couleurs si super gum


def debug_text(txt):
    return '\033[37m' + '[DEBUG]' + txt + '\033[0m'


# get the index of a position in the game_map string
def get_map_index(position):
    # We need to compute the index of that char in the string.
    # We need to add 1 to the width because the the "new line" characters
    return 1 + position[0] + (width + 1) * position[1]


# return the character in the game_map at given coordinates
def get_case_content(position):
    # TODO check if position goes outside of the map, return None in that case
    global height, width
    if position[1] >= height or position[0] >= width or position[0] < 0 or position[1] < 0:
        return None
    else:
        return game_map[get_map_index(position)]


# remove a gum of the map
def remove_gum_from_map(position):
    global game_map

    if get_case_content(position) != GUM:
        #print(debug_text('ERROR: trying to remove a non-existing gum'))
        return

    # convert the map into a list (so that we can change a character !)
    game_map_list = list(game_map)
    # remove the gum (put the empty char at the position of the gum)
    game_map_list[get_map_index(position)] = EMPTY
    # convert the list back to a string, that will be the updated game map
    game_map = "".join(game_map_list)

# move pacman at new position in the map
def move_pacman(current_position, next_position):
    # utilisez cette ligne pour modifier la variable globale game_map dans la fonction
    global game_map

    # convertit la carte en liste (pour pouvoir changer de personnage!)
    game_map_list = list(game_map)
    # enlever le chewing-gum (mettre le char vide à la position du chewing-gum)
    game_map_list[get_map_index(current_position)] = EMPTY
    # reconvertit la liste en chaîne, ce sera la carte du jeu mise à jour
    game_map_list[get_map_index(next_position)] = PACMAN
    game_map = "".join(game_map_list)


    print(debug_text('we are now moving PACMAN'))


# display the map, with fancy colors !
def show_map(map):
    # for each char of the map
    for char in map:

        if char == WALL:
            print(char, end='')
        elif char == BOMBE:
            print (blue_text(char),end='')
        elif char == ENNEMY:
            if superpouvoir == 1:
                print(pink_text(char), end='')
            else:
                print(red_text(char), end='')
        elif char == PACMAN:
            if superpouvoir == 1:
                print(blue_text(char), end='')
            else:
                print(green_text(char), end='')


        elif char == GUM:
            print(pink_text(char), end='')
        else:
            print(char, end='')

    print()



# Program starts here !
if __name__ == "__main__":

    print(green_text("Comment vous appelez-vous ? : "))
    try:
        nom = input()
    except:
        print("Merci de rentrer votre nom correctement")

    print(blue_text("Quel age as-tu %s : " % nom))

    try:
        age = int(input())
    except:
        print("La valeur n'est pas correcte  !")

    # Inital positions of PACMAN and ennemy
    current_position = [1, 1]
    enemy_position = [6, 4]
    superpouvoir = 0
    bombe = 0

    if age >= 12:
        gum = 0
        ennemy = 0
        while True:
            show_map(game_map)
            print("Appuyez sur H(Haut), B(Bas), G(Gauche), D(Droite) ou Q pour quitter")
            move = input('Votre déplacement ?').upper()

            # We copy pacman_position in next_position
            next_position = list(current_position)
            # Update next_position
            if move == 'G':
                next_position[0] -= 1
            elif move == 'D':
                next_position[0] += 1
            elif move == 'H':
                next_position[1] -= 1
            elif move == 'B':
                next_position[1] += 1
            elif move == "Q":
                print("Merci d'avoir joué!")
                break
            else:
                print('Commande incorrecte')
                continue

                # Depending of the content of the case, move PACMAN and take required actions
            case = get_case_content(next_position)
            if case == WALL:
                if bombe == 1:
                    move_pacman(current_position, next_position)
                    current_position = list(next_position)
                else:
                    print(red_text("Vous venez d'entrer dans un mur"))

            elif case == ENNEMY:
                if superpouvoir == 1:
                    move_pacman(current_position, next_position)
                    current_position = list(next_position)
                    ennemy = ennemy + 1
                else:
                    print(red_text("vous venez de rencontrer un ennemi sur votre chemin, vous etes mort!"))
                    break
            elif case == BOMBE :
                print(red_text('Vous pouvez manger les murs'))
                bombe = 1
                move_pacman(current_position, next_position)
                current_position = list(next_position)

            elif case == GUM:
                print(green_text('MIAM!'))
                gum = gum + 1

                if gum < 17:

                    print("Vous avez mangé ", gum, "gums  ")
                elif gum == 17:
                    print("Il ne vous reste qu'une gum à manger")
                elif gum == 18:

                    print (pink_text("Bravo vous avez gagné."))
                    print (green_text("vous avez mangé"), green_text(str(ennemy)), green_text("ennemies"))
                    break

                remove_gum_from_map(next_position)
                # update PACMAN position
                move_pacman(current_position, next_position)
                current_position = list(next_position)

            elif case == SUPERGUM:
                # TODO Deal with SUPERGUM effect
                print(pink_text('Vous etes en possession invincible'))
                # update PACMAN position
                superpouvoir = 1
                move_pacman(current_position, next_position)
                current_position = list(next_position)

            elif case == EMPTY:
                print(pink_text('Nothing here, keep moving'))
                # update PACMAN position
                move_pacman(current_position, next_position)
                current_position = list(next_position)
            elif case == None:
                print(red_text('Vous venez de sortir de la carte!'))
            else:
                print(debug_text('Quelque chose est arrivé !!'))

    else:
        print(red_text("Tu n'as pas l'age minimum pour jouer au jeu ! %s" % nom))
        # TODO Check is game is finished, in that case display some messages

        # TODO Make the ennemy move
