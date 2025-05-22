# -*- coding: utf-8 -*-
"""
Parser pour les messages HL7.
"""
from hl7apy import parser
import logging

def parse_hl7_message(raw_message):
    """
    Parse un message HL7 brut
    
    Args:
        raw_message (str): Message HL7 brut
    
    Returns:
        Message or None: Message HL7 parsé ou None en cas d'erreur
    """
    logger = logging.getLogger("HL7Messenger.Parser")
    
    try:
        # Nettoyer le message
        if raw_message.startswith('\x0b'):
            raw_message = raw_message[1:]
        if raw_message.endswith('\x1c\x0d'):
            raw_message = raw_message[:-2]
        
        # Parser le message
        parsed = parser.parse_message(raw_message, validation_level=0)
        logger.info(f"Message parsé avec succès: {parsed.msh.msh_9.value}")
        return parsed
        
    except Exception as e:
        logger.error(f"Erreur lors du parsing du message HL7: {str(e)}")
        return None