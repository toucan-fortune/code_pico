"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Nom: projet_simule
# S'occupe de simuler le nombre de noeuds desires
#
###########################################################################
"""


from random import randint, choice, random, seed # pour le test
from projet_noeud import Noeud
from projet_capteur import LireTemperatureCapteurIntegre
from time import sleep, localtime
import ntptime  # car datetime n'est pas disponible pour MicroPython
import math
import json
import machine  # pour la DEL


#tout ca va tres bien dans un fichier global

"""
    Avant d'aller en production, il est imperatif de verifier certains reglagess pour ne pas
    se retrouver avec des resultats desagreables. Tout au long du code se trouve des
    marqueurs, apparaissant comme "Verification", suivi par un numero
    Utiliser l'outil de recherche pour les reperer facilement
"""


metriques = ["brute", "moy_10_sec", "moy_15_sec", "moy_20_sec", "moy_30_sec", "moy_60_sec",
                      "moy_10_min", "moy_15_min", "moy_20_min", "moy_30_min", "moy_60_min"]

topic = "TOUCAN" # le canal d'envoi des messages via MQTT


def SimuleCapteurs(mqttclient):
    led = machine.Pin("LED", machine.Pin.OUT)
    led.off()

    seed()
    # la liste des noeuds (capteurs)
    Noeud.ID = 1 # nécessaire car MicroPython travail de la memoire et ne remet pas cette valeur à 0
    nombre_de_noeuds = 4  # Verification 2 (minimum 2)
    noeuds = [Noeud() for i in range(nombre_de_noeuds)]
    # on s'assurer explicitement qu'il y ait au moins un capteur d'humidite et un de temperature,
    # car a l'interne, le choix est aleatoire, et il est arrive durant des tests que lorsqu'il y a
    # que 2 ou trois noeuds, qu'ils soient tous du meme type
    noeuds[0].capteur = "temperature"
    noeuds[1].capteur = "humidite"

    # Obtention de la date et l'heure ainsi que quelques calculs relatifs
    ntptime.settime()
    aujourdhui = localtime() # datetime.datetime.now()
    annee = aujourdhui[0]
    mois = aujourdhui[1]
    jour = aujourdhui[2]

    decalage = 24 - randint(0, 5) # en heures

    # les unites des minutes et de l'angle
    # On etablit une intervalle par laquelle on divisera une heure de temps (60 minutes)
    # pour etablir la grandeur de notre pas (mesure en minutes)

    # Verification 3
    intervalle = 60 # la grandeur de pas (en minutes)
    tranches = 60 / intervalle # le nombre de tranches par heure

    # L'angle, lui, s'etale sur toute une journee (24 heures), on a donc besoin de savoir
    # le nombre de tranches en 24 heures et le diviser par ce nombre.
    inc_ang = 180.0 / (24.0 * tranches) # increment de l'angle (degres) par tranche dans 24 heures

    # le decallage est utilise pour decaller la courbe de temperature et d'humidite
    # relatif au cycle des heures.
    # Lorsque non-decalle, l'angle est remis a 0 en même temps que le debut du cycle d'heures
    # Lorsque decalle, l'angle commence par une valeur qui represente le decallage et se remet
    # a zero lorsqu'il atteint 180.0 ou plus. Cela se traduit par une valeur d'angle qui
    # correspond a:
    angle = decalage * tranches * inc_ang
    # Cela veut dire le nombre d'heures de decallage, multiplie par le nombre de tranches
    # dans une heure, multiplie par le nombre de degres par tranche

    # Pour les fins de notre demonstration, on doit produire des valeurs realistes
    # Quoique pour du temps reel on utilise la fonction datetime.datetime.now()
    # pour notre demonstration, puisqu'on simule plusieurs capteurs ainsi que
    # les dates et les heures, on utilise le montage suivant:

    nombre_de_documents = 0  # compteur

    for jour in range(jour, jour + 4): # Verification 4
        for heure in range(0, 24):
            for minute in range(0, 60, intervalle):

                # les angles sont independants du cycle d'heures en raison du decallage
                if angle > 180:
                    angle = 0

                # On produit le facteur utilise pour les calculs
                sinus = math.sin(angle / 57.3) # 57.3 pour convertir en radians

                # On genere des donnees pour chaque capteur
                for noeud in noeuds:
                    # on s'occupe de la temperature et de l'humidite. Cette derniere est l'inverse
                    # de la temperature. Lorsque la temperature est elevee, l'humidite est
                    # a son plus bas niveau, et lorsque la temperature est a son plus bas,
                    # c'est l'humidite qui est a son plus haut

                    noeud.temperature = round(noeud.tmp_min + (noeud.jeu_tmp * sinus) + 3 * random(), 3)
                    noeud.humidite = round(noeud.hum_max - (noeud.jeu_hum * sinus) + 3 * random(), 3)

                    date_et_heure = str(annee) + "-" + str(mois) + "-" + str(jour) + " " + \
                    str(heure) + ":" + str(minute) + ":00.000000"

                    # le premier noeud doit toujours avoir la valeur de la temperature du pico
                    if noeud.ID == "pico00":
                        noeud.temperature = LireTemperatureCapteurIntegre()

                    # La valeur de l'enregistrment depend de la grandeur mesuree
                    if noeud.capteur == "temperature":
                        valeur = noeud.temperature
                    else:
                        valeur = noeud.humidite

                    # on ajoute la donnee a la liste des donnees du noeud (non-implemente)
                    #noeud.donnees.append(valeur) # Verification 5

                    # le document est prepare, puis insere
                    document = { "datetime" : date_et_heure,
                                 "noeud"    : noeud.ID,
                                 "capteur"  : noeud.capteur,
                                 "metrique" : metriques[0],
                                 "valeur"   : valeur }

                    try: # la veritable insertion des documents
                        mqttclient.publieMessages(topic, json.dumps(document)) # Verification 7
                        nombre_de_documents += 1
                        led.on()
                        pass
                    except:
                        print("erreur d'enregistrement")

                    # un delai plus long afin d'eviter de stresser MQTT
                    # on ne connait pas ses limites
                    sleep(0.100)   # Verification 8
                    led.off()
                    compteur_noeuds += 1

                # fin de la boucle 'for' des noeuds
                angle += inc_ang
            # fin de la boucle 'for' des minutes
        # fin de la boucle 'for' des heures
    # fin de la boucle 'for' des jours

    print(nombre_de_documents, " documents enregistres")
    print("Fin:", localtime() )

    # on induqe la fin des messages pour que la boucle en aval arrête
    mqttclient.publieMessages(topic, "FIN")


def main():
    SimuleCapteurs("test")


if __name__ == '__main__':
    main()
