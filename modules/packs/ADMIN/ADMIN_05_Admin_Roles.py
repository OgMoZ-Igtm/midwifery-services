import streamlit as st
import pandas as pd


def render():
    """
    Cette application Streamlit sert de formulaire de gestion des rôles
    pour les administrateurs.
    """
    st.set_page_config(page_title="Gestion des Rôles", page_icon="🎭", layout="wide")

    st.title("🎭 Gestion des rôles")
    st.info(
        "Cette page permet d'attribuer et de consulter les rôles des utilisateurs du système."
    )

    # Simuler une base de données d'utilisateurs et de rôles
    # Dans une application réelle, ces données viendraient d'une base de données sécurisée
    users_data = {
        "Nom": ["Alice M.", "Dr. Jean D.", "Étudiante Léa G.", "Marc F."],
        "Email": [
            "alice@example.com",
            "jean.d@example.com",
            "lea@example.com",
            "marc.f@example.com",
        ],
        "Rôle actuel": ["patient", "doctor", "doctorante", "patient"],
    }
    df_users = pd.DataFrame(users_data)

    st.subheader("👥 Attribution d’un rôle")

    with st.form("attribuer_role_form"):
        # La liste des rôles disponibles
        roles = [
            "admin",
            "doctor",
            "nurse",
            "midwife",
            "patient",
            "stagiaire",
            "etudiante",
            "doctorante",
        ]

        # Amélioration: utilisation de st.selectbox pour une meilleure sélection
        user_emails = sorted(df_users["Email"].tolist())
        col1, col2 = st.columns(2)

        with col1:
            utilisateur_email = st.selectbox(
                "📧 Sélectionner l'utilisateur par email", user_emails
            )

        # Afficher le rôle actuel
        current_role = df_users[df_users["Email"] == utilisateur_email][
            "Rôle actuel"
        ].iloc[0]
        with col2:
            st.info(f"Rôle actuel : **{current_role}**")

        st.markdown("---")

        # Le selectbox pour choisir le nouveau rôle
        nouveau_role = st.selectbox(
            "Nouveau rôle", roles, index=roles.index(current_role)
        )

        submit = st.form_submit_button("✅ Mettre à jour le rôle")

        if submit:
            # Recherche de l'utilisateur dans le DataFrame
            user_row = df_users[df_users["Email"] == utilisateur_email]

            if not user_row.empty:
                # Simuler la mise à jour du rôle
                st.success(
                    f"✅ Le rôle de l'utilisateur **{utilisateur_email}** a été mis à jour en **{nouveau_role}**."
                )
            else:
                st.warning(
                    "⚠️ Utilisateur non trouvé. Veuillez sélectionner un e-mail valide."
                )

    st.markdown("---")

    st.subheader("🔎 Liste des utilisateurs et de leurs rôles")
    st.dataframe(df_users, use_container_width=True)


if __name__ == "__main__":
    render()
