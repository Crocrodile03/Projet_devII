import datetime
from classVehicule import Vehicule
from classEmplacement import Emplacement
from classEvent import Event
from classSubscriber import Subscriber

class Parking :

    def __init__(self):
        self.capacity = 120 
        #self.opening_hours = 
        self.tarif = 1 #unité /heure ?
        self.parking = [] #liste des objets Emplacement représentants les places du parking
        self.payment = [] #liste des transactions de paiement enregistrées

    def vehicules_entry(self, vehicule):
        """
        Paramètre : vehicule, Type : Vehicule ou Subscriber, DEscription : instance de Vehicule représentant un véhicule qui rentre dans le parking.
        PRE: L'objet vehicule est valide. 
             Une place disponible correspondant au vehicule.type existe (sauf pour les abonnés ayant des places fixes).
        POST: Un Emplacement libre est trouvé (ou attribué pour un abonné). 
              L'emplacement est mis à jour comme occupé via manage_emplacement. 
              Si le véhicule n'est pas un abonné, self.current_capacity est incrémentée de 1. 
              L'objet Emplacement attribué est retourné.
        Exceptions: Lève une exception si le parking est plein ou si aucune place appropriée n'est trouvée.
        """
        pass

    def vehicules_leave(self, vehicule):
        """
        Paramètre : vehicule, Type : Vehicule ou Subscriber, Description : instance de Vehicule
        PRE: L'objet vehicule est valide. 
             Le véhicule est associé à un Emplacement occupé dans self.parking.
        POST: L'emplacement associé est mis à jour comme libre (uniquement pour les non-abonnés) via manage_emplacement(None). 
              Si le véhicule n'est pas un abonné, self.current_capacity est décrémentée de 1. 
              Retourne True si la sortie est enregistrée, False sinon.
        """
        pass

    def calculate_tarif(self, duration):
        """
        Paramètre : duration, Type : datetime, Description : attribut entry_time de l'instance Vehicule
        PRE: self.tarif est défini
        POST: Le tarif total dû est calculé et retourné en float.
        """
        pass

    def register_payment(self, amount, methode):
        """
        Paramètre : amount, Type : Float, Description : Le montant du paiement reçu
        Paramètre : methode, Type : str, Description : méthode de paiement (carte ou cash)
        PRE: amount est un nombre non négatif. 
             methode est une chaîne de caractères valide.
        POST: Un enregistrement de paiement (contenant la date, le montant et la méthode) est ajouté à la liste self.payment.
        """
        pass

    def generate_report(self):
        """
        PRE:
        POST:
        """
        pass