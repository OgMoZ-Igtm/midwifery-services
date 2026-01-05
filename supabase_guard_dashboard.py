import streamlit as st
import os

REPORT_FILE = "inject_supabase_guard_report.txt"


def load_report():
    if not os.path.exists(REPORT_FILE):
        return []
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip().startswith("🌿")]


ROLE_ICONS = {
    "midwife": "🧑‍🍼",
    "doctor": "🩺",
    "intern": "📘",
    "student": "🎓",
    "guest": "🪶",
    "patient": "🫂",
    "nurse": "🧑‍⚕️",
    "admin": "🛡️",
    "shared": "🔗",
    "utils": "🧰",
    "backend": "🧠",
    "services": "🧭",
    "tools": "🛠️",
}


def detect_role(path):
    for role in ROLE_ICONS:
        if f"/{role}_" in path or f"/{role}/" in path:
            return role
    return "shared"


def display_dashboard(files):
    st.title("🧿 Supabase Guard Dashboard")
    st.markdown("Tous les fichiers protégés contre Supabase désactivé.")

    roles = sorted(set(detect_role(f) for f in files))
    selected_roles = st.multiselect("🎭 Filtrer par rôle :", roles, default=roles)

    st.markdown(f"🔢 Total : **{len(files)}** fichiers protégés")

    for path in files:
        role = detect_role(path)
        if role in selected_roles:
            icon = ROLE_ICONS.get(role, "📄")
            st.markdown(f"{icon} `{path}`")


files = load_report()
if files:
    display_dashboard(files)
else:
    st.warning("Aucun rapport trouvé. Lancez d'abord le script d'injection.")
