import os
import shutil

# 📦 Définition des packs et des fichiers correspondants
PACKS = {
    "patient": [
        "Patient_Dossier.py",
        "Patient_RendezVous.py",
        "Patient_CarnetSante.py",
    ],
    "admin": [
        "Admin_Logs.py",
        "Admin_Roles.py",
        "Admin_Users.py",
        "Admin_Settings.py",
    ],
    "midwife": [
        "3_Demographics.py",
        "4_Prenatal_Care.py",
        "5_Intrapartum_Care.py",
        "6_Post_Natal_Care.py",
        "7_Throughout_Midwifery_Care.py",
    ],
    "doctor": [
        "Doctors_Page.py",
        "Doctor_Diagnosis.py",
        "31_Doctor_Prescriptions.py",
        "Doctor_History.py",
        "Doctor_Consultation_Requests.py",
    ],
    "nurse": [
        "Infirmiere_Patients.py",
        "Infirmiere_Medicaments.py",
    ],
    "organisation": [
        "13_Appointments_Calendar.py",
        "45_Modify_Patient_Folder.py",
    ],
    "messages": [
        "Inbox.py",
        "Chat.py",
        "Send_Message.py",
        "Receive_Message.py",
    ],
}

# 📂 Répertoire source où sont stockés tes fichiers actuellement
SOURCE_DIR = "modules"

# 📂 Répertoire de destination (packs organisés)
DEST_DIR = "packs"

# 📄 Fichier modules.py généré
MODULES_FILE = "modules.py"


def organiser_packs():
    """Déplace les fichiers dans leurs répertoires de pack"""
    os.makedirs(DEST_DIR, exist_ok=True)

    for pack, fichiers in PACKS.items():
        pack_dir = os.path.join(DEST_DIR, pack)
        os.makedirs(pack_dir, exist_ok=True)

        for fichier in fichiers:
            src_path = os.path.join(SOURCE_DIR, fichier)
            dest_path = os.path.join(pack_dir, fichier)

            if os.path.exists(src_path):
                shutil.move(src_path, dest_path)
                print(f"✅ {fichier} → {pack_dir}")
            else:
                print(f"⚠️ {fichier} introuvable dans {SOURCE_DIR}")


def generer_modules_py():
    """Génère un fichier central modules.py qui importe toutes les pages des packs"""
    with open(MODULES_FILE, "w", encoding="utf-8") as f:
        f.write("# =========================================================\n")
        f.write("# 📦 Modules centralisés - Généré automatiquement\n")
        f.write("# =========================================================\n\n")

        for pack in PACKS:
            f.write(f"# --------- Pack {pack.capitalize()} ---------\n")
            for fichier in PACKS[pack]:
                module_name = fichier.replace(".py", "")
                f.write(f"from packs.{pack}.{module_name} import *\n")
            f.write("\n")

    print(f"\n🎉 Fichier {MODULES_FILE} généré avec succès.")


if __name__ == "__main__":
    organiser_packs()
    generer_modules_py()
