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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
from vehicule import Vehicule
from subscriber import Subscriber
from exception import (CapacityError, MissingVehiculeError, InvalidTypeError,
                       VehiculeError, SubscriberConflictError, FailToLoad, IsASubscriber)


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
        # "Lundi à Samedi : de 6h00 à 22h00 et Dimanche : de 8h00 à 20h00"
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
        PRE:
            Aucune précondition spécifique. 
        POST:
            Retourne la première instance du véhicule qui a dépassé la limite de temps autorisée.
            Sinon, retourne False. 
        """
        if len(self.parking) == 0:
            return False
        now = datetime.datetime.now()
        for v in self.parking:
            temps = now - v.entry_time
            if temps > self.timeout_limit and v.type_vehicule != 'abonné':
                return v
            if v.type_vehicule == 'abonné' and temps > self.timeout_subscriber:
                return v
        return False

    def alert(self, type_v: str):
        """
        PRE:
            Le type de véhicule est valide (visiteur, handicapé, électrique ou abonné). 
        POST:
            Retourne True si les places d'un type données sont pleines.
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

    def find_vehicule_by_type(self, type_v: str):
        """ 
        PRE:
            L'entrée type corresepond soit à visiteur, handicapé, électrique ou abonné
        POST:
            Une liste des instances Vehicule correspondant au type spécifié.
        """
        type_of_vehicule = []
        for v in self.parking :
            if v.type_vehicule == type_v :
                type_of_vehicule.append(v)
        print(f"Véhicules de type '{type_v}' dans le parking : {type_of_vehicule}")
        return type_of_vehicule

    def find_vehicule(self, immat: str):
        """
        PRE:
            L'immatriculation du vehicule est déjà instanciée dans le parking.
        POST:
            Retourne l'instance Vehicule correspondant à l'immatriculation donnée.    
        """
        for v in self.parking:
            if v.immatriculation == immat:
                return v

    def vehicules_entry(self, immatriculation: str, type_vehicule:  str):
        """
        PRE:  
            Une place disponible correspondant au type de vehicule existe
        POST:
            L'instance Vehicule est rajouté à la liste parking,
            sauf pour les abonnés ayant des places fixes.
            la capacité du type de véhicule est incrémenté (+1).
        Exceptions:
            Lève une exception si le parking est plein
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
                    # Si plus de place handicapé, on vérifie place visiteur
                    # Si il reste des places visiteur alors on change son type en visiteur
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
                    # Si plus de place électrique, on vérifie place visiteur
                    # Si il reste des places visiteur alors on change son type en visiteur
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
        return vehicule

    def vehicules_leave(self, immatriculation: str):
        """
        PRE:
            L'immatriculation est associé à une instance de vehicule qui se trouve dans le parking.
        POST:
            L'instance Vehicule correspondante est effacée de la liste parking,
            et le compteur de véhicule par type est décrémenté (-1).
            Retourne True si la sortie est enregistrée.
        Exceptions:
            Lève une exception si l'immatriculation n'est pas trouvée dans le parking.
            Lève une exception si le véhicule est un abonné.
        """
        for v in self.parking:
            if v.immatriculation == immatriculation :
                if v.type_vehicule == 'abonné':
                    raise IsASubscriber
                self.parking.remove(v)
                if v.type_vehicule == 'visiteur':
                    self.current_capacity[0] -= 1
                elif v.type_vehicule == 'handicapé':
                    self.current_capacity[1] -= 1
                elif v.type_vehicule == 'électrique':
                    self.current_capacity[2] -= 1
                print(f"Le véhicule avec l'immatriculation {immatriculation} est sorti du parking.")
                self.timeout()
                return True
        raise MissingVehiculeError(immatriculation)

    def save_state(self, filename="parking_state.json"):
        """Sauvegarde l'état actuel du parking (véhicules et capacités) dans un fichier JSON."""
        parking_data = {
            "parking": [v.to_dict() for v in self.__parking],
            "current_capacity": self.__current_capacity,
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
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
            with open(filename, 'r', encoding="utf-8") as f:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0:
                    print(f"Le fichier de sauvegarde '{filename}' est vide. Démarrage à vide.")
                    return
                f.seek(0)
                parking_data = json.load(f)

            self.__current_capacity = parking_data.get("current_capacity", [0, 0, 0, 0])
            loaded_vehicles = []
            for v_data in parking_data.get("parking", []):
                type_vehicule = v_data.get("type_vehicule", "visiteur")
                if type_vehicule == "abonné":
                    loaded_vehicles.append(Subscriber.from_dict(v_data))
                else:
                    loaded_vehicles.append(Vehicule.from_dict(v_data))
            self.__parking = loaded_vehicles

        except json.JSONDecodeError as e:
            print(f"Erreur lors du décodage JSON du fichier de sauvegarde : {e}. Démarrage à vide.")
            self.__current_capacity = [0, 0, 0, 0]
            self.__parking = []
        except FailToLoad :
            self.__current_capacity = [0, 0, 0, 0]
            self.__parking = []

    def calculate_tarif(self, immatriculation: str):
        """
        PRE:
            L'immatriculation est une chaîne de caractères non vide qui est associée à une instance de
            véhicule dans le parking.
            Le tarif est un nombre positif représentant le coût horaire du stationnement.
            Il change en fonction du temps passé dans le parking.
        POST:
            La fonction retourne le tarif à payer qui est calculé par le temps dont la voiture est garé dans le parking.
            Renvoie le tarif à payer qui est calculé en fonction du temps passé dans le parking.
        Exceptions:
            Exceptions: si l'immatriculation n'est pas trouvée dans le parking alors une exception est levée.
        """
        for v in self.parking:
            if v.immatriculation == immatriculation:
                time_in_parking = v.get_duration()

                if isinstance(time_in_parking, int) or isinstance(time_in_parking, float):
                    hours = time_in_parking
                else:
                    hours = time_in_parking.total_seconds() / 3600

                fee = hours * self.tarif
                return min(fee, self.maxtarif)

        raise MissingVehiculeError(immatriculation)

    def generer_paiement(self, immatriculation: str, amont: float):
        """
        PRE:
            L'immatriculation est une chaîne de caractères non vide qui est associée à une instance de
            véhicule dans le parking.
            La voiture est associée à un montant strictement supérieur à 0.
            Selon le temps garer dans le parking le montant change également.
        POST:
            Un fichier PDF est généré pour être le ticket de paiement.
            Il est sauvegardé dans le fichier JSON/répertoire "paiements" et le sous-répertoire de son mois.
            Le fichier PDF(le ticket) contient : 
            l'immatriculation de la voiture,
            le type de la voiture,
            la date de paiement,
            Le temps total passé dans le parking,
            le montant payé.
            La fonction retourne une chaîne de caractères représentant le chemin complet du fichier PDF généré
            Exceptions: si l'immatriculation n'est pas trouvée dans le parking alors une exception est levée.
        """
        mois_fr = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
        type_v = ""
        time_in_parking = 0
        for v in self.parking:
            if v.immatriculation == immatriculation:
                time_in_parking = v.get_duration()
                type_v = v.type_vehicule
                break
        if type_v == "abonné":
            return False
        directory = "paiements"
        file = f"paiement_{immatriculation}_{mois_fr[datetime.datetime.now().month - 1]}.pdf"
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
