import os
import re

# Définissez le répertoire racine de votre projet
PROJECT_ROOT = "./"
FIXED_FILES = []


def normalize_file_content(filepath):
    """
    1. Supprime les caractères invisibles (ZWS).
    2. Normalise l'indentation (tabulations -> 4 espaces).
    Ces corrections corrigent généralement les erreurs 'unexpected indent' et
    les erreurs de syntaxe inattendues comme 'expected except or finally block'.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {filepath}: {e}")
        return None

    original_content = content

    # 1. Nettoyage des caractères invisibles (ZWS = Zero-Width Space, \u200b)
    # et des espaces insécables (NBSP, \xa0) qui causent des erreurs de syntaxe silencieuses.
    # On remplace les insécables par un espace standard, puis on retire les ZWS.
    content = content.replace("\xa0", " ").replace("\u200b", "")

    # 2. Normalisation de l'indentation (Tabulations -> 4 espaces)
    content = content.replace("\t", "    ")

    if content != original_content:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'écriture de {filepath}: {e}")
            return False

    return False


def fix_syntax_errors():
    """
    Parcourt le répertoire du projet et applique la normalisation du contenu à tous les fichiers .py.
    """
    print(
        "🌿 Démarrage de la correction automatique des erreurs de syntaxe et d'indentation...\n"
    )

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Ignorer les répertoires de cache et virtuels
        dirs[:] = [
            d
            for d in dirs
            if d not in [".git", "__pycache__", ".venv", "venv", "node_modules"]
        ]

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)

                # Exclure le script de correction lui-même
                if os.path.basename(__file__) == os.path.basename(filepath):
                    continue

                if normalize_file_content(filepath):
                    FIXED_FILES.append(filepath)
                    print(f"✅ Fichier corrigé : {filepath}")

    print("\n🎉 Correction terminée.")
    if FIXED_FILES:
        print("🗂️ Fichiers modifiés :")
        for f in FIXED_FILES:
            print(f"  - {f}")
    else:
        print(
            "Aucun fichier n'a nécessité de correction d'indentation ou de caractères invisibles."
        )


if __name__ == "__main__":
    fix_syntax_errors()
