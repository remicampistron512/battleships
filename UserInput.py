class UserInput:

    def __init__(self):
        self.coordinates = input("sur quelle case voulez vous tirer ? (q pour quitter) :")

    @staticmethod
    def normalize_coordinates(raw_coordinates):
        """Nettoie et valide des coordonnées de type A1 à J10."""
        cleaned_coordinates = raw_coordinates.strip().lower()

        if cleaned_coordinates == "q":
            return "q"

        if len(cleaned_coordinates) < 2:
            return False

        column = cleaned_coordinates[0]
        row = cleaned_coordinates[1:]

        if not ("a" <= column <= "j"):
            return False

        if not row.isdigit():
            return False

        row_number = int(row)
        if not (1 <= row_number <= 10):
            return False

        return f"{column}{row_number}"

    def check_coordinates(self):
        """
        Vérifie que les données entrées sont valides
        :return: les coordonnées du tir nettoyées
        """

        validated_coordinates = self.normalize_coordinates(self.coordinates)
        if validated_coordinates is False:
            print("merci de rentrer des coordonnées valides")
            return False
        return validated_coordinates
