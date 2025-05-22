#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def replace_dashboard():
    """Remplace complètement le fichier dashboard.py"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "dashboard.py")
    
    new_content = '''"""
Tableau de bord principal de l'application HL7 Messenger.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime

from app.ui.departments.admission import AdmissionFrame
from app.ui.departments.laboratory import LaboratoryFrame
from app.ui.departments.radiology import RadiologyFrame
from app.ui.departments.pharmacy import PharmacyFrame
from app.ui.history_viewer import HistoryViewer

class Dashboard(ttk.Frame):
    """Tableau de bord principal de l'application"""

    def __init__(self, parent, username, department, mllp_client, message_builder, config, on_logout_callback):
        print(f"Initialisation du Dashboard pour {username} dans {department}")
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

        # Créer l'interface
        self._create_widgets()
        
        # Configurer les événements clavier 
        self._setup_keyboard_navigation()
        
        print("Widgets du Dashboard créés avec succès")

    def _setup_keyboard_navigation(self):
        # Touche F5 pour rafraîchir
        self.bind("<F5>", self._on_refresh)
        
        # Touche Échap pour gérer les popups
        self.bind("<Escape>", self._on_escape)
        
        # Touche Entrée - ne pas la capturer globalement
        # pour permettre aux widgets enfants de l'utiliser
    
    def _on_refresh(self, event=None):
        # Rafraîchit la vue actuelle
        if hasattr(self.dept_frame, 'refresh'):
            self.dept_frame.refresh()
        
    def _on_escape(self, event=None):
        # Fermer d'abord les fenêtres popup
        for child in self.winfo_toplevel().winfo_children():
            if child.winfo_class() == 'Toplevel':
                child.destroy()
                return "break"

    def _create_widgets(self):
        """Crée les widgets de l'interface"""
        print("Création des widgets...")
        
        # Créer un widget de débogage temporaire visible immédiatement
        debug_label = ttk.Label(self, text="CHARGEMENT DASHBOARD", background="red", foreground="white", font=("Arial", 14, "bold"))
        debug_label.pack(pady=20)
        self.update()  # Force la mise à jour de l'interface
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        try:
            print("Création de la barre supérieure...")
            self._create_top_bar()
            print("Barre supérieure créée")
            
            self.notification_frame = ttk.Frame(self.main_frame, padding=5)
            self.notification_frame.pack(fill=tk.X, expand=False)

            self.notification_var = tk.StringVar()
            self.notification_label = ttk.Label(self.notification_frame,
                                                textvariable=self.notification_var,
                                                background="#d4edda",
                                                foreground="#155724",
                                                padding=10)
            self.notification_label.pack(fill=tk.X, expand=True)
            self.notification_frame.pack_forget()

            content_frame = ttk.Frame(self.main_frame)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            print("Chargement du frame spécifique au département...")
            self._load_department_frame(content_frame)
            print("Frame du département chargé")
            
            self._create_status_bar()
            print("Barre de statut créée")
            
            # Supprimer le label de débogage
            debug_label.destroy()
            
        except Exception as e:
            print(f"Erreur lors de la création des widgets: {str(e)}")
            import traceback
            traceback.print_exc()
            # Afficher l'erreur dans l'interface
            error_label = ttk.Label(self.main_frame, 
                                   text=f"Erreur: {str(e)}", 
                                   background="#f8d7da", 
                                   foreground="#721c24",
                                   padding=10)
            error_label.pack(fill=tk.X, expand=False, pady=20)

    def _create_top_bar(self):
        """Crée la barre supérieure"""
        # Créer d'abord tous les widgets
        top_bar = ttk.Frame(self.main_frame, padding=10)
        
        title_label = ttk.Label(top_bar, text="HL7 Messenger", style="Title.TLabel")
        
        user_frame = ttk.Frame(top_bar)
        
        # Nouveau bouton Historique - Utiliser self._show_history au lieu de self.show_history_popup
        history_button = ttk.Button(user_frame, text="Historique", command=self._show_history, width=12)
        
        dept_names = {
            "ADMISSION": "Admissions",
            "LABORATORY": "Laboratoire",
            "RADIOLOGY": "Radiologie",
            "PHARMACY": "Pharmacie"
        }
        dept_text = dept_names.get(self.department, self.department)
        
        user_label = ttk.Label(user_frame,
                               text=f"Utilisateur: {self.username} | Département: {dept_text}")
        
        logout_button = ttk.Button(user_frame, text="Déconnexion",
                                   command=self._on_logout, width=12)
        
        # Maintenant placer tous les widgets
        top_bar.pack(fill=tk.X, expand=False)
        title_label.pack(side=tk.LEFT)
        user_frame.pack(side=tk.RIGHT)
        history_button.pack(side=tk.LEFT, padx=(0, 5))
        user_label.pack(side=tk.LEFT, padx=(0, 10))
        logout_button.pack(side=tk.LEFT)

    def _create_status_bar(self):
        status_bar = ttk.Frame(self.main_frame, padding=(10, 5))
        status_bar.pack(fill=tk.X, expand=False, side=tk.BOTTOM)

        separator = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, expand=False, side=tk.BOTTOM, pady=(0, 5))

        self.status_var = tk.StringVar(value="Prêt")
        status_label = ttk.Label(status_bar, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)

        self.clock_var = tk.StringVar()
        clock_label = ttk.Label(status_bar, textvariable=self.clock_var)
        clock_label.pack(side=tk.RIGHT)

        self._update_clock()

    def _update_clock(self):
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.clock_var.set(current_time)
        self.after(1000, self._update_clock)

    def _load_department_frame(self, parent):
        print(f"Chargement du frame pour le département: {self.department}")
        try:
            if self.department == "ADMISSION":
                self.dept_frame = AdmissionFrame(parent, self.mllp_client, self.message_builder, self._on_message_sent)
            elif self.department == "LABORATORY":
                self.dept_frame = LaboratoryFrame(
                    parent, 
                    self.mllp_client, 
                    self.message_builder, 
                    self._on_message_sent,
                    self.config
                )
            elif self.department == "RADIOLOGY":
                self.dept_frame = RadiologyFrame(parent, self.mllp_client, self.message_builder, self._on_message_sent)
            elif self.department == "PHARMACY":
                self.dept_frame = PharmacyFrame(parent, self.mllp_client, self.message_builder, self._on_message_sent)
            else:
                self.dept_frame = ttk.Frame(parent)
                ttk.Label(self.dept_frame, text=f"Département {self.department} non supporté").pack()

            self.dept_frame.pack(fill=tk.BOTH, expand=True)
            print(f"Frame du département {self.department} chargé avec succès")
        except Exception as e:
            print(f"Erreur lors du chargement du frame de département: {str(e)}")
            self.dept_frame = ttk.Frame(parent)
            ttk.Label(self.dept_frame, text=f"Erreur: {str(e)}", 
                     background="#f8d7da", foreground="#721c24", padding=10).pack(pady=20)
            self.dept_frame.pack(fill=tk.BOTH, expand=True)

    def _on_message_sent(self, success, message):
        if success:
            self.show_notification(f"✅ {message}")
        else:
            self.show_notification(f"❌ {message}", is_error=True)

    def show_notification(self, message, is_error=False):
        self.notification_var.set(message)
        if is_error:
            self.notification_label.configure(background="#f8d7da", foreground="#721c24")
        else:
            self.notification_label.configure(background="#d4edda", foreground="#155724")
        self.notification_frame.pack(fill=tk.X, expand=False, after=self.main_frame.winfo_children()[0])
        self.after(5000, self._hide_notification)

    def _hide_notification(self):
        self.notification_frame.pack_forget()

    def _on_logout(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter?"):
            self.on_logout_callback()

    def _show_history(self):
        """Ouvre la fenêtre d'historique"""
        try:
            HistoryViewer(self)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir l'historique: {str(e)}")
'''
    
    try:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"✅ Fichier dashboard.py remplacé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du remplacement du fichier dashboard.py : {e}")
        return False

if __name__ == "__main__":
    print("Remplacement du fichier dashboard.py...")
    replace_dashboard()
    print("Vous pouvez maintenant relancer l'application avec: python -m app.main")