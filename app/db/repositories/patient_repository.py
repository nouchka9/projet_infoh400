# -*- coding: utf-8 -*-
"""
Repository pour la gestion des patients.
Fournit les méthodes CRUD pour les patients avec stockage JSON.
"""
from ..database import Database
from ...models.patient import Patient

class PatientRepository:
    """Gestionnaire des opérations CRUD pour les patients"""
    
    def __init__(self, database=None):
        """
        Initialise le repository
        
        Args:
            database (Database, optional): Instance de base de données
        """
        self.db = database or Database()
        
    def get_all(self):
        """
        Récupère tous les patients
        
        Returns:
            list: Liste d'objets Patient
        """
        data = self.db.load_data()
        
        patients = []
        for item in data:
            patient = Patient.from_dict(item)
            patients.append(patient)
            
        return patients
        
    def get_by_id(self, patient_id):
        """
        Récupère un patient par son ID
        
        Args:
            patient_id (str): ID du patient
            
        Returns:
            Patient: Instance de Patient ou None si non trouvé
        """
        data = self.db.load_data()
        
        for item in data:
            if item.get('id') == patient_id:
                return Patient.from_dict(item)
                
        return None
        
    def create(self, patient):
        """
        Crée un nouveau patient
        
        Args:
            patient (Patient): Instance de Patient à créer
            
        Returns:
            Patient: Instance de Patient créée
        """
        if not patient.id:
            raise ValueError("L'ID du patient est requis")
            
        # Vérifier que le patient n'existe pas déjà
        existing = self.get_by_id(patient.id)
        if existing:
            return self.update(patient)
            
        # Ajouter le patient
        data = self.db.load_data()
        data.append(patient.to_dict())
        self.db.save_data(data)
        
        return patient
        
    def update(self, patient):
        """
        Met à jour un patient existant
        
        Args:
            patient (Patient): Instance de Patient à mettre à jour
            
        Returns:
            Patient: Instance de Patient mise à jour
        """
        if not patient.id:
            raise ValueError("L'ID du patient est requis")
            
        data = self.db.load_data()
        
        # Rechercher le patient
        found = False
        for i, item in enumerate(data):
            if item.get('id') == patient.id:
                data[i] = patient.to_dict()
                found = True
                break
                
        # Si le patient n'existe pas, l'ajouter
        if not found:
            data.append(patient.to_dict())
            
        self.db.save_data(data)
        
        return patient
        
    def delete(self, patient_id):
        """
        Supprime un patient
        
        Args:
            patient_id (str): ID du patient à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        data = self.db.load_data()
        
        # Rechercher le patient
        for i, item in enumerate(data):
            if item.get('id') == patient_id:
                del data[i]
                self.db.save_data(data)
                return True
                
        return False
        
    def search(self, query):
        """
        Recherche des patients par nom, prénom ou ID
        
        Args:
            query (str): Terme de recherche
            
        Returns:
            list: Liste d'objets Patient correspondant à la recherche
        """
        data = self.db.load_data()
        query = query.lower()
        
        patients = []
        for item in data:
            if (query in str(item.get('id', '')).lower() or
                query in str(item.get('first_name', '')).lower() or
                query in str(item.get('last_name', '')).lower()):
                
                patient = Patient.from_dict(item)
                patients.append(patient)
                
        return patients