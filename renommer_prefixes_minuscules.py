import os
import re


def ajouter_prefixes(dossier="packs"):
    for racine, _, fichiers in os.walk(dossier):
        fichiers_py = [f for f in fichiers if f.endswith(".py")]
        fichiers_py.sort()  # tri alphabétique pour cohérence

        compteur = 1
        for fichier in fichiers_py:
            chemin_complet = os.path.join(racine, fichier)

            # Vérifie si le fichier a déjà un préfixe numérique
            if re.match(r"^\d+_", fichier):
                print(f"⏩ Ignoré (déjà préfixé) : {chemin_complet}")
                continue

            # Nouveau nom avec préfixe formaté sur 2 chiffres
            nouveau_nom = f"{compteur:02d}_{fichier}"
            chemin_nouveau = os.path.join(racine, nouveau_nom)

            os.rename(chemin_complet, chemin_nouveau)
            print(f"✅ {chemin_complet} → {chemin_nouveau}")

            compteur += 1


if __name__ == "__main__":
    ajouter_prefixes("packs")  # on part du dossier packs
