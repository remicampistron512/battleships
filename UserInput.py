class UserInput:

    def __init__(self):
        self.coordinates = input("sur quelle case voulez vous tirer ? (q pour quitter) :")



    def check_coordinates(self):
        """
        Vérifie que les données entrées sont valides
        :return: les coordonnées du tir nettoyées
        """

        cleaned_coordinates = self.coordinates.strip().lower()
        if len(cleaned_coordinates) <= 3 and "a" <= cleaned_coordinates[0] <= "j" and 1 <= int(
                cleaned_coordinates[1]) <= 10:
            return cleaned_coordinates
        else:
            print("merci de rentrer des coordonnées valides")
            return False



