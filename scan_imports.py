import os

# 🔍 Mot-clé à rechercher (tu peux en ajouter plusieurs)
keywords = [
    "render_bebe_experience",
    "render_weather_card",
    "render_cultural_carousel",
    "from modules import utils",
    "from modules.utils import",
]

# 📁 Dossier racine du projet
root_dir = "/home/ygd/projets-midwifery-Services"

# 📦 Extensions de fichiers à scanner
valid_extensions = [".py"]

# 📜 Résultats
matches = []

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if any(filename.endswith(ext) for ext in valid_extensions):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    for keyword in keywords:
                        if keyword in content:
                            matches.append((filepath, keyword))
            except Exception as e:
                print(f"Erreur avec {filepath} : {e}")

# 📋 Affichage des résultats
if matches:
    print("\n📦 Fichiers contenant les imports :\n")
    for path, keyword in matches:
        print(f"✅ {keyword} → {path}")
else:
    print("❌ Aucun import trouvé pour les mots-clés spécifiés.")
