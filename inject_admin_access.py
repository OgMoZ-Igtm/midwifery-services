import json

MENU_FILE = "utils/menu_mapping.json"


def inject_admin_role():
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    for pack, entries in mapping.items():
        for entry in entries:
            roles = entry.get("roles", [])
            if pack not in ["DOCTOR", "PATIENT"] and "ADMIN" not in roles:
                roles.append("ADMIN")
                entry["roles"] = list(set(roles))  # éviter doublons

    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print("✅ Rôle ADMIN injecté dans tous les packs sauf DOCTOR et PATIENT.")


if __name__ == "__main__":
    inject_admin_role()
