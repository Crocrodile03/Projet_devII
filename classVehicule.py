import datetime
from datetime import datetime
# import math

class Vehicule:
    """
    Classe véhicule simple.
    - entry_time est enregistré comme datetime.datetime
    - les méthodes get_duration / leave renvoient des secondes (int)
    - calculate_fee prend des secondes en entrée (ou calcule depuis entry_time)
    - les différents type sont : "visiteur" (Par défaut), "abonné", "électrique", "handicapé"
    """

    def __init__(self, immatriculation: str, entry_time: datetime, type="visiteur"):
        self.immatriculation = immatriculation
        self.type = type
        self.entry_time = entry_time

    def __repr__(self):
        return f"<Vehicule {self.immatriculation} type={self.type} entry_time={self.entry_time}>"
    
    def __str__(self):
        return f"Le véhicule avec la plaque d'immatriculation : {self.immatriculation}, de type : {self.type}, est entré à : {self.entry_time}."