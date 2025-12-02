from classParking import Parking
from classEvent import Event
from classSubscriber import Subscriber
import datetime

mon_parking = Parking()
mon_parking.vehicules_entry("ABC-123", "visiteur")
a = mon_parking.calculate_tarif("ABC-123")
print(a)
imat = "ABC-123"
print(mon_parking.parking)
mon_parking.generer_paiement(imat,mon_parking.parking, a)
mon_parking.vehicules_leave("ABC-123")