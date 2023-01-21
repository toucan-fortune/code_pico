"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Nom: projet_noeud
# Comporte une classe représentant un noeud (capteur quelconque)
#
###########################################################################
"""

from random import choice, randint

capteurs  = ["temperature", "humidite"]
metriques = ["brute", "moy_10_sec", "moy_15_sec", "moy_20_sec", "moy_30_sec", "moy_60_sec",
                      "moy_10_min", "moy_15_min", "moy_20_min", "moy_30_min", "moy_60_min"]

class Noeud:
    ID = 1 # variable statique

    def __init__(self):
        self.ID = "pico" + "{:0>2d}".format(Noeud.ID) #Noeud.ID
        self.capteur = choice(capteurs)
        self.donnees = []  # stockage des données pour analyse locale

        # Réglages de température et humidité
        # Pour simuler un environnement propre à l'emplacement d'un capteur
        self.tmp_min = randint(10, 30) # degrés Celsius
        self.hum_max = randint(60, 98) # pourcentage

        # Jeu de temperature et humidité
        self.jeu_tmp = randint(5, 15) # degrés Celsius
        self.jeu_hum = 100 - self.hum_max # pourcentage

        self.temperature = self.tmp_min
        self.humidite    = self.hum_max

        Noeud.ID += 1 # la valeur est préparée pour la prochaine instance


# --------------------------------- TESTS -----------------------------------


def main():

    noeuds = [Noeud() for i in range(9)]

    print("Nombre de noeuds: ", len(noeuds))

    for noeud in noeuds:
        print( "id: ", noeud.ID, "hum:", noeud.humidite, "jeu", noeud.jeu_hum )


if __name__ == '__main__':
    main()

