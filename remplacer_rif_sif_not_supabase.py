import os

# Dossier racine de ton projet
root_dir = "/home/ygd/projets-midwifery-Services"

# Parcours récursif de tous les fichiers .py
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(subdir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remplacer toutes les occurrences de "if not supabase:" par "if not supabase:"
            new_content = content.replace("if not supabase:", "if not supabase:")

            # Remplacer aussi "if not supabase:" si ça existe
            new_content = new_content.replace("if not supabase:", "if not supabase:")

            if new_content != content:
                print(f"Corrigé : {file_path}")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
