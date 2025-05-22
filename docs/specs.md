# Spécifications du projet HL7 Messenger

## 1. Présentation

HL7 Messenger est une application simplifiée permettant aux départements hospitaliers d'échanger des messages au format HL7, un standard international de communication pour les systèmes de santé. L'application permet la création, l'envoi, la réception et le stockage de messages HL7 dans un environnement hospitalier virtuel.

## 2. Architecture

### 2.1 Structure générale

L'application suit une architecture en couches:
hl7_messenger/ ├── app/                      # Code source principal │   ├── hl7_engine/          # Traitement des messages HL7 │   ├── network/             # Communication réseau (MLLP) │   ├── db/                  # Stockage des données │   ├── models/              # Modèles de données │   └── ui/                  # Interface utilisateur ├── resources/               # Ressources externes ├── docs/                    # Documentation └── tests/                   # Tests unitaires et d'intégration
### 2.2 Flux de données

1. **Envoi de message**:
   - L'utilisateur saisit les informations patient dans l'interface
   - L'application crée un message HL7 au format approprié
   - Le client MLLP envoie le message au serveur destinataire
   - L'application affiche la confirmation de l'envoi

2. **Réception de message**:
   - Le serveur MLLP écoute les connexions entrantes
   - Un message HL7 est reçu d'un client externe
   - Le parser valide et interprète le message
   - Les données patient sont extraites et stockées
   - Un accusé de réception est envoyé au client

## 3. Technologies

- **Python 3.8+**: Langage principal
- **hl7apy**: Bibliothèque de manipulation des messages HL7
- **tkinter**: Interface graphique
- **JSON**: Stockage des données patient
- **MLLP** (Minimal Lower Layer Protocol): Transport des messages HL7

## 4. Types de messages supportés

- **ADT^A01** (Admission): Enregistrement d'un nouveau patient
- **ORU^R01** (Observation Result): Résultats d'examens

## 5. Infrastructure de communication

- **Port standard**: 2575 (port HL7)
- **Protocole**: MLLP sur TCP/IP
- **Format d'échange**: HL7 v2.5

## 6. Stockage des données

Les données patient sont stockées dans un fichier JSON (`patients.json`):
- Format unifié pour tous les patients
- Identifiant unique pour chaque patient
- Vérification des doublons lors de l'insertion

## 7. Sécurité

- Vérification de l'intégrité des messages HL7
- Validation des données avant stockage
- Isolation du réseau (communication locale uniquement dans cette version)

---

*Ce document est destiné à l'équipe de développement et peut évoluer au cours du projet.*