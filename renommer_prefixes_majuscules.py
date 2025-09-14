import os
import re

BASE_DIR = "packs"

def normalize_filename(name: str) -> str:
    """
    Normalise les noms de fichiers :
    - Corrige la casse (majuscule après underscore).
    - Supprime les doublons _message vs _Message.
    """
    parts = name.split("_", 1)
    if len(parts) == 2:
        prefix, rest = parts
        return f"{prefix}_{rest[0].upper()}{rest[1:]}"
    return name

def renommer_pack(pack_path):
    if not os.path.exists(pack_path):
        print(f"⚠️ Pack introuvable : {pack_path}")
        return
    
    fichiers = sorted([f for f in os.listdir(pack_path) if f.endswith(".py")])
    
    # Nettoyage et normalisation des noms
    fichiers_nettoyes = []
    deja_vus = set()
    for f in fichiers:
        nf = normalize_filename(f)
        if nf.lower() in deja_vus:
            print(f"🗑️ Doublon supprimé : {f}")
            os.remove(os.path.join(pack_path, f))
            continue
        deja_vus.add(nf.lower())
        if nf != f:
            os.rename(os.path.join(pack_path, f), os.path.join(pack_path, nf))
            print(f"🔤 {f} → {nf}")
        fichiers_nettoyes.append(nf)
    
    # Réattribuer des préfixes numériques
    for i, f in enumerate(sorted(fichiers_nettoyes), 1):
        nouveau_nom = f"{i:02d}_{re.sub(r'^[0-9]+_', '', f)}"
        ancien_chemin = os.path.join(pack_path, f)
        nouveau_chemin = os.path.join(pack_path, nouveau_nom)
        if f != nouveau_nom:
            os.rename(ancien_chemin, nouveau_chemin)
            print(f"✅ {f} → {nouveau_nom}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"⚠️ Dossier introuvable : {BASE_DIR}")
        return
    
    for pack in os.listdir(BASE_DIR):
        pack_path = os.path.join(BASE_DIR, pack)
        upper_pack_path = os.path.join(BASE_DIR, pack.upper())
        
        # Forcer tout en MAJUSCULES
        if pack != pack.upper():
            os.rename(pack_path, upper_pack_path)
            print(f"📂 Renommage dossier : {pack} → {pack.upper()}")
            pack_path = upper_pack_path
        
        renommer_pack(pack_path)

if __name__ == "__main__":
    main()
