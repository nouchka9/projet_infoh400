#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement du serveur HL7 MLLP
Usage: python start_server.py [port]
"""
import os
import sys
import subprocess

def main():
    print("🚀 Lancement du serveur HL7 MLLP")
    print("=" * 40)
    
    # Vérifier qu'on est dans le bon répertoire
    if not os.path.exists("app"):
        print("❌ Erreur: Ce script doit être exécuté depuis le répertoire racine du projet")
        print("💡 Naviguez vers le dossier hl7_messenger/ et relancez")
        sys.exit(1)
    
    # Port par défaut
    port = "2575"
    
    # Vérifier les arguments
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print(f"🔧 Port personnalisé: {port}")
    else:
        print(f"🌐 Port par défaut: {port}")
    
    print("📍 Démarrage du serveur...")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 40)
    
    try:
        # Lancer le serveur
        if len(sys.argv) > 1:
            subprocess.run([sys.executable, "-m", "app.network.mllp_server", port])
        else:
            subprocess.run([sys.executable, "-m", "app.network.mllp_server"])
            
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()