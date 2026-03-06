class Grid:
    cols_headings = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    rows_headings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    @classmethod
    def create_col_headings(cls):
        print("+---" * (len(cls.cols_headings) + 1) + "+")
        for index, col in enumerate(cls.cols_headings):
            if index == 0:
                print("     " f"{col:>2}", end=" |")
            elif index == len(cls.cols_headings) - 1:
                print(f"{col:>2}", end=' |\n')
            else:
                print(f"{col:>2}", end=' |')

    @classmethod
    def create_rows(cls, ships, misses_list, show_ships=False):
        """Crée la grille sans les entêtes."""

        hit_coordinates = {coordinate for ship in ships for coordinate in ship.hit_list}
        ship_coordinates = {coordinate for ship in ships for coordinate in ship.coordinates_list}
        misses = set(misses_list)

        for row in cls.rows_headings:
            print("+---" * (len(cls.cols_headings) + 1) + "+")
            print(f"{row:>2}", end='  | ')

            for col in cls.cols_headings:
                current_coordinate = f"{col.lower()}{row}"
                if current_coordinate in hit_coordinates:
                    symbol = "Ø"
                elif current_coordinate in misses:
                    symbol = "x"
                elif show_ships and current_coordinate in ship_coordinates:
                    symbol = "o"
                else:
                    symbol = " "
                print(symbol, end=" | ")
            print("\r")
