# -*- coding: utf-8 -*-
"""
Modèle représentant un patient dans le système.
"""
from datetime import datetime

class Patient:
    """Représentation d'un patient dans le système"""
    
    def __init__(self, id=None, first_name=None, last_name=None, 
                 birth_date=None, gender=None, address=None):
        """
        Initialise un patient
        
        Args:
            id (str, optional): Identifiant unique du patient
            first_name (str, optional): Prénom
            last_name (str, optional): Nom de famille
            birth_date (str, optional): Date de naissance (format YYYYMMDD)
            gender (str, optional): Genre ('M', 'F', 'O')
            address (dict, optional): Adresse du patient
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.address = address or {}
        
    @property
    def full_name(self):
        """Renvoie le nom complet du patient"""
        return f"{self.last_name}, {self.first_name}"
        
    @property
    def age(self):
        """Calcule l'âge du patient à partir de sa date de naissance"""
        if not self.birth_date:
            return None
            
        try:
            # Format de date YYYYMMDD
            year = int(self.birth_date[:4])
            month = int(self.birth_date[4:6])
            day = int(self.birth_date[6:8])
            
            birth_date = datetime(year, month, day)
            today = datetime.now()
            
            age = today.year - birth_date.year
            
            # Ajustement si l'anniversaire n'est pas encore passé cette année
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
                
            return age
        except (ValueError, TypeError, IndexError):
            return None
            
    def to_dict(self):
        """
        Convertit le patient en dictionnaire
        
        Returns:
            dict: Données du patient
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'address': self.address
        }
        
    def __str__(self):
        """Représentation textuelle du patient"""
        return f"{self.full_name} ({self.id})"
        
    @classmethod
    def from_dict(cls, data):
        """
        Crée un patient à partir d'un dictionnaire
        
        Args:
            data (dict): Données du patient
            
        Returns:
            Patient: Instance de Patient
        """
        return cls(
            id=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender'),
            address=data.get('address')
        )