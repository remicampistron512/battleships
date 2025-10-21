from Grid import Grid
from UserInput import UserInput
from Ship import Ship

if __name__ == '__main__':
    # Créé les différents navires
    aircraft_carrier = Ship("aircraft carrier", "horizontal", 5, "b", "2")
    cruiser = Ship("cruiser", "vertical", 4, "a", "4")
    destroyer = Ship("destroyer", "vertical", 3, "c", "5")
    submarine = Ship("submarine", "horizontal", 3, "h", "5")
    torpedo_boat = Ship("torpedo_boat", "horizontal", 2, "e", "9")

    # Ajoute les navires à une liste et calcule ses coordonnées
    aircraft_carrier.add_to_list()
    aircraft_carrier.compute_coordinates()

    cruiser.add_to_list()
    cruiser.compute_coordinates()

    destroyer.add_to_list()
    destroyer.compute_coordinates()

    submarine.add_to_list()
    submarine.compute_coordinates()

    torpedo_boat.add_to_list()
    torpedo_boat.compute_coordinates()

    # Initialise la liste des coups manqués
    misses_list = []
    # Créé et affiche la grille
    grid = Grid()
    grid.create_col_headings()
    grid.create_rows(Ship.ships_list,misses_list)



    while True:
        # demande à l'utilisateur de rentrer les coordonnées du tir
        ask_coordinates = UserInput()

        # l'utilisateur quitte la partie
        if ask_coordinates.coordinates == "q":
            break
        if ask_coordinates.check_coordinates():
            # valide les coordonnées
            shot_coordinates_validated = ask_coordinates.check_coordinates()
            # l'utilisateur tire
            Ship.shoot(shot_coordinates_validated)
            # la grille est mise à jour
            grid = Grid()
            grid.create_col_headings()
            grid.create_rows(Ship.ships_list, misses_list)
            endgame = True
            # tant que la liste des coordonnées n'est pas vide, la partie continue
            for a_ship in Ship.ships_list:
                if a_ship.coordinates_list:
                    endgame = False
            if endgame:
                print("GAME OVER")
                break
