import os

# Liste des fichiers à corriger
targets = [
    "modules/forms_midwife/dashboard_midwife.py",
    "modules/shared/form_chat.py",
    "modules/backend/supabase_client.py",
    "modules/form_chat.py",
    "modules/tools/upload_file.py",
    "scripts/diagnostic_supabase.py",
]


# Remplacement sacré
def fix_response_check(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if "if response.status_code == 200" in line:
            indent = line[: len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}if response.data:\n")
            new_lines.append(f"{indent}    # succès\n")
            new_lines.append(f"{indent}else:\n")
            new_lines.append(
                f'{indent}    st.error(f"❌ Erreur Supabase : {{response.error}}")\n'
            )
        elif "return response.status_code == 200" in line:
            new_lines.append("return bool(response.data)\n")
        else:
            new_lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✅ Corrigé : {path}")


# Exécution
if __name__ == "__main__":
    for path in targets:
        if os.path.exists(path):
            fix_response_check(path)
        else:
            print(f"⚠️ Fichier introuvable : {path}")
