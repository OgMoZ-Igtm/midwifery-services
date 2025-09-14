# modules/packs/admin.py
import streamlit as st
import json
import os
import importlib.util

# Assurez-vous d'importer les fonctions de sécurité nécessaires
# ou de les définir directement dans ce fichier
from utils.security import log_audit_event
from utils.admin_utils import (
    delete_page_from_pack,
)  # Assurez-vous que ce fichier existe


def render():
    """
    Rend l'interface utilisateur d'administration pour la gestion des pages.
    """
    st.header("Administration du système")
    st.markdown("---")

    # Vérification des autorisations : seule le rôle ADMIN peut accéder à cette page
    if st.session_state.get("role") != "ADMIN":
        st.error("❌ Accès refusé. Cette page est réservée aux administrateurs.")
        log_audit_event(
            st.session_state.get("full_name", "Inconnu"),
            "Unauthorized Access Attempt",
            "Attempted to access admin page.",
        )
        return

    st.info(
        "Utilisez cette interface pour gérer les packs et les pages de l'application."
    )

    # Charger la configuration du menu
    menu_mapping = st.session_state.get("MENU_MAPPING", {})
    packs_with_pages = [p for p, pages in menu_mapping.items() if pages]

    # Sélecteur de packs
    selected_pack = st.selectbox("Sélectionnez le pack :", options=packs_with_pages)

    if selected_pack:
        # Sélecteur de pages à l'intérieur du pack
        pages_in_pack = menu_mapping.get(selected_pack, [])
        page_names = {page["name"]: page for page in pages_in_pack}
        selected_page_name = st.selectbox(
            "Sélectionnez la page à gérer :", options=list(page_names.keys())
        )

        if selected_page_name:
            selected_page = page_names[selected_page_name]
            st.markdown("---")
            st.subheader("Détails de la page")
            st.write(f"**Nom de la page :** {selected_page['name']}")
            st.write(f"**Identifiant :** {selected_page['id']}")
            st.write(f"**Fichier :** `{selected_page['file']}`")

            st.markdown("---")

            # Bouton de suppression avec confirmation
            st.warning(
                "⚠️ **Attention :** Cette action est irréversible et supprimera le fichier de la page."
            )

            if st.button("Supprimer la page", key="delete_page_btn"):
                # Appeler la fonction de suppression sécurisée
                delete_page_from_pack(selected_pack, selected_page["id"])

                # Log de l'action pour la traçabilité
                log_audit_event(
                    st.session_state.get("full_name", "Inconnu"),
                    "Admin Action",
                    f"Initiated deletion of page '{selected_page['name']}' from pack '{selected_pack}'.",
                )
