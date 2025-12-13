class MyException(Exception) :
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class InvalidValueError(MyException) :
    def __init__(self):
        self.message = "Type non valide"

class CapacityError(MyException) :
    def __init__(self, vehicule_type):
        self.message = f"Aucune place {vehicule_type} disponible."

class MissingVehiculeError(MyException):
    def __init__(self, immatriculation):
        self.message = f"Aucun véhicule avec l'immatriculation {immatriculation} n'a été trouvé dans le parking."

class SubscriberConflictError(MyException):
    def __init__(self, immatriculation):
        self.message = f"Le véhicule avec l'immatriculation {immatriculation} est déjà enregistré comme abonné."

class CapacityFullError(MyException) :
    def __init__(self):
        self.message = "Le parking est plein."

class FullSubscriberCapacityError(MyException):
    def __init__(self):
        self.message = "L'enregistrement d'un nouvel abonné est impossible : la capacité maximale pour les abonnés est atteinte."

class VehiculeError(MyException):
    def __init__(self, immatriculation, type_vehicule):
        self.message = f"Le véhicule avec l'immatriculation {immatriculation} est déjà dans le parking sur une place {type_vehicule}."

class InvalidTypeError(MyException):
    def __init__(self):
        self.message = "Type non valide"

class InvalidValueSubscriberError(MyException):
    def __init__(self, input_sub, value):
        self.message = f"Le {input_sub} n'est pas valide : {value}."

class FailToLoad(MyException):
    def __init__(self):
        self.message = f"Erreur lors de la sauvegarde"

class IsASubscriber(MyException):
    def __init__(self):
        self.message = f"On ne peut pas supprimer un abonné"