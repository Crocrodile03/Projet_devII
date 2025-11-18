import datetime
from classVehicule import Vehicule

class Subscriber(Vehicule) :
    """
    Classe héritée de Vehicule et de ses attribus (surtout immatriculation), avec des attribus spécifiques : first_name, last_name, phone_number, subscribe_date, is_subscribe 
    PRE: Les attributs d'initialisation de Vehicule sont valides. 
         Les informations personnelles (first_name, last_name, phone_number) sont des chaînes de caractères valides. 
         subscribe_date est un objet datetime.
    POST: Un nouvel objet Subscriber est créé, héritant de Vehicule (en utilisant généralement un type 'ABONNE'). 
          Les attributs spécifiques à l'abonné sont définis. 
          L'attribut self.is_subscribe est initialisé à True.
    """
    def __init__(self, immatriculation : str, first_name : str, last_name : str, phone_number : str, subcscribe_date : datetime):
        Vehicule.__init__(immatriculation) #héritage de l'attribut de son parent.
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.subscribe_date = subcscribe_date #date de souscription à l'abonnement.
        self.is_subscribe = True

    def subscribe(self, immatriculation : str):
        """
        PRE:
        POST:
        """
        pass

    def calculate_timeout(self, immatriculation : str):
        """
        PRE:
        POST:
        """
        pass