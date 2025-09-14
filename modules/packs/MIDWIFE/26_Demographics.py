# BANNER_INJECTED
import streamlit as st
import re
from datetime import date, timedelta

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour les données
    démographiques d'une patiente enceinte, avec des ajouts cruciaux de sécurité et d'ergonomie.
    """
    st.set_page_config(
        page_title="Données démographiques", page_icon="🧑‍🤰", layout="wide"
    )

    st.title("🧑‍🤰 Données démographiques de la patiente")
    st.info(
        "Ce formulaire permet de saisir les informations personnelles de la femme enceinte de manière sécurisée et structurée."
    )

    with st.form(key="demo_midwife"):

        # --- Section 1: Informations d'identification ---
        st.subheader("1. Identification de la patiente")
        col1_id, col2_id = st.columns(2)
        with col1_id:
            patient_id = st.text_input(
                "🆔 ID unique de la patiente", help="Ex: PAT-2023-001"
            )
            last_name = st.text_input("Nom de famille", placeholder="Ex: DOE")
        with col2_id:
            st.date_input("Date d'enregistrement", value=date.today())
            first_name = st.text_input("Prénom", placeholder="Ex: Jane")

        st.markdown("---")

        # --- Section 2: Informations de contact et de base ---
        st.subheader("2. Contacts et informations de base")
        col1_contact, col2_contact = st.columns(2)
        with col1_contact:
            email = st.text_input(
                "📧 Adresse e-mail", placeholder="jane.doe@example.com"
            )
            phone = st.text_input(
                "📱 Numéro de téléphone", placeholder="Ex: 0123456789"
            )

        with col2_contact:
            date_of_birth = st.date_input("Date de naissance", max_value=date.today())
            age = (date.today() - date_of_birth).days // 365
            st.write(f"Âge : **{age} ans**")

        st.text_area(
            "Adresse complète",
            placeholder="123 rue des Lilas, 75001 Paris",
            help="Veuillez inclure la rue, le code postal et la ville.",
        )

        st.markdown("---")

        # --- Section 3: Informations médicales et obstétricales ---
        st.subheader("3. Historique médical et obstétrical")
        col_obs1, col_obs2, col_obs3 = st.columns(3)
        with col_obs1:
            st.markdown("**Historique de la grossesse actuelle**")
            last_period_date = st.date_input("Date des dernières règles (DDR)")
            # Calcul de la DPA (Date Prévue d'Accouchement) via la méthode de Naegele
            dpa = last_period_date + timedelta(days=280)
            st.write(
                f"Date prévue d'accouchement (DPA) : **{dpa.strftime('%d-%m-%Y')}**"
            )

        with col_obs2:
            st.markdown("**Notation GTPAL**")
            # GTPAL : Gravida, Term, Preterm, Abortion, Living
            gravida = st.number_input(
                "🤰 Grossesses (Gravida)",
                min_value=0,
                step=1,
                help="Nombre total de grossesses, y compris la grossesse actuelle.",
            )
            term = st.number_input("🍼 Naissances à terme", min_value=0, step=1)
        with col_obs3:
            st.markdown(" ")  # Espace pour l'alignement
            preterm = st.number_input("👶 Naissances prématurées", min_value=0, step=1)
            abortion = st.number_input(
                "🚫 Fausses couches/Avortements", min_value=0, step=1
            )
            living = st.number_input("👨‍👩‍👧 Enfants vivants", min_value=0, step=1)

        st.text_area(
            "📝 Antécédents médicaux pertinents",
            placeholder="Diabète, Hypertension, Césarienne antérieure, etc.",
            help="Saisissez les antécédents médicaux et chirurgicaux importants.",
        )

        st.markdown("---")

        # --- Section 4: Consentement et urgences ---
        st.subheader("4. Consentement et Contact d'urgence")

        st.text_input("Nom du contact d'urgence", placeholder="Ex: Jean Dupont")
        st.text_input("Téléphone du contact d'urgence", placeholder="Ex: 0987654321")

        consent = st.checkbox(
            "✅ J'atteste que la patiente a donné son consentement pour la collecte de ces données."
        )

        # Bouton de soumission
        submit_button = st.form_submit_button("✅ Enregistrer les données")

    if submit_button:
        # Validation des champs obligatoires
        if not patient_id or not last_name or not first_name or not consent:
            st.error(
                "❌ Les champs 'ID', 'Nom', 'Prénom' et le consentement sont obligatoires."
            )
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("❌ Le format de l'adresse e-mail est invalide.")
        else:
            # Ici, le code pour sauvegarder les données dans une base de données sécurisée
            st.success("✅ Données démographiques enregistrées avec succès!")
            st.balloons()


if __name__ == "__main__":
    render()
