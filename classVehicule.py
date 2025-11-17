import datetime
from datetime import datetime
# import math

class Vehicule:
    """
    Classe véhicule simple.
    - entry_time est enregistré comme datetime.datetime
    - les méthodes get_duration / leave renvoient des secondes (int)
    - calculate_fee prend des secondes en entrée (ou calcule depuis entry_time)
    - les différents type sont : "visiteur" (normal), "abonné", "électrique", "handicapé"
    """

    def __init__(self, immatriculation, entry_time, type="visiteur"):
        self.immatriculation = immatriculation
        self.type = type
        self.entry_time = entry_time
        # self.is_parked = False

    # def park(self, entry_time=None):
    #    """Marque le véhicule comme garé et enregistre l'heure d'entrée (now si non fourni)."""
    #    self.entry_time = entry_time
    #    self.is_parked = True

    # def leave(self, leave_time=None):
    #    """
    #    Marque le véhicule comme parti et renvoie la durée du stationnement en secondes (int).
    #    Si entry_time n'était pas défini, renvoie 0.
    #    """
    #    now = leave_time or datetime.datetime.now()
    #    if not self.entry_time:
    #        self.is_parked = False
    #        return 0
    #    seconds = int((now - self.entry_time).total_seconds())
    #    if seconds < 0:
    #        seconds = 0
    #    self.is_parked = False
    #    return seconds

    # def get_duration(self, now=None):
    #    """Renvoie la durée depuis entry_time en secondes (int)."""
    #    now = now or datetime.datetime.now()
    #    if not self.entry_time:
    #        return 0
    #    seconds = int((now - self.entry_time).total_seconds())
    #    return max(0, seconds)

    # def calculate_parking_fee(self, rate_per_hour, duration_seconds=None, round_up=True):
    #    """
    #    Calcule le tarif à payer.
    #    - rate_per_hour : prix par heure (float)
    #    - duration_seconds : durée en secondes ; si None, utilise get_duration()
    #    - round_up : si True, arrondit les heures à l'entier supérieur
    #    Retourne un float arrondi à 2 décimales.
    #    """
    #    dur = duration_seconds if duration_seconds is not None else self.get_duration()
    #    hours = dur / 3600.0
    #    if round_up:
    #        hours = math.ceil(max(0.0, hours))
    #    else:
    #        hours = max(0.0, hours)
    #    fee = hours * rate_per_hour
    #    return round(fee, 2)

    def dic(self):
        """Sérialisation simple pour debug / tests."""
        return {
            "immatriculation": self.immatriculation,
            "type": self.type,
            "entry_time": self.entry_time.isoformat() if self.entry_time else None,
            "is_parked": self.is_parked
        }

    def __repr__(self):
        return "<Vehicule {} type={} parked={}>".format(self.immatriculation, self.type, self.is_parked)