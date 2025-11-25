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
        choix = input(" \nVeuillez rentrer le type de place que le véhicule utilisera :\n\n1.\033[92m\033[1mVisiteur\033[0m\n2.\033[92m\033[1mHandicapé\033[0m\n3.\033[92m\033[1mÉlectrique\033[0m\n4.\033[91m\033[1mAnnuler\033[0m\n\n").strip()
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
            print("\033[91m\033[1mAnnulation\033[0m, bonne journée !")
            break
        else:
            print("\033[91mChoix non valide. Veuillez réessayer.\033[0m")
    print(f"Le vehicule avec l'immatriculation \033[1m{immatriculation_vehicule}\033[0m a été enregistrée dans le parking.")
    mon_parking.vehicules_entry(immatriculation_vehicule, type_vehicule)
def gerer_sortie_vehicule():
    """
    PRE:
    POST:
    """
    immatriculation_vehicule = input(" \nVeuillez rentrer l'immatriculation du vehicule\nFormat : \"ABC-123\"\n\n")
    mon_parking.calculate_tarif(immatriculation_vehicule)
    mon_parking.vehicules_leave(immatriculation_vehicule)

def afficher_etat_parking():
    """
    PRE:
    POST:
    """
    print(f"Il y a actuelement :\n{mon_parking.current_capacity[0]} places visteurs\n{mon_parking.current_capacity[1]} places handicapé\n{mon_parking.current_capacity[2]} places électriques\n{mon_parking.current_capacity[3]} places abonnés\nOccupées dans le parking.")
def gerer_abonnement_vehicule():
    """
    PRE:
    POST:
    """
    while True:
        choix = input(" \nVeuillez choisir un choix pour l'abonnement :\n1.\033[92mAbonner\033[0m une personne\n2.\033[92mRetirer\033[0m un abonné\n3.\033[92mVoir\033[0m les différents abonnés du parking\n4.\033[91mAnnuler\033[0m\n\n").strip()
        if choix == '1':     
            immatriculation_vehicule = input(" \nVeuillez rentrer l'immatriculation du vehicule\nFormat : \"ABC-123\"\n\n")
            first_name = input(" \nVeuillez rentrer le \033[1mprénom\033[0m de l'abonné\n\n")
            last_name = input(" \nVeuillez rentrer le \033[1mnom\033[0m de l'abonné\n\n")
            phone_number = input(" \nVeuillez rentrer le \033[1mnuméro de téléphone\033[0m de l'abonné\nFormat : \"+32470123456\"\n\n")
            subscriber = Subscriber(immatriculation_vehicule, first_name, last_name, phone_number, datetime.datetime.now())
            subscriber.subscribe(immatriculation_vehicule, mon_parking, first_name, last_name, phone_number)
            break
        elif choix == '2':
            print("Fonctionnalité en cours de développement.")
            break
        elif choix == '3':
            abonnés = event.find_vehicule_by_type('abonné', mon_parking)
            if not abonnés:
                print("Aucun abonné dans le parking.")
            else:
                print("Liste des abonnés dans le parking :")
                for abonné in abonnés:
                    print(abonné)
            break
        elif choix == '4':
            print("\033[91m\033[1mAnnulation\033[0m, bonne journée !")
            break
        else:
            print("\033[91mChoix non valide. Veuillez réessayer.\033[0m")

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
    print("4. Gérer les \033[92m\033[1mABONNEMENT\033[0m d'un véhicule")
    print("5. \033[91m\033[1mQUITTER\033[0m")
    print("="*40)


def main():
    while True:
        afficher_menu()
        choix = input("Votre choix (1-5) : ").strip()
        try:
            if choix == '1':
                gerer_entree_vehicule()
            elif choix == '2':
                gerer_sortie_vehicule()
            elif choix == '3':
                afficher_etat_parking()
            elif choix == '4':
                gerer_abonnement_vehicule()
            elif choix == '5':
                print("Merci d'avoir utilisé le gestionnaire de parking. Au revoir !")
                break
            else:
                print("\033[91mChoix non valide. Veuillez réessayer.\033[0m")
        except Exception as e:
            print(f"Une erreur c'est produite : {e}")
            print("Retour au menu")
if __name__ == "__main__":
    main()