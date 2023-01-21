"""
###########################################################################
#                              Projet Integrateur
# Étudiant: Linus Levi
# Cours: 420-321-AH
# Date: 20/01/2023
#
# Nom: projet_capteur
# Comporte un fonction pour lire et retourner la température du
# capteur de bord
#
###########################################################################
"""

# Le code a ete pris et adapte du lien ou livre ci-dessous
# Source 1: https://electrocredible.com/raspberry-pi-pico-temperature-sensor-tutorial/
# Source 2: Get started with MicroPython on Raspberry Pi Pico, p.97 to p.99

from machine import ADC
import time

adc = ADC(4)


def LireTemperatureCapteurIntegre():
    voltage = adc.read_u16() * ( 3.3 / 65535 )
    temperature_celcius = 27.0 - (voltage - 0.706) / 0.001721
    return temperature_celcius


# ---------------------------- TESTS --------------------------------


def main():
    print( LireTemperatureCapteurIntegre() )

if __name__ == '__main__':
    main()
