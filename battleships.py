from Grid import Grid
from UserInput import UserInput
from Ship import Ship

if __name__ == '__main__':
    aircraft_carrier = Ship("aircraft carrier", "horizontal", 5, "b", "2")
    cruiser = Ship("cruiser", "vertical", 4, "a", "4")
    destroyer = Ship("destroyer", "vertical", 3, "c", "5")
    submarine = Ship("submarine", "horizontal", 3, "h", "5")
    torpedo_boat = Ship("torpedo_boat", "horizontal", 2, "e", "9")

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

    print(Ship.ships_list)
    misses_list = []
    grid = Grid()
    grid.create_col_headings()
    grid.create_rows(Ship.ships_list,misses_list)



    while True:
        ask_coordinates = UserInput()
        shot_coordinates = ask_coordinates.ask_coordinates()
        if shot_coordinates == "q":
            break
        if ask_coordinates.check_coordinates(shot_coordinates):
            shot_coordinates_validated = ask_coordinates.check_coordinates(shot_coordinates)
            Ship.shoot(shot_coordinates_validated, Ship.ships_list)
            grid = Grid(Ship.ships_list, misses_list)
            endgame = True
            for a_ship in Ship.ships_list:
                if a_ship["ship_coordinates_list"]:
                    endgame = False
            if endgame:
                print("GAME OVER")
                break
