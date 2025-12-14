# Scénarios de Tests - Système de Gestion de Parking

## 📋 Vue d'ensemble
Ce document présente tous les scénarios de tests unitaires du système de gestion de parking, organisés par fonctionnalité pour faciliter la compréhension et la validation.

---

## 1. Tests de la Classe Vehicule

### Scénario 1.1 : Initialisation d'un véhicule
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Valeurs par défaut | immatriculation="TEST123" | type_vehicule="visiteur", entry_time défini | `test_init_default_values` |
| Immatriculation | immatriculation="TEST123" | immatriculation stockée correctement | `test_vehicule_immatriculation` |
| Type de véhicule | type_vehicule="électrique" | type assigné correctement | `test_vehicule_type` |

### Scénario 1.2 : Validation d'immatriculation véhicule
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Immatriculation vide | immat="" | Véhicule créé avec immat vide | `test_vehicule_immatriculation_vide` |
| Chiffres uniquement | immat="123456" | Véhicule créé correctement | `test_vehicule_immatriculation_chiffres_uniquement` |
| Lettres uniquement | immat="ABCDEF" | Véhicule créé correctement | `test_vehicule_immatriculation_lettres_uniquement` |
| Caractères spéciaux | immat="AB-123@#" | Véhicule créé correctement | `test_vehicule_immatriculation_caracteres_speciaux` |
| Avec espaces | immat="AB 12 CD" | Véhicule créé correctement | `test_vehicule_immatriculation_espaces` |
| Caractères unicode | immat="ÉÀÇ-123" | Véhicule créé correctement | `test_vehicule_immatriculation_unicode` |
| Très longue | immat=100 caractères | Véhicule créé correctement | `test_vehicule_immatriculation_tres_longue` |
| Casse mixte | immat="AbC-123-xYz" | Véhicule créé (sensible casse) | `test_vehicule_immatriculation_casse_mixte` |

### Scénario 1.3 : Calcul de la durée de stationnement
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Durée avec minutes (arrondi) | Stationnement de 2h30 | Durée = 3 heures (arrondi supérieur) | `test_get_duration` |
| Durée exacte en heures | Stationnement de 2h00 | Durée = 2 heures | `test_get_duration_exact_hours` |
| Type de retour | Durée quelconque | Renvoie un entier | `test_get_duration_returns_integer` |

### Scénario 1.4 : Sérialisation et setters
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Conversion en dict | Véhicule "DICT-001" | Dictionnaire avec toutes données | `test_vehicule_to_dict` |
| Création depuis dict | Dictionnaire valide | Véhicule recréé correctement | `test_vehicule_from_dict` |
| Modification immatriculation | Nouvelle immatriculation | Immatriculation mise à jour | `test_vehicule_setter_immatriculation` |
| Modification type | Nouveau type | Type mis à jour | `test_vehicule_setter_type` |

---

## 2. Tests de la Classe Subscriber (Abonné)

### Scénario 2.1 : Création d'un abonné
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Initialisation complète | immat="Test-123", prénom="Antoine", nom="Mont", tél="0123040506" | Toutes les données stockées, type="abonné" | `test_init_subscriber` |
| Type de véhicule | Abonné créé | type_vehicule="abonné" automatique | `test_subscriber_vehicule` |
| Informations personnelles | Données abonné | first_name, last_name, phone_number corrects | `test_subscriber_info` |

### Scénario 2.2 : Validation d'immatriculation abonné
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Immatriculation vide | immat="" | Abonné créé avec immat vide | `test_subscriber_immatriculation_vide` |
| Chiffres uniquement | immat="123456789" | Abonné créé correctement | `test_subscriber_immatriculation_chiffres_uniquement` |
| Lettres uniquement | immat="ABCDEFGH" | Abonné créé correctement | `test_subscriber_immatriculation_lettres_uniquement` |
| Caractères spéciaux | immat="AB-123@#$" | Abonné créé correctement | `test_subscriber_immatriculation_caracteres_speciaux` |
| Avec espaces | immat="AB 12 CD" | Abonné créé correctement | `test_subscriber_immatriculation_espaces` |
| Très longue | immat=100 caractères | Abonné créé correctement | `test_subscriber_immatriculation_tres_longue` |

### Scénario 2.3 : Validation des données personnelles
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Prénom invalide (vide) | first_name=" " | Exception InvalidValueSubscriberError | `test_subscriber_invalid_info` |
| Nom invalide (vide) | last_name=" " | Exception InvalidValueSubscriberError | `test_subscriber_invalid_info` |
| Téléphone invalide (vide) | phone_number=" " | Exception InvalidValueSubscriberError | `test_subscriber_invalid_info` |
| Valeurs valides | Données correctes | Setters acceptent les valeurs | `test_subscriber_setters_valid_values` |

### Scénario 2.4 : Tarification d'abonnement
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Tarif par défaut | Abonné créé | tarif_abonnement = 60€ | `test_tarif_subscriber` |
| Tarif négatif | tarif_abonnement = -10 | Exception InvalidValueSubscriberError | `test_tarif_abonnement_invalid_value` |
| Calcul tarif | Abonné existant | Renvoie 60€ | `test_calculate_subscribe_fee` |

### Scénario 2.5 : Abonnement au parking
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Abonnement réussi | Parking disponible | Abonné ajouté, capacité +1 | `test_subscribe_success` |
| Capacité abonnés pleine | current_capacity[3]=12 | Exception FullSubscriberCapacityError | `test_subscribe_when_full` |
| Conflit abonné existant | Immat déjà abonnée | Exception SubscriberConflictError | `test_subscribe_conflict_already_subscriber` |
| Conflit visiteur | Immat déjà en visiteur | Exception CapacityError | `test_subscribe_immatriculation_deja_presente_visiteur` |
| Conflit handicapé | Immat déjà en handicapé | Exception CapacityError | `test_subscribe_immatriculation_deja_presente_handicape` |
| Conflit électrique | Immat déjà en électrique | Exception CapacityError | `test_subscribe_immatriculation_deja_presente_electrique` |
| Doublon abonné | Même immat 2 abonnés | Exception SubscriberConflictError | `test_subscribe_immatriculation_doublon_abonne` |
| Avec chiffres | immat="999888777" | Abonnement réussi | `test_subscribe_immatriculation_chiffres` |
| Avec caractères spéciaux | immat="XX-99@!" | Abonnement réussi | `test_subscribe_immatriculation_caracteres_speciaux_success` |

### Scénario 2.6 : Sérialisation
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Conversion en dict | Abonné complet | Dictionnaire avec toutes données | `test_subscriber_to_dict` |
| Création depuis dict | Dictionnaire valide | Abonné recréé correctement | `test_subscriber_from_dict` |

---

## 3. Tests de la Classe Parking

### Scénario 3.1 : Initialisation du parking
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Valeurs par défaut | Parking() | max_capacity=(120,6,4,12), tarif=1€, maxtarif=10€ | `test_init_default_values` |
| Capacités initiales | Parking() | current_capacity=[0,0,0,0], parking=[] | `test_init_default_values` |
| Limites de temps | Parking() | timeout_limit=24h, timeout_subscriber=30j | `test_init_default_values` |

### Scénario 3.2 : Validation des setters
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| current_capacity valide | Liste [10,2,1,5] | Accepté et stocké | `test_setters_current_capacity_valid` |
| current_capacity invalide | Liste vide ou string | Exception ValueError | `test_setters_current_capacity_invalid` |
| parking valide | Liste de véhicules | Accepté et stocké | `test_setters_parking_valid` |
| parking invalide | String au lieu de liste | Exception ValueError | `test_setters_parking_invalid` |
| timeout_limit valide | timedelta(hours=48) | Accepté et stocké | `test_setters_timeout_limit_valid` |
| timeout_limit invalide | String au lieu de timedelta | Exception ValueError | `test_setters_timeout_limit_invalid` |
| timeout_subscriber valide | timedelta(days=60) | Accepté et stocké | `test_setters_timeout_subscriber_valid` |
| timeout_subscriber invalide | Int au lieu de timedelta | Exception ValueError | `test_setters_timeout_subscriber_invalid` |

### Scénario 3.3 : Système d'alerte de capacité
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Parking non plein | current_capacity=[0,0,0,0] | alert() = False pour tous types | `test_alert` |
| Parking plein | current_capacity=[120,6,4,12] | alert() = True pour tous types | `test_alert` |

### Scénario 3.4 : Recherche de véhicules
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Recherche par type | 3 véhicules dont 2 "visiteur" | Retourne les 2 véhicules visiteurs | `test_find_vehicule_by_type` |

### Scénario 3.5 : Entrée de véhicules - validation standard
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Entrée normale | immat="AA-123", type="visiteur" | Véhicule ajouté, capacity incrémentée | `test_vehicules_entry` |
| Véhicule déjà présent | immat existante "AA-123" | Exception VehiculeError | `test_vehicules_entry` |
| Type invalide | type="inconnu" | Exception InvalidTypeError | `test_vehicules_entry` |
| Abonné en conflit | Abonné déjà dans le parking | Exception SubscriberConflictError | `test_vehicules_entry` |
| Handicapé vers visiteur | Places handicapé pleines | Converti en visiteur | `test_vehicules_entry_handicape_fallback_visiteur` |
| Électrique vers visiteur | Places électrique pleines | Converti en visiteur | `test_vehicules_entry_electrique_fallback_visiteur` |
| Handicapé parking plein | Handicapé + visiteur pleins | Exception CapacityError | `test_vehicules_entry_handicape_capacity_full` |

### Scénario 3.6 : Entrée de véhicules - validation immatriculation
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Immatriculation vide | immat="" | Véhicule ajouté au parking | `test_vehicules_entry_immatriculation_vide` |
| Chiffres uniquement | immat="123456" | Véhicule ajouté, capacity +1 | `test_vehicules_entry_immatriculation_chiffres_uniquement` |
| Lettres uniquement | immat="ABCDEF" | Véhicule ajouté, capacity +1 | `test_vehicules_entry_immatriculation_lettres_uniquement` |
| Caractères spéciaux | immat="AB-123@!" | Véhicule ajouté, capacity +1 | `test_vehicules_entry_immatriculation_caracteres_speciaux` |
| Avec espaces | immat="AB 123 CD" | Véhicule ajouté, capacity +1 | `test_vehicules_entry_immatriculation_espaces` |
| Très longue | immat=100 caractères | Véhicule ajouté au parking | `test_vehicules_entry_immatriculation_tres_longue` |

### Scénario 3.7 : Sortie de véhicules - validation standard
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Sortie normale visiteur | immat="AA-123" présente | Véhicule retiré, capacity décrémentée | `test_vehicules_leave` |
| Sortie handicapé | immat handicapé présente | Véhicule retiré, capacity[1] -1 | `test_vehicules_leave_handicape` |
| Sortie électrique | immat électrique présente | Véhicule retiré, capacity[2] -1 | `test_vehicules_leave_electrique` |
| Véhicule absent | immat="NOPE-000" inexistante | Exception MissingVehiculeError | `test_vehicules_leave` |

### Scénario 3.8 : Sortie de véhicules - validation immatriculation
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Immatriculation vide | immat="" | Exception MissingVehiculeError | `test_vehicules_leave_immatriculation_vide` |
| Immatriculation inexistante | immat non présente | Exception MissingVehiculeError | `test_vehicules_leave_immatriculation_inexistante` |
| Chiffres uniquement | immat="999888" | Sortie réussie | `test_vehicules_leave_immatriculation_chiffres` |
| Lettres uniquement | immat="ZZYYXX" | Sortie réussie | `test_vehicules_leave_immatriculation_lettres` |
| Caractères spéciaux | immat="XX-99@#" | Sortie réussie | `test_vehicules_leave_immatriculation_caracteres_speciaux` |
| Avec espaces | immat="YY 88 ZZ" | Sortie réussie | `test_vehicules_leave_immatriculation_espaces` |
| Sensibilité casse | "ABC-123" vs "abc-123" | Exception si casse différente | `test_vehicules_leave_casse_sensible` |

### Scénario 3.9 : Calcul des tarifs
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Tarif normal | Durée=3h, tarif=1€/h | Montant = 3€ | `test_calculate_tarif` |
| Tarif maximum | Durée=20h, maxtarif=10€ | Montant = 10€ (plafonné) | `test_calculate_tarif` |
| Durée en int | Durée=5 (entier) | Montant = 5€ | `test_calculate_tarif_with_int_duration` |
| Durée en float | Durée=3.5 (décimal) | Montant = 3.5€ | `test_calculate_tarif_with_float_duration` |
| Véhicule inexistant | immat="NOPE" | Exception MissingVehiculeError | `test_calculate_tarif` |

### Scénario 3.10 : Détection de dépassement de temps (timeout)
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Parking vide | Aucun véhicule | timeout() = False | `test_timeout_empty_parking` |
| Visiteur dépassé | Entrée il y a 30h (>24h) | timeout() = True | `test_timeout` |
| Abonné dépassé | Entrée il y a 31j (>30j) | timeout() = True | `test_timeout` |

### Scénario 3.11 : Sauvegarde et chargement d'état
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Sauvegarde réussie | Parking avec véhicules | Fichier JSON créé | `test_save_state_success` |
| Chargement fichier inexistant | Fichier absent | Parking vide initialisé | `test_load_state_no_file` |
| Chargement fichier vide | Fichier vide | Parking vide initialisé | `test_load_state_empty_file` |
| Chargement JSON invalide | JSON corrompu | Parking vide, capacité [0,0,0,0] | `test_load_state_invalid_json` |

### Scénario 3.12 : Génération de reçu de paiement
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Génération PDF | immat="AA-123", montant=4€ | Fichier PDF créé dans dossier paiements | `test_generer_paiement` |

---

## 4. Tests des Exceptions

### Scénario 4.1 : Exceptions de base
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| MyException init | Message "Test message" | Exception avec message stocké | `test_my_exception_init` |
| MyException __str__ | Exception créée | Renvoie le message | `test_my_exception_init` |
| InvalidValueError | Aucun paramètre | Message "Type non valide" | `test_invalid_value_error` |
| InvalidTypeError | Aucun paramètre | Message "Type non valide" | `test_invalid_type_error` |

### Scénario 4.2 : Exceptions avec paramètres
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| CapacityError | type="visiteur" | Message contient "visiteur" | `test_capacity_error` |
| MissingVehiculeError | immat="ABC-123" | Message contient "ABC-123" | `test_missing_vehicule_error` |
| SubscriberConflictError | immat="XYZ-789" | Message contient "déjà enregistré" | `test_subscriber_conflict_error` |
| VehiculeError | immat="DEF-456", type="visiteur" | Message contient immat et type | `test_vehicule_error` |
| InvalidValueSubscriberError | champ="prénom", valeur="" | Message contient "prénom" | `test_invalid_value_subscriber_error` |

### Scénario 4.3 : Exceptions spécifiques
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| CapacityFullError | Aucun | Message "Le parking est plein" | `test_capacity_full_error` |
| FullSubscriberCapacityError | Aucun | Message contient "abonné" et "capacité" | `test_full_subscriber_capacity_error` |
| FailToLoad | Aucun | Message "Erreur lors de la sauvegarde" | `test_fail_to_load` |
| IsASubscriber | Aucun | Message contient "abonné" et "supprimer" | `test_is_a_subscriber` |

### Scénario 4.4 : Héritage et utilisation
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Héritage MyException | Toutes exceptions | Toutes héritent de MyException | `test_exception_inheritance` |
| Lever et attraper | raise Exception | Exception levée et attrapée | `test_exception_can_be_raised` |

---

## 📊 Résumé des Tests par Catégorie

| **Classe** | **Nombre de scénarios** | **Nombre de tests** | **Couverture** |
|------------|-------------------------|---------------------|----------------|
| Vehicule | 4 scénarios | 18 tests | Initialisation, validation, durée, sérialisation |
| Subscriber | 6 scénarios | 26 tests | Création, validation, abonnement, sérialisation |
| Parking | 12 scénarios | 41 tests | Gestion complète avec validation immatriculation |
| Exception | 4 scénarios | 14 tests | Toutes les exceptions personnalisées |
| **TOTAL** | **26 scénarios** | **99 tests** | **Couverture 92%** |

---

## 🎯 Types d'exceptions testées

| **Exception** | **Situation** | **Tests concernés** |
|--------------|---------------|-------------------|
| `VehiculeError` | Véhicule déjà présent | Entrée de véhicule |
| `InvalidTypeError` | Type de véhicule inconnu | Entrée de véhicule |
| `SubscriberConflictError` | Abonné en conflit | Entrée d'abonné |
| `MissingVehiculeError` | Véhicule introuvable | Sortie, calcul tarif |
| `InvalidValueSubscriberError` | Données abonné invalides | Validation abonné |
| `CapacityError` | Parking plein | Gestion capacité |
| `FullSubscriberCapacityError` | Capacité abonnés atteinte | Abonnement |
| `CapacityFullError` | Parking complètement plein | Gestion globale |
| `FailToLoad` | Erreur sauvegarde | Persistance données |
| `IsASubscriber` | Suppression abonné interdite | Gestion abonnés |

---

## 📝 Notes d'exécution

### Comment exécuter les tests
```bash
# Tous les tests avec couverture
python -m pytest --cov=. --cov-report=html --cov-config=.coveragerc

# Tests par classe
python -m unittest test_vehicule
python -m unittest test_subscriber  
python -m unittest test_parking
python -m unittest test_exception

# Test spécifique
python -m unittest test_parking.TestParking.test_vehicules_entry_immatriculation_vide
```

### Outils utilisés
- Framework : `unittest` + `pytest`
- Couverture : `pytest-cov`
- Mocking : `unittest.mock.MagicMock`, `patch`, `mock_open`
- Assertions : `assertEqual`, `assertTrue`, `assertRaises`, `assertIn`, etc.

### Résultats de couverture
- **exception.py** : 100% ✅
- **subscriber.py** : 100% ✅
- **vehicule.py** : 90% ✅
- **parking.py** : 88% ✅
- **TOTAL** : 92% ✅ (objectif 85% dépassé)

---

## ✅ Légende des colonnes

- **Aspect testé** : Fonctionnalité ou comportement vérifié
- **Données d'entrée** : Paramètres et conditions initiales du test
- **Résultat attendu** : Comportement ou valeur espérée après exécution
- **Méthode de test** : Nom de la méthode de test unitaire correspondante

---

*Document mis à jour avec 99 tests unitaires couvrant 26 scénarios*
