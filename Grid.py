class Grid:
    cols_headings = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    rows_headings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self,ships=None,miss_list=None):
        self.ships = ships
        self.miss_list = miss_list


    def create_rows(self, ships, miss_list):
        """
           Créer la grille sans les entêtes
           :param miss_list:
           :param rows_headings:
           :param cols_headings:
           :param ships:
           :return:
           """
        i = 0
        j = 0
        for row in Grid.rows_headings:
            print("+---" * (len(Grid.cols_headings) + 1) + "+")
            print(f"{row:>2}", end='  | ')

            for col in Grid.cols_headings:
                ship_in_square = False
                ship_hit_in_square = False
                missed_square = False
                for ship in ships:
                    for ship_hit_coordinate in ship.hit_list:
                        if ship_hit_coordinate == col.lower() + "" + str(row).lower():
                            print("Ø", end=" | ")
                            ship_hit_in_square = True
                            continue
                    if not ship_hit_in_square:
                        for ship_coordinates in ship.coordinates_list:
                            if ship_coordinates == col.lower() + "" + str(row).lower():
                                print("o", end=" | ")
                                ship_in_square = True
                if not ship_in_square and not ship_hit_in_square:
                    for miss in miss_list:
                        if miss == col.lower() + "" + str(row).lower():
                            print("x", end=" | ")
                            missed_square = True

                if not ship_in_square and not ship_hit_in_square and not missed_square:
                    print(" ", end=" | ")
            print("\r")

            i += 1
        j += 1

    def create_col_headings(self):
        """
          Créer les entêtes de la grille
          :param cols_headings:
          :return:
          """
        print("+---" * (len(Grid.cols_headings) + 1) + "+")
        i = 0
        for col in Grid.cols_headings:
            if i == 0:
                print("     "f"{col:>2}", end=" |")
            elif i == len(Grid.cols_headings) - 1:
                print(f"{col:>2}", end=' |\n')
            else:
                print(f"{col:>2}", end=' |')
            i += 1