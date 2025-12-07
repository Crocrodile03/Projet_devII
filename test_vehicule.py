import unittest
from datetime import datetime, timedelta
from vehicule import Vehicule

class TestVehicule(unittest.TestCase):
#héritage de unittest.TestCase pour que chaque test soit indépe
    """
    Une classe pour faire les tests unitaires
    
    Teste les fonctionnalités suivantes :
    - Initialisation avec valeurs par défaut
    -Test de type de véhicule
    - Calcul de la durée de stationnement
    - Tests de __str__ et __repr__
    """

    def test_init_default_values(self):
        """Test que l'initialisation définit correctement les valeurs par défaut."""
        v = Vehicule("TEST123")

        self.assertEqual(v.immatriculation, "TEST123")
        self.assertEqual(v.type_vehicule, "visiteur")
        self.assertIsNotNone(v.entry_time)
        self.assertIsInstance(v.entry_time, datetime)

    def test_vehicule_immatriculation(self):
        """Test l'immatriculation du véhicule."""
        v = Vehicule("TEST123")

        self.assertEqual(v.immatriculation, "TEST123")

    def test_vehicule_type(self):
        #vérifie si le type de la voiture est correct
        """Test le type de la voiture."""
        v = Vehicule("ELEC001", type_vehicule="électrique")

        self.assertEqual(v.type_vehicule, "électrique")

    def test_get_duration(self):
    #test qd un véhicule rentre pdnt 2h30 est ce que ça arrondit bien à 3h
        """Test que get_duration calcule correctement la durée."""
        past_time = datetime.now() - timedelta(hours=2, minutes=30)
        v = Vehicule("TEST123", entry_time=past_time)

        duration = v.get_duration()

        # Doit arrondir à l'heure supérieure : 2h30 -> 3h
        self.assertEqual(duration, 3)

    def test_get_duration_exact_hours(self):
        #test qd un véhicule rentre pdnt 2h00 est ce que ça arrondit bien à 2h
        """Test get_duration avec un nombre exact d'heures."""
        past_time = datetime.now() - timedelta(hours=2, microseconds=0)
        v = Vehicule("TEST123", entry_time=past_time)

        duration = v.get_duration()

        # PRBLM si je mets que 2 ou trois le test ne marche pas, à régler dans vehicule
        self.assertIn(duration, 2)

    def test_str_(self):
        """Test la représentation string du véhicule."""
        v = Vehicule("ABC-123", type_vehicule="visiteur")
        str_repr = str(v)

        self.assertIn("ABC-123", str_repr)
        self.assertIn("visiteur", str_repr)

    def test_repr_(self):
        """Test la représentation repr du véhicule."""
        v = Vehicule("ABC-123")
        repr_str = repr(v)

        self.assertIn("Vehicule", repr_str)
        self.assertIn("ABC-123", repr_str)
#vérifie bien si les deux méthode str et repr fonctionnent correctement en renvoyant les bonnes informations

if __name__ == "__main__":
    unittest.main()
