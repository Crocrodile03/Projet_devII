import unittest
from datetime import datetime, timedelta
from parking import Parking
from vehicule import Vehicule
from subscriber import Subscriber
from unittest.mock import MagicMock, patch, mock_open
from exception import (MissingVehiculeError, VehiculeError, InvalidTypeError, 
                       SubscriberConflictError, CapacityError, InvalidImmatriculationError)
import json
import os




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

    def test_setters_current_capacity_valid(self):
        """Test le setter de current_capacity avec valeur valide."""
        p = Parking()
        p.current_capacity = [10, 2, 1, 5]
        self.assertEqual(p.current_capacity, [10, 2, 1, 5])

    def test_setters_current_capacity_invalid(self):
        """Test le setter de current_capacity avec valeur invalide."""
        p = Parking()
        with self.assertRaises(ValueError):
            p.current_capacity = []
        with self.assertRaises(ValueError):
            p.current_capacity = "invalid"

    def test_setters_parking_valid(self):
        """Test le setter de parking avec valeur valide."""
        p = Parking()
        mock_v = MagicMock()
        p.parking = [mock_v]
        self.assertEqual(len(p.parking), 1)

    def test_setters_parking_invalid(self):
        """Test le setter de parking avec valeur invalide."""
        p = Parking()
        with self.assertRaises(ValueError):
            p.parking = "invalid"

    def test_setters_timeout_limit_valid(self):
        """Test le setter de timeout_limit avec valeur valide."""
        p = Parking()
        new_limit = timedelta(hours=48)
        p.timeout_limit = new_limit
        self.assertEqual(p.timeout_limit, new_limit)

    def test_setters_timeout_limit_invalid(self):
        """Test le setter de timeout_limit avec valeur invalide."""
        p = Parking()
        with self.assertRaises(ValueError):
            p.timeout_limit = "invalid"

    def test_setters_timeout_subscriber_valid(self):
        """Test le setter de timeout_subscriber avec valeur valide."""
        p = Parking()
        new_timeout = timedelta(days=60)
        p.timeout_subscriber = new_timeout
        self.assertEqual(p.timeout_subscriber, new_timeout)

    def test_setters_timeout_subscriber_invalid(self):
        """Test le setter de timeout_subscriber avec valeur invalide."""
        p = Parking()
        with self.assertRaises(ValueError):
            p.timeout_subscriber = 30

    def test_timeout_empty_parking(self):
        """Test timeout avec parking vide."""
        p = Parking()
        result = p.timeout()
        self.assertFalse(result)

    def test_vehicules_entry_handicape_fallback_visiteur(self):
        """Test entrée handicapé qui se rabat sur visiteur."""
        p = Parking()
        p.current_capacity = [0, 6, 0, 0]  # Places handicapé pleines
        
        with patch("parking.Vehicule") as MockVehicule:
            mock_v = MagicMock()
            mock_v.immatriculation = "HANDI-001"
            mock_v.type_vehicule = "handicapé"
            mock_v.entry_time = datetime.now()
            MockVehicule.return_value = mock_v
            
            v = p.vehicules_entry("HANDI-001", "handicapé")
            # Le véhicule devrait être converti en visiteur
            self.assertEqual(mock_v.type_vehicule, "visiteur")
            self.assertEqual(p.current_capacity[0], 1)

    def test_vehicules_entry_electrique_fallback_visiteur(self):
        """Test entrée électrique qui se rabat sur visiteur."""
        p = Parking()
        p.current_capacity = [0, 0, 4, 0]  # Places électrique pleines
        
        with patch("parking.Vehicule") as MockVehicule:
            mock_v = MagicMock()
            mock_v.immatriculation = "ELEC-001"
            mock_v.type_vehicule = "électrique"
            mock_v.entry_time = datetime.now()
            MockVehicule.return_value = mock_v
            
            v = p.vehicules_entry("ELEC-001", "électrique")
            self.assertEqual(mock_v.type_vehicule, "visiteur")
            self.assertEqual(p.current_capacity[0], 1)

    def test_vehicules_entry_handicape_capacity_full(self):
        """Test entrée handicapé quand tout est plein."""
        p = Parking()
        p.current_capacity = [120, 6, 0, 0]  # Visiteur et handicapé pleins
        
        with patch("parking.Vehicule") as MockVehicule:
            mock_v = MagicMock()
            mock_v.immatriculation = "FULL-001"
            mock_v.type_vehicule = "handicapé"
            MockVehicule.return_value = mock_v
            
            with self.assertRaises(CapacityError):
                p.vehicules_entry("FULL-001", "handicapé")

    def test_vehicules_leave_handicape(self):
        """Test sortie véhicule handicapé."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "HANDI-002"
        mock_v.type_vehicule = "handicapé"
        p.parking.append(mock_v)
        p.current_capacity = [0, 1, 0, 0]
        
        p.vehicules_leave("HANDI-002")
        self.assertEqual(p.current_capacity[1], 0)

    def test_vehicules_leave_electrique(self):
        """Test sortie véhicule électrique."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "ELEC-002"
        mock_v.type_vehicule = "électrique"
        p.parking.append(mock_v)
        p.current_capacity = [0, 0, 1, 0]
        
        p.vehicules_leave("ELEC-002")
        self.assertEqual(p.current_capacity[2], 0)

    def test_calculate_tarif_with_int_duration(self):
        """Test calcul tarif avec durée en int."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "INT-TARIF"
        mock_v.get_duration.return_value = 5
        p.parking.append(mock_v)
        
        fee = p.calculate_tarif("INT-TARIF")
        self.assertEqual(fee, 5)

    def test_calculate_tarif_with_float_duration(self):
        """Test calcul tarif avec durée en float."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.immatriculation = "FLOAT-TARIF"
        mock_v.get_duration.return_value = 3.5
        p.parking.append(mock_v)
        
        fee = p.calculate_tarif("FLOAT-TARIF")
        self.assertEqual(fee, 3.5)

    @patch("parking.os.path.exists", return_value=False)
    def test_load_state_no_file(self, mock_exists):
        """Test load_state quand le fichier n'existe pas."""
        p = Parking()
        p.load_state("non_existent.json")
        self.assertEqual(p.current_capacity, [0, 0, 0, 0])
        self.assertEqual(p.parking, [])

    @patch("builtins.open", new_callable=mock_open, read_data='')
    @patch("parking.os.path.exists", return_value=True)
    def test_load_state_empty_file(self, mock_exists, mock_file):
        """Test load_state avec fichier vide."""
        p = Parking()
        p.load_state("empty.json")
        self.assertEqual(p.current_capacity, [0, 0, 0, 0])

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("parking.os.path.exists", return_value=True)
    def test_load_state_invalid_json(self, mock_exists, mock_file):
        """Test load_state avec JSON invalide."""
        p = Parking()
        p.load_state("invalid.json")
        self.assertEqual(p.current_capacity, [0, 0, 0, 0])
        self.assertEqual(p.parking, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_save_state_success(self, mock_file):
        """Test save_state réussie."""
        p = Parking()
        mock_v = MagicMock()
        mock_v.to_dict.return_value = {"immatriculation": "SAVE-001", "type_vehicule": "visiteur"}
        p.parking = [mock_v]
        p.current_capacity = [1, 0, 0, 0]
        
        p.save_state("test_save.json")
        mock_file.assert_called_once()
    
    def test_vehicules_entry_immatriculation_vide(self):
        """Test entrée véhicule avec immatriculation vide - doit lever une exception."""
        p = Parking()
        with self.assertRaises(InvalidImmatriculationError):
            p.vehicules_entry("", "visiteur")

    def test_vehicules_entry_immatriculation_espaces_uniquement(self):
        """Test entrée véhicule avec immatriculation composée uniquement d'espaces - doit lever une exception."""
        p = Parking()
        with self.assertRaises(InvalidImmatriculationError):
            p.vehicules_entry("   ", "visiteur")

if __name__ == '__main__':
    unittest.main()
