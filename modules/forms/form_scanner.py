import os

EXPECTED_ROLES = [
    "admin",
    "midwife",
    "doctor",
    "nurse",
    "patient",
    "intern",
    "guest",
    "student",
    "doctoral",
    "public",
    "shared",
]


def scan_missing_form_modules():
    missing = []
    for role in EXPECTED_ROLES:
        path = f"modules/forms/forms_{role}"
        if not os.path.isdir(path):
            missing.append(role)
    return missing


if __name__ == "__main__":
    print("📋 Dossiers de formulaire manquants :")
    for role in scan_missing_form_modules():
        print(f"- forms_{role}/")
