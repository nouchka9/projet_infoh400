#!/usr/bin/env python3

def fix_admission_indentation():
    """Corrige l'erreur d'indentation dans admission.py"""
    print("Correction de l'erreur d'indentation dans admission.py...")
    
    file_path = "app/ui/departments/admission.py"
    
    try:
        # Lire le fichier d'origine
        with open(file_path + ".bak", 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Écrire le contenu original pour revenir à un état stable
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        print("✅ Restauration de admission.py à son état original")
        
        # Maintenant, appliquons les améliorations de comportement proprement
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Faire une sauvegarde du contenu actuel
        with open(file_path + ".before_fix", 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Ajouter les méthodes pour le comportement des Combobox à la fin du fichier
        combobox_methods = """
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
        self.update_idletasks()"""
        
        # Trouver la position pour insérer l'appel à _setup_combobox_behavior
        # Chercher la fin de la méthode __init__
        init_method = content.find("def __init__")
        next_method = content.find("def ", init_method + 10)
        
        # Trouver la dernière ligne non vide avant la prochaine méthode
        init_content = content[init_method:next_method]
        init_lines = init_content.split('\n')
        
        last_line_index = -1
        for i in range(len(init_lines) - 1, 0, -1):
            if init_lines[i].strip() and not init_lines[i].strip().startswith('#'):
                last_line_index = i
                break
        
        if last_line_index > 0:
            # Ajouter l'appel après la dernière ligne de __init__
            init_lines.insert(last_line_index + 1, "        # Configurer les comportements améliorés des menus déroulants")
            init_lines.insert(last_line_index + 2, "        self._setup_combobox_behavior()")
            
            # Reconstruire le contenu
            new_init_content = '\n'.join(init_lines)
            content = content[:init_method] + new_init_content + content[next_method:]
            
            # Ajouter les méthodes à la fin du fichier
            content += combobox_methods
            
            # Écrire le fichier modifié
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Améliorations du comportement des Combobox ajoutées correctement")
        else:
            print("⚠️ Impossible de trouver la fin de la méthode __init__")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {str(e)}")
        print("Tentative de restauration du fichier original...")
        
        try:
            # Restaurer le fichier original
            with open(file_path + ".bak", 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            print("✅ Fichier restauré à son état original")
        except Exception as e2:
            print(f"❌ Erreur lors de la restauration : {str(e2)}")
    
    return True

if __name__ == "__main__":
    fix_admission_indentation()