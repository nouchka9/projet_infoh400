# -*- coding: utf-8 -*-
"""
Tests unitaires pour l'interface utilisateur.
Ces tests vérifient que les formulaires capturent correctement les données
et que l'interface interagit correctement avec le client HL7.
"""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH pour pouvoir importer les modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import des modules à tester
from app.ui.login_screen import LoginScreen
from app.ui.dashboard import Dashboard
from app.ui.departments.admission import AdmissionFrame
from app.ui.departments.laboratory import LaboratoryFrame
from app.ui.departments.radiology import RadiologyFrame
from app.ui.departments.pharmacy import PharmacyFrame


class TestLoginScreen(unittest.TestCase):
    """Tests pour l'écran de connexion"""
    
    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.root = tk.Tk()
        self.login_callback = MagicMock()
        self.login_screen = LoginScreen(self.root, self.login_callback)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.root.destroy()
    
    def test_login_validation_empty_fields(self):
        """Test de validation avec champs vides"""
        # Simuler des champs vides
        self.login_screen.username_var.set("")
        self.login_screen.password_var.set("")
        
        # Tenter de se connecter
        self.login_screen._on_login()
        
        # Vérifier que le callback n'a pas été appelé
        self.login_callback.assert_not_called()
        
        # Vérifier que le message d'erreur est affiché
        self.assertNotEqual(self.login_screen.error_var.get(), "")
    
    def test_login_success(self):
        """Test d'une connexion réussie"""
        # Simuler des champs remplis
        self.login_screen.username_var.set("testuser")
        self.login_screen.password_var.set("password123")
        self.login_screen.department_var.set("ADMISSION")
        
        # Tenter de se connecter
        self.login_screen._on_login()
        
        # Vérifier que le callback a été appelé avec les bons paramètres
        self.login_callback.assert_called_once_with("testuser", "ADMISSION")


class TestAdmissionForm(unittest.TestCase):
    """Tests pour le formulaire d'admission"""
    
    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.root = tk.Tk()
        self.mllp_client = MagicMock()
        self.message_builder = MagicMock()
        self.message_callback = MagicMock()
        
        # Créer une instance du formulaire d'admission
        self.admission_form = AdmissionFrame(
            self.root,
            self.mllp_client,
            self.message_builder,
            self.message_callback
        )
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.root.destroy()
    
    def test_form_default_values(self):
        """Test des valeurs par défaut du formulaire"""
        # Vérifier les valeurs par défaut
        self.assertEqual(self.admission_form.patient_id_var.get(), "P12345")
        self.assertEqual(self.admission_form.last_name_var.get(), "DOE")
        self.assertEqual(self.admission_form.first_name_var.get(), "JOHN")
    
    def test_form_reset(self):
        """Test de la réinitialisation du formulaire"""
        # Réinitialiser le formulaire
        self.admission_form._reset_form()
        
        # Vérifier que les champs sont vides
        self.assertEqual(self.admission_form.patient_id_var.get(), "")
        self.assertEqual(self.admission_form.last_name_var.get(), "")
        self.assertEqual(self.admission_form.first_name_var.get(), "")
    
    @patch('tkinter.messagebox.showwarning')
    def test_validation_empty_fields(self, mock_showwarning):
        """Test de validation avec champs vides"""
        # Réinitialiser le formulaire
        self.admission_form._reset_form()
        
        # Tenter d'envoyer le message
        self.admission_form._send_message()
        
        # Vérifier qu'un avertissement est affiché
        mock_showwarning.assert_called_once()
        
        # Vérifier que le client MLLP n'est pas appelé
        self.mllp_client.send_message.assert_not_called()
    
    def test_send_message_success(self):
        """Test d'envoi de message réussi"""
        # Configuration des mocks
        self.message_builder.create_adt_a01.return_value = ("MSG|TEST", "12345")
        self.mllp_client.send_message.return_value = (True, "OK")
        
        # Envoyer le message
        self.admission_form._send_message()
        
        # Vérifier que le message builder a été appelé avec les bonnes données
        self.message_builder.create_adt_a01.assert_called_once()
        
        # Vérifier que le client MLLP a été appelé
        self.mllp_client.send_message.assert_called_once()
        
        # Vérifier que le callback a été appelé avec succès
        self.message_callback.assert_called_once_with(True, "Message ADT^A01 envoyé avec succès")
    
    def test_send_message_failure(self):
        """Test d'envoi de message échoué"""
        # Configuration des mocks
        self.message_builder.create_adt_a01.return_value = ("MSG|TEST", "12345")
        self.mllp_client.send_message.return_value = (False, "Erreur de connexion")
        
        # Envoyer le message
        self.admission_form._send_message()
        
        # Vérifier que le message builder a été appelé
        self.message_builder.create_adt_a01.assert_called_once()
        
        # Vérifier que le client MLLP a été appelé
        self.mllp_client.send_message.assert_called_once()
        
        # Vérifier que le callback a été appelé avec échec
        self.message_callback.assert_called_once_with(False, "Erreur d'envoi: Erreur de connexion")


class TestOtherDepartments(unittest.TestCase):
    """Tests basiques pour les autres départements"""
    
    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.root = tk.Tk()
        self.mllp_client = MagicMock()
        self.message_builder = MagicMock()
        self.message_callback = MagicMock()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.root.destroy()
    
    def test_laboratory_initialization(self):
        """Test d'initialisation du département de laboratoire"""
        lab_frame = LaboratoryFrame(
            self.root,
            self.mllp_client,
            self.message_builder,
            self.message_callback
        )
        # Vérifier que le frame est correctement initialisé
        self.assertIsInstance(lab_frame, LaboratoryFrame)
    
    def test_radiology_initialization(self):
        """Test d'initialisation du département de radiologie"""
        radio_frame = RadiologyFrame(
            self.root,
            self.mllp_client,
            self.message_builder,
            self.message_callback
        )
        # Vérifier que le frame est correctement initialisé
        self.assertIsInstance(radio_frame, RadiologyFrame)
    
    def test_pharmacy_initialization(self):
        """Test d'initialisation du département de pharmacie"""
        pharm_frame = PharmacyFrame(
            self.root,
            self.mllp_client,
            self.message_builder,
            self.message_callback
        )
        # Vérifier que le frame est correctement initialisé
        self.assertIsInstance(pharm_frame, PharmacyFrame)


if __name__ == '__main__':
    unittest.main()