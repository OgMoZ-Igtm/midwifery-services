# Fichier modules/forms_admin/form_dashboard_multiple.py (Correction hypothétique de l'indentation)

import streamlit as st
import pandas as pd

# S'assurer que le reste du code est correctement indenté,
# en particulier autour de la ligne 33 où l'erreur a été signalée.


def render_form(supabase_client, user_info, app_settings):
    st.title("Tableau de bord multi-formulaires d'administration")
    st.markdown("---")

    # Initialisation des états si nécessaire
    if "selected_form" not in st.session_state:
        st.session_state.selected_form = None

    # Récupérer la liste des formulaires pertinents pour l'affichage
    # Note: Ceci dépend de la structure de votre `form_registry`
    admin_forms = {
        k: v
        for k, v in app_settings["LINKED_FORMS_EXTENDED"].items()
        if v.get("role") == "ADMIN" and k != "form_dashboard_multiple"
    }

    form_options = {v["title"]: k for k, v in admin_forms.items()}

    # Sélection du formulaire
    selected_title = st.selectbox(
        "Sélectionner le formulaire à afficher",
        list(form_options.keys()),
        index=0 if list(form_options.keys()) else None,
    )

    if selected_title:
        selected_form_key = form_options[selected_title]
        st.session_state.selected_form = selected_form_key

        # Affichage des données (exemple de structure)
        st.subheader(f"Données du formulaire : {selected_title}")

        try:
            # Remplacement par une fonction de récupération de données générique
            # Vous devrez adapter cette partie pour votre client Supabase réel
            data, count = supabase_client.fetch_all_data(selected_form_key)

            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("Aucune donnée trouvée pour ce formulaire.")

        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")
            st.warning(
                "Assurez-vous que la fonction de récupération des données dans `supabase_client` est correcte."
            )


def validate_form(data):
    # Ce tableau de bord n'a généralement pas de validation car il n'enregistre pas
    return True
