# ⚠️ import cassé : os
# ⚠️ import cassé : re

# 📁 Dossier à scanner
ROOT_DIR = "modules/forms"

# 🔍 Expression régulière pour détecter les appels à run()
RUN_CALL_PATTERN = re.compile(r"\brun\(\)")

# 📦 Fichiers à ignorer (ex: dashboards qui doivent appeler run())
WHITELISTED_FILES = [
    "dashboard_admin.py",
    "dashboard_doctor.py",
    "dashboard_midwife.py",
    "dashboard_guest.py",
    "dashboard_patient.py",
    "dashboard_student.py",
    "dashboard_nurse.py",
    "dashboard_intern.py",
    "dashboard_doctoral.py",
]


def validate_run_calls():
    print("🔍 Vérification des appels à run()...")
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py") and file not in WHITELISTED_FILES:
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = RUN_CALL_PATTERN.findall(content)
                    if len(matches) > 1:
                        print(
                            f"⚠️ {file} contient {
                                len(matches)} appels à run()"
                        )
                    elif matches:
                        print(f"🔎 {file} contient un appel à run()")
    print("✅ Vérification terminée.")


if __name__ == "__main__":
    validate_run_calls()
