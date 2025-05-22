# -*- coding: utf-8 -*-
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
            
            # Styles pour boutons
            style.configure("Success.TButton", foreground="white")
            style.configure("Secondary.TButton", foreground="#2d3748")
            
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
            self._show_error_dialog(f"Erreur d'affichage: {str(e)}")

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
            self._show_error_dialog(f"Erreur de transition: {str(e)}")

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
            self._show_error_dialog(f"Impossible de charger le Dashboard : {e}")
            # Retourner à l'écran de connexion en cas d'erreur
            self.show_login_screen()

    def _safe_destroy_widget(self, widget):
        """Détruit un widget de manière sécurisée"""
        try:
            if widget and widget.winfo_exists():
                # Débinder tous les événements avant destruction
                self._unbind_widget_events(widget)
                widget.destroy()
                print("✅ Widget détruit proprement")
        except tk.TclError:
            # Widget déjà détruit, ignorer
            print("⚠️ Widget déjà détruit")
        except Exception as e:
            print(f"⚠️ Erreur destruction widget: {e}")

    def _unbind_widget_events(self, widget):
        """Supprime tous les bindings d'un widget"""
        try:
            # Débinder les événements communs
            events_to_unbind = [
                "<Return>", "<KP_Enter>", "<Escape>", "<Tab>", "<Shift-Tab>",
                "<Up>", "<Down>", "<Left>", "<Right>", "<F5>", "<Control-s>"
            ]
            
            for event in events_to_unbind:
                try:
                    widget.unbind_all(event)
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Erreur unbind événements: {e}")

    def _on_login(self, username, department):
        """Callback après connexion avec validation"""
        try:
            if not username or not department:
                self._show_error_dialog("Nom d'utilisateur ou département manquant")
                return
            
            self.current_user = username
            self.department = department
            
            self.logger.info(f"✅ Connexion réussie : {username} - {department}")
            print(f"✅ Connexion validée: {username} / {department}")
            
            # Transition vers le dashboard
            self.show_dashboard()
            
        except Exception as e:
            print(f"❌ Erreur callback connexion: {e}")
            self._show_error_dialog(f"Erreur de connexion: {str(e)}")

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
            # En cas d'erreur, forcer la fermeture
            self._force_quit()

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
            self._force_quit()

    def _cleanup_and_quit(self):
        """Nettoie les ressources et quitte proprement"""
        try:
            print("🧹 Nettoyage avant fermeture...")
            
            # Nettoyage de l'écran actuel
            if self.current_screen:
                self._safe_destroy_widget(self.current_screen)
            
            # Débinder tous les événements globaux
            self._unbind_widget_events(self.root)
            
            # Fermer les connexions réseau si nécessaire
            if hasattr(self.mllp_client, 'close'):
                try:
                    self.mllp_client.close()
                except:
                    pass
            
            print("✅ Nettoyage terminé")
            
        except Exception as e:
            print(f"⚠️ Erreur nettoyage: {e}")
        finally:
            self._force_quit()

    def _force_quit(self):
        """Force la fermeture de l'application"""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
        finally:
            print("👋 Application fermée")

    def _show_error_dialog(self, message):
        """Affiche une boîte de dialogue d'erreur"""
        try:
            messagebox.showerror("Erreur", message)
        except Exception as e:
            print(f"❌ Impossible d'afficher l'erreur: {e}")
            print(f"❌ Message d'erreur original: {message}")

    def get_current_user_info(self):
        """Retourne les informations de l'utilisateur actuel"""
        return {
            "username": self.current_user,
            "department": self.department,
            "connected": self.current_user is not None
        }

    def is_connected(self):
        """Vérifie si un utilisateur est connecté"""
        return self.current_user is not None