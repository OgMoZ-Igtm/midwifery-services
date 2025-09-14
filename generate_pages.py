# Générateur de pages
import os
import streamlit as st
import pandas as pd
import sqlite3

# 📁 Création du dossier de données
os.makedirs("data", exist_ok=True)
import os

# =========================================================
# 🌟 PACKS (Menus Thématiques)
# =========================================================
MENU_PACKS = {
    "patient": {
        "👶 Mon dossier": {
            "📅 Mes rendez-vous": "patient_rdv",
            "📖 Mon carnet de santé": "patient_carnet",
        }
    },
    "doctor": {
        "🩺 Médecins": {
            "👨‍⚕️ Espace Médecins": "doctor_space",
            "🧬 Diagnostic": "doctor_diag",
            "💊 Prescriptions": "doctor_rx",
            "📜 Historique": "doctor_hist",
            "📞 Consultations": "doctor_consult",
        }
    },
    "midwife": {
        "🌸 Sages-femmes": {
            "👩‍🍼 Mes patientes": "midwife_patients",
            "📅 Mes rendez-vous": "midwife_rdv",
            "📝 Saisir consultation": "midwife_consult",
        }
    },
    "nurse": {
        "💉 Infirmières": {
            "👩‍⚕️ Mes patients": "nurse_patients",
            "💊 Médicaments": "nurse_rx",
        }
    },
    "suivi": {
        "👩‍⚕️ Suivi des patientes": {
            "👩‍⚕️ Demographics": "suivi_demo",
            "🤰 Prenatal": "suivi_prenatal",
            "🌸 Intrapartum": "suivi_intra",
            "🍼 Postnatal": "suivi_postnatal",
            "🌿 Throughout": "suivi_global",
        }
    },
    "orga": {
        "📅 Organisation": {
            "📅 Calendar": "orga_cal",
            "📁 Folder": "orga_folder",
            "🧠 Complications": "orga_complications",
        }
    }
}

admin_menu = {
    "admin": {
        "⚙️ Administration": {
            "🔐 Sécurité & Hashage": "admin_hash",
            "👥 Rôles & Permissions": "admin_roles",
            "👤 Gestion Utilisateurs": "admin_users",
            "⚙️ Paramètres": "admin_settings",
            "📜 Historique des connexions": "admin_logs",
        }
    }
}

def run():
    st.title("📝 Consultation sage-femme")

    nom_patiente = st.text_input("Nom de la patiente")
    date_consult = st.date_input("Date de la consultation")
    terme = st.number_input("Terme gestationnel (semaines)", min_value=0, max_value=42)
    tension = st.text_input("Tension artérielle")
    fcf = st.text_input("FCF (bpm)")
    observations = st.text_area("Observations")
    recommandations = st.text_area("Recommandations")

    if st.button("Enregistrer"):
        data = {
            "Nom": nom_patiente,
            "Date": str(date_consult),
            "Terme": terme,
            "Tension": tension,
            "FCF": fcf,
            "Observations": observations,
            "Recommandations": recommandations
        }
        df = pd.DataFrame([data])
        df.to_csv("data/midwife_consult.csv", mode="a", index=False, header=False)

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS midwife_consult (
        Nom TEXT, Date TEXT, Terme INTEGER, Tension TEXT,
        FCF TEXT, Observations TEXT, Recommandations TEXT
    )
""")
def enregistrer_consultation(data, nom_patiente):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS midwife_consult (
            Nom TEXT,
            Date TEXT,
            Terme INTEGER,
            Tension TEXT,
            FCF TEXT,
            Observations TEXT,
            Recommandations TEXT
        )
    """)
    cursor.execute(
        "INSERT INTO midwife_consult VALUES (?, ?, ?, ?, ?, ?, ?)",
        tuple(data.values())
    )
    conn.commit()
    conn.close()

    st.success(f"Consultation enregistrée pour {nom_patiente}")
    """)
    cursor.execute(
        "INSERT INTO midwife_consult VALUES (?, ?, ?, ?, ?, ?, ?)",
        tuple(data.values())
    )
    conn.commit()
    conn.close()

    st.success(f"Consultation enregistrée pour {nom_patiente}")


def run():
    st.title("📖 Carnet de santé de la patiente")

    nom = st.text_input("Nom complet")
    naissance = st.date_input("Date de naissance")
    allergies = st.text_area("Allergies")
    antecedents = st.text_area("Antécédents médicaux")
    suivi = st.text_area("Suivi actuel")

    if st.button("Mettre à jour"):
        data = {
            "Nom": nom,
            "Naissance": str(naissance),
            "Allergies": allergies,
            "Antécédents": antecedents,
            "Suivi": suivi
        }

        df = pd.DataFrame([data])
        df.to_csv("data/patient_carnet.csv", mode="a", index=False, header=False)

def enregistrer_carnet(data):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

if st.button("Mettre à jour"):
    data = {
        "Nom": nom,
        "Naissance": str(naissance),
        "Allergies": allergies,
        "Antécédents": antecedents,
        "Suivi": suivi
    }

    df = pd.DataFrame([data])
    df.to_csv("data/patient_carnet.csv", mode="a", index=False, header=False)

create_table_sql = """
    CREATE TABLE IF NOT EXISTS patient_carnet (
        Nom TEXT,
        Naissance TEXT,
        Allergies TEXT,
        Antécédents TEXT,
        Suivi TEXT
    )
"""

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute(create_table_sql)
cursor.execute(
    "INSERT INTO patient_carnet VALUES (?, ?, ?, ?, ?)",
    tuple(data.values())
)
conn.commit()
conn.close()

st.success("Carnet mis à jour ✅")