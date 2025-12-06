"""
Module initialisant les importations nécessaires, incluant le module standard
`datetime` pour la gestion et la manipulation des dates et heures dans
l'application.
"""
import datetime
from datetime import datetime

class Vehicule:
    """
    Classe véhicule simple.
    - entry_time est enregistré comme datetime.datetime
    - les méthodes get_duration / leave renvoient des secondes (int)
    - calculate_fee prend des secondes en entrée (ou calcule depuis entry_time)
    - les différents type sont : "visiteur" (Par défaut), "abonné", "électrique", "handicapé"
    """
    def __init__(self, immatriculation: str,
                entry_time: datetime=datetime.now(),
                type_vehicule: str="visiteur"):
        self.__immatriculation = immatriculation
        self.__type_vehicule = type_vehicule
        self.__entry_time = entry_time

    @property
    def immatriculation(self):
        """Get l'immatriculation du véhicule."""
        return self.__immatriculation
    @immatriculation.setter
    def immatriculation(self, immatriculation):
        """Set l'immatriculation du véhicule."""
        self.__immatriculation = immatriculation

    @property
    def type_vehicule(self):
        """Get le type de place que prends véhicule."""
        return self.__type_vehicule
    @type_vehicule.setter
    def type_vehicule(self, type_vehicule):
        """Set le type de place que prends véhicule."""
        self.__type_vehicule = type_vehicule
    @property
    def entry_time(self):
        """Get l'heure d'entrée dans le parking."""
        return self.__entry_time
    def get_duration(self):
        """Renvoie la durée depuis entry_time en secondes (int)."""
        now = datetime.now() # L'heure actuelle
        seconds = (now - self.entry_time).total_seconds()
        hours = seconds // 3600  # en heure
        remainder = seconds % 3600 # le reste
        if remainder > 0:
            print(f"Tu es resté {(hours + 1):.0f} heures dans le parking.")
            return int(hours + 1)
        # Si le reste est plus grand que 0 ça veut dire que c'est pas une heure pile
        # alors on arrondit à l'heure supérieure
        else:
            print(f"Tu es resté {hours:.0f} heures dans le parking.")
        return int(hours)
        # Sinon je renvoie le nombre d'heures pile
    def __repr__(self):
        return f"""<Vehicule {self.immatriculation}
        type={self.type_vehicule}
        entry_time={self.entry_time}>"""
    def __str__(self):
        return f"""Le véhicule avec la plaque d'immatriculation : {self.immatriculation},
        de type : {self.type_vehicule},
        est entré à : {self.entry_time.hour}h{self.entry_time.minute:02}.
        """
