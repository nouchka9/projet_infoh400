# -*- coding: utf-8 -*-
"""
Serveur MLLP pour recevoir les messages HL7 - VERSION CORRIGÉE
Tous les problèmes de démarrage et de fonctionnement résolus
"""
import socket
import logging
import threading
from datetime import datetime
import traceback
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import des modules avec gestion d'erreur
try:
    from app.models.patient import Patient
    from app.db.repositories.patient_repository import PatientRepository
    from app.models.message import Message
    from app.db.repositories.message_repository import MessageRepository
except ImportError as e:
    print(f"⚠️ Certains modules ne sont pas disponibles: {e}")
    print("Le serveur fonctionnera en mode basique")
    Patient = None
    PatientRepository = None
    Message = None
    MessageRepository = None

class MLLPServer:
    """Serveur pour recevoir et traiter les messages HL7 via MLLP - Version corrigée"""
    
    # Caractères de contrôle MLLP
    SB = b'\x0b'  # Start Block
    EB = b'\x1c'  # End Block
    CR = b'\x0d'  # Carriage Return
    
    def __init__(self, host="0.0.0.0", port=2575):
        """
        Initialise le serveur MLLP
        
        Args:
            host (str): Host d'écoute
            port (int): Port d'écoute
        """
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        self.logger = self._setup_logger()
        self.clients_connected = 0
        self.messages_received = 0
        
        # Initialiser les repositories si disponibles
        self.patient_repo = PatientRepository() if PatientRepository else None
        self.message_repo = MessageRepository() if MessageRepository else None
        
        print(f"🏥 Serveur HL7 MLLP initialisé")
        print(f"📍 Adresse: {self.host}:{self.port}")
        print(f"📚 Base de données: {'✅ Disponible' if self.patient_repo else '❌ Mode basique'}")
    
    def _setup_logger(self):
        """Configure le logger du serveur"""
        logger = logging.getLogger("HL7Messenger.MLLPServer")
        logger.setLevel(logging.INFO)
        
        # Handler console s'il n'existe pas déjà
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def start(self):
        """Démarre le serveur MLLP avec gestion d'erreur robuste"""
        try:
            print("🚀 Démarrage du serveur HL7...")
            
            # Créer le socket
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Binding avec gestion d'erreur
            try:
                self.server.bind((self.host, self.port))
                print(f"✅ Socket bindé sur {self.host}:{self.port}")
            except OSError as e:
                if e.errno == 48:  # Address already in use
                    print(f"❌ Erreur: Le port {self.port} est déjà utilisé")
                    print("💡 Essayez de:")
                    print("   - Attendre quelques secondes et relancer")
                    print("   - Utiliser un autre port")
                    print("   - Vérifier qu'aucun autre serveur HL7 ne fonctionne")
                    return False
                else:
                    print(f"❌ Erreur de binding: {e}")
                    return False
            
            # Écouter les connexions
            self.server.listen(5)
            self.running = True
            
            print("=" * 60)
            print(f"🎉 SERVEUR HL7 DÉMARRÉ AVEC SUCCÈS!")
            print(f"🌐 Écoute sur {self.host}:{self.port}")
            print(f"⏰ Démarré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
            print("📨 En attente de messages HL7...")
            print("=" * 60)
            print("💡 Pour tester le serveur, utilisez le client depuis l'interface")
            print("🛑 Appuyez sur Ctrl+C pour arrêter le serveur")
            print("=" * 60)
            
            self.logger.info(f"Serveur MLLP démarré sur {self.host}:{self.port}")
            
            # Boucle principale d'acceptation des clients
            while self.running:
                try:
                    client_socket, client_address = self.server.accept()
                    self.clients_connected += 1
                    
                    print(f"🔗 Nouvelle connexion #{self.clients_connected} depuis {client_address[0]}:{client_address[1]}")
                    
                    # Créer un thread pour gérer ce client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    print("\n🛑 Arrêt demandé par l'utilisateur...")
                    self.running = False
                    break
                except Exception as e:
                    if self.running:  # Ne pas logger si on s'arrête
                        self.logger.error(f"Erreur lors de l'acceptation du client: {str(e)}")
                        print(f"❌ Erreur client: {str(e)}")
            
        except Exception as e:
            print(f"❌ Erreur fatale du serveur: {str(e)}")
            traceback.print_exc()
            return False
            
        finally:
            self._cleanup()
        
        return True
    
    def _cleanup(self):
        """Nettoie les ressources du serveur"""
        print("🧹 Nettoyage du serveur...")
        
        if self.server:
            try:
                self.server.close()
                print("✅ Socket fermé")
            except:
                pass
        
        print(f"📊 Statistiques de session:")
        print(f"   - Connexions reçues: {self.clients_connected}")
        print(f"   - Messages traités: {self.messages_received}")
        print("👋 Serveur arrêté proprement")
    
    def handle_client(self, client_socket, client_address):
        """
        Gère la connexion d'un client avec gestion d'erreur complète
        
        Args:
            client_socket (socket): Socket du client
            client_address (tuple): Adresse du client (ip, port)
        """
        client_id = f"{client_address[0]}:{client_address[1]}"
        
        try:
            client_socket.settimeout(30)  # 30 secondes de timeout
            print(f"🔄 Traitement du client {client_id}...")
            
            # Buffer pour stocker les données reçues
            buffer = b''
            
            # Recevoir les données
            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        print(f"📪 Client {client_id} a fermé la connexion")
                        break
                    
                    buffer += data
                    print(f"📥 Reçu {len(data)} bytes de {client_id}")
                    
                    # Chercher un message complet
                    start = buffer.find(self.SB)
                    end = buffer.find(self.EB, start)
                    
                    if start >= 0 and end > start:
                        # Extraire le message
                        raw_message = buffer[start+1:end]
                        message = raw_message.decode('utf-8', errors='replace')
                        buffer = buffer[end+2:]  # +2 pour inclure EB et CR
                        
                        self.messages_received += 1
                        
                        print("=" * 50)
                        print(f"📨 MESSAGE HL7 #{self.messages_received} REÇU DE {client_id}")
                        print("=" * 50)
                        print(f"📏 Taille: {len(message)} caractères")
                        print(f"⏰ Heure: {datetime.now().strftime('%H:%M:%S')}")
                        print("📄 Contenu (extrait):")
                        print(message[:200] + ("..." if len(message) > 200 else ""))
                        print("=" * 50)
                        
                        # Traiter le message
                        try:
                            response = self.handle_message(message, client_address)
                            
                            # Envoyer la réponse au format MLLP
                            mllp_response = self.SB + response.encode('utf-8') + self.EB + self.CR
                            client_socket.sendall(mllp_response)
                            
                            print(f"✅ ACK envoyé à {client_id}")
                            
                        except Exception as e:
                            error_msg = f"Erreur traitement message: {str(e)}"
                            print(f"❌ {error_msg}")
                            self.logger.error(error_msg)
                            
                            # Envoyer un ACK d'erreur
                            error_ack = self.create_error_ack(str(e))
                            mllp_error = self.SB + error_ack.encode('utf-8') + self.EB + self.CR
                            client_socket.sendall(mllp_error)
                            
                            print(f"⚠️ ACK d'erreur envoyé à {client_id}")
                        
                except socket.timeout:
                    print(f"⏰ Timeout pour le client {client_id}")
                    break
                except Exception as e:
                    print(f"❌ Erreur lors de la réception: {str(e)}")
                    break
                    
        except Exception as e:
            print(f"❌ Erreur générale client {client_id}: {str(e)}")
            self.logger.error(f"Erreur client {client_id}: {str(e)}")
            
        finally:
            try:
                client_socket.close()
                print(f"🔌 Connexion fermée avec {client_id}")
            except:
                pass
    
    def handle_message(self, message, client_address):
        """
        Traite un message HL7 reçu
        
        Args:
            message (str): Message HL7 à traiter
            client_address (tuple): Adresse du client
        
        Returns:
            str: Message ACK à renvoyer
        """
        try:
            # Parser le message basique (sans bibliothèque HL7)
            lines = message.replace('\r', '\n').split('\n')
            msh_line = None
            pid_line = None
            
            for line in lines:
                if line.startswith('MSH|'):
                    msh_line = line
                elif line.startswith('PID|'):
                    pid_line = line
            
            if not msh_line:
                return self.create_error_ack("Message HL7 invalide: pas de segment MSH")
            
            # Extraire les informations de base
            msh_parts = msh_line.split('|')
            message_type = msh_parts[8] if len(msh_parts) > 8 else "UNKNOWN"
            control_id = msh_parts[9] if len(msh_parts) > 9 else "1"
            
            print(f"📋 Type de message: {message_type}")
            print(f"🆔 ID de contrôle: {control_id}")
            
            # Extraire les informations patient si disponibles
            patient_data = {}
            if pid_line:
                patient_data = self.extract_patient_info_basic(pid_line)
                if patient_data.get('id'):
                    print(f"👤 Patient trouvé: {patient_data['id']} - {patient_data.get('name', 'N/A')}")
                    
                    # Sauvegarder le patient si repository disponible
                    if self.patient_repo and Patient:
                        try:
                            patient = Patient(
                                id=patient_data.get('id'),
                                first_name=patient_data.get('first_name'),
                                last_name=patient_data.get('last_name'),
                                birth_date=patient_data.get('birth_date'),
                                gender=patient_data.get('gender')
                            )
                            
                            self.patient_repo.create(patient)
                            print(f"💾 Patient {patient.id} enregistré en base")
                            
                        except Exception as e:
                            print(f"⚠️ Erreur sauvegarde patient: {str(e)}")
            
            # Sauvegarder le message si repository disponible
            if self.message_repo and Message:
                try:
                    msg_obj = Message(
                        message_type=message_type,
                        content=message,
                        source=f"{client_address[0]}:{client_address[1]}",
                        destination="HL7_SERVER",
                        patient_id=patient_data.get('id'),
                        status="PROCESSED"
                    )
                    
                    self.message_repo.save(msg_obj)
                    print(f"💾 Message sauvegardé avec ID: {msg_obj.id[:8]}")
                    
                except Exception as e:
                    print(f"⚠️ Erreur sauvegarde message: {str(e)}")
            
            # Créer et renvoyer un ACK de succès
            return self.create_success_ack(message_type, control_id)
            
        except Exception as e:
            error_msg = f"Erreur traitement message: {str(e)}"
            print(f"❌ {error_msg}")
            return self.create_error_ack(error_msg)
    
    def extract_patient_info_basic(self, pid_line):
        """
        Extrait les informations patient d'une ligne PID de manière basique
        
        Args:
            pid_line (str): Ligne PID du message HL7
        
        Returns:
            dict: Informations du patient
        """
        patient_info = {}
        
        try:
            parts = pid_line.split('|')
            
            # PID-3: ID patient
            if len(parts) > 3 and parts[3]:
                patient_info['id'] = parts[3].split('^')[0]
            
            # PID-5: Nom du patient (Nom^Prénom)
            if len(parts) > 5 and parts[5]:
                name_parts = parts[5].split('^')
                if len(name_parts) >= 1:
                    patient_info['last_name'] = name_parts[0]
                if len(name_parts) >= 2:
                    patient_info['first_name'] = name_parts[1]
                patient_info['name'] = f"{patient_info.get('last_name', '')} {patient_info.get('first_name', '')}".strip()
            
            # PID-7: Date de naissance
            if len(parts) > 7 and parts[7]:
                patient_info['birth_date'] = parts[7]
            
            # PID-8: Sexe
            if len(parts) > 8 and parts[8]:
                patient_info['gender'] = parts[8]
            
        except Exception as e:
            print(f"⚠️ Erreur extraction infos patient: {str(e)}")
        
        return patient_info
    
    def create_success_ack(self, message_type, control_id):
        """
        Crée un ACK de succès
        
        Args:
            message_type (str): Type du message original
            control_id (str): ID de contrôle du message original
        
        Returns:
            str: Message ACK
        """
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        ack = f"""MSH|^~\\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|{current_time}||ACK^{message_type}|{control_id}|P|2.5\rMSA|AA|{control_id}|Message traité avec succès\r"""
        
        return ack
    
    def create_error_ack(self, error_message):
        """
        Crée un ACK d'erreur
        
        Args:
            error_message (str): Description de l'erreur
        
        Returns:
            str: Message ACK négatif
        """
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        # Limiter la longueur du message d'erreur
        if len(error_message) > 100:
            error_message = error_message[:97] + "..."
        
        ack = f"""MSH|^~\\&|HL7_SERVER|HOSPITAL|HL7_CLIENT|HOSPITAL|{current_time}||ACK|1|P|2.5\rMSA|AE|1|{error_message}\r"""
        
        return ack
    
    def stop(self):
        """Arrête le serveur proprement"""
        print("\n🛑 Arrêt du serveur en cours...")
        self.running = False
        if self.server:
            self.server.close()


def main():
    """Point d'entrée principal du serveur"""
    print("🏥 Serveur HL7 MLLP - Version Corrigée")
    print("=" * 50)
    
    # Configuration par défaut
    host = "0.0.0.0"
    port = 2575
    
    # Vérifier les arguments de ligne de commande
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            print(f"🔧 Port personnalisé: {port}")
        except ValueError:
            print(f"⚠️ Port invalide '{sys.argv[1]}', utilisation du port par défaut {port}")
    
    # Créer et démarrer le serveur
    server = MLLPServer(host, port)
    
    try:
        success = server.start()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("👋 Au revoir!")


if __name__ == "__main__":
    main()