#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction pour les problèmes macOS - HL7 Messenger
Résout les problèmes de corruption mémoire et de threading
"""
import os

def fix_macos_issues():
    """Corrige les problèmes spécifiques à macOS"""
    print("🍎 Correction des problèmes macOS...")
    
    # 1. Corriger la configuration des ports
    fix_config_ports()
    
    # 2. Ajouter variables d'environnement pour macOS
    fix_environment_variables()
    
    # 3. Créer un lanceur macOS-friendly
    create_macos_launcher()
    
    print("✅ Corrections macOS appliquées!")

def fix_config_ports():
    """Corrige la configuration des ports"""
    config_content = '''# -*- coding: utf-8 -*-
"""
Configuration corrigée pour HL7 Messenger
Tous les départements pointent vers le même serveur
"""
class Config:
    def __init__(self):
        # SOLUTION: Tous les départements utilisent le même serveur
        # Le serveur MLLP écoute sur 2575, donc tout pointe vers 2575
        self.settings = {
            "hosts": {
                "ADMISSION_SYSTEM": {"host": "localhost", "port": 2575},
                "LAB_SYSTEM": {"host": "localhost", "port": 2575},
                "ORDER_SYSTEM": {"host": "localhost", "port": 2575},
                "PHARMACY_SYSTEM": {"host": "localhost", "port": 2575}
            }
        }

    def get(self, key):
        return self.settings.get(key)

    def get_section(self, section):
        return self.settings.get(section, {})
'''
    
    with open("app/config.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    print("✅ Configuration des ports corrigée")

def fix_environment_variables():
    """Ajoute les variables d'environnement pour macOS"""
    env_script = '''#!/bin/bash
# Variables d'environnement pour HL7 Messenger sur macOS

# Corriger les problèmes de mémoire objc
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Optimiser pour macOS
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Désactiver certains warnings macOS
export PYTHONWARNINGS="ignore::UserWarning"

echo "🍎 Variables d'environnement macOS configurées"
echo "🚀 Lancement de HL7 Messenger..."

# Lancer l'application
python app/main.py
'''
    
    with open("start_macos.sh", "w", encoding="utf-8") as f:
        f.write(env_script)
    
    # Rendre le script exécutable
    os.chmod("start_macos.sh", 0o755)
    print("✅ Script de lancement macOS créé")

def create_macos_launcher():
    """Crée un lanceur spécifique macOS"""
    launcher_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur HL7 Messenger optimisé pour macOS
Résout les problèmes de threading et mémoire
"""
import os
import sys

def setup_macos_environment():
    """Configure l'environnement pour macOS"""
    # Variables d'environnement pour corriger les problèmes macOS
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'
    
    # Ajouter le chemin du projet
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def main():
    """Point d'entrée principal pour macOS"""
    print("🍎 HL7 Messenger - Lanceur macOS")
    print("=" * 40)
    
    # Configuration environnement
    setup_macos_environment()
    
    try:
        # Import après configuration environnement
        from app.main import main as app_main
        app_main()
        
    except KeyboardInterrupt:
        print("\\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    
    with open("start_macos.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    print("✅ Lanceur macOS créé")

if __name__ == "__main__":
    fix_macos_issues()
    
    print("\\n" + "=" * 50)
    print("🎯 SOLUTIONS APPLIQUÉES:")
    print("✅ Ports synchronisés (tout sur 2575)")
    print("✅ Variables environnement macOS")
    print("✅ Lanceur optimisé macOS")
    print("=" * 50)
    print("🚀 UTILISEZ MAINTENANT:")
    print("   1. Terminal 1: python -m app.network.mllp_server")
    print("   2. Terminal 2: python start_macos.py")
    print("   OU: bash start_macos.sh")
    print("=" * 50)