import classVehicule as Vehicule

class Emplacement:

    """
    PRE: L'entrée type est une chaîne de caractères valide et correspond à un type de véhicule.
         L'entrée position est un tuple (ou une structure de données équivalente) représentant les coordonnées.
    POST: Un nouvel objet Emplacement est créé. Les attributs self.type et self.position sont définis. self.is_available est initialisé à True. self.vehicule_parked est initialisé à None.
    """

    def __init__(self, type : str, position : tuple):
        self.type = type # Catégorie de la place (Voiture éléctrique, etc.)
        self.is_available = True
        self.position = position # Coordonnées de la place dans le parking (allée, place)
        self.vehicule_parked = None

    def manage_emplacement(self, vehicule):
        """
        Paramètres : vehicule, Type : Vehicule ou None, Description : L'instance de véhicule à garer ou None pour libérer la place
        PRE: L'objet Emplacement est valide. 
             L'entrée vehicule est soit un objet Vehicule (ou Subscriber), soit None.
        POST: Si vehicule est un objet Vehicule : self.is_available passe à False. self.vehicule_parked est défini sur l'objet vehicule.
        POST: Si vehicule est None : self.is_available passe à True. self.vehicule_parked est défini sur None. 
        """
        pass