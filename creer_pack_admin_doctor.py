import os

# 📦 Définition des fichiers par pack
PACKS = {
    "ADMIN": {
        "01_Admin_Logs.py": """import streamlit as st

def app():
    st.title("📊 Suivi des logs")
    st.markdown("Consultez les actions enregistrées dans le système.")
    logs = [
        {"user": "midwife1", "action": "Ajout d’un patient", "time": "2025-08-30 10:21"},
        {"user": "doctor1", "action": "Prescription médicamenteuse", "time": "2025-08-30 10:45"},
    ]
    st.table(logs)
""",
        "02_Admin_Users.py": """import streamlit as st

def app():
    st.title("👥 Gestion des utilisateurs")

    st.subheader("➕ Ajouter un nouvel utilisateur")
    with st.form("ajout_utilisateur"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Adresse email")
        role = st.selectbox("Rôle", ["midwife", "nurse", "doctor", "admin", "patient", "stagiaire", "etudiante", "doctorante"])
        mot_de_passe = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("✅ Ajouter")

        if submit:
            st.success(f"Utilisateur {nom} ({role}) ajouté avec succès !")

    st.subheader("👥 Liste actuelle")
    st.write("admin1 (admin), doctor1 (doctor), patient1 (patient)")
""",
        "03_Admin_Roles.py": """import streamlit as st

def app():
    st.title("🎭 Gestion des rôles")

    roles = ["admin", "doctor", "nurse", "midwife", "patient", "stagiaire", "etudiante", "doctorante"]

    st.subheader("👥 Attribution d’un rôle")
    utilisateur = st.text_input("Nom d’utilisateur")
    role = st.selectbox("Nouveau rôle", roles)
    if st.button("✅ Mettre à jour le rôle"):
        st.success(f"Rôle de {utilisateur} mis à jour en {role}.")
""",
        "04_Admin_Settings.py": """import streamlit as st

def app():
    st.title("⚙️ Paramètres du système")

    st.checkbox("Activer la double authentification (2FA)")
    st.checkbox("Forcer la mise à jour des mots de passe tous les 90 jours")
    st.checkbox("Autoriser l’export CSV des données patients")
    st.button("💾 Sauvegarder les paramètres")
""",
        "05_Admin_Dashboard.py": """import streamlit as st

def app():
    st.title("📈 Tableau de bord administratif")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Utilisateurs actifs", 58)
    col2.metric("🍼 Naissances suivies", 12)
    col3.metric("📩 Messages envoyés", 134)

    st.markdown("### 🔍 Rapports rapides")
    rapport = st.selectbox("Choisir un rapport :", ["Utilisateurs", "Patients", "Logs"])
    if rapport == "Utilisateurs":
        st.write("58 utilisateurs actifs.")
    elif rapport == "Patients":
        st.write("245 patients enregistrés.")
    elif rapport == "Logs":
        st.write("124 actions loguées aujourd’hui.")
""",
    },
    "DOCTOR": {
        "01_Doctor_Consultation_Requests.py": """import streamlit as st

def app():
    st.title("📩 Demandes de consultation")

    patients = ["Alice M.", "John D.", "Marie L."]
    for p in patients:
        if st.button(f"➡️ Consulter {p}"):
            st.success(f"Consultation de {p} ouverte.")
""",
        "02_Doctor_Diagnosis.py": """import streamlit as st

def app():
    st.title("🩺 Diagnostic médical")

    st.text_input("Nom du patient")
    st.date_input("Date de la consultation")
    st.text_area("Observations cliniques")
    st.text_area("Diagnostic final")
    st.button("✅ Enregistrer le diagnostic")
""",
        "03_Doctor_Prescriptions.py": """import streamlit as st

def app():
    st.title("💊 Prescriptions médicales")

    st.text_input("Nom du patient")
    st.text_area("Prescription (médicaments, posologie)")
    st.date_input("Date de prescription")
    if st.button("✅ Enregistrer la prescription"):
        st.success("Prescription enregistrée avec succès.")
""",
        "04_Doctors_Page.py": """import streamlit as st

def app():
    st.title("👨‍⚕️ Tableau de bord médecin")

    st.subheader("📅 Prochains rendez-vous")
    st.write("- 02/09/2025 : Alice M. (Suivi grossesse)")
    st.write("- 05/09/2025 : John D. (Consultation générale)")

    st.subheader("📊 Statistiques rapides")
    col1, col2 = st.columns(2)
    col1.metric("Consultations ce mois", 24)
    col2.metric("Prescriptions délivrées", 18)
""",
    },
}

# 📂 Création des dossiers et fichiers
for pack, fichiers in PACKS.items():
    dossier = os.path.join("packs", pack)
    os.makedirs(dossier, exist_ok=True)

    for fichier, contenu in fichiers.items():
        chemin_fichier = os.path.join(dossier, fichier)
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            f.write(contenu)
        print(f"✅ {chemin_fichier} créé avec succès.")
