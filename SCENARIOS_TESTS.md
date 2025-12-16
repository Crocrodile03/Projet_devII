# Scénarios de Tests - Système de Gestion de Parking

## 📋 Vue d'ensemble
Ce document présente tous les scénarios de tests unitaires du système de gestion de parking, organisés par fonctionnalité pour faciliter la compréhension

---

## 1. Tests de la Classe Vehicule

### Scénario 1.1 : Initialisation d'un véhicule
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Valeurs par défaut | immatriculation="TEST123" | type_vehicule="visiteur", entry_time défini | `test_init_default_values` |
| Immatriculation | immatriculation="TEST123" | immatriculation stockée correctement | `test_vehicule_immatriculation` |
| Type de véhicule | type_vehicule="électrique" | type assigné correctement | `test_vehicule_type` |

### Scénario 1.2 : Calcul de la durée de stationnement
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Durée avec minutes (arrondi) | Stationnement de 2h30 | Durée = 3 heures (arrondi supérieur) | `test_get_duration` |
| Durée exacte en heures | Stationnement de 2h00 | Durée = 2 heures | `test_get_duration_exact_hours` |

### Scénario 1.3 : Représentation textuelle
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Méthode __str__ | Véhicule "ABC-123" type "visiteur" | Chaîne contenant immatriculation et type | `test_str_` |
| Méthode __repr__ | Véhicule "ABC-123" | Chaîne contenant "Vehicule" et l'immatriculation | `test_repr_` |

---

## 2. Tests de la Classe Subscriber (Abonné)

### Scénario 2.1 : Création d'un abonné
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Initialisation complète | immat="Test-123", prénom="Antoine", nom="Mont", tél="0123040506" | Toutes les données stockées, type="abonné" | `test_init_subscriber` |
| Type de véhicule | Abonné créé | type_vehicule="abonné" automatique | `test_subscriber_vehicule` |
| Informations personnelles | Données abonné | first_name, last_name, phone_number corrects | `test_subscriber_info` |

### Scénario 2.2 : Validation des données d'abonné
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Prénom invalide (vide) | first_name=" " | Exception InvalidValueSubscriberError | `test_subscriber_invalid_info` |
| Nom invalide (vide) | last_name=" " | Exception InvalidValueSubscriberError | `test_subscriber_invalid_info` |
| Téléphone invalide (vide) | phone_number=" " | Exception InvalidValueSubscriberError | `test_subscriber_invalid_info` |

### Scénario 2.3 : Tarification d'abonnement
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Tarif par défaut | Abonné créé | tarif_abonnement = 60€ | `test_tarif_subscriber` |
| Tarif négatif | tarif_abonnement = -10 | Exception InvalidValueSubscriberError | `test_tarif_abonnement_invalid_value` |

---

## 3. Tests de la Classe Parking

### Scénario 3.1 : Initialisation du parking
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Valeurs par défaut | Parking() | max_capacity=(120,6,4,12), tarif=1€, maxtarif=10€ | `test_init_default_values` |
| Capacités initiales | Parking() | current_capacity=[0,0,0,0], parking=[] | `test_init_default_values` |
| Limites de temps | Parking() | timeout_limit=24h, timeout_subscriber=30j | `test_init_default_values` |

### Scénario 3.2 : Système d'alerte de capacité
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Parking non plein | current_capacity=[0,0,0,0] | alert() = False pour tous types | `test_alert` |
| Parking plein | current_capacity=[120,6,4,12] | alert() = True pour tous types | `test_alert` |

### Scénario 3.3 : Recherche de véhicules
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Recherche par type | 3 véhicules dont 2 "visiteur" | Retourne les 2 véhicules visiteurs | `test_find_vehicule_by_type` |

### Scénario 3.4 : Entrée de véhicules
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Entrée normale | immat="AA-123", type="visiteur" | Véhicule ajouté, capacity incrémentée | `test_vehicules_entry` |
| Véhicule déjà présent | immat existante "AA-123" | Exception VehiculeError | `test_vehicules_entry` |
| Type invalide | type="inconnu" | Exception InvalidTypeError | `test_vehicules_entry` |
| Abonné en conflit | Abonné déjà dans le parking | Exception SubscriberConflictError | `test_vehicules_entry` |

### Scénario 3.5 : Sortie de véhicules
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Sortie normale | immat="AA-123" présente | Véhicule retiré, capacity décrémentée | `test_vehicules_leave` |
| Véhicule absent | immat="NOPE-000" inexistante | Exception MissingVehiculeError | `test_vehicules_leave` |

### Scénario 3.6 : Calcul des tarifs
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Tarif normal | Durée=3h, tarif=1€/h | Montant = 3€ | `test_calculate_tarif` |
| Tarif maximum | Durée=20h, maxtarif=10€ | Montant = 10€ (plafonné) | `test_calculate_tarif` |
| Véhicule inexistant | immat="NOPE" | Exception MissingVehiculeError | `test_calculate_tarif` |

### Scénario 3.7 : Détection de dépassement de temps (timeout)
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Visiteur dépassé | Entrée il y a 30h (>24h) | timeout() = True | `test_timeout` |
| Abonné dépassé | Entrée il y a 31j (>30j) | timeout() = True | `test_timeout` |

### Scénario 3.8 : Génération de reçu de paiement
| **Aspect testé** | **Données d'entrée** | **Résultat attendu** | **Méthode de test** |
|------------------|---------------------|---------------------|-------------------|
| Génération PDF | immat="AA-123", montant=4€ | Fichier PDF créé dans dossier paiements | `test_generer_paiement` |

---

## 📊 Résumé des Tests par Catégorie

| **Classe** | **Nombre de scénarios** | **Nombre de tests** | **Couverture** |
|------------|-------------------------|---------------------|----------------|
| Vehicule | 3 scénarios | 7 tests | Initialisation, durée, affichage |
| Subscriber | 3 scénarios | 7 tests | Création, validation, tarification |
| Parking | 8 scénarios | 15+ tests | Gestion complète du parking |
| **TOTAL** | **14 scénarios** | **29+ tests** | **Système complet** |

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

---

## 📝 Notes d'exécution

### Comment exécuter les tests
```bash

# Tests par classe
python -m unittest test_vehicule
python -m unittest test_subscriber  
python -m unittest test_parking

```

### Outils utilisés
- Framework : `unittest`
- Mocking : `unittest.mock.MagicMock`, `patch`
- Assertions : `assertEqual`, `assertTrue`, `assertRaises`, `assertIn`, etc.

---

## ✅ Légende des colonnes

- **Aspect testé** : Fonctionnalité ou comportement vérifié
- **Données d'entrée** : Paramètres et conditions initiales du test
- **Résultat attendu** : Comportement ou valeur espérée après exécution
- **Méthode de test** : Nom de la méthode de test unitaire correspondante

---
