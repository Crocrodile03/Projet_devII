"""
Module contenant les importations nécessaires pour la gestion des véhicules,
la manipulation de dates et le traitement des exceptions personnalisées.

Imports :
    - datetime : fournit des outils pour manipuler les dates et heures
    - Vehicule (depuis vehicule) : classe représentant un véhicule, utilisée
      pour gérer les caractéristiques et opérations sur les véhicules.
    - CapacityError, SubscriberConflictError, InvalidValueError (depuis exception) :
      exceptions personnalisées permettant de gérer respectivement les erreurs
      liées à une capacité insuffisante, aux conflits entre abonnés et aux
      valeurs invalides fournies aux méthodes.
"""
import datetime
from datetime import datetime
from vehicule import Vehicule
from exception import (CapacityError, SubscriberConflictError, FullSubscriberCapacityError,
                       InvalidValueSubscriberError)

class Subscriber(Vehicule) :
    """
    Classe héritée de Vehicule et de ses attribus (surtout immatriculation),
    avec des attribus spécifiques: first_name, last_name, phone_number, subscribe_date, is_subscribe 
    PRE: Les attributs d'initialisation de Vehicule sont valides. 
         Les informations personnelles (first_name, last_name, phone_number)
         sont des chaînes de caractères valides. 
         subscribe_date est un objet datetime.
    POST: Un nouvel objet Subscribe est créé, héritant de Vehicule (en utilisant un type 'abonné'). 
          Les attributs spécifiques à l'abonné sont définis.
    """
    def __init__(self,immatriculation: str,first_name: str,last_name: str,
                 phone_number: str,entry_time: datetime=datetime.now()):
        super().__init__(immatriculation,type_vehicule="abonné",entry_time=datetime.now())
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__tarif_abonnement = 60 # euro/mois
    @property
    def first_name(self):
        """Get le prénom de l'abonné."""
        return self.__first_name
    @first_name.setter
    def first_name(self, value):
        """Set le prénom de l'abonné."""
        # Changement 10 : Utilisation de InvalidValueError et message précis
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueSubscriberError("prénom", value)
        self.__first_name = value

    @property
    def last_name(self):
        """Get le nom de famille de l'abonné."""
        return self.__last_name
    @last_name.setter
    def last_name(self, value):
        """Set le nom de famille de l'abonné."""
        # Changement 11 : Utilisation de InvalidValueError et message précis
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueSubscriberError("nom", value)
        self.__last_name = value

    @property
    def phone_number(self):
        """Get le numéro de téléphone de l'abonné."""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        """Set le numéro de téléphone de l'abonné."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueSubscriberError("numéro de téléphone", value)
        self.__phone_number = value
    @property
    def tarif_abonnement(self):
        """Get tarif_abonnement"""
        return self.__tarif_abonnement
    @tarif_abonnement.setter

    def tarif_abonnement(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise InvalidValueSubscriberError("tarif d'abonnement",value)
        self.__tarif_abonnement = value

    def subscribe(self, p: list):
        """
        PRE:
            p est une liste d'instance de parking.
        POST:
            Ajoute l'abonné au parking,
            incrémente (+1) le nombre d'abonné.
        Exceptions:
            Lève une exception si le véhicule est déjà abonné ou présent dans le parking.
            Lève exception si la capacité maximale pour les abonnés est atteinte.
        """
        if p.alert('abonné'):
            raise FullSubscriberCapacityError
        for v in p.parking:
            if v.immatriculation == self.immatriculation:
                if v.type_vehicule == "abonné":
                    raise SubscriberConflictError(v.immatriculation)
                if v.type_vehicule in ["visiteur", "handicapé", "électrique"]:
                    raise CapacityError(v.type_vehicule)
        p.parking.append(self)
        p.current_capacity[3] += 1
        print(f"L'abonné {self.first_name} {self.last_name} ({self.immatriculation}) a été ajouté.")

    def calculate_subscribe_fee(self):
        """
        À enlever !
        PRE:
            Aucun prérequis spécifique. 
        POST:
            Renvoie le montant fixe de l'abonnement annuel pour un abonné.
        """
        return self.tarif_abonnement  # Tarif fixe pour l'abonnement annuel

#création de dictionnaire pour le fichier JSON
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "phone_number": self.__phone_number,
        })
        return data

    @staticmethod
    def from_dict(data):
        entry_time = datetime.fromisoformat(data["entry_time"])
        subscriber = Subscriber(
            data["immatriculation"],
            data["first_name"],
            data["last_name"],
            data["phone_number"],
            entry_time)
        return subscriber
