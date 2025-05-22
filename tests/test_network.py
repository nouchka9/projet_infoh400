# -*- coding: utf-8 -*-
"""
Tests unitaires pour le client MLLP.
"""
import unittest
import threading
import socket
import time
import os
import sys

# Ajouter le répertoire parent au path pour importer les modules de l'application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.network.mllp_client import MLLPClient

class MockMLLPServer:
    """Serveur MLLP simulé pour tests"""
    
    SB = b'\x0b'  # Start Block
    EB = b'\x1c'  # End Block
    CR = b'\x0d'  # Carriage Return
    
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.received_messages = []
    
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        # Démarrer dans un thread
        self.server_thread = threading.Thread(target=self._run)
        self.server_thread.daemon = True
        self.server_thread.start()
        
    def _run(self):
        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                client_socket.settimeout(1)
                
                # Recevoir le message
                data = b''
                while self.running:
                    try:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                        if self.EB in data:
                            break
                    except socket.timeout:
                        break
                
                # Extraire le message
                if data and self.SB in data and self.EB in data:
                    start = data.find(self.SB) + 1
                    end = data.find(self.EB)
                    if start > 0 and end > start:
                        message = data[start:end].decode('utf-8')
                        self.received_messages.append(message)
                        
                        # Envoyer un ACK
                        ack_message = "MSH|^~\\&|ACK_SERVER||CLIENT||20240517||ACK|1|P|2.5\rMSA|AA|1|Everything OK\r"
                        ack_data = self.SB + ack_message.encode('utf-8') + self.EB + self.CR
                        client_socket.sendall(ack_data)
                
                client_socket.close()
            except:
                pass
    
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()


class TestMLLPClient(unittest.TestCase):
    
    def setUp(self):
        self.mock_server = MockMLLPServer(port=12345)
        self.mock_server.start()
        time.sleep(0.1)  # Attendre que le serveur démarre
        
        # Configurer le client
        self.client = MLLPClient({
            'TEST_SERVER': {'host': 'localhost', 'port': 12345}
        })
    
    def tearDown(self):
        self.mock_server.stop()
    
    def test_send_message(self):
        """Test l'envoi d'un message et réception de l'ACK"""
        test_message = "MSH|^~\\&|SENDER|FACILITY|RECEIVER|FACILITY|20240517||ADT^A01|123456|P|2.5\rPID|||12345^^^FACILITY||DOE^JOHN||19700101|M"
        success, response = self.client.send_message(test_message, 'TEST_SERVER')
        
        # Vérifier que le message a été envoyé avec succès
        self.assertTrue(success)
        self.assertIn("Message accepté", response)
        
        # Vérifier que le serveur a bien reçu le message
        self.assertEqual(len(self.mock_server.received_messages), 1)
        self.assertEqual(self.mock_server.received_messages[0], test_message)
    
    def test_connection_failure(self):
        """Test l'envoi vers un serveur inexistant"""
        success, response = self.client.send_message("TEST", "NONEXISTENT_SERVER")
        self.assertFalse(success)
    
    def test_destination_parsing(self):
        """Test la fonction qui détermine l'hôte et le port de destination"""
        # Test avec un ID de destination dans la config
        host, port = self.client._get_destination_endpoint('TEST_SERVER')
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, 12345)
        
        # Test avec un format "host:port"
        host, port = self.client._get_destination_endpoint('example.com:8080')
        self.assertEqual(host, 'example.com')
        self.assertEqual(port, 8080)
        
        # Test avec une destination inconnue
        host, port = self.client._get_destination_endpoint('UNKNOWN')
        self.assertIsNone(host)
        self.assertIsNone(port)
    
    def test_validate_ack(self):
        """Test la validation des ACK"""
        # ACK positif
        success, message = self.client._validate_ack("MSH|^~\\&|ACK_SERVER||CLIENT||20240517||ACK|1|P|2.5\rMSA|AA|123|OK\r")
        self.assertTrue(success)
        
        # ACK erreur d'application
        success, message = self.client._validate_ack("MSH|^~\\&|ACK_SERVER||CLIENT||20240517||ACK|1|P|2.5\rMSA|AE|123|Error\r")
        self.assertFalse(success)
        
        # ACK rejet
        success, message = self.client._validate_ack("MSH|^~\\&|ACK_SERVER||CLIENT||20240517||ACK|1|P|2.5\rMSA|AR|123|Rejected\r")
        self.assertFalse(success)
        
        # Format inconnu
        success, message = self.client._validate_ack("INVALID_FORMAT")
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()