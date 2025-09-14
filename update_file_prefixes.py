import os
import json
import difflib

# Définition des chemins des dossiers
# Ce script suppose qu'il est exécuté depuis le répertoire racine du projet.
MENU_MAPPING_PATH = os.path.join("utils", "menu_mapping.json")
PACKS_DIR = "packs"


def find_all_python_files(directory):
    """
    Parcourt une arborescence de dossiers et retourne une liste de tous les fichiers Python.
    Les chemins sont relatifs au répertoire spécifié.
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and not root.endswith("__pycache__"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                python_files.append(
                    os.path.join(directory, relative_path).replace("\\", "/")
                )
    return python_files


def sanitize_filename(filename):
    """
    Nettoie le nom de fichier pour la comparaison, en enlevant le préfixe de pack et le numéro.
    Ex: 'ADMIN_01_Admin_Dashboard.py' -> 'Admin_Dashboard.py'
    Ex: '01_Admin_Dashboard.py' -> 'Admin_Dashboard.py'
    """
    # Enlever le préfixe de pack et le numéro s'ils existent
    parts = os.path.basename(filename).split("_")
    # Vérifier si c'est le format "PACK_00_Nom.py" ou "00_Nom.py"
    if len(parts) > 2 and parts[1].isdigit():
        return "_".join(parts[2:])
    if len(parts) > 1 and parts[0].isdigit():
        return "_".join(parts[1:])
    return os.path.basename(filename)


def update_file_prefixes():
    """
    Renomme les fichiers des packs en fonction de la configuration
    et met à jour les chemins dans le fichier JSON.
    Cette version inclut un mode interactif pour corriger les chemins incorrects.
    """
    print("Démarrage du renommage des fichiers...")

    # Charge le fichier de configuration JSON
    if not os.path.exists(MENU_MAPPING_PATH):
        print(
            f"❌ Erreur : Le fichier de configuration '{MENU_MAPPING_PATH}' n'a pas été trouvé."
        )
        return

    try:
        with open(MENU_MAPPING_PATH, "r", encoding="utf-8") as f:
            menu_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON dans '{MENU_MAPPING_PATH}': {e}")
        return
    except IOError as e:
        print(
            f"❌ Erreur d'entrée/sortie lors de la lecture du fichier '{MENU_MAPPING_PATH}': {e}"
        )
        return

    all_project_files = find_all_python_files(PACKS_DIR)

    changes_made = False
    for pack_name, files in menu_data.items():
        print(f"\nTraitement du pack '{pack_name}'...")
        for item in files:
            original_file_path = item.get("file")
            if not original_file_path:
                continue

            full_original_path = os.path.join(os.getcwd(), original_file_path)

            # Gérer le cas du fichier __init__.py
            if os.path.basename(original_file_path) == "__init__.py":
                # S'assurer qu'il n'a pas de préfixe
                correct_path = os.path.join(
                    os.path.dirname(original_file_path), "__init__.py"
                ).replace("\\", "/")
                if original_file_path != correct_path:
                    # Rename the file on disk first
                    if os.path.exists(original_file_path):
                        os.rename(original_file_path, correct_path)
                        print(
                            f"✅ Renommage dans le pack '{pack_name}': {original_file_path} -> {correct_path}"
                        )
                        changes_made = True
                    else:
                        print(
                            f"❌ Avertissement : Fichier {original_file_path} à corriger dans le JSON n'existe pas. Veuillez le corriger manuellement. "
                        )
                    item["file"] = correct_path
                continue

            # Vérifie si le fichier existe
            if not os.path.exists(original_file_path):
                print(
                    f"❌ Avertissement dans le pack '{pack_name}': Le fichier '{original_file_path}' n'a pas été trouvé, pas de renommage."
                )

                # Propose une correspondance en fonction du nom du fichier
                sanitized_to_find = sanitize_filename(original_file_path)
                best_match = difflib.get_close_matches(
                    sanitized_to_find,
                    [sanitize_filename(f) for f in all_project_files],
                    n=1,
                    cutoff=0.8,
                )

                if best_match:
                    # Trouver le chemin complet correspondant au nom de fichier assaini
                    found_path = next(
                        (
                            f
                            for f in all_project_files
                            if sanitize_filename(f) == best_match[0]
                        ),
                        None,
                    )
                    if found_path:
                        print(f"   ℹ️ Fichier similaire trouvé : '{found_path}'.")
                        choice = input(
                            f"   Voulez-vous mettre à jour le chemin dans le JSON vers '{found_path}' ? (oui/non) : "
                        ).lower()
                        if choice == "oui" or choice == "o":
                            item["file"] = found_path
                            print(
                                f"   ✅ Le chemin du fichier a été mis à jour dans le JSON."
                            )
                            changes_made = True
                        else:
                            print("   ⏩ Correction ignorée.")

                continue

            # Construit le nouveau nom de fichier avec le préfixe du pack
            dir_path, filename = os.path.split(original_file_path)
            prefix = f"{pack_name.upper()}_"
            new_filename = (
                f"{prefix}{filename}" if not filename.startswith(prefix) else filename
            )
            new_file_path = os.path.join(dir_path, new_filename).replace("\\", "/")

            # Met à jour le chemin dans le dictionnaire si nécessaire
            if original_file_path != new_file_path:
                item["file"] = new_file_path

            # Renomme le fichier sur le disque
            if (
                os.path.exists(original_file_path)
                and original_file_path != new_file_path
            ):
                try:
                    os.rename(original_file_path, new_file_path)
                    print(
                        f"✅ Renommage dans le pack '{pack_name}': {original_file_path} -> {new_file_path}"
                    )
                    changes_made = True
                except OSError as e:
                    print(
                        f"❌ Erreur lors du renommage de '{original_file_path}' vers '{new_file_path}': {e}"
                    )
            else:
                print(
                    f"✅ Renommage dans le pack '{pack_name}': Le fichier '{original_file_path}' a déjà le bon préfixe. Pas de changement."
                )

    # Sauvegarde les modifications dans le fichier JSON
    if changes_made:
        try:
            with open(MENU_MAPPING_PATH, "w", encoding="utf-8") as f:
                json.dump(menu_data, f, indent=4, ensure_ascii=False)
            print("\n✅ Fichier JSON et chemins d'accès mis à jour avec succès!")
        except IOError as e:
            print(f"❌ Erreur d'écriture dans le fichier '{MENU_MAPPING_PATH}': {e}")
    else:
        print(
            "\nℹ️ Aucun renommage nécessaire. Tous les fichiers ont déjà le bon préfixe."
        )


if __name__ == "__main__":
    update_file_prefixes()
