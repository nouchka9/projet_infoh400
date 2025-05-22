#!/usr/bin/env python3

def fix_admission_file():
    """Supprime les lignes problématiques de admission.py"""
    print("Correction de admission.py...")
    
    file_path = "app/ui/departments/admission.py"
    
    try:
        # Lire le fichier ligne par ligne
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Identifier et supprimer les lignes problématiques
        fixed_lines = []
        remove_next_lines = False
        
        for line in lines:
            # Si la ligne contient self._setup_combobox_behavior(), la supprimer
            if "_setup_combobox_behavior()" in line:
                print(f"Suppression de la ligne problématique: {line.strip()}")
                continue
            # Si la ligne contient une fonction _setup_combobox_behavior, supprimer la méthode entière
            if "def _setup_combobox_behavior" in line:
                remove_next_lines = True
                print("Début de suppression de la méthode _setup_combobox_behavior")
                continue
            # Si on supprime des lignes et qu'on trouve une nouvelle méthode, arrêter la suppression
            if remove_next_lines and line.strip().startswith("def "):
                remove_next_lines = False
                print("Fin de suppression de la méthode")
            
            # Si on ne supprime pas cette ligne, l'ajouter
            if not remove_next_lines:
                fixed_lines.append(line)
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("✅ Fichier admission.py corrigé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {str(e)}")
    
    return True

if __name__ == "__main__":
    fix_admission_file()