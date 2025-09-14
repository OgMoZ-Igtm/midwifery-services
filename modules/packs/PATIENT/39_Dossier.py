# BANNER_INJECTED
import streamlit as st
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire complet pour le dossier médical
    d'une patiente, permettant la saisie d'informations détaillées.
    """
    st.title("🗂️ Dossier Médical du Patient")
    st.info(
        "Utilisez ce formulaire pour créer ou mettre à jour un dossier médical complet."
    )

    with st.form("dossier_patient_form"):
        st.subheader("Informations de base")

        col1, col2 = st.columns(2)
        with col1:
            nom_complet = st.text_input(
                "Nom et prénom de la patiente", placeholder="Ex: Mme Lucie Martin"
            )
            date_naissance = st.date_input(
                "📅 Date de naissance", max_value=date.today()
            )
        with col2:
            numero_dossier = st.text_input(
                "Numéro de dossier", placeholder="Ex: 123456"
            )
            groupe_sanguin = st.selectbox(
                "Groupe sanguin",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Inconnu"],
            )

        st.markdown("---")

        st.subheader("Informations de contact et d'urgence")

        col3, col4 = st.columns(2)
        with col3:
            telephone = st.text_input(
                "Numéro de téléphone", placeholder="Ex: +33 6 12 34 56 78"
            )
            adresse = st.text_area(
                "Adresse complète", placeholder="Ex: 12 Rue de la Paix, 75000 Paris"
            )
        with col4:
            nom_contact_urgence = st.text_input(
                "Nom du contact d'urgence", placeholder="Ex: Marc Martin"
            )
            relation_contact = st.text_input(
                "Relation avec la patiente", placeholder="Ex: Époux, frère, ami(e)..."
            )
            telephone_contact = st.text_input(
                "Téléphone du contact d'urgence", placeholder="Ex: +33 6 98 76 54 32"
            )

        st.markdown("---")

        st.subheader("Antécédents médicaux")

        allergies = st.text_area(
            "Allergies", placeholder="Ex: Pénicilline, arachides..."
        )
        antecedents_medicaux = st.text_area(
            "Antécédents médicaux pertinents",
            placeholder="Ex: Diabète, hypertension, chirurgies antérieures...",
        )

        st.markdown("---")

        st.subheader("Historique des grossesses (Obstétrique)")

        col5, col6 = st.columns(2)
        with col5:
            gravida = st.number_input(
                "Nombre de grossesses (Gravida)", min_value=0, step=1
            )
            date_derniere_regle = st.date_input(
                "Date des dernières règles (DDR)", max_value=date.today()
            )
        with col6:
            parite = st.number_input(
                "Nombre de naissances (Parité)", min_value=0, step=1
            )
            nombre_cesariennes = st.number_input(
                "Nombre de césariennes", min_value=0, step=1
            )

        notes_grossesse = st.text_area(
            "Notes sur les grossesses précédentes",
            placeholder="Complications, accouchements particuliers...",
        )

        st.markdown("---")

        st.subheader("Saisie de documents")

        uploaded_files = st.file_uploader(
            "📥 Ajouter des documents (échographies, rapports, etc.)",
            accept_multiple_files=True,
        )
        if uploaded_files:
            st.success(
                f"{len(uploaded_files)} fichier(s) prêt(s) à être enregistré(s)."
            )

        submit = st.form_submit_button("✅ Enregistrer le dossier")

        if submit:
            if nom_complet and numero_dossier:
                st.success(
                    f"✅ Dossier pour {nom_complet} a été sauvegardé avec succès!"
                )
                st.balloons()
            else:
                st.error(
                    "❌ Veuillez remplir les champs obligatoires : Nom et prénom, et Numéro de dossier."
                )


if __name__ == "__main__":
    render()
