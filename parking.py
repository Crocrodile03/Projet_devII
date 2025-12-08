"""
Module regroupant les importations nécessaires à la gestion des véhicules,
à la génération de documents PDF et au traitement des erreurs personnalisées.

Imports :
    - os : fournit des fonctionnalités liées au système d'exploitation,
      notamment la manipulation de chemins et de fichiers.
    - datetime : permet de gérer les dates et heures. Principalement utilisé
      pour enregistrer les heures d'entrée et de sortie des véhicules.
    - reportlab.pdfgen.canvas : utilisé pour générer des fichiers PDF via
      l'objet Canvas.
    - reportlab.lib.pagesizes.mm : unité de mesure en millimètres pour
      définir précisément la taille des pages PDF.
    - Vehicule (depuis vehicule) : classe représentant un véhicule, utilisée
      pour gérer et manipuler les objets du parc automobile.
    - CapacityError, MissingVehiculeError (depuis exception) : exceptions
      personnalisées relatives aux problèmes de capacité ou à l'absence
      de véhicule dans une opération donnée.
"""
import os
import datetime
import json
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import mm
from vehicule import Vehicule
from exception import CapacityError, MissingVehiculeError, InvalidTypeError,VehiculeError, SubscriberConflictError, FailToLoad


class Parking :
    """Classe représentant un parking"""

    def __init__(self):
        # [0]: "visiteur" = 120
        # [1]: "handicapé" = 6
        # [2]: "électrique" = 4
        # [3]: "abonné" = 12
        self.__max_capacity = (120,6,4,12) # tuples des capacités par type de véhicule
        self.__current_capacity = [0,0,0,0] # liste des capacités par type de véhicule
        self.__parking = [] # liste des instances de véhicules dans le parking
        self.__opening_hours = "Lundi à Samedi : de 6h00 à 22h00 et Dimanche : de 8h00 à 20h00"
        self.__tarif = 1 # euro/heure
        self.__maxtarif = 10 # euro/jour
        self.__timeout_limit = datetime.timedelta(hours=24) # 24 heures
        self.__timeout_subscriber = datetime.timedelta(hours=24*30) # 30 jours en heures

    @property
    def max_capacity(self):
        """Get max_capacity"""
        return self.__max_capacity
    @property
    def current_capacity(self):
        """Get current_capacity"""
        return self.__current_capacity

    @current_capacity.setter
    def current_capacity(self, value):
        """Set current_capacity"""
        if not isinstance(value, list) or len(value) == 0:
            raise ValueError("Le type doit être une liste non vide")
        self.__current_capacity = value
    @property
    def parking(self):
        """Get parking"""
        return self.__parking
    @parking.setter
    def parking(self, value):
        """Set parking"""
        if not isinstance(value, list):
            raise ValueError("Le type doit être une liste")
        self.__parking = value
    @property
    def opening_hours(self):
        """Get opening_hours"""
        return self.__opening_hours
    @opening_hours.setter
    def opening_hours(self, value):
        """Set opening_hours"""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Le type doit être une chaine")
        self.__opening_hours = value
    @property
    def tarif(self):
        """Get tarif"""
        return self.__tarif
    @property
    def maxtarif(self):
        """Get maxtarif"""
        return self.__maxtarif
    @property
    def timeout_limit(self):
        """Get timeout_limit"""
        return self.__timeout_limit
    @timeout_limit.setter
    def timeout_limit(self, value):
        """Set timeout_limit"""
        if not isinstance(value, datetime.timedelta):
            raise ValueError("timeout_limit doit être un datetime.timedelta")
        self.__timeout_limit = value
    @property
    def timeout_subscriber(self):
        """Get timeout_subscriber"""
        return self.__timeout_subscriber
    @timeout_subscriber.setter
    def timeout_subscriber(self, value):
        """Set timeout_subscriber"""
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
                return True
            if v.type_vehicule == 'abonné' and temps > self.timeout_subscriber:
                return True
        return False

    def alert(self, type_v: str):
        """
        PRE: Les capacités sont des nombres entiers non négatifs. 
             current_capacity est inférieur ou égal à max_capacity. 
        POST: Retourne True si les places d'un type donnés sont pleines.
            sinon il retourne False.
        """
        if (type_v == 'visiteur' and
            self.current_capacity[0] >= self.max_capacity[0]):
            return True
        if (type_v == 'handicapé' and
            self.current_capacity[1] >= self.max_capacity[1]):
            return True
        if (type_v == 'électrique' and
            self.current_capacity[2] >= self.max_capacity[2]):
            return True
        if (type_v == 'abonné' and
            self.current_capacity[3] >= self.max_capacity[3]
            ):
            return True
        return False

    def find_vehicule_by_type(self, type_v: str, p: list):
        """
        Paramètre : type; Type : str;
            Description : Catégorie de véhicule à rechercher.
        Paramètre : parking; Type : list;
            Description : Liste des emplacements contenus dans l'attribu parking de l'objet Parking. 
        PRE: L'entrée type est une chaîne de caractères valide.
            L'entrée parking (p) est une lsit itérable d'instances véhicules.
        POST: Une liste ou un itérateur des objets Vehicule correspondant au type spécifié.
        """
        type_of_vehicule = []
        for v in p.parking :
            if v.type_vehicule == type_v :
                type_of_vehicule.append(v)
        print(f"Véhicules de type '{type_v}' dans le parking : {type_of_vehicule}")
        return type_of_vehicule

    def vehicules_entry(self, immatriculation: str, type_vehicule:  str):
        """
        Paramètre : immatriculation; Type: str; 
            Description : chaîne de caractères représentant l'immatriculation du véhicule.
        Paramètre : type_vehicule; Type: str; 
            Description : chaîne de caractères représentant le type de place
            PRE: L'objet vehicule est valide. 
            Une place disponible correspondant au type de vehicule existe
            (sauf pour les abonnés ayant des places fixes).
        POST: Un Emplacement libre est trouvé (ou attribué pour un abonné). 
              L'emplacement est mis à jour comme occupé via manage_emplacement. 
              Si le véhicule n'est pas un abonné, self.current_capacity est incrémentée de 1. 
              L'objet Emplacement attribué est retourné.
        Exceptions: Lève une exception si le parking est plein
                    ou si aucune place appropriée n'est trouvée.
        """
        vehicule = Vehicule(immatriculation, datetime.datetime.now(), type_vehicule)
        for v in self.parking:
            if v.immatriculation == vehicule.immatriculation:
                if v.type_vehicule == "abonné":
                    raise SubscriberConflictError(v.immatriculation)
                raise VehiculeError(v.immatriculation, v.type_vehicule)
        if vehicule.type_vehicule == 'visiteur':
            if self.alert(vehicule.type_vehicule):
                raise CapacityError(vehicule.type_vehicule)
            self.current_capacity[0] += 1
            self.parking.append(vehicule)
        elif vehicule.type_vehicule == 'handicapé':
            if self.alert(vehicule.type_vehicule):
                if self.alert('visiteur'):
                    """Si plus de place handicapé, on vérifie place visiteur
                       Si il reste des places visiteur alors on change son type en visiteur
                    """
                    raise CapacityError(f"{vehicule.type_vehicule} et visiteur")
                vehicule.type_vehicule = 'visiteur'
                self.current_capacity[0] += 1
                self.parking.append(vehicule)
            else:
                self.current_capacity[1] += 1
                self.parking.append(vehicule)
        elif vehicule.type_vehicule == 'électrique':
            if self.alert(vehicule.type_vehicule):
                if self.alert('visiteur'):
                    """Si plus de place électrique, on vérifie place visiteur
                       Si il reste des places visiteur alors on change son type en visiteur
                    """
                    raise CapacityError(f"{vehicule.type_vehicule} et visiteur")
                vehicule.type_vehicule = 'visiteur'
                self.current_capacity[0] += 1
                self.parking.append(vehicule)
            else:
                self.current_capacity[2] += 1
                self.parking.append(vehicule)
        else:
            raise InvalidTypeError
        self.timeout()
        # print(self.parking)
        return vehicule


    def vehicules_leave(self, immatriculation):
        """
        Paramètre : immatriculation; Type : str;
        Attribut immatriculation de l'instance Vehicule qui quitte le parking.
        PRE: L'immatriculation est valide. 
             L'immatriculation est associé à une instance de vehicule est occupé dans self.parking.
        POST: La place de parking associé est mis à jour comme libre
              (uniquement pour les non-abonnés). 
              Si le véhicule n'est pas un abonné, self.current_capacity
              ou splecial_current_capacity est décrémentée de 1. 
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
        raise MissingVehiculeError(immatriculation)
    
    def save_state(self, filename="parking_state.json"):
        """Sauvegarde l'état actuel du parking (véhicules et capacités) dans un fichier JSON."""
        parking_data = {
            "parking": [v.to_dict() for v in self.__parking],
            "current_capacity": self.__current_capacity,
        }

        try:
            with open(filename, 'w') as f:
                json.dump(parking_data, f, indent=4)
            print(f"État du parking sauvegardé dans {filename}.")
        except FailToLoad :
            print("gg nice try")

    def load_state(self, filename="parking_state.json"):
        """Charge l'état du parking depuis un fichier JSON au démarrage."""
        
        if not os.path.exists(filename):
            print("Aucun fichier de sauvegarde trouvé. Démarrage à vide.")
            return

        try:
            with open(filename, 'r') as f:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0: 
                    print(f"Le fichier de sauvegarde '{filename}' est vide. Démarrage à vide.")
                    return
                f.seek(0)
                parking_data = json.load(f) 

            self.__current_capacity = parking_data.get("current_capacity", [0, 0, 0, 0])
            self.__parking = [Vehicule.from_dict(v_data) 
                              for v_data in parking_data.get("parking", [])] 
            
            print(f"État du parking chargé depuis {filename}.")
            print(self.__parking)
        
        except json.JSONDecodeError as e:
            print(f"Erreur lors du décodage JSON du fichier de sauvegarde : {e}. Démarrage à vide.")
            self.__current_capacity = [0, 0, 0, 0]
            self.__parking = []
        except FailToLoad :
            self.__current_capacity = [0, 0, 0, 0]
            self.__parking = []
    
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
        raise MissingVehiculeError(immatriculation)
    def generer_paiement(self,immatriculation, p, amont):
        """
        Paramètre : immatriculation; Type : str;
            Description : immatriculation du véhicule qui quitte le parking.
        Paramètre : p; Type : list;
            Description : liste des emplacements contenus dans l'attribu parking de l'objet Parking.
        Paramètre : amont; Type : float;
            Description : montant total à payer.
        PRE: L'immatriculation est valide et associée à une instance de Vehicule dans p.
             amont est un float >= 0.
        POST: Un ticket de paiement au format PDF est généré
        et sauvegardé dans le répertoire "paiements".
              Le ticket contient les informations d'immatriculation,
              type de véhicule,
              date de paiement,
              temps passé dans le parking et montant payé.
              Le chemin du fichier PDF est retourné.
        Exceptions: Lève une exception si l'immatriculation n'est pas trouvée dans p.
        """
        mois_fr = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
        current_month = mois_fr[datetime.datetime.now().month - 1]
        type_v = ""
        time_in_parking = 0
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
        c.drawString(5 * mm,y,f"Immatriculation : {immatriculation}")
        y -= 5 * mm
        c.drawString(5 * mm,y,f"Type de véhicule : {type_v}")
        y -= 5 * mm
        c.drawString(5 * mm,y,f"Date de paiement : {datetime.datetime.now().strftime('%d/%m/%Y')}")
        y -= 5 * mm
        c.drawString(5 * mm,y,f"Temps rester dans le parking : {time_in_parking} heures")
        y -= 5 * mm
        c.drawString(5 * mm,y,f"Montant : {amont} €")
        y -= 10 * mm

        c.line(5 * mm,y,largeur - 5 * mm,y)
        y -= 5 * mm

        # Message bas du ticket
        c.setFont("Helvetica-Oblique",9)
        c.drawCentredString(largeur / 2,y,"Merci de votre visite")
        c.save()
        return file_path
