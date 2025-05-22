#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour corriger les erreurs de syntaxe dans app.py
"""
import os

def fix_app_py():
    """Corrige le fichier app.py"""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "ui", "app.py")
    
    try:
        # Lire le contenu actuel
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Créer un nouveau contenu corrigé
        new_content = []
        for i, line in enumerate(lines):
            # Ignorer la ligne problématique
            if "upgrade_comboboxes(self.current_screen)" in line and not line.strip().startswith('#'):
                # La ligne précédente doit être celle avec pack
                if i > 0 and "pack(fill=tk.BOTH, expand=True)" in lines[i-1]:
                    # Remplacer les deux lignes par une combinaison propre
                    new_content.append(lines[i-1].rstrip() + "\n")
                    new_content.append("        # Améliorer les combobox après le pack\n")
                    new_content.append("        self.after(100, lambda: upgrade_comboboxes(self.current_screen))\n")
                else:
                    # Simplement commenter la ligne
                    new_content.append("        # " + line)
            else:
                new_content.append(line)
        
        # Écrire le contenu corrigé
        with open(file_path, 'w') as f:
            f.writelines(new_content)
            
        print(f"✅ Fichier app.py corrigé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la correction du fichier app.py : {e}")
        return False

if __name__ == "__main__":
    print("Correction de l'erreur de syntaxe dans app.py...")
    fix_app_py()
    print("Vous pouvez maintenant relancer l'application avec: python -m app.main")