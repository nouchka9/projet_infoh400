#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Corrige le problème du département Laboratoire
"""
import os

def fix_laboratory_frame():
    """Corrige le fichier laboratory.py"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "departments", "laboratory.py")
    
    # Si le fichier existe
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Remplacer la définition de la classe LaboratoryFrame
        if "def __init__(self, parent, mllp_client, message_builder, on_message_callback):" in content:
            print("Le fichier laboratory.py est déjà correct.")
        else:
            # Nouveau contenu du fichier
            new_content = """\"\"\"
Interface pour le département de laboratoire.
\"\"\"
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import threading

class LaboratoryFrame(ttk.Frame):
    \"\"\"Interface pour le département de laboratoire\"\"\"
    
    def __init__(self, parent, mllp_client, message_builder, on_message_callback, config=None):
        super().__init__(parent)
        self.logger = logging.getLogger("HL7Messenger.LaboratoryUI")
        self.mllp_client = mllp_client
        self.message_builder = message_builder
        self.on_message_callback = on_message_callback
        self.config = config
        self.processing = False
        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        \"\"\"Crée les widgets de l'interface\"\"\"
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

        # Barre de statut
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Prêt")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=10)
        
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate", length=150)
        self.progress.pack(side=tk.RIGHT, padx=10)
        self.progress.pack_forget()  # Masquer jusqu'à utilisation

        # Boutons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.send_btn = ttk.Button(btn_frame, text="Envoyer", command=self._send_message, width=15)
        self.send_btn.pack(side=tk.RIGHT, padx=5)
        
        self.reset_btn = ttk.Button(btn_frame, text="Réinitialiser", command=self._reset_form, width=15)
        self.reset_btn.pack(side=tk.RIGHT, padx=5)

        self._set_default_values()

    def _add_entry(self, parent, label, var, row, col):
        \"\"\"Ajoute un champ label + entry dans un frame\"\"\"
        ttk.Label(parent, text=label).grid(row=row, column=col, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=col+1, sticky="ew", padx=5, pady=5)
        return entry

    def _bind_events(self):
        \"\"\"Attache les gestionnaires d'événements\"\"\"
        # Entrée pour naviguer entre les champs
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame) or isinstance(child, ttk.LabelFrame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Entry):
                        subchild.bind("<Return>", self._on_entry_return)
                        subchild.bind("<FocusIn>", self._on_entry_focus)
        
        # Bouton Envoyer activable avec Entrée quand il a le focus
        self.send_btn.bind("<Return>", lambda e: self._send_message())
        self.reset_btn.bind("<Return>", lambda e: self._reset_form())

    def _on_entry_return(self, event):
        \"\"\"Gère la touche Entrée dans un champ\"\"\"
        # Passer au champ suivant
        event.widget.tk_focusNext().focus()
        return "break"  # Empêcher la propagation

    def _on_entry_focus(self, event):
        \"\"\"Gère le focus sur un champ\"\"\"
        event.widget.select_range(0, tk.END)

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
        \"\"\"Réinitialise les champs du formulaire\"\"\"
        self.patient_id_var.set("")
        self.order_id_var.set("")
        self.filler_id_var.set("")
        self.test_code_var.set("")
        self.test_name_var.set("")
        
        for r in self.results:
            for var in r.values():
                var.set("")
                
        # Réinitialiser le statut
        self.status_var.set("Formulaire réinitialisé")
        self.after(3000, lambda: self.status_var.set("Prêt"))

    def _send_message(self):
        \"\"\"Envoie le message HL7 avec les résultats\"\"\"
        # Éviter les envois multiples
        if self.processing:
            return
            
        pid = self.patient_id_var.get().strip()
        if not pid:
            messagebox.showwarning("Validation", "L'ID patient est obligatoire")
            return

        # Indiquer le traitement en cours
        self.processing = True
        self.status_var.set("Envoi en cours...")
        self.send_btn.configure(state="disabled")
        self.progress.pack(side=tk.RIGHT, padx=10)
        self.progress.start(10)

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
        \"\"\"Fonction exécutée dans un thread pour envoyer le message\"\"\"
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
        \"\"\"Termine le traitement et réactive l'interface\"\"\"
        self.processing = False
        self.progress.stop()
        self.progress.pack_forget()
        self.send_btn.configure(state="normal")

    def _show_success(self, message):
        \"\"\"Affiche un message de succès\"\"\"
        self.status_var.set("✅ " + message)
        self.on_message_callback(True, message)

    def _show_error(self, message):
        \"\"\"Affiche un message d'erreur\"\"\"
        self.status_var.set("❌ " + message)
        self.on_message_callback(False, message)
"""
            
            # Enregistrer le nouveau contenu
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Le fichier laboratory.py a été mis à jour.")

def fix_admission_frame():
    """Corrige le fichier admission.py pour gérer correctement les événements"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "departments", "admission.py")
    
    # Si le fichier existe, nous allons modifier la fonction _on_login
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Rechercher la fonction _create_widgets
        if "_bind_all(\"<Return>\"" in content:
            # Remplacer la ligne problématique
            content = content.replace(
                "self.bind_all(\"<Return>\", lambda event: self._on_login())",
                "# Ne pas intercepter la touche Return globalement ici"
            )
            
            # Ajouter la gestion des événements clavier au début
            if "_bind_events" not in content:
                pos = content.find("self._create_widgets()")
                if pos > 0:
                    content = content[:pos+20] + "\n        self._bind_events()" + content[pos+20:]
                    
                # Ajouter la fonction _bind_events
                add_bind_events = """
    def _bind_events(self):
        \"\"\"Attache les gestionnaires d'événements\"\"\"
        # Pour les entrées (Entry)
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame) or isinstance(child, ttk.LabelFrame):
                self._bind_entries_in_frame(child)
        
        # Pour les boutons
        self.send_button.bind("<Return>", lambda e: self._send_message())
        self.reset_button.bind("<Return>", lambda e: self._reset_form())
    
    def _bind_entries_in_frame(self, parent):
        \"\"\"Attache les événements aux champs d'un frame\"\"\"
        for child in parent.winfo_children():
            if isinstance(child, ttk.Frame) or isinstance(child, ttk.LabelFrame):
                self._bind_entries_in_frame(child)
            elif isinstance(child, ttk.Entry):
                child.bind("<Return>", self._on_entry_return)
                child.bind("<FocusIn>", self._on_entry_focus)
                
    def _on_entry_return(self, event):
        \"\"\"Gère la touche Entrée dans un champ\"\"\"
        # Passage au widget suivant
        event.widget.tk_focusNext().focus()
        return "break"  # Empêcher la propagation
        
    def _on_entry_focus(self, event):
        \"\"\"Gère le focus sur un champ\"\"\"
        event.widget.select_range(0, tk.END)
"""
                
                # Ajouter à la fin de la classe
                content += add_bind_events
            
            # Enregistrer les modifications
            with open(file_path, 'w') as f:
                f.write(content)
                
            print(f"✅ Le fichier admission.py a été mis à jour.")
        else:
            print("Le fichier admission.py n'a pas besoin d'être mis à jour.")

def fix_dashboard():
    """Corrige le fichier dashboard.py pour la navigation clavier"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "dashboard.py")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Corriger la gestion des événements clavier
        if "_bind_keyboard_events" not in content:
            # Ajouter la méthode après l'initialisation
            pos = content.find("self._create_widgets()")
            if pos > 0:
                content = content[:pos+20] + "\n        self._bind_keyboard_events()" + content[pos+20:]
                
                # Ajouter la fonction de gestion des événements
                add_keyboard_events = """
    def _bind_keyboard_events(self):
        \"\"\"Configure les raccourcis clavier\"\"\"
        # Ne pas intercepter la touche Return globalement
        # pour éviter les conflits avec les formulaires
        for binding in self.bind_all():
            if binding == "<Return>":
                self.unbind_all("<Return>")
                
        # Raccourcis spécifiques
        self.bind("<F5>", lambda e: self._refresh_view())
        self.bind("<Escape>", lambda e: self._handle_escape())
        
    def _refresh_view(self, event=None):
        \"\"\"Rafraîchit la vue actuelle\"\"\"
        if hasattr(self.dept_frame, 'refresh'):
            self.dept_frame.refresh()
            
    def _handle_escape(self, event=None):
        \"\"\"Gère la touche échap\"\"\"
        # Fermer les fenêtres popup si elles existent
        for widget in self.winfo_toplevel().winfo_children():
            if widget.winfo_class() == 'Toplevel':
                widget.destroy()
                return "break"
"""
                
                # Ajouter à la fin de la classe
                content += add_keyboard_events
                
            # Enregistrer les modifications
            with open(file_path, 'w') as f:
                f.write(content)
                
            print(f"✅ Le fichier dashboard.py a été mis à jour.")
        else:
            print("Le fichier dashboard.py n'a pas besoin d'être mis à jour.")

def fix_combobox_behavior():
    """Améliore le comportement des combobox"""
    # Cette fonction va créer un fichier d'utilitaires pour rendre les combobox plus agréables à utiliser
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "common", "widgets.py")
    
    # Créer le dossier commun s'il n'existe pas
    common_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "common")
    if not os.path.exists(common_dir):
        os.makedirs(common_dir)
        
    # Créer le fichier __init__.py s'il n'existe pas
    init_path = os.path.join(common_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("# Package pour les composants communs d'interface utilisateur")
    
    # Créer le fichier widgets.py
    widget_content = """# -*- coding: utf-8 -*-
\"\"\"
Widgets améliorés pour l'interface utilisateur
\"\"\"
import tkinter as tk
from tkinter import ttk

class ImprovedCombobox(ttk.Combobox):
    \"\"\"
    Version améliorée de ttk.Combobox avec une meilleure gestion des événements
    \"\"\"
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configurer les événements
        self.bind("<<ComboboxSelected>>", self._on_selected)
        self.bind("<Return>", self._on_return)
        self.bind("<Tab>", self._on_tab)
        self.bind("<FocusOut>", self._on_focus_out)
        
    def _on_selected(self, event=None):
        \"\"\"Quand une option est sélectionnée\"\"\"
        # Défocaliser le combobox après sélection pour une meilleure expérience
        self.selection_clear()
        self.icursor(0)  # Positionner le curseur au début
        
        # Passer au champ suivant
        self.after(100, lambda: self.tk_focusNext().focus())
        
    def _on_return(self, event=None):
        \"\"\"Quand on appuie sur Entrée\"\"\"
        # Si le menu déroulant est ouvert, valider la sélection
        if self.winfo_ismapped():
            self.selection_clear()
            self.icursor(0)
        
        # Passer au champ suivant
        self.after(100, lambda: self.tk_focusNext().focus())
        return "break"  # Empêcher la propagation
        
    def _on_tab(self, event=None):
        \"\"\"Quand on appuie sur Tab\"\"\"
        # Si le menu déroulant est ouvert, le fermer
        if self.winfo_ismapped():
            self.selection_clear()
            self.icursor(0)
            
        # Laisser la tabulation se propager normalement
        
    def _on_focus_out(self, event=None):
        \"\"\"Quand le focus sort du widget\"\"\"
        # Réinitialiser l'état
        self.selection_clear()
        self.icursor(0)
        
# Fonction pour remplacer tous les combobox d'un frame par la version améliorée
def upgrade_comboboxes(parent):
    \"\"\"
    Remplace tous les combobox d'un parent par la version améliorée
    
    Args:
        parent: Widget parent contenant des combobox à améliorer
    \"\"\"
    # Pour les combobox directs
    for child in parent.winfo_children():
        if isinstance(child, ttk.Combobox):
            # Récupérer les propriétés
            properties = {
                "textvariable": child.cget("textvariable"),
                "values": child["values"],
                "state": child.cget("state"),
                "width": child.cget("width"),
                "font": child.cget("font"),
                "justify": child.cget("justify")
            }
            
            # Créer un nouveau combobox amélioré
            info = child.grid_info() if child.winfo_manager() == 'grid' else child.pack_info()
            
            # Détruire l'ancien
            child.destroy()
            
            # Créer le nouveau
            new_combo = ImprovedCombobox(parent, **properties)
            
            # Replacer au même endroit
            if child.winfo_manager() == 'grid':
                new_combo.grid(**info)
            else:
                new_combo.pack(**info)
                
        # Récursion pour les enfants
        elif hasattr(child, 'winfo_children'):
            upgrade_comboboxes(child)
"""
    
    # Enregistrer le fichier
    with open(file_path, 'w') as f:
        f.write(widget_content)
        
    print(f"✅ Le fichier widgets.py a été créé.")
    
    # Maintenant, modifier app.py pour utiliser ces widgets améliorés
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "app.py")
    
    if os.path.exists(app_path):
        with open(app_path, 'r') as f:
            content = f.read()
            
        # Ajouter l'import
        import_line = "from app.ui.common.widgets import upgrade_comboboxes"
        if import_line not in content:
            # Chercher le dernier import
            pos = content.rfind("import")
            if pos > 0:
                line_end = content.find("\n", pos)
                if line_end > 0:
                    content = content[:line_end+1] + "\n" + import_line + content[line_end+1:]
            
            # Améliorer les combobox après l'affichage des écrans
            if "show_login_screen" in content:
                # Ajouter après show_login_screen
                content = content.replace(
                    "self.current_screen.pack(fill=tk.BOTH, expand=True)",
                    "self.current_screen.pack(fill=tk.BOTH, expand=True)\n        upgrade_comboboxes(self.current_screen)"
                )
                
            if "show_dashboard" in content:
                # Ajouter après show_dashboard
                content = content.replace(
                    "self.current_screen.pack(fill=tk.BOTH, expand=True)",
                    "self.current_screen.pack(fill=tk.BOTH, expand=True)\n        upgrade_comboboxes(self.current_screen)"
                )
                
            # Enregistrer les modifications
            with open(app_path, 'w') as f:
                f.write(content)
                
            print(f"✅ Le fichier app.py a été mis à jour pour utiliser les combobox améliorés.")
        else:
            print("Le fichier app.py utilise déjà les combobox améliorés.")

def main():
    print("====================================================")
    print("  Amélioration de l'interface HL7 Messenger")
    print("====================================================")
    
    # 1. Correction du département de laboratoire
    print("1. Correction du département Laboratoire...")
    fix_laboratory_frame()
    
    # 2. Amélioration de la navigation clavier dans le formulaire admission
    print("2. Amélioration de la navigation clavier dans Admission...")
    fix_admission_frame()
    
    # 3. Amélioration du dashboard
    print("3. Amélioration du dashboard...")
    fix_dashboard()
    
    # 4. Amélioration des combobox
    print("4. Amélioration des combobox...")
    fix_combobox_behavior()
    
    print("====================================================")
    print("  Améliorations terminées")
    print("====================================================")
    print("Vous pouvez maintenant lancer l'application avec:")
    print("python -m app.main")
    print("La navigation au clavier et les interactions avec les")
    print("combobox devraient être beaucoup plus fluides.")
    print("====================================================")

if __name__ == "__main__":
    main()