import unittest
from unittest.mock import MagicMock
from datetime import datetime 
from subscriber import Subscriber
from parking import Parking
from exception import (InvalidValueSubscriberError, FullSubscriberCapacityError, 
                       SubscriberConflictError, CapacityError, InvalidImmatriculationError)

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

    def test_subscriber_to_dict(self):
        """Test la conversion d'un abonné en dictionnaire."""
        s = Subscriber("TEST-456", "John", "Doe", "0987654321")
        data = s.to_dict()
        
        self.assertEqual(data["immatriculation"], "TEST-456")
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["phone_number"], "0987654321")
        self.assertEqual(data["type_vehicule"], "abonné")
        self.assertIn("entry_time", data)

    def test_subscriber_from_dict(self):
        """Test la création d'un abonné depuis un dictionnaire."""
        data = {
            "immatriculation": "DICT-789",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "0123456789",
            "entry_time": datetime.now().isoformat(),
            "type_vehicule": "abonné"
        }
        s = Subscriber.from_dict(data)
        
        self.assertEqual(s.immatriculation, "DICT-789")
        self.assertEqual(s.first_name, "Jane")
        self.assertEqual(s.last_name, "Smith")
        self.assertEqual(s.phone_number, "0123456789")
        self.assertEqual(s.type_vehicule, "abonné")

    def test_subscribe_success(self):
        """Test l'ajout réussi d'un abonné au parking."""
        p = Parking()
        s = Subscriber("SUB-001", "Alice", "Wonder", "0111222333")
        
        s.subscribe(p)
        
        self.assertIn(s, p.parking)
        self.assertEqual(p.current_capacity[3], 1)

    def test_subscribe_when_full(self):
        """Test l'ajout d'un abonné quand la capacité est atteinte."""
        p = Parking()
        p.current_capacity = [0, 0, 0, 12]  # Capacité abonnés pleine
        s = Subscriber("SUB-FULL", "Bob", "Builder", "0222333444")
        
        with self.assertRaises(FullSubscriberCapacityError):
            s.subscribe(p)

    def test_subscribe_conflict_already_subscriber(self):
        """Test conflit quand le véhicule est déjà abonné."""
        p = Parking()
        s1 = Subscriber("CONFLICT-001", "Charlie", "Brown", "0333444555")
        s1.subscribe(p)
        
        s2 = Subscriber("CONFLICT-001", "Charlie", "Brown", "0333444555")
        with self.assertRaises(SubscriberConflictError):
            s2.subscribe(p)

    def test_subscribe_conflict_other_type(self):
        """Test conflit quand le véhicule est déjà présent avec un autre type."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "CONFLICT-002"
        mock_v.type_vehicule = "visiteur"
        p.parking.append(mock_v)
        
        s = Subscriber("CONFLICT-002", "David", "Test", "0444555666")
        with self.assertRaises(CapacityError):
            s.subscribe(p)

    def test_calculate_subscribe_fee(self):
        """Test le calcul du tarif d'abonnement."""
        s = Subscriber("FEE-001", "Emma", "Stone", "0555666777")
        fee = s.calculate_subscribe_fee()
        
        self.assertEqual(fee, 60)

    def test_subscriber_setters_valid_values(self):
        """Test que les setters acceptent des valeurs valides."""
        s = Subscriber("SET-001", "Frank", "Ocean", "0666777888")
        
        s.first_name = "Francis"
        s.last_name = "Oceanic"
        s.phone_number = "0999888777"
        s.tarif_abonnement = 75
        
        self.assertEqual(s.first_name, "Francis")
        self.assertEqual(s.last_name, "Oceanic")
        self.assertEqual(s.phone_number, "0999888777")
        self.assertEqual(s.tarif_abonnement, 75)


    def test_subscriber_immatriculation_vide(self):
        """Test création abonné avec immatriculation vide - doit lever une exception."""
        with self.assertRaises(InvalidImmatriculationError):
            s = Subscriber("", "Test", "User", "0123456789")

    def test_subscriber_immatriculation_espaces_uniquement(self):
        """Test création abonné avec immatriculation composée uniquement d'espaces - doit lever une exception."""
        with self.assertRaises(InvalidImmatriculationError):
            s = Subscriber("   ", "Test", "User", "0123456789")

    def test_subscriber_immatriculation_chiffres_uniquement(self):
        """Test création abonné avec immatriculation en chiffres uniquement."""
        s = Subscriber("123456789", "Jean", "Dupont", "0111222333")
        self.assertEqual(s.immatriculation, "123456789")
        self.assertEqual(s.type_vehicule, "abonné")

    def test_subscriber_immatriculation_lettres_uniquement(self):
        """Test création abonné avec immatriculation en lettres uniquement."""
        s = Subscriber("ABCDEFGH", "Marie", "Martin", "0222333444")
        self.assertEqual(s.immatriculation, "ABCDEFGH")
        self.assertEqual(s.type_vehicule, "abonné")

    def test_subscriber_immatriculation_caracteres_speciaux(self):
        """Test création abonné avec caractères spéciaux dans immatriculation."""
        s = Subscriber("AB-123@#$", "Pierre", "Durand", "0333444555")
        self.assertEqual(s.immatriculation, "AB-123@#$")
        self.assertEqual(s.type_vehicule, "abonné")

    def test_subscriber_immatriculation_espaces(self):
        """Test création abonné avec espaces dans immatriculation."""
        s = Subscriber("AB 12 CD", "Sophie", "Bernard", "0444555666")
        self.assertEqual(s.immatriculation, "AB 12 CD")
        self.assertEqual(s.type_vehicule, "abonné")

    def test_subscriber_immatriculation_tres_longue(self):
        """Test création abonné avec immatriculation très longue."""
        immat_longue = "X" * 100
        s = Subscriber(immat_longue, "Lucas", "Petit", "0555666777")
        self.assertEqual(s.immatriculation, immat_longue)

    def test_subscribe_immatriculation_deja_presente_visiteur(self):
        """Test abonnement avec immatriculation déjà présente comme visiteur."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "CONFLICT-VISIT"
        mock_v.type_vehicule = "visiteur"
        p.parking.append(mock_v)
        
        s = Subscriber("CONFLICT-VISIT", "Test", "Test", "0123456789")
        with self.assertRaises(CapacityError):
            s.subscribe(p)

    def test_subscribe_immatriculation_deja_presente_handicape(self):
        """Test abonnement avec immatriculation déjà présente comme handicapé."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "CONFLICT-HANDI"
        mock_v.type_vehicule = "handicapé"
        p.parking.append(mock_v)
        
        s = Subscriber("CONFLICT-HANDI", "Test", "Test", "0123456789")
        with self.assertRaises(CapacityError):
            s.subscribe(p)

    def test_subscribe_immatriculation_deja_presente_electrique(self):
        """Test abonnement avec immatriculation déjà présente comme électrique."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "CONFLICT-ELEC"
        mock_v.type_vehicule = "électrique"
        p.parking.append(mock_v)
        
        s = Subscriber("CONFLICT-ELEC", "Test", "Test", "0123456789")
        with self.assertRaises(CapacityError):
            s.subscribe(p)

    def test_subscribe_immatriculation_doublon_abonne(self):
        """Test abonnement avec immatriculation d'un abonné déjà existant."""
        p = Parking()
        s1 = Subscriber("DOUBLE-SUB", "First", "User", "0111111111")
        s1.subscribe(p)
        
        s2 = Subscriber("DOUBLE-SUB", "Second", "User", "0222222222")
        with self.assertRaises(SubscriberConflictError):
            s2.subscribe(p)

    def test_subscribe_immatriculation_chiffres(self):
        """Test abonnement réussi avec immatriculation en chiffres."""
        p = Parking()
        s = Subscriber("999888777", "Test", "Numbers", "0123456789")
        s.subscribe(p)
        
        self.assertIn(s, p.parking)
        self.assertEqual(p.current_capacity[3], 1)

    def test_subscribe_immatriculation_caracteres_speciaux_success(self):
        """Test abonnement réussi avec caractères spéciaux."""
        p = Parking()
        s = Subscriber("XX-99@!", "Special", "Chars", "0987654321")
        s.subscribe(p)
        
        self.assertIn(s, p.parking)
        self.assertEqual(p.current_capacity[3], 1)

if __name__ == "__main__":
    unittest.main()
