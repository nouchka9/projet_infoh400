# -*- coding: utf-8 -*-
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
        
        # Shift+Tab = navigation inverse
        self.password_entry.bind("<Shift-Tab>", lambda e: self.username_entry.focus_set())
        self.department_combo.bind("<Shift-Tab>", lambda e: self.password_entry.focus_set())
        self.login_button.bind("<Shift-Tab>", lambda e: self.department_combo.focus_set())

        # Navigation flèches dans le combobox
        self.department_combo.bind("<Up>", self._combo_up)
        self.department_combo.bind("<Down>", self._combo_down)
        self.department_combo.bind("<Left>", self._combo_up)
        self.department_combo.bind("<Right>", self._combo_down)

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

    def _clear_error(self):
        """Efface le message d'erreur"""
        self.error_var.set("")

    def _show_error(self, message):
        """Affiche un message d'erreur avec style"""
        self.error_var.set(f"⚠️ {message}")
        self.error_label.configure(foreground="#e53e3e")
        
        # Faire clignoter le message d'erreur
        def blink():
            current_color = self.error_label.cget("foreground")
            new_color = "#ff6b6b" if current_color == "#e53e3e" else "#e53e3e"
            self.error_label.configure(foreground=new_color)
            if hasattr(self, '_blink_job'):
                self.after_cancel(self._blink_job)
            self._blink_job = self.after(300, blink)
        
        # Arrêter le clignotement après 2 secondes
        blink()
        self.after(2000, lambda: setattr(self, '_blink_job', None))

    def _validate_inputs(self):
        """Validation complète des entrées utilisateur"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        department = self.department_var.get().strip()

        # Effacer les erreurs précédentes
        self._clear_error()

        # Validation du nom d'utilisateur
        if not username:
            self._show_error("Le nom d'utilisateur est requis")
            self.username_entry.focus_set()
            self.username_entry.selection_range(0, tk.END)
            return False

        if len(username) < 2:
            self._show_error("Le nom d'utilisateur doit contenir au moins 2 caractères")
            self.username_entry.focus_set()
            self.username_entry.selection_range(0, tk.END)
            return False

        # Validation du mot de passe
        if not password:
            self._show_error("Le mot de passe est requis")
            self.password_entry.focus_set()
            self.password_entry.selection_range(0, tk.END)
            return False

        if len(password) < 3:
            self._show_error("Le mot de passe doit contenir au moins 3 caractères")
            self.password_entry.focus_set()
            self.password_entry.selection_range(0, tk.END)
            return False

        # Validation du département
        if not department or department not in self.departments:
            self._show_error("Veuillez sélectionner un département valide")
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

            # Simulation d'une vérification (à remplacer par vraie authentification)
            self._simulate_login_process()

            # Appeler le callback de connexion
            self.on_login_callback(username, department)
            
            print(f"🎉 Connexion réussie pour {username}")

        except Exception as e:
            self.logger.error(f"Erreur lors de la connexion: {str(e)}")
            self._show_error(f"Erreur de connexion: {str(e)}")
            
        finally:
            # Réactiver le bouton
            self.login_button.configure(state="normal", text="🚀 Connexion")

    def _simulate_login_process(self):
        """Simule un processus de connexion avec feedback visuel"""
        # Changer l'apparence pour montrer le traitement
        self.login_button.configure(text="🔐 Vérification...")
        self.update()
        
        # Petite pause pour simuler le traitement
        self.after(500)
        
        self.login_button.configure(text="✅ Connexion réussie!")
        self.update()

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

    def reset_form(self):
        """Remet à zero le formulaire (méthode publique)"""
        self.username_var.set("")
        self.password_var.set("")
        self.department_var.set(self.departments[0])
        self._clear_error()
        self.username_entry.focus_set()

    def set_department(self, department):
        """Définit le département par défaut (méthode publique)"""
        if department in self.departments:
            self.department_var.set(department)
            index = self.departments.index(department)
            self.department_combo.current(index)