"""
Interface pour visualiser l'historique des messages HL7.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from app.db.repositories.message_repository import MessageRepository

class HistoryViewer(tk.Toplevel):
    """Fenêtre pour afficher l'historique des messages HL7"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historique des messages")
        self.geometry("900x500")
        self.configure(bg="white")

        self.repo = MessageRepository()

        self._create_widgets()
        self._load_messages()

    def _create_widgets(self):
        """Crée les widgets de l'interface"""
        self.tree = ttk.Treeview(self, columns=("id", "type", "patient", "source", "dest", "statut", "date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        refresh_btn = ttk.Button(self, text="🔄 Rafraîchir", command=self._load_messages)
        refresh_btn.pack(pady=5)

    def _load_messages(self):
        """Charge les messages récents"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            messages = self.repo.get_recent()
            for msg in messages:
                self.tree.insert("", "end", values=(
                    msg.id,
                    msg.message_type,
                    msg.patient_id,
                    msg.source,
                    msg.destination,
                    msg.status,
                    msg.created_at[:19]  # YYYY-MM-DD HH:MM:SS
                ))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les messages : {e}")

def show_history_popup(parent):
    """Fonction utilitaire pour lancer la fenêtre d'historique depuis le dashboard"""
    viewer = HistoryViewer(parent)
    viewer.grab_set()  # Pour rendre la fenêtre modale