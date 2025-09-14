import os

ROLES = {
    "MIDWIFE": {"emoji": "🌾", "image": "welcome_midwife.png"},
    "DOCTOR": {"emoji": "🩺", "image": "welcome_doctor.png"},
    "PATIENT": {"emoji": "👶", "image": "welcome_patient.png"},
    "ADMIN": {"emoji": "👩‍💻", "image": "welcome_admin.png"},
    "STUDENT": {"emoji": "📚", "image": "welcome_student.png"},
    "DOCTORAL": {"emoji": "🎓", "image": "welcome_doctoral.png"},
    "NURSE": {"emoji": "💉", "image": "welcome_nurse.png"},
    "INTERN": {"emoji": "🧪", "image": "welcome_intern.png"},
}

BASE_DIR = "packs"

TEMPLATE = """# Fichier généré automatiquement
from welcome import render

if __name__ == "__main__":
    render("{role}")
"""


def generate_welcome(role, emoji, image):
    folder = os.path.join(BASE_DIR, role)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "welcome.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(role=role))
    print(f"✅ Fichier welcome.py généré pour {role}")


if __name__ == "__main__":
    for role, config in ROLES.items():
        generate_welcome(role, config["emoji"], config["image"])
