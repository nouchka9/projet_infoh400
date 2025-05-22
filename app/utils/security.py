# -*- coding: utf-8 -*-
"""
Utilitaires de sécurité pour l'application HL7 Messenger.
Module optionnel qui pourra être utilisé dans les versions futures.
"""
import os
import hashlib
import base64
import hmac
import secrets
from datetime import datetime, timedelta
import json

def generate_secure_token(length=32):
    """
    Génère un token aléatoire et sécurisé
    
    Args:
        length (int, optional): Longueur du token en bytes
    
    Returns:
        str: Token en hexadécimal
    """
    return secrets.token_hex(length)

def hash_password(password, salt=None):
    """
    Crée un hash sécurisé d'un mot de passe
    
    Args:
        password (str): Mot de passe à hasher
        salt (bytes, optional): Sel (généré si None)
    
    Returns:
        tuple: (hash_password, salt)
    """
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    
    # Convertir le mot de passe en bytes si nécessaire
    pwd_bytes = password.encode('utf-8') if isinstance(password, str) else password
    
    # Générer le hash avec le sel
    hash_obj = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt, 100000)
    
    return hash_obj.hex(), salt.hex()

def verify_password(password, stored_hash, salt):
    """
    Vérifie un mot de passe par rapport à un hash stocké
    
    Args:
        password (str): Mot de passe à vérifier
        stored_hash (str): Hash stocké
        salt (str): Sel en hexadécimal
    
    Returns:
        bool: True si le mot de passe correspond
    """
    # Calculer le hash avec le même sel
    calculated_hash, _ = hash_password(password, salt)
    
    # Comparer les hash
    return calculated_hash == stored_hash

def create_session_token(user_id, role, secret_key, expiry_hours=24):
    """
    Crée un token de session pour un utilisateur
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        role (str): Rôle de l'utilisateur
        secret_key (str): Clé secrète pour signer le token
        expiry_hours (int, optional): Validité en heures
    
    Returns:
        str: Token de session (format JWT-like)
    """
    # Créer les données du token
    now = datetime.now()
    expiry = now + timedelta(hours=expiry_hours)
    
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp())
    }
    
    # Encoder en Base64
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    # Créer la signature
    key = secret_key.encode() if isinstance(secret_key, str) else secret_key
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(key, message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    # Assemblage du token
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_session_token(token, secret_key):
    """
    Vérifie un token de session
    
    Args:
        token (str): Token à vérifier
        secret_key (str): Clé secrète pour vérifier la signature
    
    Returns:
        dict or None: Payload du token si valide, None sinon
    """
    try:
        # Découper le token
        header_b64, payload_b64, signature_b64 = token.split('.')
        
        # Vérifier la signature
        key = secret_key.encode() if isinstance(secret_key, str) else secret_key
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(key, message.encode(), hashlib.sha256).digest()
        actual_signature = base64.urlsafe_b64decode(signature_b64 + '===')
        
        if not hmac.compare_digest(expected_signature, actual_signature):
            return None
        
        # Décoder le payload
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '===').decode())
        
        # Vérifier l'expiration
        now = datetime.now()
        if payload.get('exp', 0) < now.timestamp():
            return None
        
        return payload
        
    except Exception:
        return None

def encrypt_hl7_content(message, key):
    """
    Placeholder pour une future fonction de chiffrement des messages HL7
    Cette fonction n'est pas implémentée dans cette version.
    
    Args:
        message (str): Message HL7 à chiffrer
        key (str): Clé de chiffrement
    
    Returns:
        str: Message chiffré
    """
    # Cette fonction est un placeholder et ne fait rien pour le moment
    return message

def decrypt_hl7_content(encrypted_message, key):
    """
    Placeholder pour une future fonction de déchiffrement des messages HL7
    Cette fonction n'est pas implémentée dans cette version.
    
    Args:
        encrypted_message (str): Message HL7 chiffré
        key (str): Clé de déchiffrement
    
    Returns:
        str: Message déchiffré
    """
    # Cette fonction est un placeholder et ne fait rien pour le moment
    return encrypted_message