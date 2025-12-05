class InvalidValueError(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class CapacityError(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class MissingVehiculeError(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class SubscriberConflictError(Exception):
    def __init__(self, message=""):
        super().__init__(message)