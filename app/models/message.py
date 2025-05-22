# app/models/message.py
from datetime import datetime
import uuid
 
class Message:
    """Représentation d'un message HL7 dans le système"""
    def __init__(self, message_type=None, content=None, source=None, 
                 destination=None, patient_id=None, status="PENDING", id=None):
        """
        Initialise un message HL7
        Args:
            message_type (str, optional): Type de message (ex: ADT^A01)
            content (str, optional): Contenu brut du message
            source (str, optional): Source du message
            destination (str, optional): Destination du message
            patient_id (str, optional): ID du patient concerné
            status (str, optional): Statut du message
            id (str, optional): ID unique du message
        """
        self.id = id or str(uuid.uuid4())
        self.message_type = message_type
        self.content = content
        self.source = source
        self.destination = destination
        self.patient_id = patient_id
        self.status = status
        self.created_at = datetime.now().isoformat()
    def to_dict(self):
        """
        Convertit le message en dictionnaire
        Returns:
            dict: Données du message
        """
        return {
            'id': self.id,
            'message_type': self.message_type,
            'content': self.content,
            'source': self.source,
            'destination': self.destination,
            'patient_id': self.patient_id,
            'status': self.status,
            'created_at': self.created_at
        }
    @classmethod
    def from_dict(cls, data):
        """
        Crée un message à partir d'un dictionnaire
        Args:
            data (dict): Données du message
        Returns:
            Message: Objet message
        """
        message = cls(
            message_type=data.get('message_type'),
            content=data.get('content'),
            source=data.get('source'),
            destination=data.get('destination'),
            patient_id=data.get('patient_id'),
            status=data.get('status'),
            id=data.get('id')
        )
        if 'created_at' in data:
            message.created_at = data['created_at']
        return message