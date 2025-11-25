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
    def __init__(self, immatriculation : str, first_name : str, last_name : str, phone_number : str, subcscribe_date : datetime):
        super().__init__(immatriculation, type_vehicule="abonné") #héritage de l'attribut de son parent.
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.subscribe_date = subcscribe_date #date de souscription à l'abonnement.


    def subscribe(self, immatriculation, p, first_name, last_name, phone_number):
        event = Event()
        if event.alert(p.special_current_capacity[3], p.special_max_capacity[3], 'abonné'):
            raise Exception("Nombre maximum d'abonné atteint")
        else :
            subscriber = Subscriber(immatriculation, first_name, last_name, phone_number, datetime.datetime.now())
            for v in p.parking:
                if v.immatriculation == subscriber.immatriculation:
                    if v.type_vehicule == "abonné":
                        raise Exception(f"Cette personne est déjà abonné")
                    p.parking.remove(v)
                    if v.type_vehicule == "visiteur":
                        p.current_capacity[0] -= 1
                    elif v.type_vehicule == "handicapé":
                        p.special_current_capacity[1] -= 1
                    elif v.type_vehicule == "électrique":
                        p.special_current_capacity[2] -= 1
                p.parking.add(subscriber)
                p.special_current_capacity[3] += 1

    def calculate_subscribe_fee(self):
        """
        PRE: 
        POST:
        """
        print(f"L'abonné {self.immatriculation} doit payer son abonnement annuel qui est de .")
        pass