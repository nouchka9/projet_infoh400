# -*- coding: utf-8 -*-
"""
Module de gestion de la base de données.
Gère le stockage et la récupération des données patient au format JSON.
"""
import os
import json
from pathlib import Path

class Database:
    """Gestionnaire de données pour le stockage JSON des patients"""
    
    def __init__(self, data_path=None):
        """
        Initialise la connexion au fichier de données
        
        Args:
            data_path (str, optional): Chemin vers le fichier JSON
        """
        if data_path is None:
            # Créer le fichier dans le dossier resources par défaut
            root_dir = Path(__file__).parent.parent.parent
            data_path = os.path.join(root_dir, 'resources', 'patients.json')
            
        self.data_path = data_path
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        """S'assure que le fichier JSON existe, sinon le crée"""
        if not os.path.exists(self.data_path):
            directory = os.path.dirname(self.data_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(self.data_path, 'w') as f:
                json.dump([], f)
                
    def load_data(self):
        """
        Charge les données depuis le fichier JSON
        
        Returns:
            list: Liste des données patients
        """
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            return []
            
    def save_data(self, data):
        """
        Enregistre les données dans le fichier JSON
        
        Args:
            data (list): Liste des données à enregistrer
            
        Returns:
            bool: True si l'enregistrement a réussi, False sinon
        """
        try:
            with open(self.data_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des données: {e}")
            return False
