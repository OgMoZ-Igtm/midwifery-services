import os
import importlib


def tester_packs():
    base_dir = "packs"
    erreurs = []
    ok = []

    # Parcourt tous les sous-dossiers des packs
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                chemin_relatif = os.path.join(root, file)
                module_path = (
                    chemin_relatif.replace("/", ".")
                    .replace("\\", ".")
                    .replace(".py", "")
                )

                try:
                    module = importlib.import_module(module_path)
                    if hasattr(module, "app"):
                        ok.append(module_path)
                    else:
                        erreurs.append((module_path, "⚠️ Pas de fonction app()"))
                except Exception as e:
                    erreurs.append((module_path, f"❌ Erreur d'import : {e}"))

    # Résultats
    print("✅ Modules valides :")
    for m in ok:
        print("   -", m)

    if erreurs:
        print("\n🚨 Problèmes détectés :")
        for m, err in erreurs:
            print(f"   - {m} → {err}")
    else:
        print("\n🎉 Tous les packs sont valides !")


if __name__ == "__main__":
    tester_packs()
