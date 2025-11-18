import datetime
from classVehicule import Vehicule
from classEvent import Event
from classSubscriber import Subscriber

class Parking :

    def __init__(self):
        self.max_capacity = 120 
        self.current_capacity = 0
        self.opening_hours = "Lundi à Samedi : de 6h00 à 22h00 et Dimanche : de 8h00 à 20h00" 
        self.tarif = 1 #euro/heure
        self.maxtarif = 10 #euro/jour
        self.tarif_abonnement = 60 #euro/mois
        self.timeout_limit = 24 #24 heures
        self.special_max_capacity = ([6,"handicapé"],[4,"électrique"],[12,"abonné"]) #liste des capacités spéciales par type de véhicule
        self.special_current_capacity = ([0,"handicapé"],[0,"électrique"],[12,"abonné"]) #liste des capacités spéciales par type de véhicule
        self.parking = [] #liste des objets Vehicule représentants les instances de véhicules garés dans le parking
        self.payment = [] #liste des transactions de paiement enregistrées

    def vehicules_entry(self, immatriculation : str, type :  str):
        """
        Paramètre : immatriculation; Type : str; Description : chaîne de caractères représentant l'immatriculation du véhicule qui rentre dans le parking.
        Paramètre : type; Type: str ; Description : chaîne de caractères représentant le type de place (visiteur, abonné; électrique, handicapé) que prendra le véhicule dans le parking.
        PRE: L'objet vehicule est valide. 
             Une place disponible correspondant au vehicule.type existe (sauf pour les abonnés ayant des places fixes).
        POST: Un Emplacement libre est trouvé (ou attribué pour un abonné). 
              L'emplacement est mis à jour comme occupé via manage_emplacement. 
              Si le véhicule n'est pas un abonné, self.current_capacity est incrémentée de 1. 
              L'objet Emplacement attribué est retourné.
        Exceptions: Lève une exception si le parking est plein ou si aucune place appropriée n'est trouvée.
        """
        vehicule = Vehicule(immatriculation, datetime.datetime.now(), type)
        event = Event()
        for v in self.parking:
            if v.immatriculation == vehicule.immatriculation:
                if v.type == "abonné":
                    raise Exception(f"L'immatriculation {v.immatriculation} appartient à un abonné")
                else:
                    raise Exception(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà dans le parking.")
        if event.alert(self.current_capacity, self.max_capacity):
            raise Exception("Le parking est plein.")
        else:
            if vehicule.type == 'visiteur':
                self.current_capacity += 1
                self.parking.append(vehicule)
            elif vehicule.type == 'handicapé':
                if event.alert(self.special_current_capacity[0][0], self.special_max_capacity[0][0], 'handicapé'):
                    raise Exception("Aucune place handicapé disponible.")
                else:
                    self.special_current_capacity[0][0] += 1
                    self.parking.append(vehicule)
            elif vehicule.type == 'électrique':
                if event.alert(self.special_current_capacity[1][0], self.special_max_capacity[1][0], 'électrique'):
                    raise Exception("Aucune place électrique disponible.")
                else:
                    self.special_current_capacity[1][0] += 1
                    self.parking.append(vehicule)
        print(vehicule)
        print(self.parking)
        return vehicule


    def vehicules_leave(self, immatriculation):
        """
        Paramètre : immatriculation; Type : str; Attribut immatriculation de l'instance Vehicule qui quitte le parking.
        PRE: L'immatriculation est valide. 
             L'immatriculation est associé à une instance de vehicule est occupé dans self.parking.
        POST: La place de parking associé est mis à jour comme libre (uniquement pour les non-abonnés). 
              Si le véhicule n'est pas un abonné, self.current_capacity  ou splecial_current_capacity est décrémentée de 1. 
              Retourne True si la sortie est enregistrée, False sinon.
        """
        for v in self.parking:
            if v.immatriculation == immatriculation :
                self.parking.remove(v)
                if v.type == 'visiteur':
                    self.current_capacity -= 1
                elif v.type == 'handicapé':
                    self.special_current_capacity[0][0] -= 1
                elif v.type == 'électrique':
                    self.special_current_capacity[1][0] -= 1
                print(f"Le véhicule avec l'immatriculation {immatriculation} est sorti du parking.")
                print(self.parking)
                return True

    def calculate_tarif(self, duration):
        """
        Paramètre : duration; Type : datetime; Description : attribut entry_time de l'instance Vehicule
        PRE: self.tarif est défini
        POST: Le tarif total dû est calculé et retourné en float.
        """

    # def calculate_parking_fee(self, rate_per_hour, duration_seconds=None, round_up=True):
    #    """
    #    Calcule le tarif à payer.
    #    - rate_per_hour : prix par heure (float)
    #    - duration_seconds : durée en secondes ; si None, utilise get_duration()
    #    - round_up : si True, arrondit les heures à l'entier supérieur
    #    Retourne un float arrondi à 2 décimales.
    #    """
    #    dur = duration_seconds if duration_seconds is not None else self.get_duration()
    #    hours = dur / 3600.0
    #    if round_up:
    #        hours = math.ceil(max(0.0, hours))
    #    else:
    #        hours = max(0.0, hours)
    #    fee = hours * rate_per_hour
    #    return round(fee, 2)
        pass

    def register_payment(self, amount, methode):
        """
        Paramètre : amount; Type : Float; Description : Le montant du paiement reçu
        Paramètre : methode; Type : str; Description : méthode de paiement (carte ou cash)
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