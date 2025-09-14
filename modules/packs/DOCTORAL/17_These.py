# BANNER_INJECTED
import streamlit as st
from datetime import date
import uuid  # To generate a unique ID


if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    This Streamlit application serves as a secure and compliant form for the
    submission of a doctoral thesis.
    """
    st.set_page_config(page_title="Soumission de Thèse", page_icon="📄", layout="wide")
    st.title("📄 Soumission de Thèse de Doctorat")
    st.info(
        "Utilisez ce formulaire pour enregistrer les informations clés de votre thèse de doctorat. Les informations soumises ici seront utilisées pour l'archivage et la documentation officielle."
    )

    # Simule l'utilisateur connecté et génère un ID de thèse
    logged_in_user = "Jane Doe"
    thesis_id = str(uuid.uuid4())

    with st.form("these_complete_form"):
        # --- Section : Informations générales (avec validation) ---
        st.subheader("1. Informations de base")
        st.info(
            f"Soumission par : **{logged_in_user}** | ID de thèse : **{thesis_id[:8]}**"
        )

        col1, col2 = st.columns(2)
        with col1:
            titre_these = st.text_input(
                "Titre de la thèse",
                placeholder="Ex: L'impact de l'allaitement sur le développement néonatal",
            )
            director_name = st.text_input(
                "Nom du directeur de thèse", placeholder="Ex: Dr. Martin Dubois"
            )
        with col2:
            st.write("Date de soumission : **", date.today().strftime("%Y-%m-%d"), "**")
            date_soutenance = st.date_input("Date de soutenance", value=date.today())

        domaine_recherche = st.selectbox(
            "Domaine de recherche",
            ["Obstétrique", "Santé maternelle", "Pédiatrie", "Épidémiologie", "Autre"],
        )

        st.markdown("---")

        # --- Section : Résumé et Mots-clés ---
        st.subheader("2. Résumé et Mots-clés")

        resume = st.text_area(
            "Résumé (Abstract)",
            placeholder="Collez ici le résumé complet de votre thèse.",
            height=150,
        )
        mots_cles = st.text_input(
            "Mots-clés",
            placeholder="Ex: accouchement, post-partum, diabète gestationnel",
            help="Séparez les mots-clés par des virgules.",
        )

        st.markdown("---")

        # --- Section : Conformité et sécurité ---
        st.subheader("3. Conformité et sécurité")
        st.info(
            "Cette section est cruciale pour la validité académique et éthique de votre thèse."
        )

        col_ethique, col_conflit = st.columns(2)
        with col_ethique:
            irb_approval = st.checkbox(
                "La recherche a-t-elle une approbation éthique (IRB/CÉR)?"
            )
            if irb_approval:
                irb_number = st.text_input(
                    "Numéro d'approbation éthique", placeholder="Ex: IRB-2024-001"
                )
        with col_conflit:
            st.checkbox("Déclaration de non-conflit d'intérêts", value=True)
            st.text_area(
                "Si vous avez un conflit d'intérêts, veuillez le décrire ici.",
                placeholder="Ex: Financement par une compagnie pharmaceutique.",
            )

        st.markdown("**Sécurité des données**")
        st.text_area(
            "Décrivez comment vous avez géré la sécurité et l'anonymisation des données des patients.",
            placeholder="Ex: Les données ont été stockées sur un serveur sécurisé de l'hôpital et anonymisées.",
        )

        st.markdown("---")

        # --- Section : Soumission du document ---
        st.subheader("4. Soumission du document final")

        uploaded_file = st.file_uploader(
            "Téléchargez le document de votre thèse (format PDF)", type=["pdf"]
        )

        submit = st.form_submit_button("✅ Soumettre la thèse finale")

        if submit:
            # Vérification des champs obligatoires et de la conformité
            if not titre_these or not resume or not director_name:
                st.error(
                    "❌ Veuillez remplir les champs obligatoires : Titre, Directeur, Résumé."
                )
            elif not uploaded_file:
                st.error("❌ Veuillez télécharger le document de thèse au format PDF.")
            elif irb_approval and not irb_number:
                st.error("❌ Le numéro d'approbation éthique est requis.")
            else:
                # La logique de sauvegarde du document et des métadonnées serait ajoutée ici.
                st.success(
                    "✅ Thèse soumise avec succès! Le document a été archivé et les informations enregistrées."
                )
                st.balloons()


if __name__ == "__main__":
    render()
