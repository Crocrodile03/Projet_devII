import unittest
from datetime import datetime 
from subscriber import Subscriber
from exception import InvalidValueSubscriberError

class TestSubscriber(unittest.TestCase):
    """
    Classe de test unitaire pour la classe Subscriber.

    Teste les fonctionnalités :
    """
    def test_init_subscriber(self):
        """Valeur par défaut pour les tests"""
        s = Subscriber("Test-123", "Antoine", "Mont", "0123040506")

        self.assertEqual(s.immatriculation, "Test-123")
        self.assertEqual(s.first_name, "Antoine")
        self.assertEqual(s.last_name, "Mont")
        self.assertEqual(s.phone_number, "0123040506")
        self.assertEqual(s.type_vehicule, "abonné")
        self.assertIsNotNone(s.entry_time)
        self.assertIsInstance(s.entry_time, datetime)

    def test_subscriber_vehicule(self):
        """Test si l'immatriculation du véhicule appartient bien à un abonné"""
        s = Subscriber("Test-123", "Antoine", "Mont", "0123040506")

        self.assertEqual(s.type_vehicule, "abonné")
        self.assertTrue(hasattr(s, 'immatriculation'))
        self.assertTrue(hasattr(s, 'entry_time'))

#test pour voir si l'abonné à bien un first, last et phone number

    def test_subscriber_info(self):
        """tester les infos de l'abonné"""
        s = Subscriber("Test-123", "Antoine", "Mont", "0123040506")

        self.assertEqual(s.first_name, "Antoine")
        self.assertEqual(s.last_name, "Mont")
        self.assertEqual(s.phone_number, "0123040506")

    def test_subscriber_invalid_info(self):
        """Test que les setters lèvent des exceptions pour des valeurs invalides."""
        s = Subscriber("ABC-456", "Jake", "Dupont", "0654030201")

        # Test first_name invalide (vide ou espaces)
        with self.assertRaises(InvalidValueSubscriberError):
            s.first_name = " "

        # Test last_name invalide (vide)
        with self.assertRaises(InvalidValueSubscriberError):
            s.last_name = " "

        # Test phone_number invalide (vide)
        with self.assertRaises(InvalidValueSubscriberError):
            s.phone_number = " "

    def test_tarif_subscriber(self):
        """test le tarif de  l'abonnement"""

        s = Subscriber("Test-123", "Antoine", "Mont", "0123040506")

        self.assertEqual(s.tarif_abonnement, 60)

    def test_tarif_abonnement_invalid_value(self):
        """Test si le tarif est négatif"""
        s = Subscriber("Test-123", "Antoine", "Mont", "0123040506")
        
        with self.assertRaises(InvalidValueSubscriberError):
            s.tarif_abonnement = -10

if __name__ == "__main__":
    unittest.main()
