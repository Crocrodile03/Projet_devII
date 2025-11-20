import datetime
import random
from classVehicule import Vehicule
from classParking import Parking
from classSubscriber import Subscriber

#initialiser instance parking

def affichier_etat_parking():
    """
    PRE:
    POST:
    """
    pass

def gerer_entree_vehicule():
    """
    PRE:
    POST:
    """
    pass

def gerer_sortie_vehicule():
    """
    PRE:
    POST:
    """
    pass

def afficher_menu():
    """
    PRE:
    POST:
    """
    pass

def main():
    #boucle principale
    mon_parking = Parking()
    mon_parking.vehicules_entry("ABC-123", "visiteur")
    mon_parking.parking[0].get_duration()
    mon_parking.calculate_tarif("ABC-123")
    mon_parking.vehicules_leave("ABC-123")
if __name__ == "__main__":
    main()