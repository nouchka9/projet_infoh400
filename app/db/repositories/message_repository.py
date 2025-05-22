# -*- coding: utf-8 -*-
"""
Repository pour la gestion des messages HL7.
"""
import json
from ..database import Database
from ...models.message import Message
 
class MessageRepository:
    """Gestionnaire des opérations CRUD pour les messages HL7"""
   
    def __init__(self, database=None):
        """
        Initialise le repository
       
        Args:
            database (Database, optional): Instance de base de données
        """
        self.db = database or Database()
       
    def save(self, message):
        """
        Enregistre un message HL7
       
        Args:
            message (Message): Message à enregistrer
           
        Returns:
            Message: Message enregistré
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR REPLACE INTO messages
            (id, type, content, source, destination, patient_id, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message.id,
                message.message_type,
                message.content,
                message.source,
                message.destination,
                message.patient_id,
                message.status,
                message.created_at
            ))
            conn.commit()
           
        return message
       
    def get_by_id(self, message_id):
        """
        Récupère un message par son ID
       
        Args:
            message_id (str): ID du message
           
        Returns:
            Message: Message trouvé ou None
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM messages WHERE id = ?', (message_id,))
            row = cursor.fetchone()
           
            if row:
                return Message(
                    id=row['id'],
                    message_type=row['type'],
                    content=row['content'],
                    source=row['source'],
                    destination=row['destination'],
                    patient_id=row['patient_id'],
                    status=row['status']
                )
            return None
           
    def get_by_patient(self, patient_id):
        """
        Récupère tous les messages d'un patient
       
        Args:
            patient_id (str): ID du patient
           
        Returns:
            list: Liste des messages du patient
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM messages
            WHERE patient_id = ?
            ORDER BY created_at DESC
            ''', (patient_id,))
           
            messages = []
            for row in cursor.fetchall():
                message = Message(
                    id=row['id'],
                    message_type=row['type'],
                    content=row['content'],
                    source=row['source'],
                    destination=row['destination'],
                    patient_id=row['patient_id'],
                    status=row['status']
                )
                # Restaurer la date de création d'origine
                message.created_at = row['created_at']
                messages.append(message)
               
            return messages
           
    def get_recent(self, limit=50):
        """
        Récupère les messages les plus récents
       
        Args:
            limit (int, optional): Nombre maximum de messages
           
        Returns:
            list: Liste des messages récents
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT * FROM messages
            ORDER BY created_at DESC
            LIMIT ?
            ''', (limit,))
           
            messages = []
            for row in cursor.fetchall():
                message = Message(
                    id=row['id'],
                    message_type=row['type'],
                    content=row['content'],
                    source=row['source'],
                    destination=row['destination'],
                    patient_id=row['patient_id'],
                    status=row['status']
                )
                message.created_at = row['created_at']
                messages.append(message)
               
            return messages
           
    def delete(self, message_id):
        """
        Supprime un message
       
        Args:
            message_id (str): ID du message
           
        Returns:
            bool: True si supprimé, False sinon
        """
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
            conn.commit()
           
            return cursor.rowcount > 0
 