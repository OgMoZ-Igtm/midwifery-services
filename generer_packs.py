import os

# --- DÉFINITION DES PACKS ET PAGES ---
packs = {
    "PATIENT": {
        "01_Patient_Dossier.py": "📁 Dossier Médical",
        "02_Patient_RendezVous.py": "📅 Rendez-vous",
        "03_Patient_CarnetSante.py": "📖 Carnet de Santé",
    },
    "MIDWIFE": {
        "01_Demographics.py": "📋 Informations Démographiques",
        "02_Prenatal_Care.py": "🤰 Suivi Prénatal",
        "03_Intrapartum_Care.py": "🍼 Suivi Intrapartum",
        "04_PostNatal_Care.py": "🌸 Suivi Postnatal",
        "05_Throughout_Midwifery_Care.py": "👩‍🍼 Suivi Continu",
    },
    "DOCTOR": {
        "01_Doctor_Consultation_Requests.py": "📨 Demandes de Consultation",
        "02_Doctor_Diagnosis.py": "🩺 Diagnostic Médical",
        "03_Doctor_History.py": "📜 Historique Patient",
        "04_Doctor_Prescriptions.py": "💊 Prescriptions",
        "05_Doctors_Page.py": "🏥 Tableau de Bord Médecin",
    },
    "NURSE": {
        "01_Infirmiere_Patients.py": "🩹 Soins aux Patients",
        "02_Infirmiere_Medicaments.py": "💉 Administration Médicaments",
    },
    "ADMIN": {
        "01_Admin_Hashing.py": "🔐 Sécurité & Hashing",
        "02_Admin_Logs.py": "📑 Journaux d’Activité",
        "03_Admin_Roles.py": "🎭 Gestion des Rôles",
        "04_Admin_Settings.py": "⚙️ Paramètres",
        "05_Admin_Users.py": "👥 Gestion Utilisateurs",
    },
    "MESSAGES": {
        "01_Chat.py": "💬 Chat",
        "02_Inbox.py": "📥 Boîte de Réception",
        "03_Send_Message.py": "📤 Envoi de Message",
        "04_Receive_Message.py": "📩 Réception de Message",
    },
    "ORGANISATION": {
        "01_Calendar.py": "🗓️ Agenda Collaboratif",
        "02_Complications.py": "⚠️ Suivi Complications",
        "03_Modify_Patient_Folder.py": "✏️ Modifier Dossier Patient",
    },
    "STAGIAIRE": {
        "01_Stage_Journal.py": "📔 Journal de Stage",
        "02_Stage_Evaluations.py": "📝 Évaluations de Stage",
    },
    "ETUDIANTE": {
        "01_Cours_Suivis.py": "📚 Cours Suivis",
        "02_Examens.py": "📝 Examens",
    },
    "DOCTORANTE": {
        "01_Projet_Recherche.py": "🔬 Projet de Recherche",
        "02_Publications.py": "📄 Publications",
        "03_Suivi_These.py": "🎓 Suivi de Thèse",
    },
}


# --- GÉNÉRATION DES FICHIERS ---
def creer_fichier(path, titre):
    """Crée un fichier avec un formulaire Streamlit basique"""
    contenu = f"""import streamlit as st

def app():
    st.title("{titre}")

    with st.form("formulaire"):
        champ1 = st.text_input("Champ texte")
        champ2 = st.text_area("Zone de texte")
        champ3 = st.date_input("Date")
        submit = st.form_submit_button("Enregistrer")

        if submit:
            st.success("✅ Données enregistrées avec succès")
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenu)


def main():
    for pack, fichiers in packs.items():
        dossier = os.path.join("packs", pack)
        os.makedirs(dossier, exist_ok=True)

        for nom_fichier, titre in fichiers.items():
            chemin = os.path.join(dossier, nom_fichier)
            if not os.path.exists(chemin):
                creer_fichier(chemin, titre)
                print(f"✅ Créé : {chemin}")
            else:
                print(f"⏩ Existe déjà : {chemin}")


if __name__ == "__main__":
    main()
