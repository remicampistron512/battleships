import unittest

from Ship import Ship
from battleships import Game


class TestShipAndGame(unittest.TestCase):
    def test_ship_hit_and_sunk(self):
        ship = Ship("test", "horizontal", 2, "a", 1)
        ship.compute_coordinates()

        self.assertTrue(ship.register_hit("a1"))
        self.assertFalse(ship.is_sunk())
        self.assertTrue(ship.register_hit("b1"))
        self.assertTrue(ship.is_sunk())

    def test_game_shoot_records_miss_once(self):
        game = Game()
        result = game.shoot("j1")

        self.assertEqual(result, "miss")
        self.assertEqual(game.misses_list.count("j1"), 1)

        game.shoot("j1")
        self.assertEqual(game.misses_list.count("j1"), 1)

    def test_game_is_over_when_all_hits_registered(self):
        game = Game()
        for ship in game.ships:
            for coordinate in ship.coordinates_list:
                ship.register_hit(coordinate)

        self.assertTrue(game.is_over())


if __name__ == "__main__":
    unittest.main()
