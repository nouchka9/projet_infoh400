#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour corriger les problèmes de l'application HL7 Messenger
"""
import os
import sys
import shutil
import json

def create_dir(path):
    """Crée un répertoire s'il n'existe pas"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Répertoire créé : {path}")

def create_file(path, content):
    """Crée ou écrase un fichier avec le contenu spécifié"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        print(f"✅ Fichier créé : {path}")
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier {path} : {e}")

def create_config():
    """Crée le fichier de configuration"""
    config = {
        "hosts": {
            "ADMISSION_SYSTEM": {"host": "127.0.0.1", "port": 2576},
            "LAB_SYSTEM": {"host": "127.0.0.1", "port": 2577},
            "ORDER_SYSTEM": {"host": "127.0.0.1", "port": 2578},
            "PHARMACY_SYSTEM": {"host": "127.0.0.1", "port": 2579}
        },
        "mllp": {
            "timeout": 5,
            "retries": 3,
            "demo_mode": True
        },
        "ui": {
            "theme": "clam",
            "font_size": 10,
            "debug_mode": False
        },
        "logging": {
            "level": "INFO",
            "file_enabled": True,
            "file_path": "logs/hl7_messenger.log"
        }
    }
    
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    create_dir(config_dir)
    
    config_path = os.path.join(config_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"✅ Fichier de configuration créé : {config_path}")

def fix_config_py():
    """Corrige le fichier config.py"""
    content = """# -*- coding: utf-8 -*-
\"\"\"
Configuration globale de l'application.
\"\"\"
import os
import json
import logging

class Config:
    \"\"\"Classe de configuration de l'application\"\"\"
    
    def __init__(self, config_file=None):
        \"\"\"
        Initialise la configuration
        
        Args:
            config_file (str, optional): Chemin vers le fichier de configuration
        \"\"\"
        # Valeurs par défaut
        self.settings = {
            "hosts": {
                "ADMISSION_SYSTEM": {"host": "127.0.0.1", "port": 2576},
                "LAB_SYSTEM": {"host": "127.0.0.1", "port": 2577},
                "ORDER_SYSTEM": {"host": "127.0.0.1", "port": 2578},
                "PHARMACY_SYSTEM": {"host": "127.0.0.1", "port": 2579}
            },
            "mllp": {
                "timeout": 10,
                "retries": 3,
                "demo_mode": True
            },
            "ui": {
                "theme": "clam",
                "font_size": 10,
                "debug_mode": False
            },
            "logging": {
                "level": "INFO",
                "file_enabled": True,
                "file_path": "hl7_messenger.log",
                "console_enabled": True
            }
        }
        
        # Charger depuis le fichier si spécifié
        if config_file:
            self._load_from_file(config_file)
        else:
            # Chercher config.json dans le dossier de l'application
            try:
                default_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "config.json")
                if os.path.exists(default_path):
                    self._load_from_file(default_path)
            except Exception as e:
                print(f"Impossible de charger la configuration par défaut : {e}")
    
    def _load_from_file(self, file_path):
        \"\"\"
        Charge la configuration depuis un fichier JSON
        
        Args:
            file_path (str): Chemin vers le fichier
        \"\"\"
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Mettre à jour les valeurs par défaut avec celles du fichier
            for section, values in data.items():
                if section in self.settings and isinstance(values, dict):
                    self.settings[section].update(values)
                else:
                    self.settings[section] = values
        except Exception as e:
            raise Exception(f"Erreur lors du chargement du fichier de configuration : {e}")
    
    def _setup_logging(self):
        \"\"\"Configure le logging selon les paramètres\"\"\"
        log_config = self.settings.get("logging", {})
        
        # Niveau de log
        level_name = log_config.get("level", "INFO")
        level = getattr(logging, level_name, logging.INFO)
        
        # Configuration de base
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Fichier de log si activé
        if log_config.get("file_enabled", True):
            file_path = log_config.get("file_path", "hl7_messenger.log")
            
            # Créer le dossier parent si nécessaire
            dir_path = os.path.dirname(file_path)
            if dir_path and not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path)
                except Exception as e:
                    print(f"Impossible de créer le dossier de logs : {e}")
    
    def get(self, key, default=None):
        \"\"\"
        Récupère une valeur de configuration
        
        Args:
            key (str): Clé
            default: Valeur par défaut
            
        Returns:
            Valeur ou default si non trouvé
        \"\"\"
        return self.settings.get(key, default)
    
    def get_section(self, section, default=None):
        \"\"\"
        Récupère une section de configuration
        
        Args:
            section (str): Nom de section
            default: Valeur par défaut
            
        Returns:
            dict: Section ou default si non trouvé
        \"\"\"
        return self.settings.get(section, default or {})
    
    def set(self, key, value):
        \"\"\"
        Définit une valeur de configuration
        
        Args:
            key (str): Clé
            value: Valeur
        \"\"\"
        self.settings[key] = value
    
    def save(self, file_path):
        \"\"\"
        Enregistre la configuration dans un fichier
        
        Args:
            file_path (str): Chemin vers le fichier
            
        Returns:
            bool: True si réussi, False sinon
        \"\"\"
        try:
            # Créer le dossier parent si nécessaire
            dir_path = os.path.dirname(file_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path)
                
            with open(file_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
                
            return True
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de la configuration : {e}")
            return False
"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "config.py")
    create_file(config_path, content)

def fix_login_screen_py():
    """Corrige le fichier login_screen.py"""
    content = """# -*- coding: utf-8 -*-
\"\"\"
Écran de connexion de l'application HL7 Messenger.
\"\"\"
import tkinter as tk
from tkinter import ttk, messagebox
import logging

class LoginScreen(ttk.Frame):
    \"\"\"Écran de connexion pour l'application HL7 Messenger\"\"\"

    def __init__(self, parent, on_login_callback):
        super().__init__(parent)
        self.logger = logging.getLogger("HL7Messenger.LoginScreen")
        self.parent = parent
        self.on_login_callback = on_login_callback

        # Liste des départements disponibles
        self.departments = [
            "ADMISSION",
            "LABORATORY",
            "RADIOLOGY",
            "PHARMACY"
        ]
        
        # Mode de fonctionnement (normal ou démo)
        self.modes = ["Normal", "Démo"]

        # Créer l'interface
        self._create_widgets()

        # Activer la touche entrée
        self.bind_all("<Return>", lambda event: self._on_login())

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)  # Augmenté pour ajouter le sélecteur de mode

        login_frame = ttk.Frame(main_frame, padding=20)
        login_frame.grid(row=1, column=1, sticky="nsew")

        title_label = ttk.Label(login_frame, text="HL7 Messenger - Connexion", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        username_label = ttk.Label(login_frame, text="Nom d'utilisateur:")
        username_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=1, column=1, sticky="ew", pady=(0, 5))
        username_entry.focus_set()

        # Password
        password_label = ttk.Label(login_frame, text="Mot de passe:")
        password_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*", width=30)
        password_entry.grid(row=2, column=1, sticky="ew", pady=(0, 5))

        # Department
        department_label = ttk.Label(login_frame, text="Département:")
        department_label.grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.department_var = tk.StringVar()
        department_combo = ttk.Combobox(login_frame, textvariable=self.department_var,
                                        values=self.departments, state="readonly", width=28)
        department_combo.grid(row=3, column=1, sticky="ew", pady=(0, 5))
        department_combo.current(0)
        
        # Mode (Normal/Démo)
        mode_label = ttk.Label(login_frame, text="Mode:")
        mode_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.mode_var = tk.StringVar(value="Normal")
        mode_frame = ttk.Frame(login_frame)
        mode_frame.grid(row=4, column=1, sticky="w", pady=(0, 5))
        
        for i, mode in enumerate(self.modes):
            rb = ttk.Radiobutton(mode_frame, text=mode, variable=self.mode_var, value=mode)
            rb.pack(side=tk.LEFT, padx=10)

        # Error message
        self.error_var = tk.StringVar()
        error_label = ttk.Label(login_frame, textvariable=self.error_var, style="Error.TLabel")
        error_label.grid(row=5, column=0, columnspan=2, pady=(5, 0))

        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))

        login_button = ttk.Button(button_frame, text="Connexion", command=self._on_login, width=15)
        login_button.pack(side=tk.LEFT, padx=5)

        exit_button = ttk.Button(button_frame, text="Quitter", command=self._on_exit, width=15)
        exit_button.pack(side=tk.LEFT, padx=5)

    def _on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        department = self.department_var.get()
        mode = self.mode_var.get()
        
        # Détermine si on est en mode démo
        is_demo = (mode == "Démo")

        if not username:
            self.error_var.set("Veuillez entrer un nom d'utilisateur")
            return

        if not password:
            self.error_var.set("Veuillez entrer un mot de passe")
            return

        if not department or department not in self.departments:
            self.error_var.set("Veuillez sélectionner un département valide")
            return

        self.logger.info(f"Tentative de connexion: {username} / {department} / Mode: {mode}")
        print(f"Tentative de connexion: {username} / {department} / Mode: {mode}")

        # IMPORTANT: Nous passons seulement 2 arguments au callback comme attendu
        self.on_login_callback(username, department)

    def _on_exit(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.parent.quit()
            
    def refresh(self):
        \"\"\"Rafraîchit l'interface (appelé par F5)\"\"\"
        pass  # Rien à faire pour l'écran de login

    def cancel(self):
        \"\"\"Annule l'opération en cours (appelé par Escape)\"\"\"
        # Effacer les champs
        self.username_var.set("")
        self.password_var.set("")
        self.error_var.set("")

    def handle_return(self, event=None):
        \"\"\"Gère la touche Entrée de manière contextualisée\"\"\"
        # Si le focus est sur un champ, aller au suivant
        current = self.focus_get()
        
        if current and current.winfo_class() == 'TEntry':
            # Si c'est le dernier champ, valider
            if current == self.winfo_children()[0].winfo_children()[1].winfo_children()[5]:
                self._on_login()
            else:
                # Sinon, passer au champ suivant
                current.tk_focusNext().focus()
            return "break"
        
        # Par défaut, valider
        self._on_login()
        return "break"
"""
    login_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "login_screen.py")
    create_file(login_path, content)

def main():
    """Point d'entrée du script"""
    print("====================================================")
    print("  Script de correction HL7 Messenger")
    print("====================================================")
    print("Ce script va corriger les problèmes de l'application.")
    print("Assurez-vous d'avoir sauvegardé vos fichiers avant de continuer.")
    print("====================================================")
    
    # Créer le dossier de logs si nécessaire
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    create_dir(log_dir)
    
    # Créer le fichier de configuration
    create_config()
    
    # Corriger les fichiers
    fix_config_py()
    fix_login_screen_py()
    
    print("====================================================")
    print("  Corrections terminées")
    print("====================================================")
    print("Vous pouvez maintenant lancer l'application avec :")
    print("python -m app.main")
    print("====================================================")

if __name__ == "__main__":
    main()