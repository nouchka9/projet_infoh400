## HL7 Messenger Simplifié pour Hôpital

Application de messagerie HL7 permettant la communication entre départements hospitaliers.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow)

## 📋 Description

HL7 Messenger est une solution légère permettant aux différents services d'un hôpital (admission, laboratoire, radiologie, pharmacie) d'échanger des informations sur les patients via le protocole HL7, standard international pour les systèmes de santé.

Cette application permet de:
- Créer et envoyer des messages HL7 (ADT, ORU)
- Recevoir et interpréter des messages HL7
- Stocker les informations patients
- Visualiser l'historique des communications

## 🛠️ Technologies utilisées

- **Python**: Langage principal
- **tkinter**: Interface graphique
- **hl7apy**: Manipulation des messages HL7
- **MLLP**: Protocole de communication réseau
- **JSON**: Stockage des données

## 👥 Membres de l'équipe & Répartition des rôles

| Prénom         | Rôle principal                       | Mission globale                                                       |
| -------------- | ------------------------------------ | --------------------------------------------------------------------- |
| **Anouchka**   | Serveur HL7 + Parsing + Stockage     | Traiter les messages HL7 reçus et enregistrer les données             |
| **Christelle** | Client HL7 + Génération des messages | Créer et envoyer les messages HL7 depuis l'interface                  |
| **Roméo**      | Interface utilisateur tkinter        | Créer une interface intuitive pour envoyer les messages               |
| **Calixta**    | Données + JSON + Documentation       | Stocker les patients reçus, rédiger le README et documenter le projet |

## 🚀 Installation

### Prérequis

- Python 3.8+
- Bibliothèques requises (voir `requirements.txt`)

### Installation des dépendances

```bash
pip install -r requirements.txt
Lancement de l'application
python app/main.py
📊 Fonctionnalités
Admission de patients (ADT^A01)
L'interface d'admission permet de saisir les informations d'un nouveau patient et de les transmettre aux autres services de l'hôpital.
Résultats d'examens (ORU^R01)
Le service de laboratoire peut envoyer les résultats d'examens aux médecins traitants.
Communication interdépartementale
Chaque département dispose d'une interface spécifique pour envoyer et recevoir des messages pertinents pour ses activités.
📷 Captures d'écran
Des captures d'écran seront ajoutées lors de la finalisation de l'interface utilisateur.
🧪 Tests
L'application inclut des tests unitaires et d'intégration pour valider:
La création de messages HL7 valides
La communication client/serveur
Le stockage et la récupération des données patient
Pour exécuter les tests:
python -m unittest discover tests
📃 Licence
Ce projet est un travail académique réalisé dans le cadre du cours INFO-H-400 "Medical Information Systems".
Développé par Anouchka, Christelle, Roméo et Calixta © 2025
Ces fichiers constituent l'ensemble complet de votre projet.
