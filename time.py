from datetime import datetime
import datetime

now = datetime.datetime.now() # L'heure actuelle
entry_time = datetime.datetime(2025, 11, 21, 8, 35, 54)  # Exemple d'heure d'entrée
seconds = (now - entry_time).total_seconds()
hours = seconds // 3600  # en heure
remainder = seconds % 3600 # le reste

if remainder > 0:
    print(f"Tu es resté {(hours + 1):.0f} heures dans le parking.")
#si le reste est plus grand que 0 ça veut dire que c'est pas une heure pile alors on arrondit à l'heure supérieure
else:
    print(f"Tu es resté {hours:.0f} heures dans le parking.")
#sinon je renvoie le nombre d'heures pile