"""
Interface pour visualiser l'historique des messages HL7 - VERSION CORRIGÉE
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging

class HistoryViewer(tk.Toplevel):
    """Fenêtre pour afficher l'historique des messages HL7"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("📊 Historique des messages HL7")
        self.geometry("900x600")
        self.configure(bg="white")
        
        # Centrer la fenêtre
        self.transient(parent)
        self.grab_set()
        
        try:
            from app.db.repositories.message_repository import MessageRepository
            self.repo = MessageRepository()
        except ImportError:
            self.repo = None
            print("⚠️ MessageRepository non disponible")

        self._create_widgets()
        self._load_messages()
        
        # Focus sur la fenêtre
        self.focus_set()

    def _create_widgets(self):
        """Crée les widgets de l'interface"""
        # En-tête
        header_frame = ttk.Frame(self, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="📊 Historique des Messages HL7",
            font=("Helvetica", 14, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Bouton refresh
        refresh_btn = ttk.Button(
            header_frame, 
            text="🔄 Rafraîchir", 
            command=self._load_messages,
            width=12
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Frame principal pour le tableau
        main_frame = ttk.Frame(self, padding="10 0 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tableau avec scrollbars
        self.tree = ttk.Treeview(
            main_frame, 
            columns=("id", "type", "patient", "source", "dest", "statut", "date"), 
            show="headings",
            height=15
        )
        
        # Configuration des colonnes
        columns_config = {
            "id": ("ID", 80),
            "type": ("Type", 100),
            "patient": ("Patient", 100),
            "source": ("Source", 120),
            "dest": ("Destination", 120),
            "statut": ("Statut", 80),
            "date": ("Date/Heure", 150)
        }
        
        for col_id, (heading, width) in columns_config.items():
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack du tableau et scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configuration de la grille
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Barre de statut
        status_frame = ttk.Frame(self, padding="10 5")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Prêt")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        # Bouton fermer
        close_btn = ttk.Button(
            status_frame,
            text="❌ Fermer",
            command=self.destroy,
            width=10
        )
        close_btn.pack(side=tk.RIGHT)

    def _load_messages(self):
        """Charge les messages récents"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.status_var.set("🔄 Chargement...")
        self.update()
        
        try:
            if self.repo:
                messages = self.repo.get_recent(50)  # Derniers 50 messages
                
                for msg in messages:
                    # Formater la date
                    date_str = msg.created_at[:19] if hasattr(msg, 'created_at') else "N/A"
                    
                    self.tree.insert("", "end", values=(
                        getattr(msg, 'id', 'N/A')[:8],  # ID tronqué
                        getattr(msg, 'message_type', 'N/A'),
                        getattr(msg, 'patient_id', 'N/A'),
                        getattr(msg, 'source', 'N/A'),
                        getattr(msg, 'destination', 'N/A'),
                        getattr(msg, 'status', 'N/A'),
                        date_str
                    ))
                
                count = len(messages)
                self.status_var.set(f"✅ {count} message(s) chargé(s)")
                
            else:
                # Données de démonstration si pas de repository
                demo_data = [
                    ("MSG001", "ADT^A01", "P12345", "ADMISSION", "HIS", "SUCCESS", "2025-05-22 10:30:15"),
                    ("MSG002", "ORU^R01", "P12346", "LAB", "HIS", "SUCCESS", "2025-05-22 11:45:22"),
                    ("MSG003", "ORM^O01", "P12347", "RADIOLOGY", "PACS", "PENDING", "2025-05-22 14:20:08"),
                ]
                
                for data in demo_data:
                    self.tree.insert("", "end", values=data)
                
                self.status_var.set("📋 Données de démonstration")
                
        except Exception as e:
            self.status_var.set(f"❌ Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de charger les messages : {e}")

def show_history_popup(parent):
    """Fonction utilitaire pour lancer la fenêtre d'historique"""
    viewer = HistoryViewer(parent)
    return viewer
