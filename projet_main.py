"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Nom: projet_main
# Intègre les objets nécéssaires pour constituer et rouler l'application
#
###########################################################################
"""


from projet_reseau import Reseau
from projet_messagerie import Messagerie
from projet_simule import SimuleCapteurs
from time import sleep


def main():
    # Initialisation
    print("Programme demarre")
    reseau = Reseau()
    messagerie = Messagerie()

    # debut du travail
    sleep(1)
    SimuleCapteurs(broker)
    sleep(1)

    # preparatifs de cloture
    messagerie.deconnexion()
    reseau.deconnexion()
    print("Programme termine")
    pass


if __name__ == '__main__':
    main()


