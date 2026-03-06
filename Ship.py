class Ship:
    """Gère les navires et leurs coordonnées."""

    def __init__(self, name, direction, length, starting_x, starting_y):
        self.name = name
        self.direction = direction
        self.length = length
        self.starting_x = starting_x
        self.starting_y = str(starting_y)
        self.coordinates_list = []
        self.hit_list = []

    def compute_coordinates(self):
        """Définit les coordonnées d'un navire selon sa direction."""
        row = int(self.starting_y)
        for i in range(self.length):
            if self.direction == "vertical":
                self.coordinates_list.append(f"{self.starting_x}{row + i}")
            elif self.direction == "horizontal":
                self.coordinates_list.append(f"{chr(ord(self.starting_x) + i)}{row}")

    def occupies_coordinate(self, coordinate):
        return coordinate in self.coordinates_list

    def register_hit(self, coordinate):
        if self.occupies_coordinate(coordinate) and coordinate not in self.hit_list:
            self.hit_list.append(coordinate)
            return True
        return False

    def is_sunk(self):
        return len(self.hit_list) == self.length

    def __repr__(self):
        return (
            f"Ship(name={self.name!r}, direction={self.direction!r}, "
            f"length={self.length}, start=({self.starting_x},{self.starting_y}), "
            f"coords={self.coordinates_list}, hits={self.hit_list})"
        )
