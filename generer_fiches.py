import os

# 📁 Dossier contenant les fichiers culturels
STATIC_DIR = "/home/ygd/projets-midwifery-Services/static"

# 📦 Dictionnaire à générer
fiches = {}

# 🔍 Extensions reconnues
IMAGE_EXTS = {".png", ".jpg", ".jpeg"}
AUDIO_EXTS = {".mp3", ".wav"}

# 📂 Regroupe les fichiers par base de nom
fichiers = os.listdir(STATIC_DIR)
groupes = {}

for f in fichiers:
    base, ext = os.path.splitext(f)
    ext = ext.lower()
    if ext in IMAGE_EXTS or ext in AUDIO_EXTS:
        groupes.setdefault(base, {})[ext] = f

# 🧠 Génère les fiches
for base, fichiers_associes in groupes.items():
    titre = base.replace("_", " ").capitalize()
    fiche = {
        "titre": titre,
        "image": os.path.join(
            STATIC_DIR, fichiers_associes.get(".png", fichiers_associes.get(".jpg", ""))
        ),
        "description": f"📘 Description par défaut pour {titre}.",
        "citation": f"« Citation inspirante sur {titre.lower()} »",
        "audio": (
            os.path.join(STATIC_DIR, fichiers_associes.get(".mp3", ""))
            if ".mp3" in fichiers_associes
            else None
        ),
    }
    fiches[titre] = fiche

# 🖨️ Affiche le dictionnaire généré
print("fiches = {")
for key, fiche in fiches.items():
    print(f'    "{key}": {{')
    for k, v in fiche.items():
        print(f'        "{k}": {repr(v)},')
    print("    },")
print("}")
