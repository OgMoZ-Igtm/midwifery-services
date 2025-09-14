import os
import json

PACKS_DIR = "packs"
OUTPUT_FILE = "utils/menu_mapping.json"

# Règles de rôle par défaut
ROLE_RULES = {
    "PATIENT": ["PATIENT", "DOCTOR", "NURSE", "MIDWIFE"],
    "DOCTOR": ["DOCTOR", "ADMIN"],
    "ADMIN": ["ADMIN"],
    "MESSAGES": ["ALL"],
    "MIDWIFE": ["MIDWIFE", "NURSE", "STUDENT", "INTERN"],
    "NURSE": ["NURSE", "MIDWIFE", "STUDENT"],
    "STUDENT": ["STUDENT", "INTERN"],
    "DOCTORAL": ["DOCTORAL", "ADMIN"],
    "INTERN": ["INTERN", "STUDENT"],
    "ORGANISATION": ["NURSE", "MIDWIFE", "ADMIN"],
}


def generate_mapping():
    mapping = {}
    for pack in sorted(os.listdir(PACKS_DIR)):
        pack_path = os.path.join(PACKS_DIR, pack)
        if not os.path.isdir(pack_path):
            continue

        files = sorted([f for f in os.listdir(pack_path) if f.endswith(".py")])
        entries = []

        for i, file in enumerate(files, 1):
            entry = {
                "id": f"{pack.lower()}_{i:02d}",
                "order": i,
                "name": file.replace(".py", "").replace("_", " "),
                "file": os.path.join(pack_path, file).replace("\\", "/"),
                "roles": ROLE_RULES.get(pack.upper(), ["ALL"]),
            }
            entries.append(entry)

        if entries:
            mapping[pack.upper()] = entries

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"✅ Menu mapping mis à jour ({OUTPUT_FILE})")


if __name__ == "__main__":
    generate_mapping()
