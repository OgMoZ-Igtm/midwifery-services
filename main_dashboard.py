# main_dashboard.py

from modules.config.config_loader import config

import streamlit as st
import importlib
import sys
from datetime import datetime
from modules.router.dashboard_router import FORM_MAP

# 📦 Ajout du chemin racine
sys.path.append("/home/ygd/projets-midwifery-Services")

# 📧 Configuration SMTP (à adapter selon ton projet)


def send_email(to, subject, body):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.smtp_user
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL(config.smtp_server, config.smtp_port) as server:
        server.login(config.smtp_user, config.smtp_password)
        server.send_message(msg)


# 🧭 Configuration de la page
st.set_page_config(page_title="Midwifery Dashboard", layout="wide")
st.title("🧭 Tableau de bord obstétrique")

# 🎭 Sélecteur de rôle
role = st.selectbox(
    "Choisir un rôle",
    [
        "admin",
        "midwife",
        "doctor",
        "patient",
        "nurse",
        "student",
        "intern",
        "doctoral",
        "guest",
    ],
)
st.session_state["role"] = role

# 📄 Sélecteur de formulaire
form_labels = list(FORM_MAP.get(role, {}).keys())
st.sidebar.title("📋 Formulaires disponibles")
st.sidebar.write(f"{len(form_labels)} formulaires pour le rôle **{role}**")

selected_label = st.sidebar.selectbox("🧾 Choisir un formulaire", form_labels)

# 🔄 Chargement dynamique du module
module_path = FORM_MAP[role][selected_label]
try:
    form_module = importlib.import_module(module_path)
    if hasattr(form_module, "render_form"):
        form_module.render_form()
    else:
        st.warning(f"⚠️ Le module `{module_path}` n'a pas de fonction `render_form()`.")
except Exception as e:
    st.error(f"❌ Erreur lors du chargement du module : {e}")

# 📤 Test de messagerie
with st.expander("📧 Envoyer un e-mail de test"):
    to = st.text_input("Destinataire")
    subject = st.text_input("Sujet")
    body = st.text_area("Message")
    if st.button("📤 Envoyer"):
        try:
            send_email(to, subject, body)
            st.success("✅ E-mail envoyé avec succès.")
        except Exception as e:
            st.error(f"❌ Échec de l'envoi : {e}")

# 📋 Logs Supabase (si user_id présent)
if "user_id" in st.session_state:
    # Assure-toi que cette importation est correcte
    # ⚠️ from modules.backend.supabase_client import supabase

    supabase = create_client(...)  # Remplace par ta config Supabase

    def log_action(user_id, action, module):
        supabase.table("logs").insert(
            {
                "user_id": user_id,
                "action": action,
                "module": module,
                "timestamp": datetime.utcnow().isoformat(),
            }
        ).execute()

    logs = (
        supabase.table("logs")
        .select("*")
        .eq("user_id", st.session_state["user_id"])
        .execute()
        .data
    )
    st.subheader("📊 Historique des actions")
    st.dataframe(logs)
