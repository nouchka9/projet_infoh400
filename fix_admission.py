#!/usr/bin/env python3

import re
import os

def fix_admission_py():
    """Corrige les problèmes d'indentation dans admission.py"""
    
    file_path = "app/ui/departments/admission.py"
    
    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print(f"⚠️ Le fichier {file_path} n'existe pas.")
        return False
    
    # Lire le contenu du fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Faire une copie de sauvegarde
    backup_path = file_path + ".bak"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Sauvegarde créée: {backup_path}")
    
    # Corriger l'indentation de _set_default_values
    # Cette regex cherche le motif de la fonction avec une indentation incorrecte
    pattern_def = r'def _set_default_values\(self\):'
    fixed_def = '    def _set_default_values(self):'
    content = re.sub(pattern_def, fixed_def, content)
    
    # Corriger l'indentation du contenu de _set_default_values
    # Diviser le contenu en lignes
    lines = content.split('\n')
    in_set_default_values = False
    fixed_lines = []
    
    for line in lines:
        # Détecter le début de la fonction _set_default_values
        if '_set_default_values' in line and 'def' in line:
            in_set_default_values = True
            fixed_lines.append(line)
        # Lignes dans la fonction _set_default_values qui ne sont pas vides et ne sont pas une autre fonction
        elif in_set_default_values and line.strip() and not line.lstrip().startswith('def'):
            # Indenter avec 8 espaces
            fixed_line = '        ' + line.lstrip()
            fixed_lines.append(fixed_line)
        # Fin de la fonction _set_default_values (soit ligne vide soit nouvelle fonction)
        elif in_set_default_values and (not line.strip() or line.lstrip().startswith('def')):
            in_set_default_values = False
            fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Rejoindre les lignes
    fixed_content = '\n'.join(fixed_lines)
    
    # Écrire le contenu corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✅ Indentation corrigée dans {file_path}")
    return True

if __name__ == "__main__":
    if fix_admission_py():
        print("✅ Fichier admission.py corrigé avec succès")
        print("Vous pouvez maintenant relancer l'application avec: python -m app.main")
    else:
        print("❌ Impossible de corriger le fichier admission.py")