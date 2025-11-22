import datetime
import random
from classVehicule import Vehicule
from classParking import Parking
from classSubscriber import Subscriber
from classEvent import Event
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
    event = Event()
    mon_parking = Parking()

    actions = [
        lambda: mon_parking.vehicules_entry("ABC-123", "visiteur"),
        lambda: mon_parking.vehicules_entry("ABC-123", "visiteur"),
        lambda: mon_parking.vehicules_entry("DEF-456", "handicapé"),
        lambda: mon_parking.vehicules_leave("ABC-123"),
        lambda: mon_parking.vehicules_entry("LEJ-258", "visiteur"),
        lambda: event.find_vehicule_by_type("visiteur", mon_parking),
        lambda: mon_parking.vehicules_leave("GHI-789"),
    ]

    # boucle d’exécution sécurisée
    for action in actions:
        try:
            action()
        except Exception as e:
            print(f"Erreur : {e}")

    print("Toutes les actions ont été traitées.")

if __name__ == "__main__":
    main()