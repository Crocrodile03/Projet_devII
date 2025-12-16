import unittest
from datetime import datetime, timedelta
from parking import Parking
from unittest.mock import MagicMock, patch
from exception import MissingVehiculeError, VehiculeError, InvalidTypeError, SubscriberConflictError, CapacityError




class TestParking(unittest.TestCase):
    def test_init_default_values(self):
        p = Parking()
        self.assertEqual(p.max_capacity, (120, 6, 4, 12))
        self.assertEqual(p.current_capacity, [0, 0, 0, 0])
        self.assertEqual(p.parking, [])
        self.assertEqual(p.tarif, 1)
        self.assertEqual(p.maxtarif, 10)
        self.assertEqual(p.timeout_limit, timedelta(hours=24))
        self.assertEqual(p.timeout_subscriber, timedelta(hours=24 * 30))


    def test_alert(self):
        p = Parking()
        self.assertFalse(p.alert("visiteur"))
        p.current_capacity = [120, 6, 4, 12]
        self.assertTrue(p.alert("visiteur"))
        self.assertTrue(p.alert("handicapé"))
        self.assertTrue(p.alert("électrique"))
        self.assertTrue(p.alert("abonné"))

    def test_find_vehicule_by_type(self):
        mock_v1 = MagicMock(type_vehicule="visiteur")
        mock_v2 = MagicMock(type_vehicule="électrique")
        mock_v3 = MagicMock(type_vehicule="visiteur")
        p = Parking()
        p.parking = [mock_v1, mock_v2, mock_v3]
        res = p.find_vehicule_by_type("visiteur", p)
        self.assertEqual(len(res), 2)
        self.assertIn(mock_v1, res)
        self.assertIn(mock_v3, res)

    @patch("parking.Vehicule")
    def test_vehicules_entry(self, MockVehicule):
        p = Parking()

        # Premier véhicule (entrée normale)
        mock_v1 = MagicMock()
        mock_v1.immatriculation = "AA-123"
        mock_v1.type_vehicule = "visiteur"
        mock_v1.entry_time = datetime.now() - timedelta(hours=1)
        mock_v1.get_duration.return_value = timedelta(hours=1)

        MockVehicule.return_value = mock_v1
        new_v = p.vehicules_entry("AA-123", "visiteur")
        self.assertIn(mock_v1, p.parking)
        self.assertEqual(p.current_capacity[0], 1)
        self.assertEqual(new_v, mock_v1)

        # Cas erreur : véhicule déjà présent
        with self.assertRaises(VehiculeError):
            MockVehicule.return_value = mock_v1
            p.vehicules_entry("AA-123", "visiteur")

        # Cas erreur : type invalide avec immatriculation différente
        mock_v2 = MagicMock()
        mock_v2.immatriculation = "BB-456"
        mock_v2.type_vehicule = "inconnu"
        mock_v2.entry_time = datetime.now() - timedelta(hours=1)
        mock_v2.get_duration.return_value = timedelta(hours=1)

        MockVehicule.return_value = mock_v2
        with self.assertRaises(InvalidTypeError):
            p.vehicules_entry("BB-456", "inconnu")

        # Cas erreur : abonné déjà enregistré
        mock_v3 = MagicMock()
        mock_v3.immatriculation = "CC-789"
        mock_v3.type_vehicule = "abonné"
        mock_v3.entry_time = datetime.now() - timedelta(hours=1)
        mock_v3.get_duration.return_value = timedelta(hours=1)

        p.parking.append(mock_v3)  # déjà présent dans le parking
        MockVehicule.return_value = mock_v3
        with self.assertRaises(SubscriberConflictError):
            p.vehicules_entry("CC-789", "abonné")

    def test_vehicules_leave(self):
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "AA-123"
        mock_v.type_vehicule = "visiteur"
        p.parking.append(mock_v)
        p.current_capacity = [1,0,0,0]
        res = p.vehicules_leave("AA-123")
        self.assertTrue(res)
        self.assertEqual(p.current_capacity[0], 0)
        self.assertNotIn(mock_v, p.parking)
        # vehicle not present
        with self.assertRaises(MissingVehiculeError):
            p.vehicules_leave("NOPE-000")

    def test_calculate_tarif(self):
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "AA"
        mock_v.get_duration.return_value = timedelta(hours=3)
        p.parking.append(mock_v)
        fee = p.calculate_tarif("AA")
        self.assertEqual(fee, 3)  # tarif = 1€/h
        mock_v.get_duration.return_value = timedelta(hours=20)
        fee = p.calculate_tarif("AA")
        self.assertEqual(fee, p.maxtarif)
        with self.assertRaises(MissingVehiculeError):
            p.calculate_tarif("NOPE")

    def test_timeout(self):
        p = Parking()
        mock_v = MagicMock()
        mock_v.entry_time = datetime.now() - timedelta(hours=30)
        mock_v.type_vehicule = "visiteur"
        p.parking.append(mock_v)
        self.assertTrue(p.timeout())
        # abonné
        mock_v2 = MagicMock()
        mock_v2.entry_time = datetime.now() - timedelta(days=31)
        mock_v2.type_vehicule = "abonné"
        p.parking.append(mock_v2)
        self.assertTrue(p.timeout())

    @patch("parking.canvas.Canvas")
    @patch("parking.os.makedirs")
    @patch("parking.os.path.exists", return_value=False)
    def test_generer_paiement(self, mock_exists, mock_makedirs, MockCanvas):
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "AA-123"
        mock_v.type_vehicule = "visiteur"
        mock_v.get_duration.return_value = timedelta(hours=2)
        file_path = p.generer_paiement("AA-123", [mock_v], 4.0)
        self.assertIn("paiement_AA-123", file_path)

if __name__ == '__main__':
    unittest.main()
