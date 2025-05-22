#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import time
import logging
import os
import sys
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("HL7Server")

# Caractères de contrôle MLLP
SB = b'\x0b'  # Start Block
EB = b'\x1c'  # End Block
CR = b'\x0d'  # Carriage Return

class SimpleMLLPServer:
    def __init__(self, host="0.0.0.0", port=2575, name="Default"):
        self.host = host
        self.port = port
        self.name = name
        self.running = False
        self.server = None
        
    def start(self):
        print(f"Démarrage du serveur {self.name} sur {self.host}:{self.port}")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.running = True
            print(f"✅ Serveur {self.name} en écoute sur {self.host}:{self.port}")
            
            while self.running:
                try:
                    client, address = self.server.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    logger.error(f"Erreur d'acceptation: {e}")
                    break
        except Exception as e:
            logger.error(f"Erreur de serveur: {e}")
        finally:
            if self.server:
                self.server.close()
            
    def handle_client(self, client_socket, address):
        print(f"📨 Connexion de {address[0]}:{address[1]}")
        buffer = b''
        
        try:
            client_socket.settimeout(10)
            
            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                        
                    buffer += data
                    
                    # Chercher un message MLLP complet
                    start = buffer.find(SB)
                    end = buffer.find(EB, start)
                    
                    if start >= 0 and end > start:
                        # Extraire le message
                        message = buffer[start+1:end].decode('utf-8')
                        print(f"✉️ Message reçu de {address[0]}:{address[1]}")
                        print("-" * 50)
                        print(message)
                        print("-" * 50)
                        
                        # Créer et envoyer un ACK
                        ack = create_ack(message)
                        mllp_ack = SB + ack.encode('utf-8') + EB + CR
                        client_socket.sendall(mllp_ack)
                        print(f"✅ ACK envoyé à {address[0]}:{address[1]}")
                        
                        # Réinitialiser le buffer
                        buffer = buffer[end+2:]
                except socket.timeout:
                    print(f"⏱️ Timeout pour {address[0]}:{address[1]}")
                    break
                except Exception as e:
                    logger.error(f"Erreur client: {e}")
                    break
        finally:
            client_socket.close()
            print(f"🔌 Connexion fermée: {address[0]}:{address[1]}")
            
def create_ack(message):
    try:
        # Extraire les informations du message original
        msg_id = "1"
        msg_type = "Unknown"
        
        lines = message.split("\r")
        for line in lines:
            if line.startswith("MSH|"):
                fields = line.split("|")
                if len(fields) > 10:
                    msg_id = fields[9]
                if len(fields) > 9:
                    msg_type = fields[8]
                break
                
        # Créer l'ACK
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        ack = f"MSH|^~\&|HL7SERVER|HOSPITAL|HL7CLIENT|HOSPITAL|{current_time}||ACK^{msg_type}|{msg_id}|P|2.5\rMSA|AA|{msg_id}|Message processed successfully"
        return ack
    except Exception as e:
        logger.error(f"Erreur de création d'ACK: {e}")
        return f"MSH|^~\&|HL7SERVER|HOSPITAL|HL7CLIENT|HOSPITAL|{datetime.now().strftime('%Y%m%d%H%M%S')}||ACK|1|P|2.5\rMSA|AA|1|Message processed"

def main():
    print("=" * 50)
    print("Serveur MLLP HL7 pour HL7 Messenger")
    print("=" * 50)
    print("Ce serveur va écouter sur plusieurs ports pour recevoir les messages HL7")
    print("Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    # Créer le dossier de logs
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Configuration des serveurs
    ports = {
        2575: "Principal", 
        2576: "Admission", 
        2577: "Laboratoire",
        2578: "Radiologie", 
        2579: "Pharmacie"
    }
    
    # Démarrer un serveur pour chaque port
    servers = []
    for port, name in ports.items():
        server = SimpleMLLPServer(port=port, name=name)
        thread = threading.Thread(target=server.start)
        thread.daemon = True
        thread.start()
        servers.append((server, thread))
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt des serveurs...")
        for server, _ in servers:
            server.running = False
        
if __name__ == "__main__":
    main()
