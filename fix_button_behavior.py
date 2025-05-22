import tkinter as tk
from tkinter import ttk
import os

def fix_button_behavior():
    """
    Améliore le comportement des boutons dans l'application
    """
    print("Ajout du support amélioré pour les boutons...")
    
    # Fichier à modifier pour la connexion
    login_file = "app/ui/login_screen.py"
    
    if not os.path.exists(login_file):
        print(f"❌ Fichier non trouvé: {login_file}")
        return False
        
    print(f"Modification de {login_file}...")
    
    # Lire le contenu du fichier
    with open(login_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Faire une sauvegarde
    with open(f"{login_file}.bak", 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Modifier la méthode _create_widgets pour améliorer le comportement de la touche Entrée
    # Chercher la ligne bind_all("<Return>", lambda event: self._on_login())
    if 'bind_all("<Return>"' in content:
        # Remplacer par une version améliorée
        content = content.replace(
            'self.bind_all("<Return>", lambda event: self._on_login())',
            """
        # Amélioration de la touche Entrée
        def handle_return(event):
            # Trouver le widget qui a le focus
            focused = self.focus_get()
            
            # Si c'est dans le menu déroulant, passer au bouton de login
            if isinstance(focused, ttk.Combobox):
                self.update_idletasks()
                login_button.focus()
                return
                
            # Sinon, déclencher le login
            self._on_login()
            return "break"  # Arrêter la propagation de l'événement
            
        self.bind_all("<Return>", handle_return)
        """
        )
    
    # Écrire le contenu modifié
    with open(login_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"  ✅ Support amélioré pour les boutons dans {login_file}")
    
    # Modifier les autres fichiers pour améliorer le comportement des boutons Envoyer/Réinitialiser
    other_files = [
        "app/ui/departments/admission.py",
        "app/ui/departments/laboratory.py", 
        "app/ui/departments/radiology.py",
        "app/ui/departments/pharmacy.py"
    ]
    
    for file_path in other_files:
        if not os.path.exists(file_path):
            print(f"❌ Fichier non trouvé: {file_path}")
            continue
            
        print(f"Modification de {file_path}...")
        
        # Lire le contenu du fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Faire une sauvegarde
        with open(f"{file_path}.bak2", 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Ajouter un gestionnaire global pour la touche Entrée
        if 'bind_all("<Return>"' not in content:
            # Trouver la fin de la méthode _create_widgets
            widgets_end = content.find("def ", content.find("def _create_widgets"))
            if widgets_end == -1:
                widgets_end = len(content)
            
            # Ajouter le gestionnaire à la fin de _create_widgets
            handler_code = """
        # Amélioration de la touche Entrée pour tout l'écran
        def handle_global_return(event):
            # Trouver le widget qui a le focus
            focused = self.focus_get()
            
            # Si on est dans un champ qui n'est pas un bouton, passer au suivant
            if not isinstance(focused, ttk.Button):
                # Si c'est un menu déroulant, fermer et valider
                if isinstance(focused, ttk.Combobox):
                    value = focused.get()
                    focused.tk_focusNext().focus()
                    self.update_idletasks()
                else:
                    # Sinon, passer au champ suivant
                    focused.tk_focusNext().focus()
                return "break"
            
            # Si c'est le bouton d'envoi, déclencher l'envoi
            if focused == self.send_button:
                self._send_message()
                return "break"
                
            # Si c'est le bouton de réinitialisation, déclencher la réinitialisation
            if focused == self.reset_button:
                self._reset_form()
                return "break"
            
            return
            
        self.bind_all("<Return>", handle_global_return)
"""
            # Insérer à la fin de _create_widgets
            lines = content[:widgets_end].split('\n')
            for i in range(len(lines)-1, 0, -1):
                if lines[i].strip() and not lines[i].strip().startswith('#'):
                    insertion_index = content.find(lines[i]) + len(lines[i])
                    content = content[:insertion_index] + handler_code + content[insertion_index:]
                    break
                    
            # Écrire le contenu modifié
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"  ✅ Support amélioré pour les boutons dans {file_path}")
    
    print("\n✅ Modifications terminées. Vous pouvez maintenant relancer l'application.")
    print("Les boutons devraient maintenant fonctionner avec la touche Entrée de façon plus intuitive.")
    return True

if __name__ == "__main__":
    fix_button_behavior()