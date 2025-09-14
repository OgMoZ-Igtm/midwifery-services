import streamlit as st
from datetime import date


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour les projets
    de recherche d'une doctorante en obstétrique, avec des ajouts de sécurité et de conformité.
    """
    st.set_page_config(page_title="Projets de Recherche", page_icon="📚", layout="wide")
    st.title("📚 Projets de Recherche - Doctorant")
    st.info(
        "Déclarez vos projets de recherche en cours, en assurant la conformité éthique et la sécurité des données."
    )

    # Simule l'utilisateur connecté
    current_doctoral_student = "Marie Dupont"

    with st.form("doctoral_research_form"):
        # --- Section : Informations de base du projet ---
        st.subheader("1. Informations sur le projet")
        st.info(f"Déclaration soumise par : **{current_doctoral_student}**")

        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input(
                "📖 Titre du projet",
                placeholder="Ex: Impact de la pré-éclampsie sur le développement fœtal",
            )
            director = st.text_input(
                "👨‍🏫 Directeur de recherche", placeholder="Ex: Dr. Martin Dubois"
            )
        with col2:
            start_date = st.date_input("Date de début", value=date.today())
            expected_end_date = st.date_input("Date de fin prévue")

        domaine = st.selectbox(
            "📂 Domaine de recherche",
            [
                "Obstétrique",
                "Santé maternelle",
                "Pédiatrie",
                "Gynécologie",
                "Épidémiologie",
                "Autre",
            ],
        )
        resume = st.text_area(
            "📝 Résumé du projet",
            placeholder="Décrivez la problématique, les objectifs et la méthodologie de votre projet...",
        )

        st.markdown("---")

        # --- Section : Conformité et éthique ---
        st.subheader("2. Conformité éthique et sécurité des données")

        irb_approval = st.checkbox(
            "Le projet a-t-il une approbation éthique (IRB/CÉR)?", value=False
        )
        if irb_approval:
            col_irb1, col_irb2 = st.columns(2)
            with col_irb1:
                irb_number = st.text_input(
                    "Numéro d'approbation éthique", placeholder="Ex: IRB-2024-001"
                )
            with col_irb2:
                irb_date = st.date_input("Date d'approbation", value=date.today())
        else:
            st.warning(
                "⚠️ L'approbation éthique est obligatoire pour les recherches impliquant des données humaines. La soumission n'est pas possible sans cette approbation."
            )

        st.selectbox(
            "Type de données utilisées",
            ["Anonymisées", "Pseudonymisées", "Identifiantes"],
        )
        st.text_area(
            "Protocole de sécurité des données",
            placeholder="Décrivez comment les données sont sécurisées et stockées (Ex: Serveur chiffré, accès restreint)...",
        )

        st.markdown("---")

        # --- Section : Financement et état d'avancement ---
        st.subheader("3. Financement et statut")

        col3, col4 = st.columns(2)
        with col3:
            funding_status = st.selectbox(
                "Statut de financement",
                ["Financé", "En attente de financement", "Non financé"],
            )
        with col4:
            project_status = st.multiselect(
                "État d'avancement (plusieurs options possibles)",
                [
                    "Planification",
                    "Recrutement des participants",
                    "Collecte de données",
                    "Analyse des données",
                    "Rédaction",
                    "Terminé",
                ],
            )

        # Possibilité d'attacher des documents
        st.markdown("---")
        st.subheader("4. Documents associés")
        uploaded_file = st.file_uploader(
            "Téléchargez le protocole de recherche (.pdf)", type="pdf"
        )

        submitted = st.form_submit_button("✅ Enregistrer le projet")

    if submitted:
        if not titre or not director:
            st.error(
                "❌ Veuillez remplir le titre et le nom du directeur de recherche."
            )
        elif irb_approval and not irb_number:
            st.error("❌ Le numéro d'approbation éthique est requis.")
        else:
            # Ici, la logique de sauvegarde des données serait ajoutée, y compris les fichiers
            st.success(
                "📌 Projet de recherche ajouté avec succès. Les informations sont conformes aux exigences."
            )
            st.balloons()


if __name__ == "__main__":
    render()