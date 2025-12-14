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

    # ========== TESTS VALIDATION IMMATRICULATION VÉHICULE ==========

    def test_vehicule_immatriculation_vide(self):
        """Test création véhicule avec immatriculation vide."""
        v = Vehicule("")
        self.assertEqual(v.immatriculation, "")
        self.assertEqual(v.type_vehicule, "visiteur")

    def test_vehicule_immatriculation_chiffres_uniquement(self):
        """Test création véhicule avec immatriculation en chiffres uniquement."""
        v = Vehicule("123456")
        self.assertEqual(v.immatriculation, "123456")
        self.assertIsInstance(v.entry_time, datetime)

    def test_vehicule_immatriculation_lettres_uniquement(self):
        """Test création véhicule avec immatriculation en lettres uniquement."""
        v = Vehicule("ABCDEF")
        self.assertEqual(v.immatriculation, "ABCDEF")
        self.assertIsInstance(v.entry_time, datetime)

    def test_vehicule_immatriculation_caracteres_speciaux(self):
        """Test création véhicule avec caractères spéciaux dans immatriculation."""
        v = Vehicule("AB-123@#")
        self.assertEqual(v.immatriculation, "AB-123@#")
        self.assertEqual(v.type_vehicule, "visiteur")

    def test_vehicule_immatriculation_espaces(self):
        """Test création véhicule avec espaces dans immatriculation."""
        v = Vehicule("AB 12 CD")
        self.assertEqual(v.immatriculation, "AB 12 CD")
        self.assertEqual(v.type_vehicule, "visiteur")

    def test_vehicule_immatriculation_unicode(self):
        """Test création véhicule avec caractères unicode/accents."""
        v = Vehicule("ÉÀÇ-123")
        self.assertEqual(v.immatriculation, "ÉÀÇ-123")
        self.assertIsInstance(v.entry_time, datetime)

    def test_vehicule_immatriculation_tres_longue(self):
        """Test création véhicule avec immatriculation très longue."""
        immat_longue = "A" * 100
        v = Vehicule(immat_longue)
        self.assertEqual(v.immatriculation, immat_longue)

    def test_vehicule_immatriculation_casse_mixte(self):
        """Test création véhicule avec casse mixte dans immatriculation."""
        v = Vehicule("AbC-123-xYz")
        self.assertEqual(v.immatriculation, "AbC-123-xYz")

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

        # Accepte 2 ou 3 car le timing peut varier de quelques microsecondes
        self.assertIn(duration, [2, 3])

    def test_vehicule_to_dict(self):
        """Test la conversion d'un véhicule en dictionnaire."""
        v = Vehicule("DICT-001", type_vehicule="électrique")
        data = v.to_dict()
        
        self.assertEqual(data["immatriculation"], "DICT-001")
        self.assertEqual(data["type_vehicule"], "électrique")
        self.assertIn("entry_time", data)

    def test_vehicule_from_dict(self):
        """Test la création d'un véhicule depuis un dictionnaire."""
        data = {
            "immatriculation": "FROM-002",
            "entry_time": datetime.now().isoformat(),
            "type_vehicule": "handicapé"
        }
        v = Vehicule.from_dict(data)
        
        self.assertEqual(v.immatriculation, "FROM-002")
        self.assertEqual(v.type_vehicule, "handicapé")
        self.assertIsInstance(v.entry_time, datetime)

    def test_vehicule_setter_immatriculation(self):
        """Test le setter d'immatriculation."""
        v = Vehicule("OLD-123")
        v.immatriculation = "NEW-456"
        
        self.assertEqual(v.immatriculation, "NEW-456")

    def test_vehicule_setter_type(self):
        """Test le setter de type_vehicule."""
        v = Vehicule("SET-789", type_vehicule="visiteur")
        v.type_vehicule = "abonné"
        
        self.assertEqual(v.type_vehicule, "abonné")

    def test_get_duration_returns_integer(self):
        """Test que get_duration renvoie bien un entier."""
        past_time = datetime.now() - timedelta(hours=5, minutes=15)
        v = Vehicule("INT-001", entry_time=past_time)
        duration = v.get_duration()
        
        self.assertIsInstance(duration, int)
        self.assertEqual(duration, 6)  # Arrondi à l'heure supérieure

if __name__ == "__main__":
    unittest.main()
