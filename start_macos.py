#!/usr/bin/env python3
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
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
