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

    def __init__(self, immatriculation: str, entry_time: datetime, type_vehicule="visiteur"):
        self.immatriculation = immatriculation
        self.type_vehicule = type_vehicule
        self.entry_time = entry_time

    def get_duration(self):
        """Renvoie la durée depuis entry_time en secondes (int)."""
        now = datetime.now() # L'heure actuelle

        seconds = (now - self.entry_time).total_seconds()
        hours = seconds // 3600  # en heure
        remainder = seconds % 3600 # le reste

        if remainder > 0:
            print(f"Tu es resté {(hours + 1):.0f} heures dans le parking.")
            return (hours + 1)
        # Si le reste est plus grand que 0 ça veut dire que c'est pas une heure pile alors on arrondit à l'heure supérieure
        else:
            print(f"Tu es resté {hours:.0f} heures dans le parking.")
            return hours
        # Sinon je renvoie le nombre d'heures pile

    def __repr__(self):
        return f"<Vehicule {self.immatriculation} type={self.type_vehicule} entry_time={self.entry_time}>"
    
    def __str__(self):
        return f"Le véhicule avec la plaque d'immatriculation : {self.immatriculation}, de type : {self.type_vehicule}, est entré à : {self.entry_time.hour}h{self.entry_time.minute:02}."