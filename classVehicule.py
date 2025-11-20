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

    def __init__(self, immatriculation: str, entry_time: datetime, type="visiteur"):
        self.immatriculation = immatriculation
        self.type = type
        self.entry_time = entry_time

    def get_duration(self):
        """Renvoie la durée depuis entry_time en secondes (int)."""
        now = datetime.datetime.now()#qaund la voiture rentre

        if self.type == "abonné":
            return False
        
        seconds = (now - self.entry_time).total_seconds()
        hours = seconds // 3600 #en heure
        remainder = seconds % 3600# le reste

        if seconds <= 0:
            return 0
        #si secondes est plus petit ou égal à 0 alors 0
        elif remainder > 0:
            return (hours + 1) * 3600
        #si le reste est plus grand que 0 ça veut dire que c'est pas une heure pile alors on arrondit à l'heure supérieure
        else:
            return max(0, hours)
        #sinon je renvoie le nombre d'heures pile

    def __repr__(self):
        return f"<Vehicule {self.immatriculation} type={self.type} entry_time={self.entry_time}>"
    
    def __str__(self):
        return f"Le véhicule avec la plaque d'immatriculation : {self.immatriculation}, de type : {self.type}, est entré à : {self.entry_time}."