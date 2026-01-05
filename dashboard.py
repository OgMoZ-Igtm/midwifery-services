import streamlit as st
from modules.services.security import get_menu_mapping, est_autorise

# Simuler un rôle et des permissions (à remplacer par ta logique réelle)
role = st.selectbox(
    "Sélectionnez votre rôle", ["admin", "midwife", "student", "patient"]
)
user_permissions = st.multiselect(
    "Permissions utilisateur",
    [
        "READ_AUDIT_LOGS",
        "READ_DASHBOARD",
        "MANAGE_MODULES",
        "READ_RECORD",
        "ACCESS_PHI",
        "SCHEDULE_APT",
        "VIEW_REPORTS",
        "READ_DOCS",
        "ACCESS_LMS",
    ],
)

# Obtenir les packs autorisés
menu_mapping = get_menu_mapping()
packs = menu_mapping.get(role, [])

# Filtrer selon les permissions
accessible_packs = [
    pack for pack in packs if est_autorise(role, pack["id"], user_permissions)
]

# Affichage dynamique des onglets
if accessible_packs:
    tab_labels = [f'{pack["icon"]} {pack["label"]}' for pack in accessible_packs]
    tabs = st.tabs(tab_labels)

    for tab, pack in zip(tabs, accessible_packs):
        with tab:
            st.subheader(f"{pack['label']} ({pack['id']})")
            st.write(
                f"🔐 Permissions requises : {', '.join(pack['permissions']) or 'Aucune'}"
            )
            st.success("✅ Accès autorisé")
else:
    st.error("⛔ Aucun pack accessible avec ce rôle et ces permissions.")
