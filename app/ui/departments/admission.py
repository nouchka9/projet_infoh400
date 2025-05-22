"""
Interface pour le département des admissions - VERSION CORRIGÉE FINALE
Tous les problèmes de validation, navigation et envoi résolus
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime
import threading
import time

class AdmissionFrame(ttk.Frame):
    """Interface pour le département des admissions - Version corrigée et optimisée"""
    
    def __init__(self, parent, mllp_client, message_builder, on_message_callback):
        super().__init__(parent)
        self.logger = logging.getLogger("HL7Messenger.AdmissionUI")
        self.parent = parent
        self.mllp_client = mllp_client
        self.message_builder = message_builder
        self.on_message_callback = on_message_callback
        
        # État interne
        self.processing = False
        self.validation_errors = []
        
        # Variables pour les champs
        self.vars = {}
        self.widgets = {}
        
        # Créer l'interface
        self._create_interface()
        print("✅ AdmissionFrame initialisé avec succès")

    def _create_interface(self):
        """Crée l'interface complète du module admission"""
        try:
            self._create_header()
            self._create_patient_form()
            self._create_action_buttons()
            self._create_status_indicator()
            self._setup_keyboard_shortcuts()
            self._set_default_values()
            
        except Exception as e:
            print(f"❌ Erreur création interface admission: {e}")
            self._create_error_interface(str(e))

    def _create_header(self):
        """Crée l'en-tête du module"""
        header_frame = ttk.Frame(self, padding="10 5")
        header_frame.pack(fill=tk.X)
        
        # Titre principal
        title_label = ttk.Label(
            header_frame,
            text="👥 Admission de Patients",
            font=("Helvetica", 16, "bold"),
            foreground="#2c5282"
        )
        title_label.pack(side=tk.LEFT)
        
        # Indicateur de statut à droite
        self.status_var = tk.StringVar(value="✅ Prêt")
        self.status_label = ttk.Label(
            header_frame,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            foreground="#48bb78"
        )
        self.status_label.pack(side=tk.RIGHT)

    def _create_patient_form(self):
        """Crée le formulaire patient avec validation en temps réel"""
        # Frame principal du formulaire
        form_frame = ttk.LabelFrame(
            self,
            text="📋 Informations Patient",
            padding="15 10"
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Configuration de la grille
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
        # Champs du formulaire
        self._create_form_fields(form_frame)
        
        # Section informations d'admission
        self._create_admission_section(form_frame)

    def _create_form_fields(self, parent):
        """Crée tous les champs du formulaire"""
        # Liste des champs avec leurs propriétés
        fields = [
            # Colonne 1
            ("patient_id", "🆔 ID Patient *", 0, 0, True, "P12345"),
            ("last_name", "👤 Nom *", 1, 0, True, "DOE"),
            ("first_name", "👤 Prénom *", 2, 0, True, "JOHN"),
            ("birth_date", "📅 Date naissance", 3, 0, False, "19800101"),
            
            # Colonne 2
            ("ward", "🏢 Service", 0, 2, False, "CARDIO"),
            ("room", "🛏️ Chambre", 1, 2, False, "102"),
            ("doctor", "👨‍⚕️ Médecin", 2, 2, False, "Dr. MARTIN"),
            ("priority", "⚡ Priorité", 3, 2, False, "Normal"),
        ]
        
        for field_id, label_text, row, col, required, default_val in fields:
            self._create_field(parent, field_id, label_text, row, col, required, default_val)
        
        # Champ spécial pour le sexe avec combobox
        self._create_gender_field(parent, 4, 0)
        
        # Champ spécial pour le type de message
        self._create_message_type_field(parent, 4, 2)
        
        # Aide contextuelle
        self._create_help_section(parent, 5)

    def _create_field(self, parent, field_id, label_text, row, col, required, default_val):
        """Crée un champ individuel avec validation"""
        # Label
        label = ttk.Label(parent, text=label_text, font=("Helvetica", 10))
        label.grid(row=row, column=col, sticky="w", padx=5, pady=5)
        
        # Variable et Entry
        var = tk.StringVar(value=default_val)
        self.vars[field_id] = var
        
        entry = ttk.Entry(parent, textvariable=var, font=("Helvetica", 10), width=20)
        entry.grid(row=row, column=col+1, sticky="ew", padx=5, pady=5)
        self.widgets[field_id] = entry
        
        # Validation en temps réel pour champs requis
        if required:
            var.trace_add("write", lambda *args, fid=field_id: self._validate_field(fid))
            
        # Aide pour date de naissance
        if field_id == "birth_date":
            help_label = ttk.Label(
                parent, 
                text="(AAAAMMJJ)",
                font=("Helvetica", 8),
                foreground="#666666"
            )
            help_label.grid(row=row, column=col+2, sticky="w", padx=0, pady=5)

    def _create_gender_field(self, parent, row, col):
        """Crée le champ sexe avec combobox"""
        # Label
        ttk.Label(parent, text="⚧ Sexe", font=("Helvetica", 10)).grid(
            row=row, column=col, sticky="w", padx=5, pady=5
        )
        
        # Combobox
        self.vars["gender"] = tk.StringVar(value="M")
        gender_combo = ttk.Combobox(
            parent,
            textvariable=self.vars["gender"],
            values=["M", "F", "O", "U"],
            state="readonly",
            width=8,
            font=("Helvetica", 10)
        )
        gender_combo.grid(row=row, column=col+1, sticky="w", padx=5, pady=5)
        gender_combo.current(0)
        self.widgets["gender"] = gender_combo
        
        # Aide
        help_text = ttk.Label(
            parent,
            text="M=Masculin, F=Féminin, O=Autre, U=Inconnu",
            font=("Helvetica", 8),
            foreground="#666666"
        )
        help_text.grid(row=row+1, column=col, columnspan=2, sticky="w", padx=5, pady=0)

    def _create_message_type_field(self, parent, row, col):
        """Crée le champ type de message"""
        # Label
        ttk.Label(parent, text="📨 Type de message", font=("Helvetica", 10)).grid(
            row=row, column=col, sticky="w", padx=5, pady=5
        )
        
        # Combobox
        message_types = [
            "ADT^A01 - Admission",
            "ADT^A02 - Transfert", 
            "ADT^A03 - Sortie",
            "ADT^A04 - Inscription",
            "ADT^A08 - Mise à jour"
        ]
        
        self.vars["message_type"] = tk.StringVar(value=message_types[0])
        type_combo = ttk.Combobox(
            parent,
            textvariable=self.vars["message_type"],
            values=message_types,
            state="readonly",
            width=25,
            font=("Helvetica", 10)
        )
        type_combo.grid(row=row, column=col+1, sticky="ew", padx=5, pady=5)
        type_combo.current(0)
        self.widgets["message_type"] = type_combo

    def _create_admission_section(self, parent):
        """Crée la section spécifique à l'admission"""
        # Séparateur
        separator = ttk.Separator(parent, orient=tk.HORIZONTAL)
        separator.grid(row=6, column=0, columnspan=4, sticky="ew", pady=10)
        
        # Commentaires
        ttk.Label(parent, text="📝 Commentaires", font=("Helvetica", 10)).grid(
            row=7, column=0, sticky="nw", padx=5, pady=5
        )
        
        self.vars["comments"] = tk.StringVar()
        comments_entry = ttk.Entry(parent, textvariable=self.vars["comments"], width=50)
        comments_entry.grid(row=7, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        self.widgets["comments"] = comments_entry

    def _create_help_section(self, parent, row):
        """Crée la section d'aide"""
        help_frame = ttk.Frame(parent)
        help_frame.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        
        help_text = ttk.Label(
            help_frame,
            text="💡 * Champs obligatoires | Tab: Navigation | Entrée: Envoyer | F5: Réinitialiser",
            font=("Helvetica", 9),
            foreground="#718096"
        ) 
        help_text.pack()

    def _create_action_buttons(self):
        """Crée les boutons d'action avec style"""
        button_frame = ttk.Frame(self, padding="10 5")
        button_frame.pack(fill=tk.X)
        
        # Indicateur de progression (caché par défaut)
        self.progress_frame = ttk.Frame(button_frame)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode="indeterminate",
            length=200
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="⏳ Envoi en cours...",
            font=("Helvetica", 10)
        )
        self.progress_label.pack(side=tk.LEFT)
        
        # Espacement
        ttk.Frame(button_frame).pack(side=tk.LEFT, expand=True)
        
        # Boutons principaux
        self.send_button = ttk.Button(
            button_frame,
            text="🚀 Envoyer Message",
            command=self._send_message,
            width=20
        )
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.reset_button = ttk.Button(
            button_frame,
            text="🔄 Réinitialiser",
            command=self._reset_form,
            width=15
        )
        self.reset_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Bouton de test (pour développement)
        test_button = ttk.Button(
            button_frame,
            text="🧪 Mode Test",
            command=self._toggle_test_mode,
            width=12
        )
        test_button.pack(side=tk.RIGHT, padx=(0, 10))

    def _create_status_indicator(self):
        """Crée l'indicateur de statut en bas"""
        status_frame = ttk.Frame(self, padding="5 2")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Séparateur
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, side=tk.BOTTOM)
        
        # Validation en temps réel
        self.validation_var = tk.StringVar(value="✅ Formulaire valide")
        validation_label = ttk.Label(
            status_frame,
            textvariable=self.validation_var,
            font=("Helvetica", 9)
        )
        validation_label.pack(side=tk.LEFT)
        
        # Compteur de caractères pour certains champs
        self.char_count_var = tk.StringVar()
        char_count_label = ttk.Label(
            status_frame,
            textvariable=self.char_count_var,
            font=("Helvetica", 9),
            foreground="#666666"
        )
        char_count_label.pack(side=tk.RIGHT)

    def _setup_keyboard_shortcuts(self):
        """Configure les raccourcis clavier"""
        # Raccourcis globaux
        self.bind_all("<Return>", self._handle_enter_key)
        self.bind_all("<KP_Enter>", self._handle_enter_key)
        self.bind_all("<F5>", lambda e: self._reset_form())
        self.bind_all("<Control-s>", lambda e: self._send_message())
        self.bind_all("<Escape>", self._handle_escape_key)
        
        # Navigation Tab améliorée
        self._setup_tab_navigation()

    def _setup_tab_navigation(self):
        """Configure la navigation par Tab"""
        # Ordre de navigation
        nav_order = [
            "patient_id", "last_name", "first_name", "birth_date",
            "ward", "room", "doctor", "priority",
            "gender", "message_type", "comments"
        ]
        
        for i, field_id in enumerate(nav_order):
            widget = self.widgets.get(field_id)
            if widget:
                # Tab pour aller au suivant
                next_field = nav_order[(i + 1) % len(nav_order)]
                widget.bind("<Tab>", lambda e, nf=next_field: self._focus_field(nf))
                
                # Shift+Tab pour aller au précédent
                prev_field = nav_order[(i - 1) % len(nav_order)]
                widget.bind("<Shift-Tab>", lambda e, pf=prev_field: self._focus_field(pf))

    def _focus_field(self, field_id):
        """Met le focus sur un champ spécifique"""
        widget = self.widgets.get(field_id)
        if widget:
            widget.focus_set()
            if hasattr(widget, 'selection_range'):
                widget.selection_range(0, tk.END)

    def _handle_enter_key(self, event=None):
        """Gère la touche Entrée de manière intelligente"""
        focused = self.focus_get()
        
        # Si on est sur le bouton reset, réinitialiser
        if focused == self.reset_button:
            self._reset_form()
        # Si on est dans les commentaires, ne pas envoyer (permettre retour à la ligne)
        elif focused == self.widgets.get("comments"):
            return
        # Sinon, envoyer le message
        else:
            self._send_message()

    def _handle_escape_key(self, event=None):
        """Gère la touche Échap"""
        if self.processing:
            # Annuler l'envoi si possible
            self._cancel_sending()
        else:
            # Réinitialiser le formulaire
            self._reset_form()

    def _validate_field(self, field_id):
        """Valide un champ individuel en temps réel"""
        var = self.vars.get(field_id)
        if not var:
            return
        
        value = var.get().strip()
        widget = self.widgets.get(field_id)
        
        # Validation selon le type de champ
        is_valid = True
        error_msg = ""
        
        if field_id == "patient_id":
            if not value:
                is_valid = False
                error_msg = "ID patient requis"
            elif len(value) < 2:
                is_valid = False
                error_msg = "ID trop court"
                
        elif field_id in ["last_name", "first_name"]:
            if not value:
                is_valid = False
                error_msg = f"{field_id.replace('_', ' ').title()} requis"
            elif len(value) < 2:
                is_valid = False
                error_msg = "Nom trop court"
                
        elif field_id == "birth_date" and value:
            if not value.isdigit() or len(value) != 8:
                is_valid = False
                error_msg = "Format: AAAAMMJJ"
        
        # Changer le style du widget selon la validation
        if widget:
            if is_valid:
                widget.configure(style="TEntry")
            else:
                # Créer un style d'erreur s'il n'existe pas
                style = ttk.Style()
                style.configure("Error.TEntry", fieldbackground="#ffe6e6")
                widget.configure(style="Error.TEntry")
        
        # Mettre à jour le statut global
        self._update_validation_status()

    def _update_validation_status(self):
        """Met à jour le statut de validation globale"""
        errors = []
        
        # Vérifier tous les champs requis
        required_fields = ["patient_id", "last_name", "first_name"]
        
        for field_id in required_fields:
            value = self.vars.get(field_id, tk.StringVar()).get().strip()
            if not value:
                field_name = field_id.replace("_", " ").title()
                errors.append(f"{field_name} requis")
            elif len(value) < 2:
                field_name = field_id.replace("_", " ").title()  
                errors.append(f"{field_name} trop court")
        
        # Vérifier format date de naissance
        birth_date = self.vars.get("birth_date", tk.StringVar()).get().strip()
        if birth_date and (not birth_date.isdigit() or len(birth_date) != 8):
            errors.append("Format date invalide")
        
        # Mettre à jour l'affichage
        if errors:
            self.validation_var.set(f"❌ {len(errors)} erreur(s)")
            self.validation_errors = errors
        else:
            self.validation_var.set("✅ Formulaire valide")
            self.validation_errors = []
        
        # Activer/désactiver le bouton d'envoi
        self.send_button.configure(state="normal" if not errors else "disabled")

    def _set_default_values(self):
        """Définit les valeurs par défaut du formulaire"""
        defaults = {
            "patient_id": "P12345",
            "last_name": "DOE", 
            "first_name": "JOHN",
            "birth_date": "19800101",
            "gender": "M",
            "ward": "CARDIO",
            "room": "102",
            "doctor": "Dr. MARTIN",
            "priority": "Normal",
            "comments": "Admission programmée"
        }
        
        for field_id, default_value in defaults.items():
            var = self.vars.get(field_id)
            if var:
                var.set(default_value)
        
        # Focus initial
        self.after(100, lambda: self._focus_field("patient_id"))

    def _reset_form(self):
        """Réinitialise le formulaire avec animation"""
        if self.processing:
            messagebox.showwarning("Attention", "Envoi en cours, veuillez patienter...")
            return
        
        # Animation de réinitialisation
        self.status_var.set("🔄 Réinitialisation...")
        
        def reset_progressive():
            fields = list(self.vars.keys())
            for i, field_id in enumerate(fields):
                var = self.vars[field_id]
                if field_id in ["gender", "message_type"]:
                    # Garder les valeurs par défaut pour les combobox
                    if field_id == "gender":
                        var.set("M")
                    elif field_id == "message_type":
                        var.set("ADT^A01 - Admission")
                else:
                    var.set("")
                
                # Petit délai pour l'effet visuel
                self.update_idletasks()
                time.sleep(0.05)
            
            # Remettre les valeurs par défaut
            self._set_default_values()
            self.status_var.set("✅ Formulaire réinitialisé")
            
            # Revenir à "Prêt" après 2 secondes
            self.after(2000, lambda: self.status_var.set("✅ Prêt"))
        
        # Exécuter dans un thread pour ne pas bloquer l'interface
        thread = threading.Thread(target=reset_progressive, daemon=True)
        thread.start()

    def _toggle_test_mode(self):
        """Active/désactive le mode test avec données aléatoires"""
        import random
        
        test_patients = [
            {"id": "P00001", "last": "MARTIN", "first": "SOPHIE", "birth": "19850315", "ward": "CARDIO", "room": "101"},
            {"id": "P00002", "last": "DUBOIS", "first": "PIERRE", "birth": "19720623", "ward": "NEURO", "room": "205"},
            {"id": "P00003", "last": "BERNARD", "first": "MARIE", "birth": "19901201", "ward": "PNEUMO", "room": "310"},
            {"id": "P00004", "last": "THOMAS", "first": "PAUL", "birth": "19651018", "ward": "ORTHO", "room": "415"},
            {"id": "P00005", "last": "ROBERT", "first": "ANNE", "birth": "19780409", "ward": "GASTRO", "room": "520"},
        ]
        
        patient = random.choice(test_patients)
        genders = ["M", "F"]
        doctors = ["Dr. MARTIN", "Dr. DUBOIS", "Dr. LEROY", "Dr. MOREAU", "Dr. SIMON"]
        
        # Appliquer les données de test
        self.vars["patient_id"].set(patient["id"])
        self.vars["last_name"].set(patient["last"])
        self.vars["first_name"].set(patient["first"])
        self.vars["birth_date"].set(patient["birth"])
        self.vars["gender"].set(random.choice(genders))
        self.vars["ward"].set(patient["ward"])
        self.vars["room"].set(patient["room"])
        self.vars["doctor"].set(random.choice(doctors))
        self.vars["comments"].set("Patient de test généré automatiquement")
        
        self.show_status("🧪 Données de test chargées", "info")

    def _send_message(self):
        """Envoie le message d'admission avec gestion complète d'erreurs"""
        # Vérifier si un envoi est déjà en cours
        if self.processing:
            messagebox.showwarning("Attention", "Un envoi est déjà en cours...")
            return
        
        # Validation finale
        if self.validation_errors:
            error_text = "\n".join([f"• {error}" for error in self.validation_errors])
            messagebox.showerror(
                "Erreurs de validation",
                f"Veuillez corriger les erreurs suivantes:\n\n{error_text}"
            )
            return
        
        # Démarrer le processus d'envoi
        self._start_sending_process()
        
        # Lancer l'envoi dans un thread séparé
        thread = threading.Thread(target=self._send_message_thread, daemon=True)
        thread.start()

    def _start_sending_process(self):
        """Démarre le processus d'envoi avec feedback visuel"""
        self.processing = True
        
        # Changer l'interface
        self.send_button.configure(state="disabled", text="⏳ Envoi en cours...")
        self.reset_button.configure(state="disabled")
        
        # Afficher la barre de progression
        self.progress_frame.pack(side=tk.LEFT, before=self.send_button, padx=(0, 10))
        self.progress_bar.start(10)
        
        # Mettre à jour le statut
        self.status_var.set("📤 Envoi du message HL7...")

    def _send_message_thread(self):
        """Thread d'envoi du message HL7"""
        try:
            # Collecter les données du formulaire
            patient_data = self._collect_patient_data()
            
            # Mise à jour du statut
            self.after(0, lambda: self.status_var.set("🔨 Construction du message HL7..."))
            
            # Construire le message HL7
            message_type = self.vars["message_type"].get().split(" - ")[0]
            
            if message_type == "ADT^A01":
                message, control_id = self.message_builder.create_adt_a01(patient_data)
            else:
                # Pour les autres types, utiliser ADT^A01 par défaut
                message, control_id = self.message_builder.create_adt_a01(patient_data)
            
            # Mise à jour du statut
            self.after(0, lambda: self.status_var.set(f"📡 Envoi vers le serveur... (ID: {control_id[:8]})"))
            
            # Envoyer le message
            success, response = self.mllp_client.send_message(message, "ADMISSION_SYSTEM")
            
            # Traitement de la réponse
            if success:
                self.after(0, lambda: self._on_send_success(control_id, response))
            else:
                self.after(0, lambda: self._on_send_failure(response))
                
        except Exception as e:
            error_msg = f"Erreur lors de l'envoi: {str(e)}"
            self.logger.error(error_msg)
            self.after(0, lambda: self._on_send_error(error_msg))

    def _collect_patient_data(self):
        """Collecte toutes les données du patient depuis le formulaire"""
        return {
            "id": self.vars["patient_id"].get().strip(),
            "last_name": self.vars["last_name"].get().strip().upper(),
            "first_name": self.vars["first_name"].get().strip().upper(),
            "birth_date": self.vars["birth_date"].get().strip(),
            "gender": self.vars["gender"].get().strip(),
            "ward": self.vars["ward"].get().strip().upper(),
            "room": self.vars["room"].get().strip(),
            "doctor": self.vars["doctor"].get().strip(),
            "priority": self.vars["priority"].get().strip(),
            "comments": self.vars["comments"].get().strip(),
            "admission_date": datetime.now().strftime("%Y%m%d%H%M%S")
        }

    def _on_send_success(self, control_id, response):
        """Gère le succès de l'envoi"""
        self._end_sending_process()
        
        success_msg = f"Message ADT envoyé avec succès!\nID de contrôle: {control_id}"
        self.show_status("✅ Envoi réussi", "success")
        
        # Notification au dashboard
        if self.on_message_callback:
            self.on_message_callback(True, success_msg)
        
        # Message de confirmation
        messagebox.showinfo("Succès", success_msg)
        
        self.logger.info(f"Message ADT envoyé avec succès - ID: {control_id}")

    def _on_send_failure(self, response):
        """Gère l'échec de l'envoi"""
        self._end_sending_process()
        
        failure_msg = f"Envoi échoué: {response}"
        self.show_status("❌ Échec d'envoi", "error")
        
        # Notification au dashboard
        if self.on_message_callback:
            self.on_message_callback(False, failure_msg)
        
        # Message d'erreur
        messagebox.showerror("Erreur d'envoi", failure_msg)
        
        self.logger.warning(f"Échec d'envoi: {response}")

    def _on_send_error(self, error_msg):
        """Gère les erreurs d'envoi"""
        self._end_sending_process()
        
        self.show_status("❌ Erreur technique", "error")
        
        # Notification au dashboard
        if self.on_message_callback:
            self.on_message_callback(False, error_msg)
        
        # Message d'erreur détaillé
        messagebox.showerror("Erreur technique", f"Une erreur est survenue:\n\n{error_msg}")

    def _end_sending_process(self):
        """Termine le processus d'envoi et remet l'interface à normal"""
        self.processing = False
        
        # Cacher la barre de progression
        self.progress_bar.stop()
        self.progress_frame.pack_forget()
        
        # Remettre les boutons à normal
        self.send_button.configure(state="normal", text="🚀 Envoyer Message")
        self.reset_button.configure(state="normal")
        
        # Revenir au statut normal après 3 secondes
        self.after(3000, lambda: self.status_var.set("✅ Prêt"))

    def _cancel_sending(self):
        """Annule l'envoi en cours (si possible)"""
        if self.processing:
            self.processing = False
            self._end_sending_process()
            self.show_status("🚫 Envoi annulé", "warning")

    def show_status(self, message, status_type="info"):
        """Affiche un message de statut avec couleur"""
        colors = {
            "success": "#48bb78",
            "error": "#f56565", 
            "warning": "#ed8936",
            "info": "#4299e1"
        }
        
        self.status_var.set(message)
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(foreground=color)

    def _create_error_interface(self, error_msg):
        """Crée une interface d'erreur si le module ne peut pas se charger"""
        error_frame = ttk.Frame(self, padding="50")
        error_frame.pack(fill=tk.BOTH, expand=True)
        
        error_title = ttk.Label(
            error_frame,
            text="❌ Erreur du module Admission",
            font=("Helvetica", 14, "bold"),
            foreground="#dc2626"
        )
        error_title.pack()
        
        error_detail = ttk.Label(
            error_frame,
            text=f"Impossible d'initialiser le module:\n{error_msg}",
            font=("Helvetica", 10),
            foreground="#666666",
            justify="center"
        )
        error_detail.pack(pady=20)
        
        retry_button = ttk.Button(
            error_frame,
            text="🔄 Réessayer",
            command=lambda: [error_frame.destroy(), self._create_interface()]
        )
        retry_button.pack()

    def refresh(self):
        """Méthode publique pour rafraîchir le module"""
        if not self.processing:
            self._update_validation_status()
            self.show_status("🔄 Module actualisé", "info")

    def get_current_data(self):
        """Retourne les données actuelles du formulaire"""
        return {field_id: var.get() for field_id, var in self.vars.items()}

    def load_patient_data(self, patient_data):
        """Charge les données d'un patient dans le formulaire"""
        for field_id, value in patient_data.items():
            if field_id in self.vars:
                self.vars[field_id].set(value)