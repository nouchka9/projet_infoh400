"""
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
        
        # Titre avec style
        title_frame = ttk.Frame(top_bar)
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(
            title_frame,
            text="🏥 HL7 Messenger",
            font=("Helvetica", 18, "bold"),
            foreground="#2c5282"
        )
        title_label.pack(side=tk.LEFT)
        
        # Frame utilisateur à droite
        user_frame = ttk.Frame(top_bar)
        user_frame.pack(side=tk.RIGHT)
        
        # Bouton Historique
        self.history_button = ttk.Button(
            user_frame,
            text="📊 Historique",
            command=self._show_history,
            width=12
        )
        self.history_button.pack(side=tk.LEFT, padx=(0, 10))
        
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
        # Ne pas pack maintenant, sera affiché quand nécessaire
        
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
        """Charge le frame spécifique au département avec gestion d'erreur robuste"""
        print(f"🔄 Chargement du département: {self.department}")
        
        try:
            # Frame de chargement temporaire
            loading_dept = ttk.Label(
                self.content_frame,
                text=f"🔄 Chargement du module {self.department}...",
                font=("Helvetica", 12)
            )
            loading_dept.pack(expand=True)
            self.update()
            
            # Petite pause
            self.after(200)
            
            # Supprimer le message de chargement
            loading_dept.destroy()
            
            # Créer le frame du département
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
        
        info = ttk.Label(
            fallback_frame,
            text="Ce module sera bientôt implémenté.",
            font=("Helvetica", 10),
            foreground="#666666"
        )
        info.pack(pady=(10, 0))

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
        
        # Bouton pour réessayer
        retry_button = ttk.Button(
            error_frame,
            text="🔄 Réessayer",
            command=self._retry_load_department
        )
        retry_button.pack(pady=(20, 0))

    def _retry_load_department(self):
        """Réessaie de charger le département"""
        # Nettoyer le contenu actuel
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Réessayer le chargement
        self._load_department_frame()

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
            self.status_var.set("✅ Message envoyé avec succès")
        else:
            self.show_notification(f"❌ {message}", "error")
            self.status_var.set("❌ Erreur d'envoi")
        
        # Revenir au statut normal après 5 secondes
        self.after(5000, lambda: self.status_var.set("✅ Prêt"))

    def show_notification(self, message, notification_type="info"):
        """Affiche une notification avec style"""
        self.notification_var.set(message)
        
        # Couleurs selon le type
        colors = {
            "success": {"bg": "#d4edda", "fg": "#155724"},
            "error": {"bg": "#f8d7da", "fg": "#721c24"},
            "warning": {"bg": "#fff3cd", "fg": "#856404"},
            "info": {"bg": "#cce7ff", "fg": "#004085"}
        }
        
        color = colors.get(notification_type, colors["info"])
        self.notification_label.configure(
            background=color["bg"],
            foreground=color["fg"]
        )
        
        # Afficher la notification
        self.notification_frame.pack(fill=tk.X, pady=(5, 0), after=self.main_frame.winfo_children()[0])
        
        # Animation d'apparition
        self._animate_notification_in()
        
        # Cacher après 5 secondes
        self.after(5000, self._hide_notification)

    def _animate_notification_in(self):
        """Animation d'apparition de la notification"""
        def fade_in(alpha=0.1):
            if alpha <= 1.0:
                # Simuler le fade avec padding
                padding = int(10 * alpha)
                self.notification_label.configure(pady=padding)
                self.after(50, lambda: fade_in(alpha + 0.1))
        
        fade_in()

    def _hide_notification(self):
        """Cache la notification avec animation"""
        def fade_out(alpha=1.0):
            if alpha > 0:
                padding = int(10 * alpha)
                self.notification_label.configure(pady=padding)
                self.after(50, lambda: fade_out(alpha - 0.1))
            else:
                self.notification_frame.pack_forget()
        
        fade_out()

    def _on_logout(self):
        """Gère la déconnexion avec confirmation"""
        result = messagebox.askyesno(
            "Confirmation de déconnexion",
            f"👤 {self.username}\n\nVoulez-vous vraiment vous déconnecter ?",
            icon="question"
        )
        if result:
            self.logger.info(f"Déconnexion de {self.username}")
            self.on_logout_callback()

    def _show_history(self):
        """Ouvre la fenêtre d'historique avec gestion d'erreur"""
        try:
            self.history_button.configure(state="disabled", text="⏳ Chargement...")
            
            # Créer la fenêtre d'historique
            history_window = HistoryViewer(self)
            
            # Réactiver le bouton quand la fenêtre se ferme
            def on_history_close():
                self.history_button.configure(state="normal", text="📊 Historique")
            
            history_window.protocol("WM_DELETE_WINDOW", lambda: [history_window.destroy(), on_history_close()])
            
        except Exception as e:
            self.history_button.configure(state="normal", text="📊 Historique")
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
            text=f"Une erreur est survenue lors du chargement:\n\n{error_msg}",
            font=("Helvetica", 11),
            foreground="#666666",
            wraplength=400,
            justify="center"
        )
        error_detail.pack(pady=(0, 30))
        
        # Boutons d'action
        button_frame = ttk.Frame(error_frame)
        button_frame.pack()
        
        retry_button = ttk.Button(
            button_frame,
            text="🔄 Réessayer",
            command=self._retry_dashboard_load
        )
        retry_button.pack(side=tk.LEFT, padx=(0, 10))
        
        logout_button = ttk.Button(
            button_frame,
            text="🚪 Retour à la connexion",
            command=self._on_logout
        )
        logout_button.pack(side=tk.LEFT)

    def _retry_dashboard_load(self):
        """Réessaie de charger le dashboard"""
        # Nettoyer l'interface
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Relancer le chargement
        self._create_interface_progressive()

    def refresh_content(self):
        """Méthode publique pour rafraîchir le contenu"""
        if self.dept_frame:
            try:
                # Rafraîchir le département si la méthode existe
                if hasattr(self.dept_frame, 'refresh'):
                    self.dept_frame.refresh()
                self.show_notification("🔄 Contenu actualisé", "info")
            except Exception as e:
                self.show_notification(f"Erreur de rafraîchissement: {str(e)}", "error")

    def set_status(self, message, status_type="info"):
        """Méthode publique pour changer le statut"""
        icons = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "info": "ℹ️",
            "loading": "⏳"
        }
        icon = icons.get(status_type, "ℹ️")
        self.status_var.set(f"{icon} {message}")

    def get_current_user_info(self):
        """Retourne les informations de l'utilisateur actuel"""
        return {
            "username": self.username,
            "department": self.department,
            "session_start": getattr(self, 'session_start', datetime.now()),
            "status": "active"
        }