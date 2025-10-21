class Ship:
    """
    Gère les navires et leurs coordonnées ainsi que l'action de tir de l'utilisateur
    """
    ships_list = []
    misses_list = []

    def __init__(self, name, direction, length, starting_x, starting_y, coordinates_list=None, hit_list=None):
        if coordinates_list is None:
            coordinates_list = []
        self.name = name
        self.direction = direction
        self.length = length
        self.starting_x = starting_x
        self.starting_y = starting_y

        if coordinates_list is None:
            self.coordinates_list = []
        else:
            self.coordinates_list = coordinates_list

        if hit_list is None:
            self.hit_list = []
        else:
            self.hit_list = hit_list

    def compute_coordinates(self):
        """
         Définit les coordonnées d'un navire selon sa direction
        :return:
        """
        for i in range(0, self.length):
            if self.direction == "vertical":
                self.coordinates_list.append(self.starting_x + (chr(ord(self.starting_y) + i)))
            elif self.direction == "horizontal":
                self.coordinates_list.append((chr(ord(self.starting_x) + i)) + self.starting_y)

    def add_to_list(self):
        """
         Constitue la liste des navires
        :return:
        """
        Ship.ships_list.append(self)

    @classmethod
    def shoot(cls, coordinates):
        """
        On tire, On compare les coordonnées enregistrées pour tous les navires avec les coordonnées du tir
        :param coordinates:
        :return:
        """
        is_a_hit = False
        is_a_miss = False
        for ship in cls.ships_list:
            if not is_a_hit:
                for ship_coordinates in ship.coordinates_list:
                    if not is_a_hit:
                        if ship_coordinates == coordinates:
                            print("touché")
                            ship.length = ship.length - 1
                            ship.coordinates_list.remove(coordinates)
                            ship.hit_list.append(coordinates)
                            if not ship.coordinates_list:
                                print("coulé !!!")
                            is_a_hit = True
                        else:
                            is_a_miss = True
            else:
                break

        if not is_a_hit and is_a_miss:
            cls.misses_list.append(coordinates)
            print('raté')
        return "raté", None

    def __repr__(self):
        """
        récupère une représentation sous forme de chaines des navires
        :return:
        """
        return (f"Ship(name={self.name!r}, direction={self.direction!r}, "
                f"length={self.length}, start=({self.starting_x},{self.starting_y}), "
                f"coords={self.coordinates_list}, hits={self.hit_list})")
