
"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Classe: Reseau
# S'occupe de gérer la connexion via le WiFi
#
###########################################################################
"""

import network
import sys
from time import sleep
from projet_prive import monSSID, monPASSWORD
import projet_prive


# Code adapté du lien ci dessous:
# source: https://www.cnx-software.com/2022/07/03/getting-started-with-wifi-on-raspberry-pi-pico-w-board/


class Reseau():

    def __init__(self):
        # On etablit une connection via le modem
        try:
            self.wlan = None
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.connect( monSSID, monPASSWORD )
        except:
            print("WiFi: ERREUR au constructeur()")
            sys.exit()

        # On accorde du temps pour la connexion se fasse
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print("WiFi: connexion en cours...")
            sleep(1)

        # On traite les erreurs de connection
        if self.wlan.status() != 3:
            raise RuntimeError("WiFi: ERREUR, la connexion au reseau n'a pu se faire")
        else:
            print( "WiFi: connecte" )
            status = self.wlan.ifconfig()
            #print( 'ip = ' + status[0] )


    def deconnexion(self):
        # déconnexion du réseau WiFi
        if self.wlan is not None:
            sleep(1)
            self.wlan.disconnect()
            print( "WiFi: deconnecte" )


# --------------------------------- TESTS -------------------------------------


def main():
    reseau = Reseau()
    sleep(1)
    reseau.deconnexion()
    print("Programme termine")
    pass

if __name__ == '__main__':
    main()
