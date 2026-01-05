import streamlit as st
from modules.backend.secrets_loader import (
    get_supabase_credentials,
    get_postgres_credentials,
    get_email_credentials,
    get_security_key,
    get_api_service_config,
)

st.set_page_config(page_title="🔐 État des secrets", page_icon="🧿", layout="centered")
st.title("🔐 État des secrets")
st.markdown(
    "Cette page vérifie la présence des clés sacrées dans `.streamlit/secrets.toml`."
)

# 🌿 Supabase
try:
    supabase = get_supabase_credentials()
    st.success(f"✅ Supabase connecté à : `{supabase['url']}`")
    st.info(f"Mode : `{supabase['mode']}`")
except:
    st.error("❌ Supabase non configuré")

# 🗄️ PostgreSQL
try:
    db = get_postgres_credentials()
    st.success(f"✅ PostgreSQL : `{db['url']}`")
except:
    st.error("❌ PostgreSQL non configuré")

# 📧 Email
try:
    email = get_email_credentials()
    st.success(
        f"✅ Email SMTP : `{email['user']}` via `{email['server']}:{email['port']}`"
    )
except:
    st.error("❌ Email SMTP non configuré")

# 🔐 Clé secrète
try:
    secret = get_security_key()
    st.success("✅ Clé secrète chargée")
except:
    st.error("❌ Clé secrète manquante")

# 🌐 API externe
api = get_api_service_config()
if api:
    st.success("✅ API externe configurée")
    st.code(api)
else:
    st.warning("⚠️ Bloc [api_service] absent ou vide")

st.markdown("---")
st.caption(
    "🌸 Cette vérification est un rituel de sécurité avant toute invocation Supabase ou PostgreSQL."
)
