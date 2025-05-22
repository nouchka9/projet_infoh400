#!/usr/bin/env python3

def fix_indentation_error():
    """Corrige l'erreur d'indentation dans login_screen.py"""
    print("Correction de l'erreur d'indentation dans login_screen.py...")
    
    file_path = "app/ui/login_screen.py"
    
    try:
        # Lire le fichier ligne par ligne
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Faire une copie de sauvegarde
        with open(file_path + ".bak3", 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        # Rechercher et corriger la ligne avec l'indentation incorrecte
        fixed_lines = []
        in_method = False
        current_indent = ""
        
        for line in lines:
            # Détecter si nous sommes dans une méthode
            if line.strip().startswith("def "):
                in_method = True
                # Déterminer l'indentation de la méthode
                current_indent = " " * (len(line) - len(line.lstrip()))
                fixed_lines.append(line)
            # Si la ligne contient self._setup_combobox_behavior() avec une mauvaise indentation
            elif "self._setup_combobox_behavior()" in line:
                # Corriger l'indentation
                fixed_line = current_indent + "        self._setup_combobox_behavior()\n"
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print("✅ Indentation corrigée dans login_screen.py")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {str(e)}")
        
        # Solution alternative - remplacer complètement le fichier
        try:
            print("Tentative de réparation complète du fichier...")
            
            # Lire le fichier d'origine
            with open(file_path + ".bak", 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Restaurer le fichier d'origine
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            print("✅ Restauration du fichier d'origine. Tentez de réexécuter les scripts un par un.")
            
        except Exception as e2:
            print(f"❌ Échec de la restauration : {str(e2)}")
            print("Veuillez corriger manuellement le fichier login_screen.py")
    
    return True

if __name__ == "__main__":
    fix_indentation_error()