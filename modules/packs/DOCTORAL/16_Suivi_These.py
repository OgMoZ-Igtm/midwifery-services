import streamlit as st
from datetime import date, datetime
import uuid  # Pour l'identifiant de session
import pandas as pd
import plotly.express as px


def render():
    """
    Cette application Streamlit sert de formulaire pour le suivi de la progression
    d'une thèse de doctorat, avec des fonctionnalités de sécurité et de gestion de projet.
    """
    st.set_page_config(page_title="Suivi de Thèse", page_icon="🎓", layout="wide")
    st.title("🎓 Suivi de Thèse (Doctorante)")
    st.info(
        "Utilisez ce formulaire pour documenter l'avancement de votre thèse, de la planification à la soutenance, en respectant les normes de recherche."
    )

    # Simule l'utilisateur connecté pour la traçabilité
    current_doctoral_student = "Marie Dupont"

    # Session state pour stocker les jalons
    if "milestones" not in st.session_state:
        st.session_state.milestones = []

    if "thesis_id" not in st.session_state:
        st.session_state.thesis_id = str(uuid.uuid4())

    with st.form("thesis_tracking_form"):

        # --- Section 1: Informations de base et sécurité ---
        st.subheader("1. Informations sur la thèse")
        st.info(
            f"Nom de la doctorante : **{current_doctoral_student}** (ID de la thèse : **{st.session_state.thesis_id[:8]}**)"
        )
        st.info(
            f"Dernière mise à jour : **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**"
        )

        col1, col2 = st.columns(2)
        with col1:
            director_name = st.text_input(
                "Nom du directeur de thèse", placeholder="Ex: Dr. Martin Dubois"
            )
        with col2:
            submission_date = st.date_input("Date de soumission prévue")

        st.text_area(
            "Sujet de recherche",
            placeholder="Décrivez le sujet de votre thèse et la question de recherche.",
            height=100,
        )

        # Vérification d'approbation éthique pour les projets impliquant des données humaines
        st.markdown("---")
        st.subheader("2. Conformité éthique et sécurité")
        irb_approval = st.checkbox(
            "Le projet a-t-il une approbation éthique (IRB/CÉR)?"
        )
        if irb_approval:
            irb_number = st.text_input(
                "Numéro d'approbation éthique", placeholder="Ex: IRB-2024-001"
            )
        else:
            st.warning(
                "⚠️ L'approbation éthique est requise pour la collecte de données. Continuez à vos risques et périls."
            )

        st.markdown("**Sécurité des données**")
        st.text_area(
            "Décrivez comment les données sont sécurisées et stockées (Ex: Serveur de l'hôpital, anonymisation, etc.)",
            height=80,
        )

        st.markdown("---")

        # --- Section 3: Progression et jalons ---
        st.subheader("3. Progression et avancement")
        current_stage = st.selectbox(
            "Étape actuelle",
            [
                "Revue de littérature",
                "Collecte de données",
                "Analyse des données",
                "Rédaction",
                "Soumission",
                "Soutenue",
            ],
        )

        # Saisie des jalons
        st.markdown("**Jalons (Milestones)**")
        col_milestone, col_date = st.columns(2)
        with col_milestone:
            milestone_name = st.text_input("Nom du jalon")
        with col_date:
            milestone_date = st.date_input("Date de réalisation")

        add_milestone_button = st.button("Ajouter un jalon")
        if add_milestone_button and milestone_name:
            st.session_state.milestones.append(
                {"Jalon": milestone_name, "Date": milestone_date}
            )
            st.success(f"Jalon '{milestone_name}' ajouté!")

        # Affichage des jalons dans un tableau
        if st.session_state.milestones:
            df_milestones = pd.DataFrame(st.session_state.milestones)
            st.dataframe(df_milestones, use_container_width=True)

            # Affichage de la progression dans un graphique
            fig = px.bar(df_milestones, x="Jalon", y="Date", title="Jalons de la thèse")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        submitted = st.form_submit_button("✅ Enregistrer la progression")

    if submitted:
        # Ici, vous ajouteriez la logique de sauvegarde des données.
        st.success("✅ Progression de thèse enregistrée avec succès!")
        st.balloons()


if __name__ == "__main__":
    render()
