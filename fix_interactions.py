#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour améliorer le comportement des widgets Tkinter
"""
import os

def improve_combobox_behavior():
    """Crée un fichier de widgets améliorés pour les combobox"""
    # S'assurer que le dossier common existe
    common_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "common")
    if not os.path.exists(common_dir):
        os.makedirs(common_dir)
    
    # S'assurer que __init__.py existe
    init_path = os.path.join(common_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("# Package pour les widgets communs\n")
    
    # Créer le fichier widgets.py
    widgets_path = os.path.join(common_dir, "widgets.py")
    widgets_content = '''# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class BetterCombobox(ttk.Combobox):
    """Combobox avec meilleur comportement des touches"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configurer les événements
        self.bind("<<ComboboxSelected>>", self._on_selection)
        self.bind("<Return>", self._on_return)
        self.bind("<Double-1>", self._on_double_click)
        self.bind("<FocusOut>", self._on_focus_out)
        
    def _on_selection(self, event=None):
        """Quand un élément est sélectionné"""
        # Passer au prochain widget
        self.tk_focusNext().focus()
    
    def _on_return(self, event=None):
        """Quand la touche Entrée est pressée"""
        # Si la liste est affichée, sélectionner l'élément courant
        if self.winfo_viewable():
            self.selection_clear()
            self.focus_set()
            
        # Passer au widget suivant
        self.tk_focusNext().focus()
        return "break"  # Empêcher la propagation
    
    def _on_double_click(self, event=None):
        """Quand un double-clic est effectué"""
        # Valider explicitement la sélection
        self.selection_clear()
        
        # Passer au widget suivant
        self.after(100, lambda: self.tk_focusNext().focus())
    
    def _on_focus_out(self, event=None):
        """Quand le focus quitte le widget"""
        # S'assurer que la liste déroulante est fermée
        self.selection_clear()
'''
    
    with open(widgets_path, 'w') as f:
        f.write(widgets_content)
    
    print(f"✅ Widgets améliorés créés avec succès")

def fix_admission_navigation():
    """Corrige la navigation dans le formulaire d'admission"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "departments", "admission.py")
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} introuvable")
        return False
    
    # Lire le contenu actuel
    with open(file_path, 'r') as f:
        content = f.read()
    
    # 1. Supprimer la capture globale de la touche Entrée
    content = content.replace(
        'self.bind_all("<Return>", lambda event: self._on_login())',
        '# Ne pas intercepter Return globalement'
    )
    
    # 2. Ajouter une méthode pour gérer les entrées individuellement
    if "_add_entry_navigation" not in content:
        # Trouver un bon endroit pour ajouter la méthode
        pos = content.find("def _create_widgets")
        if pos > 0:
            # Chercher la fin de la méthode _create_widgets
            next_method = content.find("def ", pos + 10)
            if next_method > 0:
                # Ajouter la nouvelle méthode juste après
                new_method = '''
    def _add_entry_navigation(self):
        """Ajoute la navigation entre les champs"""
        # Parcourir tous les Entry et les connecter
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    self._connect_entries(subchild)
    
    def _connect_entries(self, parent):
        """Connecte les événements de touche pour les Entry"""
        for child in parent.winfo_children():
            if isinstance(child, ttk.Entry):
                child.bind("<Return>", self._on_entry_return)
                child.bind("<FocusIn>", self._on_entry_focus)
            elif isinstance(child, ttk.Combobox):
                # Remplacer l'événement Return des combobox
                child.bind("<Return>", self._on_entry_return, add="+")
            elif hasattr(child, "winfo_children"):
                self._connect_entries(child)
    
    def _on_entry_return(self, event):
        """Passe au champ suivant quand on appuie sur Entrée"""
        event.widget.tk_focusNext().focus()
        return "break"  # Important: arrête la propagation
    
    def _on_entry_focus(self, event):
        """Sélectionne tout le texte quand on entre dans un champ"""
        event.widget.select_range(0, tk.END)
'''
                content = content[:next_method] + new_method + content[next_method:]
        
        # Appeler la méthode après création des widgets
        pos = content.find("def _create_widgets")
        if pos > 0:
            end_method = content.find("def ", pos + 10)
            if end_method > 0:
                # Chercher la fin de la méthode
                last_line = content.rfind("\n", pos, end_method)
                if last_line > 0:
                    # Ajouter l'appel à _add_entry_navigation
                    content = content[:last_line] + "\n        # Configurer la navigation\n        self._add_entry_navigation()" + content[last_line:]
        
    # 3. Modifier _send_message pour éviter les envois multiples
    if "_send_message" in content:
        send_pos = content.find("def _send_message")
        if send_pos > 0:
            # Ajouter l'attribut processing dans __init__
            init_pos = content.find("def __init__")
            if init_pos > 0:
                end_init = content.find("def ", init_pos + 10)
                if end_init > 0:
                    # Trouver la dernière ligne de __init__
                    last_line = content.rfind("\n", init_pos, end_init)
                    if last_line > 0:
                        # Ajouter l'attribut processing
                        content = content[:last_line] + "\n        # Pour éviter les envois multiples\n        self.processing = False" + content[last_line:]
            
            # Modifier _send_message
            next_line = content.find("\n", send_pos)
            if next_line > 0:
                # Chercher le premier commentaire ou code
                first_line = content.find("\n        ", next_line)
                if first_line > 0:
                    # Ajouter la vérification des envois multiples
                    new_code = '''
        # Éviter les envois multiples
        if self.processing:
            return
            
        # Marquer comme en cours
        self.processing = True
'''
                    content = content[:first_line] + new_code + content[first_line:]
            
            # Ajouter la réinitialisation à la fin de _send_message
            end_method = content.find("def ", send_pos + 10)
            if end_method > 0:
                last_line = content.rfind("\n", send_pos, end_method)
                if last_line > 0:
                    content = content[:last_line] + "\n        # Réinitialiser l'état\n        self.processing = False" + content[last_line:]
    
    # Enregistrer les modifications
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Navigation dans AdmissionFrame améliorée")
    return True

def improve_dashboard_comboboxes():
    """Améliore les combobox dans le dashboard"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "dashboard.py")
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} introuvable")
        return False
    
    # Lire le contenu actuel
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Ajouter import pour les widgets améliorés
    if "from app.ui.common.widgets import BetterCombobox" not in content:
        import_pos = content.find("import")
        if import_pos > 0:
            last_import = content.rfind("import", 0, content.find("class Dashboard"))
            if last_import > 0:
                next_line = content.find("\n", last_import)
                if next_line > 0:
                    # Ajouter l'import avec try/except
                    new_import = '''

# Import des widgets améliorés
try:
    from app.ui.common.widgets import BetterCombobox
except ImportError:
    # Fallback si le module n'existe pas
    BetterCombobox = ttk.Combobox
'''
                    content = content[:next_line+1] + new_import + content[next_line+1:]
    
    # Ajouter une méthode pour remplacer les combobox
    if "_upgrade_comboboxes" not in content:
        # Trouver un bon endroit pour ajouter la méthode
        pos = content.find("def _create_widgets")
        if pos > 0:
            next_method = content.find("def ", pos + 15)
            if next_method > 0:
                new_method = '''
    def _upgrade_comboboxes(self, parent=None):
        """Remplace les combobox standard par les améliorés"""
        if parent is None:
            parent = self
            
        # Obtenir la référence à BetterCombobox
        better_combo = None
        try:
            better_combo = globals().get("BetterCombobox")
        except:
            return  # Ne rien faire si BetterCombobox n'est pas disponible
        
        if not better_combo:
            return
            
        # Parcourir tous les widgets enfants
        for child in parent.winfo_children():
            if isinstance(child, ttk.Combobox) and not isinstance(child, better_combo):
                # Récupérer les propriétés
                props = {}
                try:
                    props = {
                        "values": child["values"],
                        "textvariable": child.cget("textvariable"),
                        "state": child.cget("state"),
                        "width": child.cget("width")
                    }
                except:
                    continue
                
                # Récupérer les infos de placement
                grid_info = None
                pack_info = None
                
                try:
                    if child.winfo_manager() == "grid":
                        grid_info = child.grid_info()
                    elif child.winfo_manager() == "pack":
                        pack_info = child.pack_info()
                    else:
                        continue  # Ignorer les autres gestionnaires
                except:
                    continue
                    
                # Remplacer le combobox
                try:
                    # Créer un nouveau combobox amélioré
                    new_combo = better_combo(parent, **props)
                    
                    # Détruire l'ancien
                    child.destroy()
                    
                    # Placer le nouveau avec les mêmes infos
                    if grid_info:
                        new_combo.grid(**grid_info)
                    elif pack_info:
                        new_combo.pack(**pack_info)
                except Exception as e:
                    print(f"Erreur lors du remplacement du combobox: {e}")
                    continue
                    
            # Traiter récursivement les enfants
            elif hasattr(child, "winfo_children"):
                self._upgrade_comboboxes(child)
'''
                content = content[:next_method] + new_method + content[next_method:]
    
    # Appeler la méthode après chargement des départements
    if "_load_department_frame" in content:
        pos = content.find("print(f\"Frame du département {self.department} chargé avec succès\")")
        if pos > 0:
            next_line = content.find("\n", pos)
            if next_line > 0:
                # Ajouter l'appel
                content = content[:next_line+1] + "\n            # Améliorer les combobox\n            self.after(100, lambda: self._upgrade_comboboxes(self.dept_frame))" + content[next_line+1:]
    
    # Enregistrer les modifications
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Combobox dans le dashboard améliorés")
    return True

def create_quick_fix_script():
    """Crée un script pour corriger rapidement les problèmes dans l'application en cours d'exécution"""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_comboboxes.py")
    
    script_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour corriger rapidement les problèmes de combobox
"""
import tkinter as tk
from tkinter import ttk, messagebox

class FixComboboxesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Corriger les ComboBox")
        self.root.geometry("400x300")
        
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(frame, text="Correcteur de ComboBox", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        
        msg = ttk.Label(frame, text="""Ce script va corriger les problèmes
d'interaction avec les menus déroulants.

L'application HL7 Messenger doit être
fermée avant d'exécuter ce script.""", justify="center")
        msg.pack(pady=10)
        
        self.fix_btn = ttk.Button(frame, text="Corriger les ComboBox", command=self.fix_comboboxes)
        self.fix_btn.pack(pady=10)
        
        self.status_var = tk.StringVar(value="Prêt")
        status = ttk.Label(frame, textvariable=self.status_var, font=("Helvetica", 10, "italic"))
        status.pack(pady=10)
        
        quit_btn = ttk.Button(frame, text="Quitter", command=root.destroy)
        quit_btn.pack(pady=10)
    
    def fix_comboboxes(self):
        """Corrige les problèmes de combobox"""
        try:
            # Créer le dossier des widgets améliorés
            import os
            common_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "common")
            if not os.path.exists(common_dir):
                os.makedirs(common_dir)
            
            # Créer le fichier __init__.py
            init_path = os.path.join(common_dir, "__init__.py")
            with open(init_path, 'w') as f:
                f.write("# Module des widgets communs\\n")
            
            # Créer le fichier widgets.py
            widgets_path = os.path.join(common_dir, "widgets.py")
            with open(widgets_path, 'w') as f:
                f.write("""import tkinter as tk
from tkinter import ttk

class BetterCombobox(ttk.Combobox):
    \"""Combobox avec meilleur comportement\"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configurer les événements
        self.bind("<<ComboboxSelected>>", self._on_selection)
        self.bind("<Return>", self._on_return)
        self.bind("<Double-1>", self._on_double_click)
        self.bind("<FocusOut>", self._on_focus_out)
        
    def _on_selection(self, event=None):
        \"""Quand un élément est sélectionné\"""
        # Passer au prochain widget
        self.tk_focusNext().focus()
    
    def _on_return(self, event=None):
        \"""Quand la touche Entrée est pressée\"""
        # Si la liste est affichée, sélectionner l'élément courant
        if self.winfo_viewable():
            self.selection_clear()
            self.focus_set()
            
        # Passer au widget suivant
        self.tk_focusNext().focus()
        return "break"  # Empêcher la propagation
    
    def _on_double_click(self, event=None):
        \"""Quand un double-clic est effectué\"""
        # Valider explicitement la sélection
        self.selection_clear()
        
        # Passer au widget suivant
        self.after(100, lambda: self.tk_focusNext().focus())
    
    def _on_focus_out(self, event=None):
        \"""Quand le focus quitte le widget\"""
        # S'assurer que la liste déroulante est fermée
        self.selection_clear()
""")
            
            # Modifier dashboard.py pour utiliser les combobox améliorés
            dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "dashboard.py")
            with open(dashboard_path, 'r') as f:
                dashboard_content = f.read()
            
            # Ajouter l'import s'il n'existe pas
            if "from app.ui.common.widgets import" not in dashboard_content:
                # Trouver la position pour ajouter l'import
                import_pos = dashboard_content.find("import")
                if import_pos >= 0:
                    end_imports = dashboard_content.find("class Dashboard")
                    if end_imports > 0:
                        # Trouver le dernier import
                        last_import = dashboard_content.rfind("import", 0, end_imports)
                        if last_import >= 0:
                            next_line = dashboard_content.find("\\n", last_import)
                            if next_line > 0:
                                dashboard_content = dashboard_content[:next_line+1] + """
try:
    from app.ui.common.widgets import BetterCombobox
except ImportError:
    BetterCombobox = ttk.Combobox  # Fallback
""" + dashboard_content[next_line+1:]
            
            # Enregistrer les modifications
            with open(dashboard_path, 'w') as f:
                f.write(dashboard_content)
            
            # Message de succès
            self.status_var.set("✅ Correction réussie!")
            messagebox.showinfo("Succès", "Les ComboBox ont été corrigés avec succès.\\n\\nVous pouvez maintenant relancer l'application principale.")
            
        except Exception as e:
            self.status_var.set(f"❌ Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Une erreur est survenue:\\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FixComboboxesApp(root)
    root.mainloop()
'''
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Script de correction rapide créé: fix_comboboxes.py")
    return True

def main():
    """Point d'entrée du script"""
    print("=" * 50)
    print("  Correction des problèmes d'interface  ")
    print("=" * 50)
    
    # 1. Créer les widgets améliorés
    print("\n1. Création des widgets améliorés...")
    improve_combobox_behavior()
    
    # 2. Corriger la navigation dans le formulaire d'admission
    print("\n2. Amélioration de la navigation dans Admission...")
    fix_admission_navigation()
    
    # 3. Améliorer les combobox dans le dashboard
    print("\n3. Amélioration des combobox dans le dashboard...")
    improve_dashboard_comboboxes()
    
    # 4. Créer un script de correction rapide
    print("\n4. Création d'un script de correction rapide...")
    create_quick_fix_script()
    
    print("\n" + "=" * 50)
    print("  Corrections terminées  ")
    print("=" * 50)
    print("Redémarrez l'application avec: python -m app.main")
    print("\nSi des problèmes persistent, vous pouvez exécuter:")
    print("python fix_comboboxes.py")
    print("=" * 50)

if __name__ == "__main__":
    main()