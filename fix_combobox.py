import tkinter as tk
from tkinter import ttk
import os

def fix_combobox_behavior():
    """
    Améliore le comportement des menus déroulants (Combobox) dans toute l'application
    """
    print("Ajout du support double-clic et touche Entrée pour les menus déroulants...")
    
    # Fichiers à modifier
    files = [
        "app/ui/login_screen.py",
        "app/ui/departments/admission.py",
        "app/ui/departments/laboratory.py",
        "app/ui/departments/radiology.py",
        "app/ui/departments/pharmacy.py",
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"❌ Fichier non trouvé: {file_path}")
            continue
            
        print(f"Modification de {file_path}...")
        
        # Lire le contenu du fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Faire une sauvegarde
        with open(f"{file_path}.bak", 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Vérifier si le fichier contient des Combobox
        if "Combobox" not in content:
            print(f"  ⚠️ Pas de Combobox dans {file_path}, passage...")
            continue
        
        # Ajouter la fonction _setup_combobox_behavior si elle n'existe pas déjà
        if "_setup_combobox_behavior" not in content:
            # Trouver la classe principale (qui hérite de ttk.Frame)
            class_index = content.find("class ") 
            if class_index == -1:
                print(f"  ❌ Impossible de trouver la classe principale dans {file_path}")
                continue
            
            # Trouver la fin de la méthode __init__
            init_end = content.find("def ", content.find("def __init__"))
            if init_end == -1:
                # Si pas d'autre méthode, chercher la fin du fichier
                init_end = len(content)
            
            # Insérer l'appel à _setup_combobox_behavior à la fin de __init__
            init_call = "\n        # Configurer les comportements améliorés des menus déroulants\n        self._setup_combobox_behavior()\n"
            
            # Trouver un bon endroit pour insérer l'appel - avant la dernière ligne de __init__
            # Chercher la dernière ligne non-vide avant la prochaine méthode
            lines = content[:init_end].split('\n')
            for i in range(len(lines)-1, 0, -1):
                if lines[i].strip() and not lines[i].strip().startswith('#'):
                    insertion_index = content.find(lines[i]) + len(lines[i])
                    content = content[:insertion_index] + init_call + content[insertion_index:]
                    break
            
            # Ajouter la méthode elle-même
            combobox_method = """
    def _setup_combobox_behavior(self):
        \"\"\"Configure les comportements améliorés pour tous les Combobox\"\"\"
        # Trouver tous les Combobox dans l'interface
        for widget in self.winfo_children():
            self._find_and_setup_comboboxes(widget)
    
    def _find_and_setup_comboboxes(self, parent):
        \"\"\"Recherche et configure récursivement tous les Combobox\"\"\"
        for child in parent.winfo_children():
            if isinstance(child, ttk.Combobox):
                # Configurer le double-clic pour valider la sélection
                child.bind("<Double-1>", lambda e: self._on_combobox_doubleclick(e))
                
                # Configurer la touche Entrée pour valider aussi
                child.bind("<Return>", lambda e: self._on_combobox_enter(e))
                
                # S'assurer que la sélection est appliquée lors du clic
                child.bind("<<ComboboxSelected>>", lambda e: self._on_combobox_selected(e))
            
            # Chercher récursivement dans les enfants
            if hasattr(child, "winfo_children"):
                self._find_and_setup_comboboxes(child)
    
    def _on_combobox_doubleclick(self, event):
        \"\"\"Gère le double-clic sur un menu déroulant\"\"\"
        combobox = event.widget
        
        # Si le menu est ouvert, le fermer et valider la sélection
        if combobox["state"] == "readonly":
            # Forcer la mise à jour de la variable liée
            value = combobox.get()
            var_name = str(combobox.cget("textvariable"))
            
            # Passer au champ suivant
            combobox.tk_focusNext().focus()
            
            # Forcer la mise à jour visuelle
            self.update_idletasks()
    
    def _on_combobox_enter(self, event):
        \"\"\"Gère la touche Entrée dans un menu déroulant\"\"\"
        combobox = event.widget
        
        # Forcer la mise à jour de la variable liée
        value = combobox.get()
        
        # Passer au champ suivant
        combobox.tk_focusNext().focus()
        
        # Forcer la mise à jour visuelle
        self.update_idletasks()
    
    def _on_combobox_selected(self, event):
        \"\"\"Gère la sélection dans un menu déroulant\"\"\"
        # Forcer la mise à jour visuelle
        self.update_idletasks()
"""
            # Ajouter la méthode à la fin du fichier
            content += combobox_method
        
        # Écrire le contenu modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"  ✅ Support double-clic et Entrée ajouté pour les menus déroulants dans {file_path}")
    
    print("\n✅ Modifications terminées. Vous pouvez maintenant relancer l'application.")
    print("Les menus déroulants devraient maintenant fonctionner avec double-clic et touche Entrée.")

if __name__ == "__main__":
    fix_combobox_behavior()