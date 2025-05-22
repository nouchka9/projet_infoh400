# -*- coding: utf-8 -*-
"""
Tests unitaires pour le moteur HL7 (builder, parser, etc.)
"""
import unittest
import os
import sys

# Ajouter le répertoire parent au path pour importer les modules de l'application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.hl7_engine.builder import HL7MessageBuilder

class TestHL7Builder(unittest.TestCase):
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.builder = HL7MessageBuilder()
        
        # Données de test patient
        self.patient_data = {
            "id": "P12345",
            "last_name": "DOE",
            "first_name": "JOHN",
            "birth_date": "19800101",
            "gender": "M",
            "ward": "CARDIO",
            "room": "102"
        }
        
        # Données de test résultats
        self.results_data = [{
            "order_id": "O98765",
            "filler_id": "LAB123",
            "test_code": "CBC",
            "test_name": "Hémogramme complet",
            "results": [
                {
                    "code": "HGB",
                    "name": "Hémoglobine",
                    "value": "14.2",
                    "unit": "g/dL",
                    "type": "NM"
                }
            ]
        }]
        
        # Données de test demande
        self.order_data = {
            "order_id": "ORD87654",
            "test_code": "XR",
            "test_name": "Radiographie Thorax",
            "scheduled_date": "20250518",
            "priority": "Normal",
            "comments": "Suspicion pneumonie"
        }
    
    def test_create_adt_a01(self):
        """Test la création d'un message ADT^A01"""
        message, control_id = self.builder.create_adt_a01(self.patient_data)
        
        # Vérifier le type et le format
        self.assertIsInstance(message, str)
        self.assertIsInstance(control_id, str)
        
        # Vérifier les éléments du message
        self.assertIn("MSH|", message)
        self.assertIn("PID|", message)
        self.assertIn("PV1|", message)
        self.assertIn("ADT^A01", message)
        
        # Vérifier les données patient
        self.assertIn("DOE^JOHN", message)
        self.assertIn("P12345", message)
        self.assertIn("19800101", message)
        self.assertIn("CARDIO^102", message)
    
    def test_create_oru_r01(self):
        """Test la création d'un message ORU^R01"""
        message, control_id = self.builder.create_oru_r01("P12345", self.results_data)
        
        # Vérifier le type et le format
        self.assertIsInstance(message, str)
        self.assertIsInstance(control_id, str)
        
        # Vérifier les éléments du message
        self.assertIn("MSH|", message)
        self.assertIn("PID|", message)
        self.assertIn("OBR|", message)
        self.assertIn("OBX|", message)
        self.assertIn("ORU^R01", message)
        
        # Vérifier les données du message
        self.assertIn("O98765", message)  # ID de commande
        self.assertIn("LAB123", message)  # ID exécutant
        self.assertIn("CBC^Hémogramme complet", message)  # Code et nom du test
        self.assertIn("HGB^Hémoglobine", message)  # Code et nom du résultat
        self.assertIn("14.2", message)  # Valeur
        self.assertIn("g/dL", message)  # Unité
    
    def test_create_orm_o01(self):
        """Test la création d'un message ORM^O01"""
        message, control_id = self.builder.create_orm_o01("P12345", self.order_data)
        
        # Vérifier le type et le format
        self.assertIsInstance(message, str)
        self.assertIsInstance(control_id, str)
        
        # Vérifier les éléments du message
        self.assertIn("MSH|", message)
        self.assertIn("PID|", message)
        self.assertIn("ORC|", message)
        self.assertIn("OBR|", message)
        self.assertIn("ORM^O01", message)
        
        # Vérifier les données du message
        self.assertIn("P12345", message)  # ID patient
        self.assertIn("ORD87654", message)  # ID commande
        self.assertIn("XR^Radiographie Thorax", message)  # Code et nom de l'examen
        self.assertIn("Suspicion pneumonie", message)  # Commentaires
    
    def test_control_id_uniqueness(self):
        """Test l'unicité des ID de contrôle"""
        message1, control_id1 = self.builder.create_adt_a01(self.patient_data)
        message2, control_id2 = self.builder.create_adt_a01(self.patient_data)
        
        # Vérifier que les ID de contrôle sont différents
        self.assertNotEqual(control_id1, control_id2)
    
    def test_timestamp_format(self):
        """Test le format du timestamp"""
        timestamp = self.builder._get_timestamp()
        
        # Vérifier la longueur (format YYYYMMDDHHMMSS)
        self.assertEqual(len(timestamp), 14)
        
        # Vérifier que c'est un nombre
        self.assertTrue(timestamp.isdigit())


if __name__ == '__main__':
    unittest.main()