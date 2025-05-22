#!/usr/bin/env python3

def fix_login_screen():
    """Supprime les lignes problématiques de login_screen.py"""
    print("Correction de login_screen.py...")
    
    file_path = "app/ui/login_screen.py"
    
    try:
        # Lire le fichier ligne par ligne
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Identifier et supprimer les lignes problématiques
        fixed_lines = []
        remove_next_lines = False
        
        for line in lines:
            # Si la ligne contient self._setup_combobox_behavior(), la supprimer
            if "_setup_combobox_behavior()" in line:
                print(f"Suppression de la ligne problématique: {line.strip()}")
                continue
            # Si la ligne contient une fonction _setup_combobox_behavior, supprimer la méthode entière
            if "def _setup_combobox_behavior" in line:
                remove_next_lines = True
                print("Début de suppression de la méthode _setup_combobox_behavior")
                continue
            # Si on supprime des lignes et qu'on trouve une nouvelle méthode, arrêter la suppression
            if remove_next_lines and line.strip().startswith("def "):
                remove_next_lines = False
                print("Fin de suppression de la méthode")
            
            # Si on ne supprime pas cette ligne, l'ajouter
            if not remove_next_lines:
                fixed_lines.append(line)
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("✅ Fichier login_screen.py corrigé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {str(e)}")
        
        # Tentative de restauration depuis la sauvegarde originale
        try:
            # Si nous avons une sauvegarde, la restaurer
            with open(file_path + ".original", 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            print("✅ Fichier restauré depuis la sauvegarde originale")
            
        except Exception as e2:
            print(f"❌ Erreur lors de la restauration : {str(e2)}")
            print("Tentative de recréation complète du fichier...")
            
            # Contenu de base du fichier login_screen.py
            basic_content = """# -*- coding: utf-8 -*-
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
        main_frame.rowconfigure(6, weight=1)

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

        # Error message
        self.error_var = tk.StringVar()
        error_label = ttk.Label(login_frame, textvariable=self.error_var, style="Error.TLabel")
        error_label.grid(row=4, column=0, columnspan=2, pady=(5, 0))

        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))

        login_button = ttk.Button(button_frame, text="Connexion", command=self._on_login, width=15)
        login_button.pack(side=tk.LEFT, padx=5)

        exit_button = ttk.Button(button_frame, text="Quitter", command=self._on_exit, width=15)
        exit_button.pack(side=tk.LEFT, padx=5)

    def _on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        department = self.department_var.get()

        if not username:
            self.error_var.set("Veuillez entrer un nom d'utilisateur")
            return

        if not password:
            self.error_var.set("Veuillez entrer un mot de passe")
            return

        if not department or department not in self.departments:
            self.error_var.set("Veuillez sélectionner un département valide")
            return

        self.logger.info(f"Tentative de connexion: {username} / {department}")
        print(f"Tentative de connexion: {username} / {department}")

        self.on_login_callback(username, department)

    def _on_exit(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.parent.quit()"""
            
            # Écrire le fichier de base
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(basic_content)
            
            print("✅ Fichier login_screen.py recréé avec le contenu de base")
    
    return True

if __name__ == "__main__":
    fix_login_screen()