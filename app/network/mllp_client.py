# MLLP Client implementation
"""
Client MLLP pour envoyer des messages HL7 à des serveurs distants.
Implémentation du protocole MLLP (Minimal Lower Layer Protocol) pour HL7.
"""
import socket
import logging
from datetime import datetime

class MLLPClient:
    SB = b'\x0b'
    EB = b'\x1c'
    CR = b'\x0d'
    
    def __init__(self, host_config=None):
        self.logger = logging.getLogger("HL7Messenger.MLLPClient")
        self.host_config = host_config or {}
        self.timeout = 30
        self.default_hosts = {
            "ADMISSION_SYSTEM": {"host": "localhost", "port": 2576},
            "LAB_SYSTEM": {"host": "localhost", "port": 2577},
            "ORDER_SYSTEM": {"host": "localhost", "port": 2578},
            "PHARMACY_SYSTEM": {"host": "localhost", "port": 2579}
        }
    
    def log_message(self, direction, message, endpoint):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.logger.info(f"[{timestamp}] {direction} | {endpoint} | {message[:50]}...")
    
    def test_connection(self, destination):
        """Teste la connexion à une destination sans envoyer de message
        
        Args:
            destination (str): Nom de la destination à tester
            
        Returns:
            tuple: (success, error_message)
        """
        host, port = self._get_destination_endpoint(destination)
        if not host or not port:
            return False, f"Destination inconnue: {destination}"
            
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)  # Timeout court pour le test
                s.connect((host, port))
                return True, "Connexion établie"
        except socket.timeout:
            return False, f"Timeout lors de la connexion à {host}:{port}"
        except ConnectionRefusedError:
            return False, f"Connexion refusée par {host}:{port} - Vérifiez que le serveur MLLP est démarré"
        except Exception as e:
            return False, f"Erreur lors du test de connexion: {str(e)}"
    
    def send_message(self, message, destination, test_mode=False):
        """Envoie un message HL7 via MLLP
        
        Args:
            message (str): Message HL7 à envoyer
            destination (str): Destination (nom ou host:port)
            test_mode (bool, optional): Mode test (pas d'envoi réel)
            
        Returns:
            tuple: (success, response)
        """
        if test_mode:
            self.logger.info(f"[MODE TEST] Message simulé envoyé à {destination}")
            return True, "Message accepté (simulation)"
            
        host, port = self._get_destination_endpoint(destination)
        if not host or not port:
            error_msg = f"Destination inconnue: {destination}"
            self.logger.error(error_msg)
            return False, error_msg
            
        mllp_message = self.SB + message.encode('utf-8') + self.EB + self.CR
        self.log_message("ENVOI", message, f"{host}:{port}")
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((host, port))
                s.sendall(mllp_message)
                ack_data = b''
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    ack_data += chunk
                    if self.EB in chunk:
                        break
                        
                if ack_data:
                    start = ack_data.find(self.SB) + 1
                    end = ack_data.find(self.EB)
                    if start > 0 and end > start:
                        ack_message = ack_data[start:end].decode('utf-8')
                        self.log_message("ACK", ack_message, f"{host}:{port}")
                        return self._validate_ack(ack_message)
                        
                self.logger.warning(f"Pas d'accusé de réception reçu de {destination}")
                return False, "Pas d'accusé de réception"
                
        except socket.timeout:
            return False, f"Timeout lors de la connexion à {host}:{port}"
        except ConnectionRefusedError:
            return False, f"Connexion refusée par {host}:{port} - Vérifiez que le serveur MLLP est démarré"
        except Exception as e:
            return False, f"Erreur lors de l'envoi du message: {str(e)}"
    
    def _get_destination_endpoint(self, destination):
        if destination in self.host_config:
            config = self.host_config[destination]
            return config.get("host", "localhost"), int(config.get("port", 0))
        elif destination in self.default_hosts:
            config = self.default_hosts[destination]
            return config["host"], config["port"]
        elif ":" in destination:
            parts = destination.split(":")
            if len(parts) == 2 and parts[1].isdigit():
                return parts[0], int(parts[1])
        return None, None

    def _validate_ack(self, ack_message):
        try:
            if "MSA|AA|" in ack_message:
                return True, "Message accepté"
            elif "MSA|AE|" in ack_message:
                return False, "Erreur d'application"
            elif "MSA|AR|" in ack_message:
                return False, "Message rejeté"
            else:
                return False, "ACK non reconnu"
        except Exception as e:
            return False, f"Erreur de validation: {str(e)}"
    def set_demo_mode(self, demo_mode):
        """Active ou désactive le mode démo Args: demo_mode (bool): True pour activer le mode démo """
        self.demo_mode = demo_mode
        if demo_mode:
           self.logger.info("Mode démo activé - Les messages ne seront pas réellement envoyés")
        else:
           self.logger.info("Mode démo désactivé - Les messages seront envoyés réellement")