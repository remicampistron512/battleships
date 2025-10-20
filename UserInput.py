class UserInput:

    def __init__(self):
        pass



    def check_coordinates(self,coordinates):
        """
        Vérifie que les données entrées sont valides
        :param coordinates: les coordonnées envoyées par l'utilisateur
        :return: les coordonnées du tir nettoyées
        """

        cleaned_coordinates = coordinates.strip().lower()
        if len(cleaned_coordinates) <= 3 and "a" <= cleaned_coordinates[0] <= "j" and 1 <= int(
                cleaned_coordinates[1]) <= 10:
            return cleaned_coordinates
        else:
            print("merci de rentrer des coordonnées valides")
            return False

    def ask_coordinates(self):
        return input("sur quelle case voulez vous tirer ? (q pour quitter) :")

