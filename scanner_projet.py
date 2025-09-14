import os
import re

BASE_DIR = "packs"
# correspondance des anciens noms (minuscules) → nouveaux noms (MAJUSCULES)
MAPPING = {
    "patient": "PATIENT",
    "doctor": "DOCTOR",
    "messages": "MESSAGES",
    "midwife": "MIDWIFE",
    "nurse": "NURSE",
    "admin": "ADMIN",
    "organisation": "ORGANISATION",
}


def corriger_imports(dossier="."):
    for root, _, files in os.walk(dossier):
        for file in files:
            if file.endswith(".py"):
                chemin = os.path.join(root, file)
                with open(chemin, "r", encoding="utf-8") as f:
                    contenu = f.read()

                nouveau_contenu = contenu
                for ancien, nouveau in MAPPING.items():
                    # corrige "from packs.PATIENT..." et "import packs.PATIENT..."
                    nouveau_contenu = re.sub(
                        rf"(from|import)\s+packs\.{ancien}",
                        rf"\1 packs.{nouveau}",
                        nouveau_contenu,
                    )

                if nouveau_contenu != contenu:
                    with open(chemin, "w", encoding="utf-8") as f:
                        f.write(nouveau_contenu)
                    print(f"✅ Imports corrigés dans {chemin}")


if __name__ == "__main__":
    corriger_imports(".")
