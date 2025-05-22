"""
Interface pour le département de laboratoire.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import threading

class LaboratoryFrame(ttk.Frame):
    """Interface pour le département de laboratoire"""
    
    def __init__(self, parent, mllp_client, message_builder, on_message_callback, config=None):
        super().__init__(parent)
        self.logger = logging.getLogger("HL7Messenger.LaboratoryUI")
        self.mllp_client = mllp_client
        self.message_builder = message_builder
        self.on_message_callback = on_message_callback
        self.config = config
        self.processing = False
        self._create_widgets()

    def _create_widgets(self):
        """Crée les widgets de l'interface"""
        title_label = ttk.Label(self, text="Résultats de Laboratoire", style="Title.TLabel")
        title_label.pack(pady=(10, 5))

        form = ttk.LabelFrame(self, text="Informations Résultats", padding=10)
        form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Patient & Demande
        self.patient_id_var = tk.StringVar()
        self.order_id_var = tk.StringVar()
        self.filler_id_var = tk.StringVar()
        self.test_code_var = tk.StringVar()
        self.test_name_var = tk.StringVar()

        self._add_entry(form, "ID Patient:", self.patient_id_var, row=0, col=0)
        self._add_entry(form, "ID Demande:", self.order_id_var, row=1, col=0)
        self._add_entry(form, "ID Exécutant:", self.filler_id_var, row=1, col=2)
        self._add_entry(form, "Code Examen:", self.test_code_var, row=2, col=0)
        self._add_entry(form, "Nom Examen:", self.test_name_var, row=2, col=2)

        # Résultats
        ttk.Separator(form).grid(row=3, column=0, columnspan=4, sticky="ew", pady=10)
        ttk.Label(form, text="Résultats", style="Subtitle.TLabel").grid(row=4, column=0, columnspan=4, sticky="w")

        self.results = []
        for i in range(2):
            result = {}
            frame = ttk.LabelFrame(form, text=f"Résultat {i+1}")
            frame.grid(row=5+i, column=0, columnspan=4, sticky="ew", pady=5)

            result["code"] = tk.StringVar()
            result["name"] = tk.StringVar()
            result["value"] = tk.StringVar()
            result["unit"] = tk.StringVar()

            self._add_entry(frame, "Code:", result["code"], row=0, col=0)
            self._add_entry(frame, "Nom:", result["name"], row=0, col=2)
            self._add_entry(frame, "Valeur:", result["value"], row=1, col=0)
            self._add_entry(frame, "Unité:", result["unit"], row=1, col=2)

            self.results.append(result)

        # Boutons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.send_btn = ttk.Button(btn_frame, text="Envoyer", command=self._send_message, width=15)
        self.send_btn.pack(side=tk.RIGHT, padx=5)
        
        self.reset_btn = ttk.Button(btn_frame, text="Réinitialiser", command=self._reset_form, width=15)
        self.reset_btn.pack(side=tk.RIGHT, padx=5)

        self._set_default_values()

    def _add_entry(self, parent, label, var, row, col):
        """Ajoute un champ label + entry dans un frame"""
        ttk.Label(parent, text=label).grid(row=row, column=col, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=col+1, sticky="ew", padx=5, pady=5)
        return entry

    def _set_default_values(self):
        self.patient_id_var.set("P12345")
        self.order_id_var.set("O98765")
        self.filler_id_var.set("LAB123")
        self.test_code_var.set("CBC")
        self.test_name_var.set("Hémogramme complet")

        self.results[0]["code"].set("HGB")
        self.results[0]["name"].set("Hémoglobine")
        self.results[0]["value"].set("14.2")
        self.results[0]["unit"].set("g/dL")

        self.results[1]["code"].set("WBC")
        self.results[1]["name"].set("Leucocytes")
        self.results[1]["value"].set("6.8")
        self.results[1]["unit"].set("10^9/L")

    def _reset_form(self):
        """Réinitialise les champs du formulaire"""
        self.patient_id_var.set("")
        self.order_id_var.set("")
        self.filler_id_var.set("")
        self.test_code_var.set("")
        self.test_name_var.set("")
        
        for r in self.results:
            for var in r.values():
                var.set("")

    def _send_message(self):
        """Envoie le message HL7 avec les résultats"""
        # Éviter les envois multiples
        if self.processing:
            return
            
        pid = self.patient_id_var.get().strip()
        if not pid:
            messagebox.showwarning("Validation", "L'ID patient est obligatoire")
            return

        # Indiquer le traitement en cours
        self.processing = True
        self.send_btn.configure(state="disabled")

        results_data = [{
            "order_id": self.order_id_var.get().strip(),
            "filler_id": self.filler_id_var.get().strip(),
            "test_code": self.test_code_var.get().strip(),
            "test_name": self.test_name_var.get().strip(),
            "results": []
        }]

        for r in self.results:
            if r["code"].get() and r["value"].get():
                results_data[0]["results"].append({
                    "code": r["code"].get().strip(),
                    "name": r["name"].get().strip(),
                    "value": r["value"].get().strip(),
                    "unit": r["unit"].get().strip(),
                    "type": "NM"  # Type numérique par défaut
                })

        if not results_data[0]["results"]:
            messagebox.showwarning("Validation", "Au moins un résultat est requis")
            self._end_processing()
            return

        # Utiliser un thread pour ne pas bloquer l'interface
        threading.Thread(target=self._send_thread, args=(pid, results_data), daemon=True).start()

    def _send_thread(self, pid, results_data):
        """Fonction exécutée dans un thread pour envoyer le message"""
        try:
            message, control_id = self.message_builder.create_oru_r01(pid, results_data)
            destination = "LAB_SYSTEM"
            
            # Tentative d'envoi avec 3 essais en cas d'échec
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                self.logger.info(f"Tentative d'envoi #{attempt}")
                
                success, response = self.mllp_client.send_message(message, destination)
                
                if success:
                    self.logger.info(f"Message ORU^R01 envoyé avec succès (ID: {control_id})")
                    self.after(0, lambda: self._show_success(f"Message ORU^R01 envoyé avec succès"))
                    break
                else:
                    self.logger.warning(f"Échec de l'envoi (tentative {attempt}/{max_attempts}): {response}")
                    if attempt == max_attempts:
                        self.after(0, lambda: self._show_error(f"Erreur: {response}"))

        except Exception as e:
            self.logger.error(f"Erreur: {str(e)}")
            self.after(0, lambda: self._show_error(f"Erreur: {str(e)}"))
        
        finally:
            # Réactiver l'interface
            self.after(0, self._end_processing)

    def _end_processing(self):
        """Termine le traitement et réactive l'interface"""
        self.processing = False
        self.send_btn.configure(state="normal")

    def _show_success(self, message):
        """Affiche un message de succès"""
        self.on_message_callback(True, message)

    def _show_error(self, message):
        """Affiche un message d'erreur"""
        self.on_message_callback(False, message)
