import datetime
from classVehicule import Vehicule
from classEvent import Event
from classException import SubscriberConflictError, InvalidValueError, FullSubscriberCapacityError, VehiculeError
class Subscriber(Vehicule) :
    """
    Classe héritée de Vehicule et de ses attribus (surtout immatriculation), avec des attribus spécifiques : first_name, last_name, phone_number, subscribe_date, is_subscribe 
    PRE: Les attributs d'initialisation de Vehicule sont valides. 
         Les informations personnelles (first_name, last_name, phone_number) sont des chaînes de caractères valides. 
         subscribe_date est un objet datetime.
    POST: Un nouvel objet Subscribe est créé, héritant de Vehicule (en utilisant un type 'abonné'). 
          Les attributs spécifiques à l'abonné sont définis.
    """
    def __init__(self, immatriculation : str, first_name : str, last_name : str, phone_number : str, subcscribe_date : datetime):
        super().__init__(immatriculation, type_vehicule="abonné") #héritage de l'attribut de son parent.
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number
        self.__subscribe_date = subcscribe_date #date de souscription à l'abonnement.

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        # Changement 10 : Utilisation de InvalidValueError et message précis
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueError
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        # Changement 11 : Utilisation de InvalidValueError et message précis
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueError
        self.__last_name = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise InvalidValueError
        self.__phone_number = value 

    @property
    def subscribe_date(self):
        return self.__subscribe_date

    @subscribe_date.setter
    def subscribe_date(self, value):
        if not isinstance(value, datetime.datetime):
            raise InvalidValueError
        self.__subscribe_date = value


    def subscribe(self, immatriculation, p, first_name, last_name, phone_number):
        event = Event()
        if event.alert(p.current_capacity[3], p.max_capacity[3], 'abonné'):
            raise FullSubscriberCapacityError
        else :
            subscriber = Subscriber(immatriculation, first_name, last_name, phone_number, datetime.datetime.now())
            for v in p.parking:
                if v.immatriculation == subscriber.immatriculation:
                    if v.type_vehicule == "abonné":
                        raise SubscriberConflictError(v.immatriculation)
                    elif v.type_vehicule in ["visiteur", "handicapé", "électrique"]:
                        raise VehiculeError(v.immatriculation, v.type_vehicule)
            p.parking.append(subscriber)
            p.current_capacity[3] += 1
            print(f"L'abonné {first_name} {last_name} ({immatriculation}) a été ajouté.")
            
    def calculate_subscribe_fee(self):
        """
        PRE: Aucun prérequis spécifique. 
        POST: Renvoie le montant fixe de l'abonnement annuel pour un abonné.
        60 euros est le tarif fixe pour l'abonnement annuel.
        """
        self.tarif_abonnement = 60
        return self.tarif_abonnement  # Tarif fixe pour l'abonnement annuel