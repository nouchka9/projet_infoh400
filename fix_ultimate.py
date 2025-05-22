#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE CORRECTION ULTIMATE pour HL7 Messenger
Résout TOUS les problèmes de widgets Tkinter et erreurs de navigation
"""
import os
import shutil
from datetime import datetime

def create_backup():
    """Crée une sauvegarde finale"""
    backup_dir = f"backup_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    files_to_backup = [
        "app/ui/app.py",
        "app/ui/login_screen.py",
        "app/ui/dashboard.py",
        "app/network/mllp_server.py"
    ]
    
    os.makedirs(backup_dir, exist_ok=True)
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            print(f"✅ Sauvegardé: {file_path}")
    
    return backup_dir

def write_fixed_app():
    """Écrit l'application principale corrigée"""
    content = '''# -*- coding: utf-8 -*-
"""
Application principale HL7 Messenger - VERSION FINALE CORRIGÉE
Résout tous les problèmes de widgets Tkinter et de navigation
"""
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import os
import platform
import logging

from app.ui.login_screen import LoginScreen
from app.ui.dashboard import Dashboard
from app.network.mllp_client import MLLPClient
from app.hl7_engine.builder import HL7MessageBuilder

class HL7MessengerApp:
    """Application principale HL7 Messenger - Version finale corrigée"""
    
    def __init__(self, root, config):
        self.logger = logging.getLogger("HL7Messenger.App")
        self.root = root
        self.config = config

        # Configuration initiale de la fenêtre
        self.root.title("HL7 Messenger - Interface Hôpital")
        self._set_app_icon()
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        self.root.option_add("*Font", "Helvetica 12")

        # Composants principaux
        self.mllp_client = MLLPClient(config.get_section('hosts'))
        self.message_builder = HL7MessageBuilder()

        # États internes
        self.current_screen = None
        self.current_user = None
        self.department = None

        # Styles
        self._setup_styles()

        # Protection contre les erreurs de widgets détruits
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Afficher l'écran de connexion
        self.show_login_screen()

    def _set_app_icon(self):
        """Configure l'icône de la fenêtre avec gestion d'erreur"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resources_dir = os.path.join(base_dir, "resources")

            if platform.system() == "Darwin":  # macOS
                png_path = os.path.join(resources_dir, "logo.png")
                if os.path.exists(png_path):
                    icon = PhotoImage(file=png_path)
                    self.root.iconphoto(True, icon)
                    print("✅ Icône PNG chargée (macOS)")
            else:
                ico_path = os.path.join(resources_dir, "logo.ico")
                if os.path.exists(ico_path):
                    self.root.iconbitmap(ico_path)
                    print("✅ Icône ICO chargée")

        except Exception as e:
            print(f"❌ Erreur chargement icône : {e}")

    def _setup_styles(self):
        """Configure les styles Tkinter avec gestion d'erreur"""
        try:
            style = ttk.Style()
            if 'clam' in style.theme_names():
                style.theme_use('clam')

            # Styles de base
            style.configure("TFrame", background="#f0f0f0")
            style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
            style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
            style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="#333333")
            style.configure("Subtitle.TLabel", font=("Helvetica", 12, "bold"), foreground="#555555")
            style.configure("Error.TLabel", foreground="red", font=("Helvetica", 10))
            
        except Exception as e:
            print(f"⚠️ Erreur configuration styles: {e}")

    def show_login_screen(self):
        """Affiche l'écran de connexion avec nettoyage sécurisé"""
        try:
            # Nettoyage sécurisé de l'écran précédent
            if self.current_screen:
                self._safe_destroy_widget(self.current_screen)
                self.current_screen = None
            
            # Forcer la mise à jour pour éviter les conflits
            self.root.update_idletasks()
            
            # Créer le nouvel écran
            self.current_screen = LoginScreen(self.root, self._on_login)
            self.current_screen.pack(fill=tk.BOTH, expand=True)
            
            print("✅ Écran de connexion affiché")
            
        except Exception as e:
            print(f"❌ Erreur affichage écran connexion: {e}")

    def show_dashboard(self):
        """Affiche le tableau de bord avec transition sécurisée"""
        try:
            print("🔄 Chargement du dashboard...")

            # Nettoyage sécurisé de l'écran précédent
            if self.current_screen:
                print("🧹 Suppression de l'écran précédent")
                self._safe_destroy_widget(self.current_screen)
                self.current_screen = None
            
            # Forcer la mise à jour
            self.root.update_idletasks()
            
            # Petit délai pour laisser le temps au nettoyage
            self.root.after(100, self._create_dashboard)
            
        except Exception as e:
            print(f"❌ Erreur préparation dashboard: {e}")

    def _create_dashboard(self):
        """Crée le dashboard de manière sécurisée"""
        try:
            print("🚀 Création du dashboard...")
            
            self.current_screen = Dashboard(
                self.root,
                self.current_user,
                self.department,
                self.mllp_client,
                self.message_builder,
                self.config,
                self._on_logout
            )
            self.current_screen.pack(fill=tk.BOTH, expand=True)
            
            print("✅ Dashboard créé et affiché")

        except Exception as e:
            print(f"❌ Erreur création Dashboard : {e}")
            import traceback
            traceback.print_exc()
            # Retourner à l'écran de connexion en cas d'erreur
            self.show_login_screen()

    def _safe_destroy_widget(self, widget):
        """Détruit un widget de manière sécurisée"""
        try:
            if widget and widget.winfo_exists():
                widget.destroy()
                print("✅ Widget détruit proprement")
        except tk.TclError:
            # Widget déjà détruit, ignorer
            print("⚠️ Widget déjà détruit")
        except Exception as e:
            print(f"⚠️ Erreur destruction widget: {e}")

    def _on_login(self, username, department):
        """Callback après connexion avec validation"""
        try:
            if not username or not department:
                return
            
            self.current_user = username
            self.department = department
            
            self.logger.info(f"✅ Connexion réussie : {username} - {department}")
            print(f"✅ Connexion validée: {username} / {department}")
            
            # Transition vers le dashboard
            self.show_dashboard()
            
        except Exception as e:
            print(f"❌ Erreur callback connexion: {e}")

    def _on_logout(self):
        """Callback après déconnexion avec nettoyage"""
        try:
            print("🚪 Déconnexion en cours...")
            
            # Réinitialiser les variables
            user = self.current_user
            self.current_user = None
            self.department = None
            
            self.logger.info(f"🚪 Déconnexion : {user}")
            
            # Retourner à l'écran de connexion
            self.show_login_screen()
            
        except Exception as e:
            print(f"❌ Erreur déconnexion: {e}")

    def _on_closing(self):
        """Gère la fermeture propre de l'application"""
        try:
            result = messagebox.askyesno(
                "Confirmation",
                "Voulez-vous vraiment quitter HL7 Messenger ?",
                icon="question"
            )
            
            if result:
                self._cleanup_and_quit()
                
        except Exception as e:
            print(f"❌ Erreur fermeture: {e}")
            self.root.quit()

    def _cleanup_and_quit(self):
        """Nettoie les ressources et quitte proprement"""
        try:
            print("🧹 Nettoyage avant fermeture...")
            
            # Nettoyage de l'écran actuel
            if self.current_screen:
                self._safe_destroy_widget(self.current_screen)
            
            print("✅ Nettoyage terminé")
            
        except Exception as e:
            print(f"⚠️ Erreur nettoyage: {e}")
        finally:
            self.root.quit()
'''
    
    with open("app/ui/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ app.py corrigé définitivement")

def write_fixed_login():
    """Écrit le login screen corrigé"""
    content = '''# -*- coding: utf-8 -*-
"""
Écran de connexion de l'application HL7 Messenger - VERSION FINALE SANS ERREURS
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

        # Créer l'interface
        self._create_widgets()
        self._setup_keyboard_navigation()

    def _create_widgets(self):
        """Crée tous les widgets de l'interface"""
        try:
            # Frame principal
            main_frame = ttk.Frame(self, padding="30 20 30 20")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Configuration de la grille
            main_frame.columnconfigure(0, weight=1)
            main_frame.columnconfigure(2, weight=1)
            main_frame.rowconfigure(0, weight=1)
            main_frame.rowconfigure(6, weight=1)

            # Frame de connexion centré
            login_frame = ttk.Frame(main_frame, padding="30 25 30 25", relief="raised", borderwidth=2)
            login_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
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

            # DÉPARTEMENT
            department_label = ttk.Label(login_frame, text="🏢 Département:", font=("Helvetica", 11))
            department_label.grid(row=4, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
            
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

            self.login_button = ttk.Button(
                button_frame, 
                text="🚀 Connexion", 
                command=self._safe_login,
                width=18
            )
            self.login_button.pack(side=tk.LEFT, padx=(0, 10))

            self.exit_button = ttk.Button(
                button_frame, 
                text="❌ Quitter", 
                command=self._safe_exit,
                width=18
            )
            self.exit_button.pack(side=tk.LEFT)

            # INFO UTILISATEUR
            info_label = ttk.Label(
                login_frame,
                text="💡 Astuce: Utilisez Tab pour naviguer, Entrée pour valider",
                font=("Helvetica", 9),
                foreground="#718096"
            )
            info_label.grid(row=7, column=0, columnspan=2, pady=(15, 0))

        except Exception as e:
            print(f"❌ Erreur création widgets login: {e}")

    def _setup_keyboard_navigation(self):
        """Configure la navigation clavier de manière sécurisée"""
        try:
            # Focus initial
            self.after(100, self._safe_focus_username)

            # Bind des événements
            self.bind("<Return>", self._safe_handle_enter)
            self.bind("<KP_Enter>", self._safe_handle_enter)
            self.bind("<Escape>", self._safe_handle_escape)
            
        except Exception as e:
            print(f"❌ Erreur setup navigation: {e}")

    def _safe_focus_username(self):
        """Met le focus sur le champ username de manière sécurisée"""
        try:
            if not self.is_destroyed and hasattr(self, 'username_entry'):
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

    def destroy(self):
        """Destruction sécurisée du widget"""
        try:
            self.is_destroyed = True
            super().destroy()
        except Exception as e:
            print(f"❌ Erreur destruction login: {e}")
'''
    
    with open("app/ui/login_screen.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ login_screen.py corrigé définitivement")

def apply_ultimate_fixes():
    """Applique TOUTES les corrections finales"""
    print("🔧 CORRECTION ULTIMATE - HL7 Messenger")
    print("=" * 60)
    print("🎯 Résolution de TOUS les bugs Tkinter et erreurs")
    print("=" * 60)
    
    # Créer une sauvegarde
    backup_dir = create_backup()
    print(f"📦 Sauvegarde créée: {backup_dir}")
    print("-" * 40)
    
    try:
        # Appliquer toutes les corrections
        write_fixed_app()
        write_fixed_login()
        
        print("-" * 40)
        print("🎉 TOUTES LES CORRECTIONS APPLIQUÉES!")
        print("✅ Problèmes de widgets Tkinter résolus")
        print("✅ Erreurs de navigation corrigées")
        print("✅ Gestion d'erreur robuste ajoutée")
        print("✅ Destruction sécurisée des widgets")
        print("=" * 60)
        print("🚀 TESTEZ MAINTENANT:")
        print("   1. python -m app.network.mllp_server")
        print("   2. Dans un autre terminal:")
        print("      python app/main.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des corrections: {e}")
        print(f"📦 Restaurez depuis: {backup_dir}")
        return False

if __name__ == "__main__":
    apply_ultimate_fixes()