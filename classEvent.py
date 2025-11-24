import classVehicule as Vehicule
import classParking as Parking
import datetime
class Event:

    def __init__(self):
        pass


    def alert(self, current_capacity, max_capacity, type='visiteur'):
        """
        Paramètre : current_capacity; Type : int; Description : nombre actuel de places occupées.
        Paramètre : max_capacity; Type : int; Description : Attribu capacity de l'objet Parking
        Paramètre : type; Type : str; Description : Catégorie de véhicule (par défaut 'visiteur').
        PRE: Les capacités sont des nombres entiers non négatifs. 
             current_capacity est inférieur ou égal à max_capacity.
        POST: Un message ou une notification est généré si la capacité atteint un seuil prédéfini. 
              Retourne True si une alerte est déclenchée, False sinon.
        """
        if current_capacity == max_capacity:
            # Générer une alerte (par exemple, envoyer un email ou afficher un message)
            # print(f"Alerte : Les places {type} sont pleines!")
            return True
        else :
            # places_restantes = int(max_capacity) - int(current_capacity)
            # print(f"Il reste {places_restantes} places {type}s disponibles.")
            return False

    def find_vehicule_by_type(self, type, p):
        """
        Paramètre : type; Type : str; Description : Catégorie de véhicule à rechercher.
        Paramètre : parking; Type : list; Description : Liste des emplacements contenus dans l'attribu parking de l'objet Parking. 
        PRE: L'entrée type est une chaîne de caractères valide. L'entrée parking est une collection itérable d'objets contenant des informations sur les véhicules/emplacements.
        POST: Une liste ou un itérateur des objets Vehicule (ou des immatriculations) correspondant au type spécifié est retourné.
        """
        type_of_vehicule = []
        for v in p.parking :
            if v.type == type :
                type_of_vehicule.append(v)
        print(f"Véhicules de type '{type}' dans le parking : {type_of_vehicule}")
        return type_of_vehicule

    def timeout(self, vehicule, parking):
        """
        Paramètre : vehicule; Type : Vehicule; Description : L'instance de véhicule concerné.
        Paramètre : date_time; Type : datetime; Descritption : Lheure actuelle pour calculer la durée du stationnement.
        Paramètre : parking; Type : Parking; Description : L'instance de parking pour accéder à la limite de temps.
        PRE: L'objet vehicule est valide et possède un entry_time. 
             date_time est un objet datetime valide.
        POST: La durée totale de stationnement (un objet timedelta) est calculée. 
              Si cette durée dépasse une limite prédéfinie, une alerte est déclenchée ???
        """

        time_in_parking = vehicule.get_duration()
        if time_in_parking >= parking.timeout_limit and vehicule.type != 'abonné':
            print(f"Alerte : Le véhicule {vehicule.immatriculation} a dépassé la limite de temps de stationnement.")
            return True
        elif time_in_parking >= 24 * vehicule.entry_time.month and vehicule.type == 'abonné':
            print(f"Alerte : Le véhicule {vehicule.immatriculation} a dépassé la limite de temps de stationnement pour un abonné.")
        else:
            print(f"Le véhicule {vehicule.immatriculation} est dans la limite de temps de stationnement.")
            return False