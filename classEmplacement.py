# from classVehicule import Vehicule

# class Emplacement:
#     """
#     PRE: L'entrée type est une chaîne de caractères valide et correspond à un type de véhicule.
#          L'entrée position est un tuple représentant les coordonnées.
#     POST: Un nouvel objet Emplacement est créé.
#     """

#     def __init__(self, type, position):
#         self.type = type
#         self.is_available = True
#         self.position = position
#         self.vehicule_parked = None

#     def manage_emplacement(self, vehicule):
#         """
#         Paramètres : vehicule, Type : Vehicule ou None, Description : L'instance de véhicule à garer ou None pour libérer la place
#         PRE: L'objet Emplacement est valide. 
#              L'entrée vehicule est soit un objet Vehicule (ou Subscriber), soit None.
#         POST: Si vehicule est un objet Vehicule : self.is_available passe à False. self.vehicule_parked est défini sur l'objet vehicule.
#         POST: Si vehicule est None : self.is_available passe à True. self.vehicule_parked est défini sur None. 
#         """
#         if vehicule is None:
#             # libérer la place si un véhicule y est présent
#             if self.vehicule_parked is None:
#                 return False
#             try:
#                 duration = self.vehicule_parked.leave()
#             except Exception:
#                 # si leave() n'existe pas ou lève une erreur, on retourne None
#                 duration = None
#             self.vehicule_parked = None
#             self.is_available = True
#             return duration

#         # garer un véhicule : on accepte tout objet exposant une méthode park()
#         if not hasattr(vehicule, "park"):
#             return False
#         if not self.is_available:
#             return False

#         # enregistrer l'entrée sur le véhicule et marquer la place comme occupée
#         try:
#             vehicule.park()
#         except Exception:
#             # si park() existe mais échoue, on ne modifie pas l'état
#             return False

#         self.vehicule_parked = vehicule
#         self.is_available = False
#         return True

#     def park_vehicle(self, vehicule, entry_time=None):
#         """Garer un véhicule sur la place. Retourne True si la place est libre, sinon False si la place est occupée."""
#         if vehicule is None:
#             return False
#         if not hasattr(vehicule, "park"):
#         #la fonction hasttr sert à check si l'objet a un attribut ou une méthode
#             return False
#         if not self.is_available:
#             return False
#         try:
#             if entry_time is not None:
#                 vehicule.park(entry_time)
#             else:
#                 vehicule.park()
#         except Exception:
#             return False
#         self.vehicule_parked = vehicule
#         self.is_available = False
#         return True

#     def free_spot(self, leave_time=None):
#         """Libère la place, passe le véhicule en sortie et renvoie la durée en secondes ou False."""
#         if self.vehicule_parked is None:
#             return False
#         duration = self.vehicule_parked.leave(leave_time)
#         self.vehicule_parked = None
#         self.is_available = True
#         return duration

#     def can_accept(self, vehicule_type):
#         """
#         Vérifie si le type de la place accepte le type donné(normal, electric, free, disabled).
#         """
#         if self.type in ("all", "electric", "free", "disabled"):
#             return True
#         return self.type == vehicule_type

#     def get_vehicule(self):
#         return self.vehicule_parked

#     def dic(self):
#         return {
#             "type": self.type,
#             "position": self.position,
#             "is_available": self.is_available,
#             "vehicule": getattr(self.vehicule_parked, "immatriculation", None)
#         }

#     def __repr__(self):
#         return "<Emplacement pos={} type={} free={}>".format(self.position, self.type, self.is_available)

