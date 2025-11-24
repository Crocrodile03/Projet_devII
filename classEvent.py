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