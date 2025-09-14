import os
import json

MENU_FILE = "utils/menu_mapping.json"
PACKS_DIR = "packs"
VALID_ROLES = {
    "ADMIN",
    "DOCTOR",
    "MIDWIFE",
    "PATIENT",
    "STUDENT",
    "INTERN",
    "DOCTORAL",
    "NURSE",
    "MESSAGES",
    "ALL",
}


def verify_menu():
    if not os.path.exists(MENU_FILE):
        print("❌ Fichier menu_mapping.json introuvable.")
        return

    with open(MENU_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    errors = []
    for pack, entries in mapping.items():
        if not entries:
            errors.append(f"⚠️ Pack vide : {pack}")
            continue

        for entry in entries:
            name = entry.get("name", "Nom inconnu")
            file_path = entry.get("file")
            roles = entry.get("roles", [])

            # Vérification du fichier
            if not file_path or not os.path.exists(file_path):
                errors.append(
                    f"❌ Fichier manquant pour '{name}' dans {pack} → {file_path}"
                )

            # Vérification des rôles
            if not roles:
                errors.append(f"⚠️ Aucun rôle défini pour '{name}' dans {pack}")
            else:
                for role in roles:
                    if role.upper() not in VALID_ROLES:
                        errors.append(
                            f"❌ Rôle invalide '{role}' pour '{name}' dans {pack}"
                        )

    if errors:
        print("\n".join(errors))
    else:
        print("✅ Tous les fichiers et rôles sont valides.")


if __name__ == "__main__":
    verify_menu()
