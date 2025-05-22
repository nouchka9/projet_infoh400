#!/bin/bash
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
