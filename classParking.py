import datetime
from classVehicule import Vehicule
from classEvent import Event
from classException import CapacityError, MissingVehiculeError
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
import os


class Parking :

    def __init__(self):
        # [0]: "visiteur" = 120
        # [1]: "handicapé" = 6
        # [2]: "électrique" = 4
        # [3]: "abonné" = 12
        self.__max_capacity = (120,6,4,12) # tuples des capacités par type de véhicule
        self.__current_capacity = [0,0,0,0] # liste des capacités par type de véhicule
        self.__parking = [] # liste des objets Vehicule représentants les instances de véhicules garés dans le parking
        self.__opening_hours = "Lundi à Samedi : de 6h00 à 22h00 et Dimanche : de 8h00 à 20h00" 
        self.__tarif = 1 # euro/heure
        self.__maxtarif = 10 # euro/jour
        self.__tarif_abonnement = 60 # euro/mois
        self.__timeout_limit = datetime.timedelta(hours=24) # 24 heures
        self.__timeout_subscriber = datetime.timedelta(hours=24*30) # 30 jours en heures

    @property
    def max_capacity(self):
        return self.__max_capacity
      
    @property
    def current_capacity(self):
        return self.__current_capacity

    @current_capacity.setter
    def current_capacity(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise ValueError("Le type doit être une liste non vide")
        self.__current_capacity = value
    
    @property
    def parking(self):
        return self.__parking

    @parking.setter
    def parking(self, value):
        if not isinstance(value, list):
            raise ValueError("Le type doit être une liste")
        self.__parking = value

    @property
    def opening_hours(self):
        return self.__opening_hours

    @parking.setter
    def opening_hours(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Le type doit être une chaine")
        self.__opening_hours = value

    @property
    def tarif(self):
        return self.__tarif

    @property
    def maxtarif(self):
        return self.__maxtarif

    @property
    def tarif_abonnement(self):
        return self.__tarif_abonnement

    @tarif_abonnement.setter
    def tarif_abonnement(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("tarif_abonnement doit être un nombre >= 0")
        self.__tarif_abonnement = value

    @property
    def timeout_limit(self):
        return self.__timeout_limit
    
    @timeout_limit.setter
    def timeout_limit(self, value):
        if not isinstance(value, datetime.timedelta):
            raise ValueError("timeout_limit doit être un datetime.timedelta")
        self.__timeout_limit = value

    @property
    def timeout_subscriber(self):
        return self.__timeout_subscriber
    
    @timeout_subscriber.setter
    def timeout_subscriber(self, value):
        if not isinstance(value, datetime.timedelta):
            raise ValueError("timeout_subscriber doit être un datetime.timedelta")
        self.__timeout_subscriber = value
    
    def timeout(self):
        """
        PRE: L'objet vehicule est valide et possède un entry_time. 
        POST: La durée totale de stationnement (un objet timedelta) est calculée. 
              Si cette durée dépasse une limite prédéfinie, une alerte est déclenchée ???
        """
        if len(self.parking) == 0: 
            print("Le parking est vide")
        now = datetime.datetime.now()
        for v in self.parking:
            temps = now - v.entry_time
            if temps > self.timeout_limit and v.type_vehicule != 'abonné':
                print(f"Alerte : Le véhicule {v.immatriculation} a dépassé la limite de temps de stationnement.")
                # return True
            elif v.type_vehicule == 'abonné' and temps > self.timeout_subriber:
                print(f"Le véhicule {v.immatriculation} a dépassé la limite de temps de stationnement pour un abonné.")
                # return True

    def vehicules_entry(self, immatriculation : str, type_vehicule :  str):
        """
        Paramètre : immatriculation; Type : str; Description : chaîne de caractères représentant l'immatriculation du véhicule qui rentre dans le parking.
        Paramètre : type_vehicule; Type: str ; Description : chaîne de caractères représentant le type de place (visiteur, abonné; électrique, handicapé) que prendra le véhicule dans le parking.
        PRE: L'objet vehicule est valide. 
             Une place disponible correspondant au vehicule.type existe (sauf pour les abonnés ayant des places fixes).
        POST: Un Emplacement libre est trouvé (ou attribué pour un abonné). 
              L'emplacement est mis à jour comme occupé via manage_emplacement. 
              Si le véhicule n'est pas un abonné, self.current_capacity est incrémentée de 1. 
              L'objet Emplacement attribué est retourné.
        Exceptions: Lève une exception si le parking est plein ou si aucune place appropriée n'est trouvée.
        """
        vehicule = Vehicule(immatriculation, datetime.datetime.now(), type_vehicule)
        event = Event()
        for v in self.parking:
            if v.immatriculation == vehicule.immatriculation:
                if v.type_vehicule == "abonné":
                    raise Exception(f"L'immatriculation {v.immatriculation} appartient à un abonné")
                else:
                    raise Exception(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà dans le parking.")
        if event.alert(self.current_capacity[0], self.max_capacity[0]):
            raise CapacityError("Le parking est plein.")
        else:
            if vehicule.type_vehicule == 'visiteur':
                self.current_capacity[0] += 1
                self.parking.append(vehicule)
            elif vehicule.type_vehicule == 'handicapé':
                if event.alert(self.current_capacity[1], self.max_capacity[1], 'handicapé'):
                    raise CapacityError("Aucune place handicapé disponible.")
                else:
                    self.current_capacity[1] += 1
                    self.parking.append(vehicule)
            elif vehicule.type_vehicule == 'électrique':
                if event.alert(self.current_capacity[2], self.max_capacity[2], 'électrique'):
                    raise CapacityError("Aucune place électrique disponible.")
                else:
                    self.current_capacity[2] += 1
                    self.parking.append(vehicule)
            else:
                raise CapacityError("Type non valide")
        print(vehicule)
        self.timeout()
        # print(self.parking)
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
                if v.type_vehicule == 'visiteur':
                    self.current_capacity[0] -= 1
                elif v.type_vehicule == 'handicapé':
                    self.current_capacity[1] -= 1
                elif v.type_vehicule == 'électrique':
                    self.current_capacity[2] -= 1
                print(f"Le véhicule avec l'immatriculation {immatriculation} est sorti du parking.")
                self.timeout()
                # print(self.parking)
                return True
        raise MissingVehiculeError(f"Aucun véhicule avec l'immatriculation {immatriculation} n'a été trouvé dans le parking.")
    
    def calculate_tarif(self, immatriculation):
        """
        Paramètre : vehicule; Type : Vehicule; Description : Instance de vehicule
        PRE: self.tarif est défini
        POST: Le tarif total dû est calculé et retourné en float.
        """
        for v in self.parking:
            if v.immatriculation == immatriculation:
                time_in_parking = v.get_duration()
                if time_in_parking * self.tarif >= self.maxtarif:
                    fee = self.maxtarif 
                else:
                    fee = time_in_parking * self.tarif
                # print(f"Le montant est de {fee} euros.")
                return fee
        raise MissingVehiculeError(f"Aucun véhicule avec l'immatriculation {immatriculation} n'a été trouvé dans le parking.")
       
    
    def register_payment(self, amount, methode):
        """
        Paramètre : amount; Type : Float; Description : Le montant du paiement reçu
        Paramètre : methode; Type : str; Description : méthode de paiement (carte ou cash)
        PRE: amount est un nombre non négatif. 
             methode est une chaîne de caractères valide.
        POST: Un enregistrement de paiement (contenant la date, le montant et la méthode) est ajouté à la liste self.payment.
        """

    def generer_paiement(self,immatriculation, p, amont):

        mois_fr = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
        current_month = mois_fr[datetime.datetime.now().month - 1]
        for v in p:
            if v.immatriculation == immatriculation:
                time_in_parking = v.get_duration()
                type_v = v.type_vehicule
       
        directory = "paiements"
        file = f"paiement_{immatriculation}_{current_month}.pdf"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, file)


        # Format ticket
        largeur, hauteur = 90 * mm, 120 * mm
        c = canvas.Canvas(file_path, pagesize=(largeur, hauteur))

        # Décalage vertical pour placer le texte
        y = hauteur - 10 * mm

        # Titre
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(largeur / 2, y, "TICKET PARKING Reçu de Paiement")
        
        y -= 10 * mm
        # Informations
        c.setFont("Helvetica", 10)
        c.drawString(5 * mm, y, f"Immatriculation : {immatriculation}")
        y -= 5 * mm
        c.drawString(5 * mm, y, f"Type de véhicule : {type_v}")
        y -= 5 * mm
        c.drawString(5 * mm, y, f"Date de paiement : {datetime.datetime.now().strftime('%d/%m/%Y')}")
        y -= 5 * mm
        c.drawString(5 * mm, y, f"Temps rester dans le parking : {time_in_parking} heures")
        y -= 5 * mm
        c.drawString(5 * mm, y, f"Montant : {amont} €")
        y -= 10 * mm

        c.line(5 * mm, y, largeur - 5 * mm, y)
        y -= 5 * mm

        # Message bas du ticket
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(largeur / 2, y, "Merci de votre visite")
        c.save()
        return file_path
