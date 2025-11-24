import datetime
import random
from classVehicule import Vehicule
from classParking import Parking
from classSubscriber import Subscriber
from classEvent import Event

event = Event()
mon_parking = Parking()

def gerer_entree_vehicule():
    """
    PRE:
    POST:
    """
    immatriculation_vehicule = input("rentrer l'immatriculation\nFormat : ABC-123\n")
    type_vehicule = input("rentrer le type du véhicule\nFormat : visiteur - handicapé - éléctrique\n")
    mon_parking.vehicules_entry(immatriculation_vehicule, type_vehicule)
    print(f"Le vehicule avec l'immatriculation {immatriculation_vehicule} a été enregistrée dans le parking.")

def gerer_sortie_vehicule():
    """
    PRE:
    POST:
    """
    immatriculation_vehicule = input("rentrer l'immatriculation du vehicule\nFormat : ABC-123\n")
    mon_parking.vehicules_leave(immatriculation_vehicule)

def afficher_etat_parking():
    """
    PRE:
    POST:
    """
    print(f"Il y a actuellement :\n{mon_parking.current_capacity[0]} places visteurs\n{mon_parking.current_capacity[1]} places handicapé\n{mon_parking.current_capacity[2]} places éléctriques\n{mon_parking.current_capacity[3]} places abonnés\nOccupées dans le parking.")

def afficher_menu():
    """
    PRE:
    POST:
    """
    """Affiche le menu principal."""
    print("\n" + "="*40)
    print("Gestionnaire de Parking CLI ")
    print("="*40)
    print("1. **ENTRÉE** d'un véhicule")
    print("2. **SORTIE** d'un véhicule / Payer")
    print("3. Afficher l'**ÉTAT** du parking")
    print("4. **QUITTER**")
    print("="*40)


def main():
    #boucle principale
    # mon_parking.vehicules_entry("ABC-123", "visiteur")
    # mon_parking.parking[0].entry_time -= datetime.timedelta(hours=3, minutes=15)

    # actions = [
    #     lambda: mon_parking.calculate_tarif("ABC-123"),
    #     # lambda: mon_parking.vehicules_entry("ABC-123", "visiteur"),
    #     # lambda: mon_parking.vehicules_entry("DEF-456", "handicapé"),
    #     # lambda: mon_parking.vehicules_leave("ABC-123"),
    #     # lambda: mon_parking.vehicules_entry("LEJ-258", "visiteur"),
    #     # lambda: event.find_vehicule_by_type("visiteur", mon_parking),
    #     # lambda: mon_parking.vehicules_leave("GHI-789"),
    # ]

    # # boucle d’exécution sécurisée
    # for action in actions:
    #     try:
    #         action()
    #     except Exception as e:
    #         print(f"Erreur : {e}")

    # print("Toutes les actions ont été traitées.")

    while True:
        afficher_menu()
        choix = input("Votre choix (1-5) : ").strip()

        if choix == '1':
            gerer_entree_vehicule()
        elif choix == '2':
            gerer_sortie_vehicule()
        elif choix == '3':
            afficher_etat_parking()
        elif choix == '4':
            print("Merci d'avoir utilisé le gestionnaire de parking. Au revoir !")
            break
        else:
            print("Choix non valide. Veuillez réessayer.")

if __name__ == "__main__":
    main()