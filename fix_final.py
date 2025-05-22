#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction complète pour le projet HL7 Messenger
Résout tous les problèmes de navigation, validation et fluidité
"""
import os
import shutil
import sys
from datetime import datetime

def backup_files():
    """Crée une sauvegarde des fichiers actuels"""
    print("📦 Création d'une sauvegarde...")
    
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    files_to_backup = [
        "app/ui/login_screen.py",
        "app/ui/dashboard.py", 
        "app/ui/departments/admission.py",
        "app/ui/departments/laboratory.py",
        "app/ui/departments/radiology.py",
        "app/ui/departments/pharmacy.py",
        "app/ui/history_viewer.py"
    ]
    
    os.makedirs(backup_dir, exist_ok=True)
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            print(f"✅ Sauvegardé: {file_path} -> {backup_path}")
    
    print(f"📦 Sauvegarde créée dans: {backup_dir}")
    return backup_dir

def write_fixed_login_screen():
    """Écrit le fichier login_screen.py corrigé"""
    content = '''# -*- coding: utf-8 -*-
"""
Écran de connexion de l'application HL7 Messenger - VERSION CORRIGÉE DÉFINITIVE
Tous les problèmes de validation, menu déroulant et navigation clavier résolus
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

class LoginScreen(ttk.Frame):
    """Écran de connexion pour l'application HL7 Messenger - Version corrigée"""

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

        # Variables pour les champs
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.department_var = tk.StringVar(value=self.departments[0])  # Valeur par défaut
        self.error_var = tk.StringVar()

        # Créer l'interface
        self._create_widgets()
        self._setup_keyboard_navigation()

    def _create_widgets(self):
        """Crée tous les widgets de l'interface avec un style moderne"""
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

        subtitle_label = ttk.Label(
            login_frame,
            text="Connexion Sécurisée",
            font=("Helvetica", 12),
            foreground="#4a5568"
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # CHAMP USERNAME
        username_label = ttk.Label(login_frame, text="👤 Nom d'utilisateur:", font=("Helvetica", 11))
        username_label.grid(row=2, column=0, sticky="w", pady=(10, 5), padx=(0, 10))
        
        self.username_entry = ttk.Entry(
            login_frame, 
            textvariable=self.username_var, 
            width=25,
            font=("Helvetica", 11)
        )
        self.username_entry.grid(row=2, column=1, sticky="ew", pady=(10, 5))

        # CHAMP PASSWORD
        password_label = ttk.Label(login_frame, text="🔒 Mot de passe:", font=("Helvetica", 11))
        password_label.grid(row=3, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
        
        self.password_entry = ttk.Entry(
            login_frame, 
            textvariable=self.password_var, 
            show="*", 
            width=25,
            font=("Helvetica", 11)
        )
        self.password_entry.grid(row=3, column=1, sticky="ew", pady=(5, 5))

        # DÉPARTEMENT - MENU DÉROULANT AMÉLIORÉ
        department_label = ttk.Label(login_frame, text="🏢 Département:", font=("Helvetica", 11))
        department_label.grid(row=4, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
        
        # Style pour le combobox
        style = ttk.Style()
        style.configure("Modern.TCombobox", 
                       fieldbackground="white",
                       selectbackground="#4299e1",
                       selectforeground="white")
        
        self.department_combo = ttk.Combobox(
            login_frame, 
            textvariable=self.department_var,
            values=self.departments, 
            state="readonly",  # Empêche la saisie manuelle
            width=23,
            font=("Helvetica", 11),
            style="Modern.TCombobox"
        )
        self.department_combo.grid(row=4, column=1, sticky="ew", pady=(5, 5))
        self.department_combo.current(0)  # Sélectionne le premier élément par défaut

        # MESSAGE D'ERREUR
        self.error_label = ttk.Label(
            login_frame, 
            textvariable=self.error_var, 
            foreground="red",
            font=("Helvetica", 10),
            wraplength=300
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=(15, 5))

        # BOUTONS
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))

        # Style pour les boutons
        style.configure("Success.TButton",
                       background="#48bb78",
                       foreground="white",
                       font=("Helvetica", 11, "bold"))
        
        style.configure("Secondary.TButton",
                       background="#cbd5e0",
                       foreground="#2d3748",
                       font=("Helvetica", 11))

        self.login_button = ttk.Button(
            button_frame, 
            text="🚀 Connexion", 
            command=self._on_login,
            width=18,
            style="Success.TButton"
        )
        self.login_button.pack(side=tk.LEFT, padx=(0, 10))

        self.exit_button = ttk.Button(
            button_frame, 
            text="❌ Quitter", 
            command=self._on_exit,
            width=18,
            style="Secondary.TButton"
        )
        self.exit_button.pack(side=tk.LEFT)

        # INFO UTILISATEUR (aide)
        info_label = ttk.Label(
            login_frame,
            text="💡 Astuce: Utilisez Tab pour naviguer, Entrée pour valider",
            font=("Helvetica", 9),
            foreground="#718096"
        )
        info_label.grid(row=7, column=0, columnspan=2, pady=(15, 0))

    def _setup_keyboard_navigation(self):
        """Configure la navigation clavier complète"""
        # Focus initial sur le champ username
        self.after(100, lambda: self.username_entry.focus_set())

        # RACCOURCIS CLAVIER
        # Entrée = valider la connexion
        self.bind_all("<Return>", self._handle_enter_key)
        self.bind_all("<KP_Enter>", self._handle_enter_key)  # Entrée du pavé numérique
        
        # Échap = quitter
        self.bind_all("<Escape>", lambda e: self._on_exit())
        
        # Tab = navigation entre champs
        self.username_entry.bind("<Tab>", lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Tab>", lambda e: self.department_combo.focus_set())
        self.department_combo.bind("<Tab>", lambda e: self.login_button.focus_set())
        
        # Navigation flèches dans le combobox
        self.department_combo.bind("<Up>", self._combo_up)
        self.department_combo.bind("<Down>", self._combo_down)

    def _handle_enter_key(self, event=None):
        """Gère la touche Entrée de manière intelligente"""
        focused_widget = self.focus_get()
        
        # Si on est sur le bouton quitter, quitter
        if focused_widget == self.exit_button:
            self._on_exit()
        # Sinon, tenter la connexion
        else:
            self._on_login()

    def _combo_up(self, event=None):
        """Navigation vers le haut dans le combobox"""
        current = self.department_combo.current()
        if current > 0:
            self.department_combo.current(current - 1)

    def _combo_down(self, event=None):
        """Navigation vers le bas dans le combobox"""
        current = self.department_combo.current()
        if current < len(self.departments) - 1:
            self.department_combo.current(current + 1)

    def _validate_inputs(self):
        """Validation complète des entrées utilisateur"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        department = self.department_var.get().strip()

        # Effacer les erreurs précédentes
        self.error_var.set("")

        # Validation du nom d'utilisateur
        if not username:
            self.error_var.set("⚠️ Le nom d'utilisateur est requis")
            self.username_entry.focus_set()
            return False

        if len(username) < 2:
            self.error_var.set("⚠️ Le nom d'utilisateur doit contenir au moins 2 caractères")
            self.username_entry.focus_set()
            return False

        # Validation du mot de passe
        if not password:
            self.error_var.set("⚠️ Le mot de passe est requis")
            self.password_entry.focus_set()
            return False

        if len(password) < 3:
            self.error_var.set("⚠️ Le mot de passe doit contenir au moins 3 caractères")
            self.password_entry.focus_set()
            return False

        # Validation du département
        if not department or department not in self.departments:
            self.error_var.set("⚠️ Veuillez sélectionner un département valide")
            self.department_combo.focus_set()
            return False

        return True

    def _on_login(self):
        """Gère la connexion avec validation complète"""
        print("🔄 Tentative de connexion...")
        
        # Désactiver temporairement le bouton pour éviter les clics multiples
        self.login_button.configure(state="disabled", text="⏳ Connexion...")
        
        try:
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
            self.on_login_callback(username, department)
            
            print(f"🎉 Connexion réussie pour {username}")

        except Exception as e:
            self.logger.error(f"Erreur lors de la connexion: {str(e)}")
            self.error_var.set(f"⚠️ Erreur de connexion: {str(e)}")
            
        finally:
            # Réactiver le bouton
            self.login_button.configure(state="normal", text="🚀 Connexion")

    def _on_exit(self):
        """Gère la fermeture de l'application avec confirmation"""
        result = messagebox.askyesno(
            "Confirmation", 
            "Voulez-vous vraiment quitter l'application HL7 Messenger ?",
            icon="question"
        )
        if result:
            self.logger.info("Application fermée par l'utilisateur")
            self.parent.quit()
'''
    
    with open("app/ui/login_screen.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ login_screen.py corrigé")

def write_fixed_dashboard():
    """Écrit le fichier dashboard.py corrigé"""
    content = '''"""
Tableau de bord principal de l'application HL7 Messenger - VERSION CORRIGÉE
Tous les problèmes de chargement et de fluidité résolus
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime
import threading
import time

# Import des modules départements avec gestion d'erreur
try:
    from app.ui.departments.admission import AdmissionFrame
    from app.ui.departments.laboratory import LaboratoryFrame
    from app.ui.departments.radiology import RadiologyFrame
    from app.ui.departments.pharmacy import PharmacyFrame
    from app.ui.history_viewer import HistoryViewer
except ImportError as e:
    print(f"⚠️ Erreur d'import: {e}")

class Dashboard(ttk.Frame):
    """Tableau de bord principal de l'application - Version corrigée et optimisée"""

    def __init__(self, parent, username, department, mllp_client, message_builder, config, on_logout_callback):
        super().__init__(parent)
        self.logger = logging.getLogger("HL7Messenger.Dashboard")
        self.parent = parent
        self.username = username
        self.department = department
        self.mllp_client = mllp_client
        self.message_builder = message_builder
        self.config = config
        self.on_logout_callback = on_logout_callback

        # État interne
        self.status_message = ""
        self.is_loading = False
        self.dept_frame = None

        print(f"🚀 Initialisation du Dashboard pour {username} dans {department}")
        
        # Créer l'interface avec chargement progressif
        self._create_interface_progressive()

    def _create_interface_progressive(self):
        """Crée l'interface de manière progressive pour éviter les blocages"""
        # Étape 1: Structure de base
        self._create_base_structure()
        
        # Étape 2: Chargement asynchrone du contenu
        self.after(100, self._load_content_async)

    def _create_base_structure(self):
        """Crée la structure de base du dashboard"""
        try:
            # Frame principal
            self.main_frame = ttk.Frame(self)
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Indicateur de chargement
            self.loading_frame = ttk.Frame(self.main_frame)
            self.loading_frame.pack(fill=tk.BOTH, expand=True)
            
            loading_label = ttk.Label(
                self.loading_frame, 
                text="🔄 Chargement du tableau de bord...",
                font=("Helvetica", 14),
                foreground="#4299e1"
            )
            loading_label.pack(expand=True)
            
            # Barre de progression
            self.progress_bar = ttk.Progressbar(
                self.loading_frame, 
                mode="indeterminate",
                length=300
            )
            self.progress_bar.pack(pady=20)
            self.progress_bar.start(10)
            
            print("✅ Structure de base créée")
            
        except Exception as e:
            print(f"❌ Erreur création structure de base: {e}")
            self._show_error_interface(str(e))

    def _load_content_async(self):
        """Charge le contenu de manière asynchrone"""
        def load_in_thread():
            try:
                print("🔄 Chargement du contenu...")
                time.sleep(0.5)  # Petite pause pour fluidité
                
                # Charger dans le thread principal
                self.after(0, self._create_main_interface)
                
            except Exception as e:
                print(f"❌ Erreur chargement async: {e}")
                self.after(0, lambda: self._show_error_interface(str(e)))
        
        # Lancer dans un thread séparé
        thread = threading.Thread(target=load_in_thread, daemon=True)
        thread.start()

    def _create_main_interface(self):
        """Crée l'interface principale du dashboard"""
        try:
            # Arrêter et cacher l'indicateur de chargement
            self.progress_bar.stop()
            self.loading_frame.destroy()
            
            # Créer l'interface principale
            self._create_top_bar()
            self._create_notification_system()
            self._create_content_area()
            self._create_status_bar()
            
            print("✅ Interface principale créée avec succès")
            
        except Exception as e:
            print(f"❌ Erreur création interface principale: {e}")
            self._show_error_interface(str(e))

    def _create_top_bar(self):
        """Crée la barre supérieure avec navigation"""
        top_bar = ttk.Frame(self.main_frame, padding="10 5")
        top_bar.pack(fill=tk.X, expand=False)
        
        # Titre
        title_label = ttk.Label(
            top_bar,
            text="🏥 HL7 Messenger",
            font=("Helvetica", 18, "bold"),
            foreground="#2c5282"
        )
        title_label.pack(side=tk.LEFT)
        
        # Frame utilisateur à droite
        user_frame = ttk.Frame(top_bar)
        user_frame.pack(side=tk.RIGHT)
        
        # Bouton Historique
        history_button = ttk.Button(
            user_frame,
            text="📊 Historique",
            command=self._show_history,
            width=12
        )
        history_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Info utilisateur
        dept_names = {
            "ADMISSION": "👥 Admissions",
            "LABORATORY": "🧪 Laboratoire", 
            "RADIOLOGY": "📸 Radiologie",
            "PHARMACY": "💊 Pharmacie"
        }
        dept_text = dept_names.get(self.department, self.department)
        
        user_info = ttk.Label(
            user_frame,
            text=f"👤 {self.username} | {dept_text}",
            font=("Helvetica", 10)
        )
        user_info.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton déconnexion
        logout_button = ttk.Button(
            user_frame,
            text="🚪 Déconnexion",
            command=self._on_logout,
            width=12
        )
        logout_button.pack(side=tk.LEFT)

    def _create_notification_system(self):
        """Crée le système de notifications"""
        self.notification_frame = ttk.Frame(self.main_frame)
        
        self.notification_var = tk.StringVar()
        self.notification_label = ttk.Label(
            self.notification_frame,
            textvariable=self.notification_var,
            padding="10 5",
            font=("Helvetica", 10)
        )
        self.notification_label.pack(fill=tk.X)

    def _create_content_area(self):
        """Crée la zone de contenu principal"""
        # Séparateur
        separator = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=5)
        
        # Zone de contenu
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Charger le département
        self._load_department_frame()

    def _load_department_frame(self):
        """Charge le frame spécifique au département"""
        print(f"🔄 Chargement du département: {self.department}")
        
        try:
            if self.department == "ADMISSION":
                self.dept_frame = AdmissionFrame(
                    self.content_frame, 
                    self.mllp_client, 
                    self.message_builder, 
                    self._on_message_sent
                )
            elif self.department == "LABORATORY":
                self.dept_frame = LaboratoryFrame(
                    self.content_frame,
                    self.mllp_client,
                    self.message_builder,
                    self._on_message_sent
                )
            elif self.department == "RADIOLOGY":
                self.dept_frame = RadiologyFrame(
                    self.content_frame,
                    self.mllp_client,
                    self.message_builder,
                    self._on_message_sent
                )
            elif self.department == "PHARMACY":
                self.dept_frame = PharmacyFrame(
                    self.content_frame,
                    self.mllp_client,
                    self.message_builder,
                    self._on_message_sent
                )
            else:
                # Département non supporté
                self._create_fallback_interface()
                return
            
            # Afficher le frame
            self.dept_frame.pack(fill=tk.BOTH, expand=True)
            print(f"✅ Module {self.department} chargé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur chargement département {self.department}: {e}")
            self._create_error_department_interface(str(e))

    def _create_fallback_interface(self):
        """Interface de secours pour départements non supportés"""
        fallback_frame = ttk.LabelFrame(
            self.content_frame,
            text=f"Département {self.department}",
            padding="20"
        )
        fallback_frame.pack(fill=tk.BOTH, expand=True)
        
        message = ttk.Label(
            fallback_frame,
            text=f"⚠️ Le module pour le département {self.department} n'est pas encore disponible.",
            font=("Helvetica", 12),
            foreground="#e68a00"
        )
        message.pack(expand=True)

    def _create_error_department_interface(self, error_msg):
        """Interface d'erreur pour problèmes de chargement"""
        error_frame = ttk.LabelFrame(
            self.content_frame,
            text="❌ Erreur de chargement",
            padding="20"
        )
        error_frame.pack(fill=tk.BOTH, expand=True)
        
        error_label = ttk.Label(
            error_frame,
            text=f"Impossible de charger le module {self.department}",
            font=("Helvetica", 12, "bold"),
            foreground="#dc2626"
        )
        error_label.pack()
        
        detail_label = ttk.Label(
            error_frame,
            text=f"Détails: {error_msg}",
            font=("Helvetica", 9),
            foreground="#666666",
            wraplength=400
        )
        detail_label.pack(pady=(10, 0))

    def _create_status_bar(self):
        """Crée la barre de statut"""
        # Séparateur
        separator = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_bar = ttk.Frame(self.main_frame, padding="5 3")
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Statut à gauche
        self.status_var = tk.StringVar(value="✅ Prêt")
        status_label = ttk.Label(
            status_bar,
            textvariable=self.status_var,
            font=("Helvetica", 9)
        )
        status_label.pack(side=tk.LEFT)
        
        # Horloge à droite
        self.clock_var = tk.StringVar()
        clock_label = ttk.Label(
            status_bar,
            textvariable=self.clock_var,
            font=("Helvetica", 9)
        )
        clock_label.pack(side=tk.RIGHT)
        
        # Démarrer l'horloge
        self._update_clock()

    def _update_clock(self):
        """Met à jour l'horloge"""
        try:
            current_time = datetime.now().strftime("🕐 %d/%m/%Y %H:%M:%S")
            self.clock_var.set(current_time)
            self.after(1000, self._update_clock)
        except Exception as e:
            print(f"Erreur horloge: {e}")

    def _on_message_sent(self, success, message):
        """Callback pour les messages envoyés par les départements"""
        if success:
            self.show_notification(f"✅ {message}", "success")
        else:
            self.show_notification(f"❌ {message}", "error")

    def show_notification(self, message, notification_type="info"):
        """Affiche une notification avec style"""
        self.notification_var.set(message)
        
        # Couleurs selon le type
        colors = {
            "success": {"bg": "#d4edda", "fg": "#155724"},
            "error": {"bg": "#f8d7da", "fg": "#721c24"},
            "info": {"bg": "#cce7ff", "fg": "#004085"}
        }
        
        color = colors.get(notification_type, colors["info"])
        self.notification_label.configure(
            background=color["bg"],
            foreground=color["fg"]
        )
        
        # Afficher la notification
        self.notification_frame.pack(fill=tk.X, pady=(5, 0), after=self.main_frame.winfo_children()[0])
        
        # Cacher après 5 secondes
        self.after(5000, self._hide_notification)

    def _hide_notification(self):
        """Cache la notification"""
        self.notification_frame.pack_forget()

    def _on_logout(self):
        """Gère la déconnexion avec confirmation"""
        result = messagebox.askyesno(
            "Confirmation de déconnexion",
            f"👤 {self.username}\\n\\nVoulez-vous vraiment vous déconnecter ?",
            icon="question"
        )
        if result:
            self.logger.info(f"Déconnexion de {self.username}")
            self.on_logout_callback()

    def _show_history(self):
        """Ouvre la fenêtre d'historique avec gestion d'erreur"""
        try:
            HistoryViewer(self)
        except Exception as e:
            error_msg = f"Impossible d'ouvrir l'historique: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Erreur", error_msg)

    def _show_error_interface(self, error_msg):
        """Affiche une interface d'erreur générale"""
        try:
            # Nettoyer tout
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        except:
            pass
        
        # Frame d'erreur
        error_frame = ttk.Frame(self.main_frame, padding="50")
        error_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icône et titre d'erreur
        error_title = ttk.Label(
            error_frame,
            text="❌ Erreur de chargement du Dashboard",
            font=("Helvetica", 16, "bold"),
            foreground="#dc2626"
        )
        error_title.pack(pady=(0, 20))
        
        # Message d'erreur
        error_detail = ttk.Label(
            error_frame,
            text=f"Une erreur est survenue:\\n\\n{error_msg}",
            font=("Helvetica", 11),
            foreground="#666666",
            wraplength=400,
            justify="center"
        )
        error_detail.pack(pady=(0, 30))
'''
    
    with open("app/ui/dashboard.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ dashboard.py corrigé")

def write_fixed_history_viewer():
    """Écrit le fichier history_viewer.py corrigé"""
    content = '''"""
Interface pour visualiser l'historique des messages HL7 - VERSION CORRIGÉE
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

class HistoryViewer(tk.Toplevel):
    """Fenêtre pour afficher l'historique des messages HL7"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("📊 Historique des messages HL7")
        self.geometry("900x600")
        self.configure(bg="white")
        
        # Centrer la fenêtre
        self.transient(parent)
        self.grab_set()
        
        try:
            from app.db.repositories.message_repository import MessageRepository
            self.repo = MessageRepository()
        except ImportError:
            self.repo = None
            print("⚠️ MessageRepository non disponible")

        self._create_widgets()
        self._load_messages()
        
        # Focus sur la fenêtre
        self.focus_set()

    def _create_widgets(self):
        """Crée les widgets de l'interface"""
        # En-tête
        header_frame = ttk.Frame(self, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="📊 Historique des Messages HL7",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Bouton refresh
        refresh_btn = ttk.Button(
            header_frame, 
            text="🔄 Rafraîchir", 
            command=self._load_messages,
            width=12
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Frame principal pour le tableau
        main_frame = ttk.Frame(self, padding="10 0 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tableau avec scrollbars
        self.tree = ttk.Treeview(
            main_frame, 
            columns=("id", "type", "patient", "source", "dest", "statut", "date"), 
            show="headings",
            height=15
        )
        
        # Configuration des colonnes
        columns_config = {
            "id": ("ID", 80),
            "type": ("Type", 100),
            "patient": ("Patient", 100),
            "source": ("Source", 120),
            "dest": ("Destination", 120),
            "statut": ("Statut", 80),
            "date": ("Date/Heure", 150)
        }
        
        for col_id, (heading, width) in columns_config.items():
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack du tableau et scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configuration de la grille
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Barre de statut
        status_frame = ttk.Frame(self, padding="10 5")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Prêt")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        # Bouton fermer
        close_btn = ttk.Button(
            status_frame,
            text="❌ Fermer",
            command=self.destroy,
            width=10
        )
        close_btn.pack(side=tk.RIGHT)

    def _load_messages(self):
        """Charge les messages récents"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.status_var.set("🔄 Chargement...")
        self.update()
        
        try:
            if self.repo:
                messages = self.repo.get_recent(50)  # Derniers 50 messages
                
                for msg in messages:
                    # Formater la date
                    date_str = msg.created_at[:19] if hasattr(msg, 'created_at') else "N/A"
                    
                    self.tree.insert("", "end", values=(
                        getattr(msg, 'id', 'N/A')[:8],  # ID tronqué
                        getattr(msg, 'message_type', 'N/A'),
                        getattr(msg, 'patient_id', 'N/A'),
                        getattr(msg, 'source', 'N/A'),
                        getattr(msg, 'destination', 'N/A'),
                        getattr(msg, 'status', 'N/A'),
                        date_str
                    ))
                
                count = len(messages)
                self.status_var.set(f"✅ {count} message(s) chargé(s)")
                
            else:
                # Données de démonstration si pas de repository
                demo_data = [
                    ("MSG001", "ADT^A01", "P12345", "ADMISSION", "HIS", "SUCCESS", "2025-05-22 10:30:15"),
                    ("MSG002", "ORU^R01", "P12346", "LAB", "HIS", "SUCCESS", "2025-05-22 11:45:22"),
                    ("MSG003", "ORM^O01", "P12347", "RADIOLOGY", "PACS", "PENDING", "2025-05-22 14:20:08"),
                ]
                
                for data in demo_data:
                    self.tree.insert("", "end", values=data)
                
                self.status_var.set("📋 Données de démonstration")
                
        except Exception as e:
            self.status_var.set(f"❌ Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de charger les messages : {e}")

def show_history_popup(parent):
    """Fonction utilitaire pour lancer la fenêtre d'historique"""
    viewer = HistoryViewer(parent)
    return viewer
'''
    
    with open("app/ui/history_viewer.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ history_viewer.py corrigé")

def apply_all_fixes():
    """Applique toutes les corrections"""
    print("🔧 Début de la correction complète du projet HL7 Messenger")
    print("=" * 60)
    
    # Créer une sauvegarde
    backup_dir = backup_files()
    
    # Appliquer toutes les corrections
    try:
        write_fixed_login_screen()
        write_fixed_dashboard() 
        write_fixed_history_viewer()
        
        print("=" * 60)
        print("✅ TOUTES LES CORRECTIONS APPLIQUÉES AVEC SUCCÈS!")
        print(f"📦 Sauvegarde créée dans: {backup_dir}")
        print("🚀 Vous pouvez maintenant lancer l'application:")
        print("   python app/main.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'application des corrections: {e}")
        print(f"📦 Fichiers de sauvegarde disponibles dans: {backup_dir}")
        return False

if __name__ == "__main__":
    apply_all_fixes()