import os

# Packs et fichiers associés avec champs spécifiques
packs = {
    "patient": {
        "Patient_Dossier.py": [
            ("Nom complet", "text"),
            ("Date de naissance", "date"),
            ("Adresse", "text"),
        ],
        "Patient_RendezVous.py": [
            ("Date du rendez-vous", "date"),
            ("Heure", "time"),
            ("Motif de consultation", "text"),
        ],
        "Patient_CarnetSante.py": [
            ("Vaccins reçus", "text"),
            ("Allergies", "text"),
            ("Antécédents médicaux", "text"),
        ],
    },
    "admin": {
        "Admin_Logs.py": [("Filtrer par date", "date")],
        "Admin_Roles.py": [
            ("Nom d’utilisateur", "text"),
            (
                "Rôle attribué",
                "select",
                ["admin", "doctor", "midwife", "nurse", "patient"],
            ),
        ],
        "Admin_Users.py": [
            ("Nom complet", "text"),
            ("Email", "text"),
            ("Rôle", "select", ["admin", "doctor", "midwife", "nurse", "patient"]),
        ],
        "Admin_Settings.py": [("Paramètre clé", "text"), ("Valeur", "text")],
    },
    "midwife": {
        "3_Demographics.py": [
            ("Âge", "number"),
            ("Ethnie", "text"),
            ("Statut marital", "select", ["Célibataire", "Mariée", "Veuve", "Autre"]),
        ],
        "4_Prenatal_Care.py": [
            ("Âge gestationnel (semaines)", "number"),
            ("Poids de la mère (kg)", "number"),
            ("Pression artérielle", "text"),
        ],
        "5_Intrapartum_Care.py": [
            ("Durée du travail (heures)", "number"),
            ("Mode d’accouchement", "select", ["Vaginal", "Césarienne"]),
            ("Complications", "text"),
        ],
        "6_Post_Natal_Care.py": [
            ("Allaitement", "select", ["Oui", "Non"]),
            ("État de santé du bébé", "text"),
            ("Dépression post-partum", "select", ["Oui", "Non"]),
        ],
        "7_Throughout_Midwifery_Care.py": [
            ("Nombre total de visites", "number"),
            ("Notes générales", "text"),
        ],
    },
    "doctor": {
        "Doctors_Page.py": [
            ("Nom du patient", "text"),
            ("Observation générale", "text"),
        ],
        "Doctor_Diagnosis.py": [("Diagnostic", "text"), ("Recommandations", "text")],
        "31_Doctor_Prescriptions.py": [
            ("Nom du médicament", "text"),
            ("Dosage", "text"),
            ("Durée (jours)", "number"),
        ],
        "Doctor_History.py": [
            ("Nom du patient", "text"),
            ("Antécédents médicaux", "text"),
        ],
        "Doctor_Consultation_Requests.py": [
            ("Patient concerné", "text"),
            ("Raison de la consultation", "text"),
        ],
    },
    "nurse": {
        "Infirmiere_Patients.py": [
            ("Nom du patient", "text"),
            ("Température (°C)", "number"),
            ("Tension artérielle", "text"),
        ],
        "Infirmiere_Medicaments.py": [
            ("Médicament administré", "text"),
            ("Dosage", "text"),
            ("Heure", "time"),
        ],
    },
    "organisation": {
        "13_Appointments_Calendar.py": [
            ("Date", "date"),
            ("Heure", "time"),
            ("Patient", "text"),
        ],
        "45_Modify_Patient_Folder.py": [
            ("ID du dossier", "text"),
            ("Champs à modifier", "text"),
            ("Nouvelle valeur", "text"),
        ],
    },
    "messages": {
        "Inbox.py": [],
        "Chat.py": [("Destinataire", "text"), ("Message", "text")],
        "Send_Message.py": [
            ("Destinataire", "text"),
            ("Objet", "text"),
            ("Message", "text"),
        ],
        "Receive_Message.py": [],
    },
}


# Génération du code avec champs spécifiques
def generate_code(filename, pack, fields):
    form_id = filename.replace(".py", "").lower()
    fields_code = ""
    process_code = (
        "submitted = st.form_submit_button('✅ Enregistrer')\n\n        if submitted:\n"
    )
    process_code += "            st.success('✅ Données enregistrées avec succès !')\n"

    for i, (label, ftype, *options) in enumerate(fields):
        var = f"champ{i+1}"
        if ftype == "text":
            fields_code += f'        {var} = st.text_input("{label}")\n'
        elif ftype == "number":
            fields_code += (
                f'        {var} = st.number_input("{label}", min_value=0, step=1)\n'
            )
        elif ftype == "date":
            fields_code += f'        {var} = st.date_input("{label}")\n'
        elif ftype == "time":
            fields_code += f'        {var} = st.time_input("{label}")\n'
        elif ftype == "select":
            opts = options[0]
            fields_code += f'        {var} = st.selectbox("{label}", {opts})\n'

    return f"""import streamlit as st
from utils.navigation import navigation_controls

# =========================================================
# 📄 {filename}
# ---------------------------------------------------------
# 🎯 Objectif :
#   Page de collecte pour {filename} dans le pack {pack}.
# =========================================================

def app():
    st.title("📄 {filename}")

    st.markdown("Veuillez remplir les informations ci-dessous.")

    # 📝 Formulaire spécifique
    with st.form("form_{form_id}"):
{fields_code}
{process_code}

    # 🔄 Navigation
    navigation_controls("{filename}")

if __name__ == "__main__":
    app()
"""


# Création des fichiers
for pack, files in packs.items():
    os.makedirs(f"packs/{pack}", exist_ok=True)
    for f, fields in files.items():
        path = f"packs/{pack}/{f}"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.write(generate_code(f, pack, fields))
            print(f"✅ {f} créé dans packs/{pack}")
        else:
            print(f"⚠️ {f} existe déjà, ignoré")
