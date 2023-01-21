"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Classe: projet_messagerie
# S'occupe de gérer la connexion à MQTT
#
###########################################################################
"""


from projet_prive import monMQTTHost, monMQTTPort, monMQTTClientID, monMQTTUsername, monMQTTPassword
from umqtt.simple import MQTTClient
from time import sleep


class Messagerie():

    def __init__(self):
        self.client = None
        try:
            self.client = MQTTClient(server = monMQTTHost, client_id = monMQTTClientID, keepalive = 10,
                                     user = monMQTTUsername, password = monMQTTPassword, port = monMQTTPort)
            self.client.connect()
            print("MQTT connected to", monMQTTHost)
        except:
            print("MQTT: ERREUR constructeur()")


    def publieMessages(self, sujet, valeur):
        self.client.publish( sujet, valeur )


    def deconnexion(self):
        if self.client is not None:
            self.client.disconnect()
            print("MQTT: deconnecte")


# --------------------------------- TESTS --------------------------------------


def main():
    from projet_reseau import Reseau
    from projet_simule import SimuleCapteurs

    print("Programme demarre")
    reseau = Reseau()
    messagerie = Messagerie()
    sleep(1)
    messagerie.deconnexion()
    reseau.deconnexion()
    print("Programme termine")
    pass


if __name__ == '__main__':
    main()
