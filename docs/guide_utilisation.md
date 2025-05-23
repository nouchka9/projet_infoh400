# Guide d'utilisation : HL7 Messenger v2.0 - Version finale macOS

## 📖 Présentation

**HL7 Messenger** est une application Python complète pour les échanges de messages HL7 entre les départements hospitaliers (Admission, Laboratoire, Radiologie, Pharmacie). Cette version finale est **optimisée spécifiquement pour macOS** avec des corrections pour éviter les déconnexions et problèmes de stabilité.

### ✅ **Fonctionnalités principales**
* Interface utilisateur moderne avec navigation clavier fluide
* Génération, envoi et réception de messages HL7 (ADT, ORU, ORM)
* Serveur MLLP robuste avec gestion complète des ACK
* Stockage des données patients (fichier JSON)
* Optimisations spécifiques macOS pour stabilité maximale
* Scripts de lancement automatique
* Gestion d'erreurs complète et destruction sécurisée des widgets

---

## 🍎 **Spécificités macOS - IMPORTANT**

### **Problèmes macOS résolus**
Cette version corrige spécifiquement les problèmes suivants sur macOS :
- ❌ `autorelease pool page corrupted` → ✅ **RÉSOLU**
- ❌ Déconnexions après envoi de messages → ✅ **RÉSOLU**
- ❌ Erreurs threading avec Tkinter → ✅ **RÉSOLU**
- ❌ Corruption mémoire avec `objc` → ✅ **RÉSOLU**

### **Scripts macOS optimisés**
- **`stable_launcher.py`** : Lanceur principal avec protection macOS
- **`start_macos.py`** : Lanceur alternatif avec variables environnement
- **`start_macos.sh`** : Script bash avec configuration complète
- **`threading_fix.py`** : Correction automatique du threading

---

## 🚀 **Installation et démarrage**

### **Prérequis**
```bash
# Vérifier Python
python --version  # Doit être 3.8+

# Installer les dépendances
pip install -r requirements.txt
```

### **Démarrage sur macOS (recommandé)**

#### **Option 1 : Lanceur stable (RECOMMANDÉ)**
```bash
# Terminal 1 : Serveur HL7
python -m app.network.mllp_server

# Terminal 2 : Application stable
python stable_launcher.py
```

#### **Option 2 : Lanceur macOS optimisé**
```bash
# Terminal 1 : Serveur HL7
python -m app.network.mllp_server

# Terminal 2 : Application avec optimisations macOS
python start_macos.py
```

#### **Option 3 : Script bash complet**
```bash
# Terminal 1 : Serveur HL7
python -m app.network.mllp_server

# Terminal 2 : Script avec toutes les variables environnement
bash start_macos.sh
```

### **Démarrage classique (peut avoir problèmes sur macOS)**
```bash
# Uniquement si les autres options ne fonctionnent pas
python app/main.py
```

---

## 🏥 **Utilisation par département**

### **1. Connexion**
1. **Nom d'utilisateur** : n'importe quel nom (ex: "admin", "anouchka")
2. **Mot de passe** : n'importe quel mot de passe (ex: "123", "password")
3. **Département** : choisir parmi ADMISSION, LABORATORY, RADIOLOGY, PHARMACY
4. **Navigation** : Tab pour naviguer, Entrée pour valider

### **2. Module Admission (ADT^A01)**
**Fonctionnalités :**
- Saisie informations patient (ID, nom, prénom, date naissance)
- Choix service et chambre
- Génération messages ADT^A01 conformes HL7 v2.5
- **Envoi SANS threading** (stable sur macOS)

**Champs importants :**
- **ID Patient*** : Identifiant unique (requis)
- **Nom/Prénom*** : Obligatoires, validation temps réel
- **Date naissance** : Format AAAAMMJJ (19800101)
- **Sexe** : M/F/O/U avec menu déroulant
- **Service/Chambre** : Pour localisation hospitalière

**Navigation clavier :**
- **Tab** : Navigation entre champs
- **Entrée** : Envoyer le message
- **F5** : Réinitialiser le formulaire
- **Échap** : Annuler

### **3. Module Laboratoire (ORU^R01)**
**Fonctionnalités :**
- Saisie résultats d'examens biologiques
- Support multiple résultats par patient
- Codes LOINC et unités de mesure
- Génération messages ORU^R01

**Utilisation :**
- ID Patient, ID Demande, Code examen
- Jusqu'à 2 résultats par message
- Valeurs, unités, codes de référence
- Envoi vers LAB_SYSTEM (port 2575)

### **4. Module Radiologie (ORM^O01)**
**Fonctionnalités :**
- Demandes d'examens radiologiques
- Résultats avec rapports textuels
- Gestion priorités et commentaires
- Double interface : demandes + résultats

**Types d'examens :**
- Radiographies, échographies, IRM, scanner
- Codes personnalisables
- Dates programmées
- Rapports détaillés

### **5. Module Pharmacie (ORM^O01)**
**Fonctionnalités :**
- Prescriptions médicamenteuses
- Support jusqu'à 2 médicaments par ordonnance
- Posologies et fréquences
- Instructions détaillées

**Informations prescriptions :**
- Code médicament, nom commercial
- Dosage et fréquence d'administration
- Instructions spéciales
- Médecin prescripteur

---

## 🔧 **Fonctions essentielles et architecture**

### **Structure du projet**
```
hl7_messenger/
├── app/                          # Code source principal
│   ├── ui/                       # Interface utilisateur
│   │   ├── app.py               # Application principale ✅ CORRIGÉE
│   │   ├── login_screen.py      # Écran connexion ✅ CORRIGÉE
│   │   ├── dashboard.py         # Tableau de bord ✅ CORRIGÉ
│   │   └── departments/         # Modules départements
│   │       ├── admission.py     # ✅ SANS THREADING (stable macOS)
│   │       ├── laboratory.py    # Module laboratoire
│   │       ├── radiology.py     # Module radiologie
│   │       └── pharmacy.py      # Module pharmacie
│   ├── network/                 # Communication réseau
│   │   ├── mllp_client.py      # Client MLLP pour envoi
│   │   └── mllp_server.py      # Serveur MLLP ✅ CORRIGÉ
│   ├── hl7_engine/             # Moteur HL7
│   │   ├── builder.py          # Construction messages HL7
│   │   ├── parser.py           # Analyse messages reçus
│   │   └── ack.py              # Gestion accusés réception
│   ├── db/                     # Base de données
│   │   ├── database.py         # Gestionnaire fichiers JSON
│   │   └── repositories/       # Accès données
│   └── models/                 # Modèles de données
├── stable_launcher.py          # 🍎 LANCEUR STABLE MACOS
├── start_macos.py             # 🍎 LANCEUR OPTIMISÉ MACOS
├── start_macos.sh             # 🍎 SCRIPT BASH MACOS
├── threading_fix.py           # 🍎 CORRECTION THREADING
├── resources/                 # Ressources
│   ├── patients.json         # Base données patients
│   ├── logo.png             # Icône application
│   └── config.json          # Configuration
└── docs/                    # Documentation
```

### **Fonctions clés stabilité macOS**

#### **1. stable_launcher.py** 🍎
```python
def setup_stable_environment():
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    os.environ['MALLOC_NANO_ZONE'] = '0'
    # Corrections spécifiques macOS
```
**Rôle** : Évite les corruptions mémoire et déconnexions

#### **2. Admission sans threading** 🔧
```python
def _send_message_safe(self):
    # ENVOI SYNCHRONE (pas de threading)
    success, response = self.mllp_client.send_message()
```
**Rôle** : Envoi stable sans problèmes threading macOS

#### **3. Gestion sécurisée widgets** 🛡️
```python
def _safe_destroy_widget(self, widget):
    if widget and widget.winfo_exists():
        widget.destroy()
```
**Rôle** : Évite les erreurs TclError lors des transitions

#### **4. Serveur MLLP robuste** 🌐
```python
def handle_client(self, client_socket, client_address):
    # Gestion complète erreurs + logging détaillé
```
**Rôle** : Réception fiable messages HL7 avec diagnostics

---

## 📊 **Communication HL7**

### **Types de messages supportés**
- **ADT^A01** : Admission patient
- **ADT^A02** : Transfert patient  
- **ADT^A03** : Sortie patient
- **ORU^R01** : Résultats examens
- **ORM^O01** : Demandes examens

### **Configuration réseau**
```python
# Tous pointent vers le même serveur (2575)
"ADMISSION_SYSTEM": {"host": "localhost", "port": 2575}
"LAB_SYSTEM": {"host": "localhost", "port": 2575}
"ORDER_SYSTEM": {"host": "localhost", "port": 2575}
"PHARMACY_SYSTEM": {"host": "localhost", "port": 2575}
```

### **Protocole MLLP**
- **Start Block** : `\x0b`
- **End Block** : `\x1c`
- **Carriage Return** : `\x0d`
- **ACK automatique** : MSA|AA|ID pour succès

---

## 🧪 **Tests et démonstration**

### **Test complet**
1. **Démarrer serveur** : `python -m app.network.mllp_server`
2. **Lancer application** : `python stable_launcher.py`
3. **Se connecter** : admin/123 → ADMISSION
4. **Remplir formulaire** patient
5. **Envoyer message** : Bouton ou Entrée
6. **Vérifier réception** dans logs serveur
7. **Application reste connectée** ✅

### **Données de test intégrées**
- **Bouton "Mode Test"** : Génère données patients aléaoires
- **Valeurs par défaut** : Formulaires pré-remplis
- **Validation temps réel** : Erreurs affichées immédiatement

---

## 🔍 **Diagnostic et résolution problèmes**

### **Problèmes courants macOS**

#### **1. Application se déconnecte après envoi**
**Solution** : Utiliser `stable_launcher.py` au lieu de `app/main.py`
```bash
python stable_launcher.py  # ✅ Stable
```

#### **2. Erreur "autorelease pool corrupted"**
**Solution** : Variables environnement dans `start_macos.py`
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

#### **3. Port déjà utilisé**
**Solution** : Arrêter processus ou changer port
```bash
lsof -ti:2575 | xargs kill  # Tuer processus port 2575
python -m app.network.mllp_server 2576  # Utiliser autre port
```

#### **4. Connexion refusée**
**Vérifications** :
- Serveur démarré : `python -m app.network.mllp_server`
- Port correct : 2575 dans config.py
- Firewall : Autoriser connexions locales

### **Logs et débogage**
```bash
# Logs serveur détaillés
INFO:HL7Messenger.MLLPServer:Serveur démarré sur 0.0.0.0:2575
INFO:HL7Messenger.MLLPServer:Message reçu de 127.0.0.1:xxxxx

# Logs client détaillés  
INFO:HL7Messenger.MLLPClient:ENVOI | localhost:2575 | MSH|...
INFO:HL7Messenger.MLLPClient:ACK | localhost:2575 | MSA|AA|...
```

---

## 🎯 **Fonctionnalités avancées**

### **Historique des messages**
- **Bouton "Historique"** dans dashboard
- **Base SQLite** : `resources/hl7_messages.db`
- **Filtrage** par date, type, statut
- **Export possible** des données

### **Sauvegarde patients**
- **Fichier JSON** : `resources/patients.json`
- **Sauvegarde automatique** à chaque réception
- **Format structuré** pour export/import

### **Scripts utilitaires**
- **`threading_fix.py`** : Correction threading si problème
- **`quick_fix.py`** : Correction configuration rapide
- **Dossiers backup/** : Sauvegardes automatiques versions

---

## 💡 **Conseils d'utilisation**

### **Bonnes pratiques**
1. **Toujours démarrer le serveur** avant l'application
2. **Utiliser le lanceur stable** sur macOS
3. **Vérifier les logs** en cas de problème
4. **Sauvegarder** le dossier resources/ régulièrement
5. **Tester** chaque département avant démonstration

### **Navigation optimale**
- **Tab** : Navigation rapide entre champs
- **Entrée** : Validation/envoi direct
- **F5** : Réinitialisation formulaires
- **Menus déroulants** : Flèches haut/bas

### **Personnalisation**
- **Modifier** `resources/config.json` pour ports
- **Ajouter** logos dans `resources/`
- **Étendre** types messages dans `hl7_engine/builder.py`

---

## 📚 **Documentation technique**

### **Standards respectés**
- **HL7 v2.5** : Messages conformes standard international
- **MLLP** : Protocole transport standard HL7
- **TCP/IP** : Communication réseau fiable
- **JSON** : Stockage données structurées

### **Architecture modulaire**
- **MVC Pattern** : Séparation interface/logique/données
- **Repository Pattern** : Accès données centralisé
- **Observer Pattern** : Notifications événements
- **Factory Pattern** : Construction messages HL7

---

## 🎓 **Projet académique INFO-H-400**

### **Objectifs atteints**
✅ **Interface utilisateur** moderne et intuitive  
✅ **Communication HL7** complète et conforme  
✅ **Architecture logicielle** professionnelle  
✅ **Gestion d'erreurs** robuste  
✅ **Documentation** complète  
✅ **Tests** fonctionnels validés  
✅ **Optimisations** spécifiques plateforme  

### **Compétences démontrées**
- Programmation Python avancée
- Interfaces graphiques Tkinter
- Protocoles de communication médicale
- Gestion bases de données
- Architecture logicielle
- Débogage et optimisation
- Documentation technique

---

**Développé par Jeannette; Calixtha, Romeo et Chrystelle**  
📧 jeannett.ngue@ulb.be  
🎓 Université Libre de Bruxelles - INFO-H-400  
🌐 https://github.com/nouchka9/projet_infoh400  

*Version finale v2.0 - Optimisée macOS - Mai 2025*
