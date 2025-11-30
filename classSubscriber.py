import datetime
from classVehicule import Vehicule
from classEvent import Event

class Subscriber(Vehicule) :
    """
    Classe héritée de Vehicule et de ses attribus (surtout immatriculation), avec des attribus spécifiques : first_name, last_name, phone_number, subscribe_date, is_subscribe 
    PRE: Les attributs d'initialisation de Vehicule sont valides. 
         Les informations personnelles (first_name, last_name, phone_number) sont des chaînes de caractères valides. 
         subscribe_date est un objet datetime.
    POST: Un nouvel objet Subscribe est créé, héritant de Vehicule (en utilisant un type 'abonné'). 
          Les attributs spécifiques à l'abonné sont définis.
    """
    def __init__(self, immatriculation : str, first_name : str, last_name : str, phone_number : str):
        super().__init__(immatriculation, entry_time=datetime.datetime.now(), type_vehicule="abonné") #héritage de l'attribut de son parent.
        self.__first_name = first_name
        self.__last_name = last_name
        self.__phone_number = phone_number

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Prénom doit être une chaine")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Nom de famille doit être une chaine")
        self.__last_name = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Doit être une chaine")
        self.__last_name = value


    def subscribe(self,p):
        event = Event()
        if event.alert(p.current_capacity[3], p.max_capacity[3], 'abonné'):
            raise Exception("Nombre maximum d'abonné atteint")
        else :
            subscriber = Subscriber(self.immatriculation, self.first_name, self.last_name, self.phone_number)
            for v in p.parking:
                if v.immatriculation == subscriber.immatriculation:
                    if v.type_vehicule == "abonné":
                        raise Exception(f"Cette personne est déjà abonné")
                    elif v.type_vehicule == "visiteur":
                        raise Exception(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà dans le parking sur une place visiteur.")
                    elif v.type_vehicule == "handicapé":
                        raise Exception(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà dans le parking sur une place handicapé.")
                    elif v.type_vehicule == "électrique":
                        raise Exception(f"Le véhicule avec l'immatriculation {v.immatriculation} est déjà dans le parking sur une place électrique.")
            p.parking.append(subscriber)
            p.current_capacity[3] += 1
            
    def calculate_subscribe_fee(self):
        """
        PRE: 
        POST:
        """
        print(f"L'abonné {self.immatriculation} doit payer son abonnement annuel qui est de .")
        pass