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
from vehicule import Vehicule
from exception import CapacityError, SubscriberConflictError, InvalidValueError

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
    def __init__(self,immatriculation: str,first_name: str,last_name: str,phone_number: str):
        super().__init__(immatriculation,type_vehicule="abonné",entry_time=datetime.datetime.now())
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number
    @property
    def first_name(self):
        """Get le prénom de l'abonné."""
        return self.__first_name
    @first_name.setter
    def first_name(self, value):
        """Set le prénom de l'abonné."""
        # Changement 10 : Utilisation de InvalidValueError et message précis
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueError("L'attribut 'first_name' (prénom) doit être une chaîne de caractères non vide.")
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
            raise InvalidValueError("L'attribut 'last_name' (nom de famille) doit être une chaîne de caractères non vide.")
        self.__last_name = value

    @property
    def phone_number(self):
        """Get le numéro de téléphone de l'abonné."""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        """Set le numéro de téléphone de l'abonné."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueError("L'attribut 'phone_number' (numéro de téléphone) doit être une chaîne de caractères non vide.")
        self.__phone_number = value

    def subscribe(self, p):
        """PRE: immatriculation est une chaîne de caractères valide.
        p est un objet Parking valide.
        POST: Ajoute l'abonné au parking s'il n'y a pas de conflit et si la capacité le permet.
        Lève SubscriberConflictError si le véhicule est déjà abonné ou présent dans le parking.
        Lève CapacityError si la capacité maximale pour les abonnés est atteinte.
        """
        if p.alert('abonné'):
            raise CapacityError("""L'enregistrement d'un nouvel abonné est impossible:
                                la capacité maximale pour les abonnés est atteinte.""")
        for v in p.parking:
            if v.immatriculation == self.immatriculation:
                if v.type_vehicule == "abonné":
                    raise SubscriberConflictError(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà enregistré comme abonné.")
                if v.type_vehicule in ["visiteur", "handicapé", "électrique"]:
                    raise CapacityError(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà dans le parking sur une place {v.type_vehicule}.")
        p.parking.append(self)
        p.current_capacity[3] += 1
        print(f"L'abonné {self.first_name} {self.last_name} ({self.immatriculation}) a été ajouté.")         
    def calculate_subscribe_fee(self):
        """
        PRE: 
        POST:
        """
        print(f"L'abonné {self.immatriculation} doit payer son abonnement annuel qui est de .")
        return 60  # Tarif fixe pour l'abonnement annuel