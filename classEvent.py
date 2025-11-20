import classVehicule as Vehicule

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
            print(f"Alerte : Les places {type} sont pleines!")
            return True
        else :
            print(f"Places {type} disponibles.")
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
        return type_of_vehicule

    def timeout(self, vehicule):
        """
        Paramètre : vehicule; Type : Vehicule; Description : L'instance de véhicule concerné.
        Paramètre : date_time; Type : datetime; Descritption : Lheure actuelle pour calculer la durée du stationnement.
        PRE: L'objet vehicule est valide et possède un entry_time. 
             date_time est un objet datetime valide.
        POST: La durée totale de stationnement (un objet timedelta) est calculée. 
              Si cette durée dépasse une limite prédéfinie, une alerte est déclenchée ???
        """
        time_in_parking = vehicule.get_duration()
        if time_in_parking >= 24 :
            pass