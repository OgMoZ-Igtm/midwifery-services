# BANNER_INJECTED
import streamlit as st
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour un carnet de santé,
    permettant un suivi médical complet du patient.
    """
    st.title("📖 Carnet de Santé du Patient")
    st.info(
        "Utilisez ce formulaire pour enregistrer les informations médicales et le suivi d'un patient."
    )

    with st.form("carnet_sante_form"):
        st.subheader("Informations de base")

        col1, col2 = st.columns(2)
        with col1:
            nom_patient = st.text_input(
                "Nom de la patiente", placeholder="Ex: Mme Dubois"
            )
            date_naissance = st.date_input("Date de naissance", max_value=date.today())
        with col2:
            numero_dossier = st.text_input(
                "Numéro de dossier", placeholder="Ex: 123456"
            )
            groupe_sanguin = st.selectbox(
                "Groupe sanguin",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Inconnu"],
            )

        st.markdown("---")

        st.subheader("Mesures vitales et morphologiques")

        col3, col4, col5 = st.columns(3)
        with col3:
            poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
            pression_arterielle = st.text_input(
                "Pression artérielle", placeholder="Ex: 120/80"
            )
        with col4:
            taille = st.number_input("Taille (cm)", min_value=0.0, step=0.1)
            temperature = st.number_input(
                "Température (°C)", min_value=35.0, max_value=42.0, step=0.1
            )
        with col5:
            bmi = st.number_input(
                "IMC (BMI)",
                min_value=0.0,
                step=0.1,
                disabled=True,
                help="Calculé automatiquement",
            )
            frequence_cardiaque = st.text_input(
                "Fréquence cardiaque (bpm)", placeholder="Ex: 75"
            )

        st.markdown("---")

        st.subheader("Antécédents médicaux")

        allergies = st.text_area(
            "Allergies", placeholder="Ex: Pénicilline, arachides..."
        )
        antecedents = st.text_area(
            "Antécédents médicaux pertinents",
            placeholder="Ex: Diabète, hypertension, chirurgies antérieures...",
        )

        st.markdown("---")

        st.subheader("Notes médicales")

        notes_medicales = st.text_area(
            "Notes de consultation",
            placeholder="Détails de la consultation, observations, diagnostic, plan de traitement...",
        )

        submit = st.form_submit_button("✅ Enregistrer")

        if submit:
            if nom_patient and numero_dossier:
                st.success("✅ Données enregistrées avec succès !")
                st.balloons()
            else:
                st.error(
                    "❌ Veuillez remplir les champs obligatoires (Nom de la patiente et Numéro de dossier)."
                )


if __name__ == "__main__":
    render()
