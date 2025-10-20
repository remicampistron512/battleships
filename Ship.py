

class Ship:
    ships_list = []
    def __init__(self,name,direction,length,starting_x,starting_y,coordinates_list="",hit_list=""):
        self.name = name
        self.direction = direction
        self.length = length
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.coordinates_list = coordinates_list
        self.hit_list = hit_list

    def compute_coordinates(self,length, ship_data, starting_x, starting_y):
        pass

    def add_to_list(self):
        Ship.ships_list.append(self)

    def __repr__(self):
        return (f"Ship(name={self.name!r}, direction={self.direction!r}, "
                f"length={self.length}, start=({self.starting_x},{self.starting_y}), "
                f"coords={self.coordinates_list}, hits={self.hit_list})")

