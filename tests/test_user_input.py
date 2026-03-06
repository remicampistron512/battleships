import unittest

from UserInput import UserInput


class TestUserInput(unittest.TestCase):
    def test_valid_coordinates_are_normalized(self):
        self.assertEqual(UserInput.normalize_coordinates(" A1 "), "a1")
        self.assertEqual(UserInput.normalize_coordinates("J10"), "j10")

    def test_invalid_coordinates(self):
        self.assertFalse(UserInput.normalize_coordinates("Z1"))
        self.assertFalse(UserInput.normalize_coordinates("A11"))
        self.assertFalse(UserInput.normalize_coordinates("1A"))


if __name__ == "__main__":
    unittest.main()
