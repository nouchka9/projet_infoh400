# 📖 Guide d'utilisation complet - HL7 Messenger v1.0

## 🏥 Présentation du système

**HL7 Messenger** est une solution complète de messagerie hospitalière développée pour faciliter la communication standardisée entre les départements hospitaliers. Cette application production-ready implémente le standard HL7 v2.5 avec le protocole de transport MLLP pour assurer des échanges sécurisés et fiables.

### 🎯 **Objectifs du système**
- **Standardisation** : Communication HL7 v2.5 conforme aux standards internationaux
- **Interopérabilité** : Échanges fluides entre départements hospitaliers
- **Fiabilité** : Architecture robuste avec gestion d'erreurs complète
- **Simplicité** : Interface intuitive pour utilisateurs non-techniques
- **Traçabilité** : Historique complet des messages et patients

### 🏥 **Départements supportés**
- **🏥 Admission** : Enregistrement et gestion des patients
- **🔬 Laboratoire** : Transmission des résultats d'analyses
- **📡 Radiologie** : Commandes d'examens et résultats d'imagerie
- **💊 Pharmacie** : Gestion des prescriptions médicamenteuses

---

## 🚀 Installation et configuration

### 📋 **Prérequis système**

#### Configuration minimale
- **Système d'exploitation** : Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Python** : Version 3.8 ou supérieure
- **RAM** : 4 GB minimum, 8 GB recommandé
- **Espace disque** : 500 MB disponibles
- **Réseau** : Ports TCP 2575-2579 disponibles

#### Vérification de l'environnement
```bash
# Vérifier la version Python
python --version
# Doit afficher : Python 3.8.x ou supérieur

# Vérifier pip
pip --version

# Vérifier les ports disponibles (Linux/macOS)
netstat -an | grep 2575
# Aucun résultat = port disponible
```

### 📦 **Installation des dépendances**

#### Installation standard
```bash
# Naviguer vers le dossier du projet
cd hl7_messenger

# Installer toutes les dépendances
pip install -r requirements.txt

# Vérifier l'installation
python validate_fixes.py
```

#### Dépendances principales
- **hl7apy** : Bibliothèque HL7 officielle pour Python
- **tkinter** : Interface graphique (inclus avec Python)
- **threading** : Gestion multi-clients (standard Python)
- **json** : Persistance des données (standard Python)
- **socket** : Communication réseau (standard Python)

### ⚙️ **Configuration du système**

#### Configuration réseau (`app/config.py`)
```python
# Configuration serveur principal
MLLP_SERVER_HOST = "0.0.0.0"      # Écoute sur toutes les interfaces
MLLP_SERVER_PORT = 2575            # Port principal HL7

# Destinations par département
DESTINATIONS = {
    "ADMISSION_SYSTEM": {"host": "localhost", "port": 2575},
    "LAB_SYSTEM": {"host": "localhost", "port": 2575},
    "ORDER_SYSTEM": {"host": "localhost", "port": 2575},
    "PHARMACY_SYSTEM": {"host": "localhost", "port": 2575}
}

# Paramètres de communication
TIMEOUT = 30                       # Timeout réseau en secondes
MAX_MESSAGE_SIZE = 1048576         # Taille maximale message (1MB)
BUFFER_SIZE = 4096                 # Taille buffer de réception
```

#### Configuration authentification (`app/utils/security.py`)
```python
# Comptes utilisateurs par défaut
DEFAULT_USERS = {
    "admin": {"password": "password", "role": "administrator"},
    "anouchka": {"password": "libre", "role": "admission"},
    "christelle": {"password": "456", "role": "laboratory"},
    "romeo": {"password": "789", "role": "radiology"},
    "calixta": {"password": "abc", "role": "pharmacy"}
}
```

---

## 🎮 Démarrage du système

### 🖥️ **Méthodes de lancement**

#### Méthode 1 : Démarrage rapide (Recommandée)
```bash
# Terminal 1 : Serveur HL7 (obligatoire)
python app/network/mllp_server.py

# Terminal 2 : Interface utilisateur
python run_app.py
```

#### Méthode 2 : Démarrage classique
```bash
# Terminal 1 : Serveur HL7
python -m app.network.mllp_server

# Terminal 2 : Application principale
python app/main.py
```

#### Méthode 3 : Démarrage avec validation
```bash
# Validation complète puis lancement
python validate_fixes.py && python run_app.py
```

### 🔍 **Vérification du démarrage**

#### Serveur HL7 démarré correctement
```
🏥 Serveur HL7 MLLP initialisé
📍 Adresse: 0.0.0.0:2575
📚 Base de données: ✅ Disponible
🚀 Démarrage du serveur HL7...
✅ Socket bindé sur 0.0.0.0:2575
===============================================
🎉 SERVEUR HL7 DÉMARRÉ AVEC SUCCÈS!
🌐 Écoute sur 0.0.0.0:2575
⏰ Démarré le 29/05/2025 à 19:15:32
📨 En attente de messages HL7...
===============================================
```

#### Application démarrée correctement
```
🚀 Initialisation de HL7 Messenger...
✅ Configuration chargée
✅ Base de données initialisée
✅ Interface utilisateur prête
📱 Application démarrée avec succès
```

---

## 🔐 Authentification et navigation

### 🚪 **Écran de connexion**

#### Interface de connexion
L'écran de connexion présente trois champs principaux :
- **👤 Nom d'utilisateur** : Identifiant de l'utilisateur
- **🔒 Mot de passe** : Mot de passe associé
- **🏥 Département** : Service hospitalier d'affectation

#### Comptes par défaut
| Utilisateur | Mot de passe | Département | Rôle |
|-------------|--------------|-------------|------|
| `admin` | `password` | Tous | Administrateur |
| `anouchka` | `libre` | ADMISSION | Responsable admissions |
| `christelle` | `456` | LABORATORY | Technicien laboratoire |
| `romeo` | `789` | RADIOLOGY | Manipulateur radio |
| `calixta` | `abc` | PHARMACY | Pharmacien |

#### Navigation clavier
- **Tab** : Passer au champ suivant
- **Shift+Tab** : Revenir au champ précédent
- **Entrée** : Valider la connexion
- **Échap** : Effacer tous les champs

### 🏠 **Dashboard principal**

#### Vue d'ensemble
Le tableau de bord central affiche :
- **📊 Statistiques temps réel** : Nombre de messages envoyés/reçus
- **🔗 État connexions** : Statut serveur et clients MLLP
- **👥 Patients actifs** : Liste des derniers patients traités
- **📈 Activité récente** : Historique des dernières actions

#### Fonctionnalités disponibles
- **🏥 Accès départements** : Boutons pour chaque service
- **📜 Historique complet** : Consultation des messages échangés
- **⚙️ Configuration** : Paramètres système et réseau
- **🔌 Test connexions** : Diagnostic des communications
- **📊 Rapports** : Génération de statistiques d'utilisation

---

## 🏥 Guide par département

### 🏥 **Module Admission**

#### Fonctionnalités principales
Le module d'admission permet la gestion complète des patients entrants :
- **Enregistrement nouveaux patients** avec validation complète
- **Transferts inter-services** avec traçabilité
- **Mises à jour dossiers** patients existants
- **Sorties programmées** avec notifications
- **Génération messages ADT** conformes HL7 v2.5

#### Interface utilisateur

##### Formulaire patient (obligatoires marqués *)
```
📋 Informations Patient
┌─────────────────────────────────────────────────────────┐
│ 🆔 ID Patient *     : [P12345    ] 👤 Nom *      : [DOE    ]│
│ 👤 Prénom *         : [JOHN      ] 📅 Naissance  : [19800101]│
│ ⚧ Sexe             : [M ▼]        🏢 Service    : [CARDIO  ]│
│ 🛏️ Chambre          : [102       ] 👨‍⚕️ Médecin    : [Dr.MARTIN]│
│ 📨 Type message    : [ADT^A01 - Admission ▼]              │
│ 📝 Commentaires    : [Admission programmée              ] │
└─────────────────────────────────────────────────────────┘
[🔄 Réinitialiser] [🚀 Envoyer Message] ✅ Prêt
```

##### Types de messages ADT supportés
- **ADT^A01** : Admission patient
- **ADT^A02** : Transfert patient
- **ADT^A03** : Sortie patient
- **ADT^A04** : Inscription patient
- **ADT^A08** : Mise à jour informations

##### Validation des données
- **ID Patient** : Minimum 2 caractères, unique
- **Nom/Prénom** : Minimum 2 caractères, format alphabétique
- **Date naissance** : Format AAAAMMJJ (ex: 19800101)
- **Sexe** : M (Masculin), F (Féminin), O (Autre), U (Inconnu)
- **Service** : Code service hospitalier
- **Chambre** : Numéro de chambre disponible

#### Workflow d'utilisation
1. **Saisie informations** patient dans le formulaire
2. **Validation temps réel** des champs obligatoires
3. **Sélection type** de message ADT approprié
4. **Ajout commentaires** si nécessaire
5. **Envoi message** vers le système d'admission
6. **Réception ACK** de confirmation
7. **Sauvegarde automatique** du patient en base

#### Messages HL7 générés
```
MSH|^~\&|HL7MESSENGER|HOSPITAL|ADT|HOSPITAL|20250529191532||ADT^A01|12345|P|2.5
EVN||20250529191532
PID|1||P12345||DOE^JOHN||19800101|M
PV1|1|I|CARDIO^102||||||||||||||20250529191532
```

### 🔬 **Module Laboratoire**

#### Fonctionnalités principales
Le module laboratoire gère la transmission des résultats d'analyses :
- **Résultats biologiques** multi-paramètres
- **Codes LOINC** standardisés
- **Valeurs de référence** avec anomalies
- **Commentaires techniques** détaillés
- **Génération messages ORU** conformes HL7 v2.5

#### Interface utilisateur

##### Formulaire résultats laboratoire
```
🔬 Résultats de Laboratoire
┌─────────────────────────────────────────────────────────┐
│ 👤 ID Patient *     : [P12345    ] 📋 ID Demande : [LAB001 ]│
│ 🧪 Code Examen *    : [GLU       ] 📝 Nom Examen : [Glucose]│
│ 📅 Date Examen     : [20250529  ] ⏰ Heure      : [14:30  ]│
│                                                           │
│ 📊 Résultat 1                                            │
│ 🔬 Code Test       : [GLU       ] 📝 Nom Test   : [Glucose]│
│ 📈 Valeur          : [95        ] 📏 Unité      : [mg/dL  ]│
│ 📊 Référence       : [70-110    ] ⚠️ Anomalie   : [Normal ]│
│                                                           │
│ 📊 Résultat 2 (optionnel)                               │
│ 🔬 Code Test       : [HBA1C     ] 📝 Nom Test   : [HbA1c  ]│
│ 📈 Valeur          : [5.8       ] 📏 Unité      : [%      ]│
│ 📊 Référence       : [<6.5      ] ⚠️ Anomalie   : [Normal ]│
│                                                           │
│ 📝 Commentaires    : [Résultats dans les normes        ] │
└─────────────────────────────────────────────────────────┘
[🔄 Réinitialiser] [🚀 Envoyer Résultats] ✅ Prêt
```

##### Codes d'anomalies
- **N** : Normal (dans les limites)
- **H** : Élevé (au-dessus de la normale)
- **L** : Bas (en-dessous de la normale)
- **HH** : Critique élevé
- **LL** : Critique bas
- **A** : Anormal (sans précision)

#### Workflow d'utilisation
1. **Réception demande** d'analyse du médecin
2. **Réalisation examens** au laboratoire
3. **Saisie résultats** dans l'interface
4. **Validation biologique** par le technicien
5. **Envoi résultats** au dossier patient
6. **Notification médecin** prescripteur
7. **Archivage résultats** en base

#### Messages HL7 générés
```
MSH|^~\&|HL7MESSENGER|HOSPITAL|LAB|HOSPITAL|20250529143000||ORU^R01|LAB001|P|2.5
PID|1||P12345
OBR|1|LAB001||GLU^Glucose|||20250529143000
OBX|1|NM|GLU^Glucose|95|mg/dL|70-110|N||F||20250529143000
OBX|2|NM|HBA1C^HbA1c|5.8|%|<6.5|N||F||20250529143000
```

### 📡 **Module Radiologie**

#### Fonctionnalités principales
Le module radiologie couvre deux aspects :
- **Commandes d'examens** (ORM^O01) pour planification
- **Résultats d'imagerie** (ORU^R01) avec comptes-rendus
- **Gestion priorités** et urgences
- **Suivi workflow** complet examen

#### Interface commandes d'examens
```
📡 Commandes d'Examens Radiologiques
┌─────────────────────────────────────────────────────────┐
│ 👤 ID Patient *     : [P12345    ] 📋 ID Commande: [RX001 ]│
│ 🔬 Code Examen *    : [CHEST     ] 📝 Nom Examen : [Radio thorax]│
│ 📅 Date Programme   : [20250530  ] ⏰ Heure      : [09:00  ]│
│ ⚡ Priorité         : [ROUTINE ▼] 📍 Localisation: [Salle 1]│
│ 👨‍⚕️ Médecin Demandeur: [Dr.MARTIN ] 🎯 Indication : [Toux persistante]│
│ 📝 Commentaires    : [Patient claustrophobe - prévoir sédation]│
└─────────────────────────────────────────────────────────┘
[🔄 Réinitialiser] [🚀 Programmer Examen] ✅ Prêt
```

#### Interface résultats d'examens
```
📡 Résultats d'Examens Radiologiques
┌─────────────────────────────────────────────────────────┐
│ 👤 ID Patient *     : [P12345    ] 📋 ID Examen  : [RX001 ]│
│ 🔬 Code Examen *    : [CHEST     ] 📝 Nom Examen : [Radio thorax]│
│ 📅 Date Réalisation : [20250530  ] ⏰ Heure      : [09:15  ]│
│ 👨‍⚕️ Radiologue      : [Dr.DUPONT ] 📊 Statut     : [FINAL ▼]│
│                                                           │
│ 📋 Compte-rendu                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ TECHNIQUE :                                         │ │
│ │ Radiographie thoracique de face et profil          │ │
│ │                                                     │ │
│ │ RESULTATS :                                         │ │
│ │ - Poumons bien déployés                            │ │
│ │ - Pas d'opacité parenchymateuse                    │ │
│ │ - Silhouette cardiaque normale                     │ │
│ │ - Coupoles diaphragmatiques libres                 │ │
│ │                                                     │ │
│ │ CONCLUSION :                                        │ │
│ │ Examen thoracique normal                           │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
[🔄 Réinitialiser] [🚀 Envoyer Résultats] ✅ Prêt
```

#### Types d'examens supportés
- **CHEST** : Radiographie thoracique
- **ABDO** : Radiographie abdominale
- **SKULL** : Radiographie crâne
- **ECHO** : Échographie
- **SCAN** : Scanner
- **IRM** : Imagerie par résonance magnétique
- **MAMMO** : Mammographie

#### Workflow d'utilisation
1. **Réception prescription** médicale
2. **Programmation examen** avec créneaux
3. **Préparation patient** si nécessaire
4. **Réalisation examen** par manipulateur
5. **Interprétation images** par radiologue
6. **Rédaction compte-rendu** détaillé
7. **Validation finale** et envoi résultats

### 💊 **Module Pharmacie**

#### Fonctionnalités principales
Le module pharmacie gère les prescriptions médicamenteuses :
- **Prescriptions multi-médicaments** (jusqu'à 2 par ordonnance)
- **Posologies détaillées** avec fréquences
- **Vérification interactions** médicamenteuses
- **Instructions spéciales** pour le patient
- **Génération messages ORM** pour dispensation

#### Interface utilisateur
```
💊 Prescriptions Médicamenteuses
┌─────────────────────────────────────────────────────────┐
│ 👤 ID Patient *     : [P12345    ] 📋 ID Prescription: [RX001]│
│ 👨‍⚕️ Médecin *       : [Dr.MARTIN ] 📅 Date Prescription: [20250529]│
│                                                           │
│ 💊 Médicament 1                                          │
│ 🔢 Code Médicament  : [PARA500   ] 📝 Nom Commercial: [Doliprane]│
│ 💉 Dosage          : [500mg     ] 📊 Forme         : [Comprimé▼]│
│ ⏰ Posologie        : [1 cp x 3/j] 🔄 Durée        : [7 jours ]│
│ 📝 Instructions    : [À prendre pendant les repas]       │
│                                                           │
│ 💊 Médicament 2 (optionnel)                             │
│ 🔢 Code Médicament  : [AMOX1000  ] 📝 Nom Commercial: [Clamoxyl]│
│ 💉 Dosage          : [1000mg    ] 📊 Forme         : [Comprimé▼]│
│ ⏰ Posologie        : [1 cp x 2/j] 🔄 Durée        : [10 jours]│
│ 📝 Instructions    : [Traitement à terminer complètement]│
│                                                           │
│ 📝 Commentaires    : [Vérifier allergie pénicilline]    │
└─────────────────────────────────────────────────────────┘
[🔄 Réinitialiser] [🚀 Envoyer Prescription] ✅ Prêt
```

#### Formes pharmaceutiques
- **Comprimé** : Forme solide standard
- **Gélule** : Forme encapsulée
- **Sirop** : Forme liquide orale
- **Solution** : Forme liquide injectable
- **Pommade** : Forme topique
- **Suppositoire** : Forme rectale
- **Patch** : Forme transdermique

#### Workflow d'utilisation
1. **Réception prescription** médicale
2. **Vérification disponibilité** médicaments
3. **Contrôle interactions** et contre-indications
4. **Préparation pilulier** si nécessaire
5. **Étiquetage posologie** détaillée
6. **Dispensation patient** avec conseils
7. **Suivi observance** si traitement au long cours

---

## 📊 Gestion des données et historique

### 💾 **Base de données patients**

#### Structure des données patient
```json
{
    "id": "P12345",
    "personal_info": {
        "last_name": "DOE",
        "first_name": "JOHN", 
        "birth_date": "19800101",
        "gender": "M"
    },
    "hospital_info": {
        "ward": "CARDIO",
        "room": "102",
        "attending_doctor": "Dr.MARTIN",
        "admission_date": "20250529191532"
    },
    "contact_info": {
        "phone": "+32123456789",
        "address": "123 Rue de la Santé, 1000 Bruxelles",
        "emergency_contact": "Jane DOE - Épouse"
    },
    "medical_info": {
        "allergies": ["Pénicilline"],
        "medical_history": ["Hypertension", "Diabète type 2"],
        "current_medications": ["Metformine 850mg", "Amlodipine 5mg"]
    },
    "metadata": {
        "created_date": "20250529191532",
        "last_updated": "20250529191532",
        "created_by": "anouchka",
        "total_visits": 3
    }
}
```

#### Fichier de stockage
- **Localisation** : `resources/patients.json`
- **Format** : JSON structuré avec validation automatique
- **Sauvegarde** : Automatique après chaque modification
- **Backup** : Copies horodatées dans `backup_*/`

### 📨 **Historique des messages**

#### Structure des messages HL7
```json
{
    "id": "msg_12345678-1234-5678-9abc-123456789abc",
    "message_info": {
        "type": "ADT^A01",
        "control_id": "20250529-12345",
        "timestamp": "20250529191532",
        "status": "SENT_SUCCESS"
    },
    "communication": {
        "source": "HL7MESSENGER",
        "destination": "ADMISSION_SYSTEM", 
        "source_ip": "127.0.0.1:54321",
        "destination_ip": "127.0.0.1:2575"
    },
    "patient_ref": {
        "patient_id": "P12345",
        "patient_name": "DOE^JOHN"
    },
    "content": {
        "raw_message": "MSH|^~\\&|HL7MESSENGER|...",
        "parsed_segments": {
            "MSH": {...},
            "PID": {...},
            "PV1": {...}
        }
    },
    "acknowledgment": {
        "ack_received": true,
        "ack_code": "AA",
        "ack_message": "Message traité avec succès",
        "ack_timestamp": "20250529191533"
    }
}
```

### 📈 **Interface historique**

#### Fonctionnalités de consultation
```
📜 Historique des Messages HL7
┌─────────────────────────────────────────────────────────┐
│ 🔍 Filtres                                              │
│ 📅 Du: [29/05/2025] Au: [29/05/2025] 📨 Type: [Tous ▼]│
│ 👤 Patient: [Tous     ] 🏥 Département: [Tous      ▼] │
│ 📊 Statut: [Tous     ▼] 🔄 [Appliquer Filtres]        │
│                                                         │
│ 📋 Messages (25 résultats)                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │19:15:32│ADT^A01│P12345│DOE JOHN    │✅ Envoyé      │ │
│ │19:12:15│ORU^R01│P12344│SMITH JANE  │✅ Envoyé      │ │
│ │19:08:45│ORM^O01│P12343│MARTIN PAUL │❌ Erreur      │ │
│ │19:05:22│ADT^A02│P12342│BROWN MARY  │✅ Envoyé      │ │
│ │18:58:11│ORU^R01│P12341│WILSON TOM  │✅ Envoyé      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [📄 Exporter CSV] [🔍 Détails] [🔄 Actualiser]        │
└─────────────────────────────────────────────────────────┘
```

#### Options d'export
- **CSV** : Fichier Excel pour analyse
- **PDF** : Rapport formaté pour impression
- **JSON** : Données brutes pour intégration
- **HL7** : Messages bruts pour debug

---

## 🌐 Communication réseau et protocoles

### 📡 **Architecture réseau**

#### Schéma de communication
```
┌─────────────────┐    MLLP/TCP     ┌─────────────────┐
│  Interface UI   │ ─────────────► │  Serveur HL7    │
│  (Départements) │                │  (Port 2575)    │
└─────────────────┘                └─────────────────┘
        │                                    │
        ▼                                    ▼
┌─────────────────┐                ┌─────────────────┐
│  Client MLLP    │                │ Réception MLLP  │
│  (Envoi)        │                │ (Multi-client)  │
└─────────────────┘                └─────────────────┘
        │                                    │
        ▼                                    ▼
┌─────────────────┐                ┌─────────────────┐
│ Message HL7     │◄──── ACK ──────│  Parser HL7     │
│ (ADT/ORU/ORM)   │                │  (Validation)   │
└─────────────────┘                └─────────────────┘
                                            │
                                            ▼
                                  ┌─────────────────┐
                                  │ Base de données │
                                  │ (JSON Storage)  │
                                  └─────────────────┘
```

### 🔌 **Protocole MLLP**

#### Structure des messages MLLP
```
[SB] + [Message HL7] + [EB] + [CR]
 ↓         ↓           ↓       ↓
0x0B   Contenu HL7   0x1C    0x0D
```

#### Exemple complet
```
Hexadécimal : 0B 4D 53 48 7C ... 1C 0D
ASCII       : [SB]MSH|^~\&|HL7MESSENGER|...[EB][CR]
```

#### Gestion des ACK
```python
# ACK de succès
MSH|^~\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|20250529191533||ACK^ADT^A01|12345|P|2.5
MSA|AA|12345|Message traité avec succès

# ACK d'erreur applicative  
MSH|^~\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|20250529191533||ACK|12345|P|2.5
MSA|AE|12345|Erreur: Patient inexistant

# ACK de rejet
MSH|^~\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|20250529191533||ACK|12345|P|2.5
MSA|AR|12345|Message rejeté: Format invalide
```

### 🔍 **Test rapide du système**

#### Connexion et test basique
1. **Démarrer le serveur** : `python app/network/mllp_server.py`
2. **Lancer l'application** : `python run_app.py`
3. **Se connecter** : 
   - Utilisateur : `anouchka`
   - Mot de passe : `libre`
   - Département : `ADMISSION`
4. **Tester l'envoi** d'un message ADT^A01
5. **Vérifier la réception** dans les logs du serveur
6. **Confirmer le stockage** du patient en base

#### Données de test prêtes à l'emploi
Les formulaires sont pré-remplis avec des données de test valides :
- **Patient** : P12345 - DOE JOHN
- **Service** : CARDIO, Chambre 102
- **Médecin** : Dr. MARTIN
- **Date** : Automatiquement aujourd'hui

### 🔧 **Configuration avancée**

#### Paramètres de performance
```python
