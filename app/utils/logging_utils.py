# -*- coding: utf-8 -*-
"""
Utilitaires de journalisation pour l'application HL7 Messenger.
"""
import logging
import os
from datetime import datetime

def setup_logger(name="HL7Messenger", log_file=None, level=logging.INFO, console=True):
    """
    Configure un logger avec les paramètres spécifiés
    
    Args:
        name (str): Nom du logger
        log_file (str, optional): Chemin du fichier de log
        level (int, optional): Niveau de log
        console (bool, optional): Affichage dans la console
    
    Returns:
        logging.Logger: Logger configuré
    """
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Format de date et message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler pour fichier de log
    if log_file:
        # Créer le dossier si nécessaire
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Handler pour la console
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

def log_message(logger, direction, message, endpoint, max_length=100):
    """
    Journalise un message HL7
    
    Args:
        logger (logging.Logger): Logger à utiliser
        direction (str): Direction du message (ENVOI/RECEPTION)
        message (str): Contenu du message
        endpoint (str): Point d'extrémité (serveur:port)
        max_length (int, optional): Longueur maximale du message à afficher
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Nettoyer le message pour l'affichage
    if message and len(message) > max_length:
        display_message = message[:max_length] + "..."
    else:
        display_message = message or ""
    
    # Remplacer les retours à la ligne pour la lisibilité
    display_message = display_message.replace("\r", "\\r").replace("\n", "\\n")
    
    logger.info(f"[{timestamp}] {direction} | {endpoint} | {display_message}")

def get_formatted_message(message, indent=0, max_segments=None, highlight_segment=None):
    """
    Formate un message HL7 pour une meilleure lisibilité
    
    Args:
        message (str): Message HL7 brut
        indent (int, optional): Indentation (nombre d'espaces)
        max_segments (int, optional): Nombre maximum de segments à afficher
        highlight_segment (str, optional): Segment à mettre en évidence (ex: 'PID')
    
    Returns:
        str: Message formaté
    """
    if not message:
        return "Message vide"
    
    # Diviser le message en segments
    segments = message.split('\r')
    
    # Limiter le nombre de segments si nécessaire
    if max_segments and len(segments) > max_segments:
        displayed_segments = segments[:max_segments]
        has_more = True
    else:
        displayed_segments = segments
        has_more = False
    
    # Formater chaque segment
    formatted_segments = []
    for segment in displayed_segments:
        if not segment:
            continue
        
        # Identifier le type de segment
        segment_type = segment[:3] if len(segment) >= 3 else ""
        
        # Ajouter l'indentation
        formatted_segment = " " * indent + segment
        
        # Mettre en évidence si demandé
        if highlight_segment and segment_type == highlight_segment:
            formatted_segment = f">>> {formatted_segment}"
        
        formatted_segments.append(formatted_segment)
    
    # Ajouter une indication s'il y a plus de segments
    if has_more:
        formatted_segments.append(f"{' ' * indent}... ({len(segments) - max_segments} segments supplémentaires)")
    
    return "\n".join(formatted_segments)