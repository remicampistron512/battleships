from Grid import Grid
from UserInput import UserInput
from Ship import Ship


class Game:
    def __init__(self):
        self.ships = self._create_default_ships()
        self.misses_list = []

    @staticmethod
    def _create_default_ships():
        ships = [
            Ship("aircraft carrier", "horizontal", 5, "b", 2),
            Ship("cruiser", "vertical", 4, "a", 4),
            Ship("destroyer", "vertical", 3, "c", 5),
            Ship("submarine", "horizontal", 3, "h", 5),
            Ship("torpedo_boat", "horizontal", 2, "e", 9),
        ]
        for ship in ships:
            ship.compute_coordinates()
        return ships

    def render(self):
        Grid.create_col_headings()
        Grid.create_rows(self.ships, self.misses_list)

    def shoot(self, coordinates):
        for ship in self.ships:
            if ship.register_hit(coordinates):
                print("touché")
                if ship.is_sunk():
                    print("coulé !!!")
                return "hit"

        if coordinates not in self.misses_list:
            self.misses_list.append(coordinates)
        print("raté")
        return "miss"

    def is_over(self):
        return all(ship.is_sunk() for ship in self.ships)


if __name__ == '__main__':
    game = Game()
    game.render()

    while True:
        ask_coordinates = UserInput()
        shot_coordinates_validated = ask_coordinates.check_coordinates()

        if shot_coordinates_validated == "q":
            break

        if shot_coordinates_validated:
            game.shoot(shot_coordinates_validated)
            game.render()
            if game.is_over():
                print("GAME OVER")
                break
