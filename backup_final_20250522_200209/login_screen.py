# -*- coding: utf-8 -*-
"""
Écran de connexion de l'application HL7 Messenger - VERSION FINALE SANS ERREURS
Correction complète des problèmes de widgets détruits et événements
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

class LoginScreen(ttk.Frame):
    """Écran de connexion pour l'application HL7 Messenger - Version sans erreurs"""

    def __init__(self, parent, on_login_callback):
        super().__init__(parent)
        self.logger = logging.getLogger("HL7Messenger.LoginScreen")
        self.parent = parent
        self.on_login_callback = on_login_callback
        
        # État interne pour éviter les erreurs
        self.is_destroyed = False
        self.processing = False

        # Liste des départements disponibles
        self.departments = [
            "ADMISSION",
            "LABORATORY", 
            "RADIOLOGY",
            "PHARMACY"
        ]

        # Variables pour les champs
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.department_var = tk.StringVar(value=self.departments[0])
        self.error_var = tk.StringVar()

        # Widgets (pour nettoyage)
        self.widgets = {}

        # Créer l'interface
        self._create_widgets()
        self._setup_keyboard_navigation()

    def _create_widgets(self):
        """Crée tous les widgets de l'interface"""
        try:
            # Frame principal avec padding
            main_frame = ttk.Frame(self, padding="30 20 30 20")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Configuration de la grille pour centrer le contenu
            main_frame.columnconfigure(0, weight=1)
            main_frame.columnconfigure(2, weight=1)
            main_frame.rowconfigure(0, weight=1)
            main_frame.rowconfigure(6, weight=1)

            # Frame de connexion centré
            login_frame = ttk.Frame(main_frame, padding="30 25 30 25", relief="raised", borderwidth=2)
            login_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

            # Configuration de la grille du login_frame
            login_frame.columnconfigure(1, weight=1)

            # TITRE
            title_label = ttk.Label(
                login_frame, 
                text="🏥 HL7 Messenger", 
                font=("Helvetica", 20, "bold"),
                foreground="#2c5282"
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="ew")
            self.widgets['title'] = title_label

            subtitle_label = ttk.Label(
                login_frame,
                text="Connexion Sécurisée",
                font=("Helvetica", 12),
                foreground="#4a5568"
            )
            subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
            self.widgets['subtitle'] = subtitle_label

            # CHAMP USERNAME
            username_label = ttk.Label(login_frame, text="👤 Nom d'utilisateur:", font=("Helvetica", 11))
            username_label.grid(row=2, column=0, sticky="w", pady=(10, 5), padx=(0, 10))
            self.widgets['username_label'] = username_label
            
            self.username_entry = ttk.Entry(
                login_frame, 
                textvariable=self.username_var, 
                width=25,
                font=("Helvetica", 11)
            )
            self.username_entry.grid(row=2, column=1, sticky="ew", pady=(10, 5))
            self.widgets['username_entry'] = self.username_entry

            # CHAMP PASSWORD
            password_label = ttk.Label(login_frame, text="🔒 Mot de passe:", font=("Helvetica", 11))
            password_label.grid(row=3, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
            self.widgets['password_label'] = password_label
            
            self.password_entry = ttk.Entry(
                login_frame, 
                textvariable=self.password_var, 
                show="*", 
                width=25,
                font=("Helvetica", 11)
            )
            self.password_entry.grid(row=3, column=1, sticky="ew", pady=(5, 5))
            self.widgets['password_entry'] = self.password_entry

            # DÉPARTEMENT
            department_label = ttk.Label(login_frame, text="🏢 Département:", font=("Helvetica", 11))
            department_label.grid(row=4, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
            self.widgets['department_label'] = department_label
            
            self.department_combo = ttk.Combobox(
                login_frame, 
                textvariable=self.department_var,
                values=self.departments, 
                state="readonly",
                width=23,
                font=("Helvetica", 11)
            )
            self.department_combo.grid(row=4, column=1, sticky="ew", pady=(5, 5))
            self.department_combo.current(0)
            self.widgets['department_combo'] = self.department_combo

            # MESSAGE D'ERREUR
            self.error_label = ttk.Label(
                login_frame, 
                textvariable=self.error_var, 
                foreground="red",
                font=("Helvetica", 10),
                wraplength=300
            )
            self.error_label.grid(row=5, column=0, columnspan=2, pady=(15, 5))
            self.widgets['error_label'] = self.error_label

            # BOUTONS
            button_frame = ttk.Frame(login_frame)
            button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
            self.widgets['button_frame'] = button_frame

            self.login_button = ttk.Button(
                button_frame, 
                text="🚀 Connexion", 
                command=self._safe_login,  # Utiliser la version sécurisée
                width=18
            )
            self.login_button.pack(side=tk.LEFT, padx=(0, 10))
            self.widgets['login_button'] = self.login_button

            self.exit_button = ttk.Button(
                button_frame, 
                text="❌ Quitter", 
                command=self._safe_exit,  # Utiliser la version sécurisée
                width=18
            )
            self.exit_button.pack(side=tk.LEFT)
            self.widgets['exit_button'] = self.exit_button

            # INFO UTILISATEUR
            info_label = ttk.Label(
                login_frame,
                text="💡 Astuce: Utilisez Tab pour naviguer, Entrée pour valider",
                font=("Helvetica", 9),
                foreground="#718096"
            )
            info_label.grid(row=7, column=0, columnspan=2, pady=(15, 0))
            self.widgets['info_label'] = info_label

        except Exception as e:
            print(f"❌ Erreur création widgets login: {e}")

    def _setup_keyboard_navigation(self):
        """Configure la navigation clavier de manière sécurisée"""
        try:
            # Focus initial sur le champ username
            self.after(100, self._safe_focus_username)

            # Bind des événements de manière sécurisée
            self.bind("<Return>", self._safe_handle_enter)
            self.bind("<KP_Enter>", self._safe_handle_enter)
            self.bind("<Escape>", self._safe_handle_escape)
            
        except Exception as e:
            print(f"❌ Erreur setup navigation: {e}")

    def _safe_focus_username(self):
        """Met le focus sur le champ username de manière sécurisée"""
        try:
            if not self.is_destroyed and self.username_entry.winfo_exists():
                self.username_entry.focus_set()
        except:
            pass

    def _safe_handle_enter(self, event=None):
        """Gère la touche Entrée de manière sécurisée"""
        try:
            if not self.is_destroyed and not self.processing:
                self._safe_login()
        except Exception as e:
            print(f"❌ Erreur handle enter: {e}")

    def _safe_handle_escape(self, event=None):
        """Gère la touche Échap de manière sécurisée"""
        try:
            if not self.is_destroyed:
                self._safe_exit()
        except Exception as e:
            print(f"❌ Erreur handle escape: {e}")

    def _validate_inputs(self):
        """Validation des entrées utilisateur"""
        try:
            username = self.username_var.get().strip()
            password = self.password_var.get().strip()
            department = self.department_var.get().strip()

            # Effacer les erreurs précédentes
            self.error_var.set("")

            if not username:
                self.error_var.set("⚠️ Le nom d'utilisateur est requis")
                return False

            if len(username) < 2:
                self.error_var.set("⚠️ Le nom d'utilisateur doit contenir au moins 2 caractères")
                return False

            if not password:
                self.error_var.set("⚠️ Le mot de passe est requis")
                return False

            if len(password) < 3:
                self.error_var.set("⚠️ Le mot de passe doit contenir au moins 3 caractères")
                return False

            if not department or department not in self.departments:
                self.error_var.set("⚠️ Veuillez sélectionner un département valide")
                return False

            return True
            
        except Exception as e:
            print(f"❌ Erreur validation: {e}")
            return False

    def _safe_login(self):
        """Gère la connexion de manière sécurisée"""
        if self.is_destroyed or self.processing:
            return
            
        try:
            self.processing = True
            print("🔄 Tentative de connexion...")
            
            # Désactiver le bouton temporairement (avec vérification)
            if self._widget_exists('login_button'):
                self.login_button.configure(state="disabled", text="⏳ Connexion...")
            
            # Validation des entrées
            if not self._validate_inputs():
                return

            # Récupérer les valeurs
            username = self.username_var.get().strip()
            password = self.password_var.get().strip()
            department = self.department_var.get().strip()

            # Log de la tentative
            self.logger.info(f"Tentative de connexion: {username} / {department}")
            print(f"✅ Validation réussie: {username} / {department}")

            # Appeler le callback de connexion
            if self.on_login_callback:
                self.on_login_callback(username, department)
            
            print(f"🎉 Connexion réussie pour {username}")

        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            self.logger.error(f"Erreur lors de la connexion: {str(e)}")
            if not self.is_destroyed:
                self.error_var.set(f"⚠️ Erreur: {str(e)}")
            
        finally:
            self.processing = False
            # Réactiver le bouton (avec vérification)
            if self._widget_exists('login_button'):
                try:
                    self.login_button.configure(state="normal", text="🚀 Connexion")
                except:
                    pass

    def _safe_exit(self):
        """Gère la fermeture de manière sécurisée"""
        if self.is_destroyed:
            return
            
        try:
            result = messagebox.askyesno(
                "Confirmation", 
                "Voulez-vous vraiment quitter l'application HL7 Messenger ?",
                icon="question"
            )
            if result:
                self.logger.info("Application fermée par l'utilisateur")
                if self.parent:
                    self.parent.quit()
                    
        except Exception as e:
            print(f"❌ Erreur fermeture: {e}")

    def _widget_exists(self, widget_name):
        """Vérifie si un widget existe encore"""
        try:
            widget = self.widgets.get(widget_name)
            return widget and widget.winfo_exists()
        except:
            return False

    def destroy(self):
        """Destruction sécurisée du widget"""
        try:
            self.is_destroyed = True
            
            # Nettoyer les bindings
            self.unbind("<Return>")
            self.unbind("<KP_Enter>") 
            self.unbind("<Escape>")
            
            # Destruction normale
            super().destroy()
            
        except Exception as e:
            print(f"❌ Erreur destruction login: {e}")

    def reset_form(self):
        """Remet à zéro le formulaire de manière sécurisée"""
        try:
            if not self.is_destroyed:
                self.username_var.set("")
                self.password_var.set("")
                self.department_var.set(self.departments[0])
                self.error_var.set("")
                if self._widget_exists('username_entry'):
                    self.username_entry.focus_set()
        except Exception as e:
            print(f"❌ Erreur reset form: {e}")