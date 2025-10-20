

class Ship:
    ships_list = []
    def __init__(self,name,direction,length,starting_x,starting_y,coordinates_list=list,hit_list=list,misses_list=list):
        self.name = name
        self.direction = direction
        self.length = length
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.coordinates_list = coordinates_list
        self.hit_list = hit_list
        self.misses_list = misses_list

    def compute_coordinates(self,length, ship_data, starting_x, starting_y):
        for i in range(0, length):
            if ship_data["direction"] == "vertical":
                self.coordinates_list.append(starting_coord_x + (chr(ord(starting_coord_y) + i)))
            elif ship_data["direction"] == "horizontal":
                ship_data["ship_coordinates_list"].append((chr(ord(starting_coord_x) + i)) + starting_coord_y)

    def add_to_list(self):
        Ship.ships_list.append(self)

    def shoot(coordinates, ships):
        """
        On tire, On compare les coordonnées enregistrées pour tous les navires avec les coordonnées du tir
        :param coordinates:
        :param ships:
        :return: la liste des navires avec leurs coordonnées mises à jour
        """
        is_a_hit = False
        is_a_miss = False
        for ship in ships:
            if not is_a_hit:
                for ship_coordinates in ship["ship_coordinates_list"]:
                    if not is_a_hit:
                        if ship_coordinates == coordinates:
                            print("touché")
                            ship["length"] = ship["length"] - 1
                            ship["ship_coordinates_list"].remove(coordinates)
                            ship["ship_hit_list"].append(coordinates)
                            if not ship["ship_coordinates_list"]:
                                print("coulé !!!")
                            is_a_hit = True
                        else:
                            is_a_miss = True
            else:
                break

        if not is_a_hit and is_a_miss:
            misses_list.append(coordinates)
            print('raté')
        return ships

    def __repr__(self):
        return (f"Ship(name={self.name!r}, direction={self.direction!r}, "
                f"length={self.length}, start=({self.starting_x},{self.starting_y}), "
                f"coords={self.coordinates_list}, hits={self.hit_list})")

