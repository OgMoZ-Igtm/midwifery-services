import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import logging
import streamlit_authenticator as stauth

# --- Logging ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Authentification ---
credentials = {
    "usernames": {
        "dr_alice": {
            "email": "dr.alice@example.com",
            "name": "Docteur Alice",
            "password": "$2b$12$Kj.wE.6o.c.Lp.8xZ.JtUuY.0O/N/wE.x.JtUuY.0O/N/wE",  # 'alice_123'
        },
        "dr_bob": {
            "email": "dr.bob@example.com",
            "name": "Docteur Bob",
            "password": "$2b$12$R.u.tA.d.J.C.c.D.w.e.Q.p.r.W.y.z.A.a.b.c.d.e",  # 'bob_123'
        },
    }
}

authenticator = stauth.Authenticate(
    credentials, "consult_cookie", "abcdef", cookie_expiry_days=30
)

# --- Connexion à la base SQLite ---
conn = sqlite3.connect("consultations.db", check_same_thread=False)
cursor = conn.cursor()

# --- Initialisation de la base ---
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS demandes (
    id TEXT PRIMARY KEY,
    patient TEXT,
    motif TEXT,
    date_demande TEXT,
    statut TEXT,
    priorite TEXT
)
"""
)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS reponses (
    id TEXT,
    medecin TEXT,
    action TEXT,
    commentaire TEXT,
    date_reponse TEXT
)
"""
)
conn.commit()

# --- Données de démonstration (si vide) ---
cursor.execute("SELECT COUNT(*) FROM demandes")
if cursor.fetchone()[0] == 0:
    demo_data = [
        (
            "req_001",
            "Alice M.",
            "Douleur abdominale sévère, demande urgente",
            "2023-10-25 10:30",
            "En attente",
            "Urgent",
        ),
        (
            "req_002",
            "John D.",
            "Suivi de diabète gestationnel",
            "2023-10-24 15:00",
            "En attente",
            "Normal",
        ),
        (
            "req_003",
            "Marie L.",
            "Questions sur le plan de naissance",
            "2023-10-23 09:15",
            "En attente",
            "Normal",
        ),
        (
            "req_004",
            "Luc F.",
            "Consultation pré-natale de routine",
            "2023-10-25 11:45",
            "En attente",
            "Normal",
        ),
        (
            "req_005",
            "Sophie R.",
            "Problèmes de lactation",
            "2023-10-25 08:00",
            "En attente",
            "Urgent",
        ),
    ]
    cursor.executemany("INSERT INTO demandes VALUES (?, ?, ?, ?, ?, ?)", demo_data)
    conn.commit()

# --- Authentification ---
login_result = authenticator.login("Connexion")
if login_result:
    name, authentication_status, username = login_result

    if authentication_status:
        authenticator.logout("🔓 Déconnexion", "main")
        st.write(f"👩‍⚕️ Bienvenue *{name}*")

        st.set_page_config(page_title="Consultations", page_icon="📩", layout="wide")
        st.title("📩 Gestion des consultations")

        # --- Chargement des demandes ---
        df = pd.read_sql_query("SELECT * FROM demandes WHERE statut='En attente'", conn)
        df["date_demande"] = pd.to_datetime(df["date_demande"])
        sorted_df = df.sort_values(
            by=["priorite", "date_demande"], ascending=[False, True]
        )

        st.subheader("Demandes en attente")
        st.dataframe(sorted_df.set_index("id"), width="stretch")

        st.markdown("---")
        st.subheader("Répondre à une demande")

        col1, col2 = st.columns([3, 1])
        with col1:
            request_id = st.selectbox(
                "Sélectionner une demande",
                sorted_df["id"].tolist(),
                format_func=lambda x: f"{x} - {sorted_df[sorted_df['id'] == x]['patient'].iloc[0]}",
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📁 Voir le dossier patient"):
                patient_name = sorted_df[sorted_df["id"] == request_id]["patient"].iloc[
                    0
                ]
                st.info(f"Ouverture du dossier de {patient_name}")
                logging.info(f"{username} a consulté le dossier de {request_id}")

        with st.form("consultation_response_form"):
            action = st.radio(
                "Action",
                [
                    "Planifier un rendez-vous",
                    "Répondre par message",
                    "Marquer comme résolu",
                ],
            )

            if action == "Planifier un rendez-vous":
                st.markdown("#### Créneaux disponibles")
                today = datetime.now()
                dates = [today + timedelta(days=i) for i in range(7)]
                selected_date = st.selectbox(
                    "Date", dates, format_func=lambda x: x.strftime("%d-%m-%Y")
                )
                selected_time = st.selectbox(
                    "Heure", ["9h00", "10h30", "14h00", "15h30"]
                )

            commentaire = st.text_area(
                "Commentaire", placeholder="Détails de la réponse..."
            )
            confirm = st.checkbox("Je confirme que la réponse est complète.")
            submit = st.form_submit_button("✅ Envoyer", disabled=not confirm)

        if submit:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO reponses VALUES (?, ?, ?, ?, ?)",
                (request_id, username, action, commentaire, now),
            )
            cursor.execute(
                "UPDATE demandes SET statut='Traité' WHERE id=?", (request_id,)
            )
            conn.commit()

            st.success(f"Réponse envoyée pour {request_id}")
            st.balloons()

            # --- Simulation d'envoi d'email ---
            patient = sorted_df[sorted_df["id"] == request_id]["patient"].iloc[0]
            st.info(f"📬 Email envoyé à {patient} pour l'action : {action}")

        # --- Tableau de bord ---
        st.markdown("---")
        st.subheader("📊 Statistiques")

        stats = pd.read_sql_query(
            "SELECT statut, COUNT(*) as total FROM demandes GROUP BY statut", conn
        )
        st.bar_chart(stats.set_index("statut"))

    elif authentication_status is False:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")
    elif authentication_status is None:
        st.warning("Veuillez entrer vos identifiants.")
else:
    st.error("Erreur : impossible de charger le formulaire de connexion.")
