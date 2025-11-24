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
    immatriculation_vehicule = input(" \nVeuillez rentrer l'immatriculation\nFormat : \"ABC-123\"\n\n")
    while True:
        choix = input(" \nVeuillez rentrer le type de place que le véhicule utilisera \n\033[92m1.Visiteur\n2.Handicapé\n3.Électrique\033[91m\n4.Annuler\033[0m\n\n").strip()
        type_vehicule = ""
        if choix == '1':
            type_vehicule = "visiteur"
            break
        elif choix == '2':
            type_vehicule = "handicapé"
            break
        elif choix == '3':
            type_vehicule = "électrique"
            break
        elif choix == '4':
            print("\033[91mAnnulation\033[0m, bonne journée !")
            break
        else:
            print("\033[91mChoix non valide. Veuillez réessayer.\033[0m")
    print(f"Le vehicule avec l'immatriculation {immatriculation_vehicule} a été enregistrée dans le parking.")
    mon_parking.vehicules_entry(immatriculation_vehicule, type_vehicule)
def gerer_sortie_vehicule():
    """
    PRE:
    POST:
    """
    immatriculation_vehicule = input("\nVeuillez rentrer l'immatriculation du vehicule\nFormat : \"ABC-123\"\n\n")
    mon_parking.calculate_tarif(immatriculation_vehicule)
    mon_parking.vehicules_leave(immatriculation_vehicule)

def afficher_etat_parking():
    """
    PRE:
    POST:
    """
    print(f"Il y a actuelement :\n{mon_parking.current_capacity[0]} places visteurs\n{mon_parking.current_capacity[1]} places handicapé\n{mon_parking.current_capacity[2]} places électriques\n{mon_parking.current_capacity[3]} places abonnés\nOccupées dans le parking.")

def afficher_menu():
    """
    PRE:
    POST:
    """
    """Affiche le menu principal."""
    print("\n" + "="*40)
    print("\033[95mGestionnaire de Parking CLI\033[0m")
    print("="*40)
    print("1. \033[92m\033[1mENTRÉE\033[0m d'un véhicule")
    print("2. \033[92m\033[1mSORTIE\033[0m d'un véhicule / Payer")
    print("3. Afficher l'\033[92m\033[1mÉTAT\033[0m du parking")
    print("4. \033[92m\033[1mQUITTER\033[0m")
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
        choix = input("Votre choix (1-4) : ").strip()
        try:
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
                print("\033[91mChoix non valide. Veuillez réessayer.\033[0m")
        except Exception as e:
            print(f"Une erreur c'est produite : {e}")
            print("Retour au menu")
if __name__ == "__main__":
    main()