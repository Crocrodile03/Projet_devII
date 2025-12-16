"""
Exceptions personnalisées pour la gestion des erreurs dans le système de parking.
"""
class InvalidValueError(Exception) :
    """Exception levée pour une valeur invalide."""
    def __init__(self):
        self.message = "Type non valide"

    def __str__(self):
        return self.message

class CapacityError(Exception):
    """Exception levée lorsque la capacité maximale pour un type de véhicule est atteinte."""
    def __init__(self, vehicule_type):
        self.message = f"Aucune place {vehicule_type} disponible."

    def __str__(self):
        return self.message

class MissingVehiculeError(Exception):
    """Exception levée lorsque le véhicule n'est pas trouvé dans le parking."""
    def __init__(self, immatriculation):
        self.message = (
        f"Aucun véhicule avec l'immatriculation {immatriculation} n'a été trouvé dans le parking.")

    def __str__(self):
        return self.message

class SubscriberConflictError(Exception):
    """Exception levée lorsqu'un véhicule est déjà enregistré comme abonné."""
    def __init__(self, immatriculation):
        self.message = (
        f"Le véhicule avec l'immatriculation {immatriculation} est déjà enregistré comme abonné.")

    def __str__(self):
        return self.message

class CapacityFullError(Exception):
    """Exception levée lorsque le parking est plein."""
    def __init__(self):
        self.message = "Le parking est plein."

    def __str__(self):
        return self.message

class FullSubscriberCapacityError(Exception):
    """Exception levée lorsque la capacité maximale pour les abonnés est atteinte."""
    def __init__(self):
        self.message = (
            """L'enregistrement d'un nouvel abonné est impossible:
            la capacité maximale pour les abonnés est atteinte.""")

    def __str__(self):
        return self.message

class VehiculeError(Exception):
    """Exception levée lorsqu'un véhicule est déjà dans le parking."""
    def __init__(self, immatriculation, type_vehicule):
        self.message = (
        f"""Le véhicule avec l'immatriculation {immatriculation} est déjà
        dans le parking sur une place {type_vehicule}.""")

    def __str__(self):
        return self.message

class InvalidTypeError(Exception):
    """Exception levée pour un type invalide."""
    def __init__(self):
        self.message = "Type non valide"

    def __str__(self):
        return self.message

class InvalidValueSubscriberError(Exception):
    """Exception levée pour une valeur invalide dans Subscriber."""
    def __init__(self, input_sub, value):
        self.message = f"Le {input_sub} n'est pas valide : {value}."

    def __str__(self):
        return self.message

class FailToLoad(Exception):
    """Exception levée lors d'une erreur de chargement des données."""
    def __init__(self):
        self.message = "Erreur lors de la sauvegarde"

    def __str__(self):
        return self.message

class IsASubscriber(Exception):
    """Exception levée lorsqu'on tente de supprimer un abonné."""
    def __init__(self):
        self.message = f"On ne peut pas supprimer un abonné"
        
    def __str__(self):
        return self.message

class InvalidImmatriculationError(Exception):
    """Exception levée lorsqu'on tente de mettre une immatriculation vide"""
    def __init__(self):
        self.message = "L'immatriculation ne peut pas être vide ou composée uniquement d'espaces."
    
    def __str__(self):
        return self.message