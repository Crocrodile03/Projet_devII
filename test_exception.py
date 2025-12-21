import unittest
from exception import (
    InvalidValueError, CapacityError, MissingVehiculeError,
    SubscriberConflictError, CapacityFullError, FullSubscriberCapacityError,
    VehiculeError, InvalidTypeError, InvalidValueSubscriberError,
    FailToLoad, IsASubscriber
)


class TestExceptions(unittest.TestCase):
    """Tests unitaires pour toutes les exceptions personnalisées."""

    def test_invalid_value_error(self):
        """Test InvalidValueError."""
        exc = InvalidValueError()
        self.assertEqual(exc.message, "Type non valide")
        self.assertEqual(str(exc), "Type non valide")

    def test_capacity_error(self):
        """Test CapacityError avec type de véhicule."""
        exc = CapacityError("visiteur")
        self.assertEqual(exc.message, "Aucune place visiteur disponible.")
        self.assertIn("visiteur", str(exc))
        
        exc2 = CapacityError("électrique")
        self.assertIn("électrique", str(exc2))

    def test_missing_vehicule_error(self):
        """Test MissingVehiculeError avec immatriculation."""
        exc = MissingVehiculeError("ABC-123")
        self.assertIn("ABC-123", exc.message)
        self.assertIn("n'a été trouvé", str(exc))

    def test_subscriber_conflict_error(self):
        """Test SubscriberConflictError."""
        exc = SubscriberConflictError("XYZ-789")
        self.assertIn("XYZ-789", exc.message)
        self.assertIn("déjà enregistré comme abonné", str(exc))

    def test_capacity_full_error(self):
        """Test CapacityFullError."""
        exc = CapacityFullError()
        self.assertEqual(exc.message, "Le parking est plein.")
        self.assertEqual(str(exc), "Le parking est plein.")

    def test_full_subscriber_capacity_error(self):
        """Test FullSubscriberCapacityError."""
        exc = FullSubscriberCapacityError()
        self.assertIn("abonné", exc.message)
        self.assertIn("capacité maximale", str(exc))

    def test_vehicule_error(self):
        """Test VehiculeError avec immatriculation et type."""
        exc = VehiculeError("DEF-456", "visiteur")
        self.assertIn("DEF-456", exc.message)
        self.assertIn("visiteur", exc.message)
        self.assertIn("déjà", str(exc))
        self.assertIn("parking", str(exc))

    def test_invalid_type_error(self):
        """Test InvalidTypeError."""
        exc = InvalidTypeError()
        self.assertEqual(exc.message, "Type non valide")
        self.assertEqual(str(exc), "Type non valide")

    def test_invalid_value_subscriber_error(self):
        """Test InvalidValueSubscriberError avec paramètres."""
        exc = InvalidValueSubscriberError("prénom", "")
        self.assertIn("prénom", exc.message)
        self.assertIn("n'est pas valide", str(exc))
        
        exc2 = InvalidValueSubscriberError("téléphone", "123")
        self.assertIn("téléphone", str(exc2))

    def test_fail_to_load(self):
        """Test FailToLoad."""
        exc = FailToLoad()
        self.assertIn("sauvegarde", exc.message)
        self.assertEqual(str(exc), "Erreur lors de la sauvegarde")

    def test_is_a_subscriber(self):
        """Test IsASubscriber."""
        exc = IsASubscriber()
        self.assertIn("abonné", exc.message)
        self.assertIn("supprimer", str(exc))

    def test_exception_inheritance(self):
        """Test que toutes les exceptions héritent de Exception."""
        self.assertTrue(issubclass(InvalidValueError, Exception))
        self.assertTrue(issubclass(CapacityError, Exception))
        self.assertTrue(issubclass(MissingVehiculeError, Exception))
        self.assertTrue(issubclass(VehiculeError, Exception))
        self.assertTrue(issubclass(FailToLoad, Exception))

    def test_exception_can_be_raised(self):
        """Test que les exceptions peuvent être levées et attrapées."""
        with self.assertRaises(CapacityError):
            raise CapacityError("handicapé")
        
        with self.assertRaises(MissingVehiculeError):
            raise MissingVehiculeError("GHI-999")
        
        with self.assertRaises(IsASubscriber):
            raise IsASubscriber()


if __name__ == '__main__':
    unittest.main()
