#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour remplacer complètement le fichier app.py
"""
import os

def replace_app_py():
    """Remplace complètement le fichier app.py"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "app.py")
    
    new_content = """# -*- coding: utf-8 -*-
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
    \"\"\"Application principale HL7 Messenger\"\"\"
    
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
        self.current_focus = None

        # Styles
        self._setup_styles()
        
        # Configuration des raccourcis clavier globaux
        self._setup_global_shortcuts()

        # Afficher l'écran de connexion
        self.show_login_screen()

    def _set_app_icon(self):
        \"\"\"Configure l'icône de la fenêtre\"\"\"
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
                    print("⚠️ logo.png introuvable")
            else:
                ico_path = os.path.join(resources_dir, "logo.ico")
                if os.path.exists(ico_path):
                    self.root.iconbitmap(ico_path)
                    print("✅ Icône ICO chargée")
                else:
                    print("⚠️ logo.ico introuvable")

        except Exception as e:
            print(f"❌ Erreur chargement icône : {e}")

    def _setup_styles(self):
        \"\"\"Configure les styles Tkinter\"\"\"
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("TButton", background="#007bff", foreground="white", font=("Helvetica", 10, "bold"), padding=5)
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground="#333333")
        style.configure("Subtitle.TLabel", font=("Helvetica", 12, "bold"), foreground="#555555")
        style.configure("Error.TLabel", foreground="red", font=("Helvetica", 10))
        style.configure("Success.TLabel", foreground="green", font=("Helvetica", 10, "bold"))
        style.configure("Warning.TLabel", foreground="orange", font=("Helvetica", 10, "bold"))

    def _setup_global_shortcuts(self):
        \"\"\"Configure les raccourcis clavier globaux\"\"\"
        self.root.bind("<F5>", self._on_refresh)
        self.root.bind("<Escape>", self._on_escape)
        self.root.bind("<FocusIn>", self._on_focus_change, "+")
        self.root.bind("<Return>", self._on_return_key)
        
    def _on_focus_change(self, event):
        \"\"\"Enregistre le widget ayant le focus\"\"\"
        self.current_focus = event.widget
        
    def _on_return_key(self, event):
        \"\"\"Gère la touche Return de manière globale\"\"\"
        # Si nous sommes sur l'écran de login, valider la connexion
        if isinstance(self.current_screen, LoginScreen):
            self.current_screen._on_login()
            return "break"  # Empêcher la propagation
        
        # Pour les widgets Entry, passer au champ suivant
        if event.widget and event.widget.winfo_class() == 'Entry':
            # Trouver le prochain widget à parcourir
            event.widget.tk_focusNext().focus()
            return "break"
        
        # Pour les boutons, simuler un clic
        if event.widget and event.widget.winfo_class() == 'Button':
            event.widget.invoke()
            return "break"
        
        # Pour les autres cas, laisser la propagation normale
        return None

    def _on_refresh(self, event=None):
        \"\"\"Actualise l'interface\"\"\"
        if hasattr(self.current_screen, 'refresh'):
            self.current_screen.refresh()
            
    def _on_escape(self, event=None):
        \"\"\"Gère la touche Échap\"\"\"
        # Si un dialogue est ouvert, le fermer
        for widget in self.root.winfo_children():
            if widget.winfo_class() == 'Toplevel':
                widget.destroy()
                return "break"
        
        # Sinon, demander si on veut quitter
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.root.quit()

    def show_login_screen(self):
        \"\"\"Affiche l'écran de connexion\"\"\"
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = LoginScreen(self.root, self._on_login)
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def show_dashboard(self):
        \"\"\"Affiche le tableau de bord principal\"\"\"
        print("Chargement du dashboard...")

        if self.current_screen:
            print("Suppression de l'écran précédent")
            self.current_screen.destroy()
            self.root.update()

        try:
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
            print("✅ Dashboard affiché")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Erreur chargement Dashboard : {e}")
            messagebox.showerror("Erreur", f"Impossible de charger le Dashboard : {e}")

    def _on_login(self, username, department):
        \"\"\"Callback après connexion\"\"\"
        self.current_user = username
        self.department = department
        self.logger.info(f"✅ Connexion réussie : {username} - {department}")
        self.show_dashboard()

    def _on_logout(self):
        \"\"\"Callback après déconnexion\"\"\"
        self.current_user = None
        self.department = None
        self.show_login_screen()
"""
    
    try:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"✅ Fichier app.py remplacé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du remplacement du fichier app.py : {e}")
        return False

if __name__ == "__main__":
    print("Remplacement complet du fichier app.py...")
    replace_app_py()
    print("Vous pouvez maintenant relancer l'application avec: python -m app.main")