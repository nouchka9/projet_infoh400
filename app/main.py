# -*- coding: utf-8 -*-
"""
Point d'entrée principal de l'application HL7 Messenger.
"""

import tkinter as tk
from tkinter import PhotoImage, messagebox
import os
import logging
import platform
import sys
from app.config import Config
from app.ui.app import HL7MessengerApp

def main():
    print("====================================================")
    print("  HL7 Messenger - Interface de messages hospitaliers")
    print("====================================================")
    print("Cette application permet aux départements hospitaliers d'envoyer")
    print("et recevoir des messages HL7 standardisés. Utilisez le mode 'Démo'")
    print("pour tester sans serveur ou 'Normal' pour connexion réelle.")
    print("====================================================")
    
    # Configuration du logging
    logging.basicConfig(level=logging.INFO)
    
    # Charger la configuration
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                  "resources", "config.json")
        config = Config(config_path)
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement de la configuration: {e}")
        print("Utilisation de la configuration par défaut.")
        config = Config()
    
    # Interface graphique
    root = tk.Tk()
    root.title("HL7 Messenger - Interface Hôpital")
    
    # Déterminer le chemin de base du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resources_dir = os.path.join(base_dir, "resources")
    
    print(f"Dossier base : {base_dir}")
    print(f"Dossier ressources : {resources_dir}")
    
    # Gestion des icônes selon le système d'exploitation
    if platform.system() == "Darwin":  # macOS
        try:
            png_path = os.path.join(resources_dir, "logo.png")
            print(f"Tentative de chargement de l'icône PNG depuis : {png_path}")
            
            if os.path.exists(png_path):
                icon = PhotoImage(file=png_path)
                root.iconphoto(True, icon)
                print("✅ Icône PNG chargée avec succès")
            else:
                print(f"⚠️ Fichier PNG introuvable : {png_path}")
        except Exception as e:
            print(f"❌ Erreur chargement icône macOS : {e}")
    else:
        # Windows/Linux
        try:
            ico_path = os.path.join(resources_dir, "logo.ico")
            print(f"Tentative de chargement de l'icône ICO depuis : {ico_path}")
            
            if os.path.exists(ico_path):
                root.iconbitmap(ico_path)
                print("✅ Icône ICO chargée avec succès")
            else:
                print(f"⚠️ Fichier ICO introuvable : {ico_path}")
        except Exception as e:
            print(f"❌ Erreur chargement icône Windows/Linux : {e}")
    
    # Vérification du mode démo
    mllp_config = config.get_section('mllp')
    if mllp_config.get('demo_mode', False):
        messagebox.showinfo("Mode Démo", 
                          "L'application fonctionne en mode démo.\n"
                          "Les messages ne seront pas réellement envoyés "
                          "à un serveur distant.")
    
    # Configuration de la taille initiale de la fenêtre
    width, height = 1024, 768
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Créer l'application
    try:
        app = HL7MessengerApp(root, config)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Erreur d'initialisation de l'application : {e}")
        messagebox.showerror("Erreur", f"Impossible de démarrer l'application : {e}")
        sys.exit(1)
    
    # Démarrer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()