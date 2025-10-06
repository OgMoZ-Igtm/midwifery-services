# modules/services/config.py

ROLES = [
    "admin",
    "midwife",
    "doctor",
    "nurse",
    "patient",
    "student",
    "intern",
    "doctoral",
    "guest",
]
DEFAULT_VIEW = "🏠 Tableau de bord"

import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
