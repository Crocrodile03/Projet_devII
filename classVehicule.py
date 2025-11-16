import datetime

class Vehicule:

    """
    PRE: L'entrée immatriculation est une chaîne de caractères non vide. 
         L'entrée type est une chaîne de caractères valide.
         L'entrée entry_time est un objet datetime.
    POST: Un nouvel objet Vehicule est créé et initialisé. Les attributs self.immatriculation, self.type, et self.entry_time sont définis.
    """

    def __init__(self, immatriculation : str, type : str, entry_time : datetime):

        self.immatriculation = immatriculation # Identifiant unique du véhicule
        self.type = type # Catégorie du véhicule (Voiture éléctrique, Handicapé, etc.)
        self.entry_time = entry_time # Date et heure d'entrée dans le parking (obtenu à l'instanciation du véhicule)
        self.is_parked = False #surement pas utile finalement.