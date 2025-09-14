import streamlit as st
import sqlite3
from datetime import datetime

# Connexion à la base SQLite
conn = sqlite3.connect("consultations.db", check_same_thread=False)
cursor = conn.cursor()

# Initialisation de la table si elle n'existe pas
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
conn.commit()

# Configuration de la page
st.set_page_config(
    page_title="Demande de consultation", page_icon="📝", layout="centered"
)
st.title("📝 Formulaire de demande de consultation")

st.info("Veuillez remplir ce formulaire pour soumettre votre demande au médecin.")

with st.form("formulaire_patient"):
    nom = st.text_input("Votre nom complet")
    motif = st.text_area(
        "Motif de la consultation", placeholder="Décrivez brièvement votre situation..."
    )
    priorite = st.selectbox("Niveau de priorité", ["Normal", "Urgent"])
    confirmer = st.checkbox("Je confirme que les informations sont exactes.")
    envoyer = st.form_submit_button("📨 Envoyer la demande", disabled=not confirmer)

if envoyer:
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    request_id = (
        f"req_{int(datetime.now().timestamp())}"  # ID unique basé sur le timestamp
    )

    cursor.execute(
        "INSERT INTO demandes VALUES (?, ?, ?, ?, ?, ?)",
        (request_id, nom, motif, date_now, "En attente", priorite),
    )
    conn.commit()

    st.success("✅ Votre demande a été envoyée avec succès !")
    st.info("Un médecin vous répondra dans les plus brefs délais.")
