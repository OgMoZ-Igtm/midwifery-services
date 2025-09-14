# BANNER_INJECTED
import streamlit as st
from datetime import date
import uuid  # Pour générer un identifiant unique


if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour les
    publications scientifiques, avec des fonctionnalités de sécurité et de conformité.
    """
    st.set_page_config(page_title="Publications", page_icon="📄", layout="wide")
    st.title("📄 Publications Scientifiques en Obstétrique")
    st.info(
        "Ce formulaire permet de suivre les articles soumis, acceptés ou publiés, en assurant la conformité aux normes scientifiques."
    )

    # Simule l'utilisateur connecté pour la traçabilité
    current_doctoral_student = "Marie Dupont"

    # --- Section Auteurs (hors du formulaire) ---
    # Cette section est déplacée ici pour respecter la contrainte de st.form()
    st.subheader("1. Ajout des auteurs 🧑‍🔬")
    st.info(
        "Ajoutez les auteurs un par un. L'ordre est important car il est conforme au protocole d'obstétrique pour les publications."
    )

    if "auteurs" not in st.session_state:
        st.session_state.auteurs = []

    col_auteur1, col_auteur2 = st.columns([3, 1])
    with col_auteur1:
        nouvel_auteur = st.text_input("Nom de l'auteur", key="auteur_input")
    with col_auteur2:
        st.markdown("<br>", unsafe_allow_html=True)  # Espace pour aligner le bouton
        ajouter_auteur_btn = st.button("➕ Ajouter")

    if ajouter_auteur_btn and nouvel_auteur:
        st.session_state.auteurs.append(nouvel_auteur)
        st.experimental_rerun()  # Nécessaire pour vider l'input et mettre à jour la liste

    # Affichage de la liste des auteurs avec une option pour les supprimer
    if st.session_state.auteurs:
        st.write("**Liste des auteurs**:")
        for i, auteur in enumerate(st.session_state.auteurs):
            col_list_auteur, col_btn_supprimer = st.columns([0.9, 0.1])
            with col_list_auteur:
                st.write(f"- {auteur}")
            with col_btn_supprimer:
                if st.button("❌", key=f"supprimer_{i}"):
                    st.session_state.auteurs.pop(i)
                    st.experimental_rerun()
    st.markdown("---")

    # --- Section Formulaire ---
    # Le reste du formulaire est dans un st.form()
    with st.form("publications_form"):
        # Génération d'un identifiant unique pour chaque soumission
        submission_id = str(uuid.uuid4())

        # --- Section 2: Informations de base de la publication ---
        st.subheader("2. Informations de la publication")
        st.info(
            f"Déclaration soumise par : **{current_doctoral_student}** (ID de soumission : **{submission_id[:8]}**)"
        )

        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input(
                "Titre de la publication",
                placeholder="Ex: Taux de césarienne et santé maternelle au Québec",
            )
        with col2:
            publication_type = st.selectbox(
                "Type de publication",
                [
                    "Article de revue",
                    "Communication de conférence",
                    "Chapitre de livre",
                    "Thèse",
                    "Autre",
                ],
            )

        journal_name = st.text_input(
            "Nom de la revue/conférence",
            placeholder="Ex: The Lancet, New England Journal of Medicine, etc.",
        )

        # Champ spécifique pour la recherche en obstétrique
        st.markdown("---")
        st.subheader("3. Spécificités en obstétrique")
        st.info(
            "Ces champs sont cruciaux pour la traçabilité et la qualité de la recherche clinique."
        )

        col_obs1, col_obs2 = st.columns(2)
        with col_obs1:
            # Sécurité des données sensibles
            st.markdown("**Cohorte/étude de référence**")
            etude_reference = st.text_input(
                "Nom de la cohorte ou de l'étude (si applicable)",
                placeholder="Ex: Étude Nutri-Maman, Registre des naissances du Québec",
            )
        with col_obs2:
            # Traçabilité et éthique
            date_debut_etude = st.date_input(
                "Date de début de l'étude", value=date.today()
            )

        st.text_area(
            "Mots-clés pertinents (MeSH, etc.)",
            placeholder="Séparez les mots-clés par des virgules. Ex: Césarienne, Santé maternelle, Grossesse, Obstétrique, Épidémiologie",
        )

        st.markdown("---")

        # --- Section 4: Détails et statut ---
        st.subheader("4. Détails et statut")

        col3, col4 = st.columns(2)
        with col3:
            date_soumission = st.date_input("Date de soumission", value=date.today())
        with col4:
            publication_status = st.selectbox(
                "Statut",
                ["En cours de rédaction", "Soumis", "En révision", "Accepté", "Publié"],
            )

        if publication_status == "Publié":
            doi_url = st.text_input(
                "Lien DOI ou URL de la publication", placeholder="Ex: 10.1002/12345abc"
            )
            st.info(
                "Le DOI est un identifiant unique qui garantit la traçabilité de votre publication."
            )

        st.text_area(
            "Résumé",
            placeholder="Copiez-collez ici le résumé de votre publication.",
            height=150,
        )

        st.markdown("---")

        # --- Section 5: Conformité et fichiers joints ---
        st.subheader("5. Conformité et documents")

        st.markdown("**Vérification éthique**")
        irb_approval = st.checkbox("Projet avec approbation éthique (IRB/CÉR)")
        if irb_approval:
            st.text_input(
                "Numéro d'approbation éthique", placeholder="Ex: IRB-2024-001"
            )

        st.markdown("**Déclaration de conflits d'intérêts**")
        st.checkbox("Aucun conflit d'intérêts à déclarer")
        st.text_area("Si non, veuillez décrire les conflits d'intérêts")

        st.markdown("**Documents de la publication**")
        uploaded_manuscript = st.file_uploader(
            "Téléchargez le manuscrit (.pdf)", type="pdf"
        )

        # Le bouton de soumission du formulaire
        submitted = st.form_submit_button("✅ Enregistrer la publication")

    if submitted:
        if not titre or not st.session_state.auteurs or not journal_name:
            st.error(
                "❌ Veuillez remplir les champs obligatoires (Titre, Auteurs, Revue)."
            )
        else:
            # Ici, la logique de sauvegarde des données, y compris l'ID et le fichier téléchargé
            st.success(
                "✅ Publication enregistrée avec succès! Les informations ont été validées."
            )
            st.balloons()


if __name__ == "__main__":
    render()
