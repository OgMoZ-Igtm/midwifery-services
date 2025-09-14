import streamlit as st
import pandas as pd
import bcrypt  # Nécessite l'installation : pip install bcrypt
import re  # Pour la validation des emails


def render():
    """
    Cette application Streamlit sert de formulaire pour la gestion des utilisateurs,
    permettant à l'administrateur d'ajouter, de modifier ou de supprimer des utilisateurs.
    """
    st.set_page_config(
        page_title="Gestion des utilisateurs", page_icon="👥", layout="wide"
    )

    st.title("👥 Gestion des utilisateurs")
    st.info(
        "Cette page permet de gérer les utilisateurs du système, d'attribuer des rôles et de réinitialiser des mots de passe."
    )

    # Simuler une base de données d'utilisateurs
    # Dans une application réelle, ces données viendraient d'une base de données sécurisée
    @st.cache_data
    def get_users_data():
        return pd.DataFrame(
            [
                {"Nom": "admin1", "Email": "admin1@mail.com", "Rôle": "admin"},
                {"Nom": "doctor1", "Email": "doctor1@mail.com", "Rôle": "doctor"},
                {"Nom": "patient1", "Email": "patient1@mail.com", "Rôle": "patient"},
            ]
        )

    df_users = get_users_data()

    # Fonctions de validation
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_strong_password(password):
        return (
            len(password) >= 8
            and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
            and re.search(r"[0-9]", password)
            and re.search(r"[\W_]", password)
        )

    # --- Section : Ajouter un nouvel utilisateur ---
    st.subheader("➕ Ajouter un nouvel utilisateur")
    with st.form("ajout_utilisateur"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet", placeholder="Ex: Jean Dupont")
        with col2:
            email = st.text_input(
                "Adresse email", placeholder="Ex: jean.dupont@example.com"
            )

        role = st.selectbox(
            "Rôle",
            [
                "midwife",
                "nurse",
                "doctor",
                "admin",
                "patient",
                "stagiaire",
                "etudiante",
                "doctorante",
            ],
        )

        mot_de_passe = st.text_input(
            "Mot de passe",
            type="password",
            help="Le mot de passe initial de l'utilisateur. Il doit contenir au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.",
        )

        submit = st.form_submit_button("✅ Ajouter l'utilisateur")

        if submit:
            if not nom or not email or not mot_de_passe:
                st.error("❌ Veuillez remplir tous les champs obligatoires.")
            elif not is_valid_email(email):
                st.error("❌ Le format de l'email est invalide.")
            elif email in df_users["Email"].tolist():
                st.error("❌ Un utilisateur avec cet email existe déjà.")
            elif not is_strong_password(mot_de_passe):
                st.error("❌ Le mot de passe n'est pas assez fort.")
            else:
                # Hachage du mot de passe
                hashed_password = bcrypt.hashpw(
                    mot_de_passe.encode("utf-8"), bcrypt.gensalt()
                )

                # Ajout de l'utilisateur (simulé)
                new_user = {
                    "Nom": nom,
                    "Email": email,
                    "Rôle": role,
                    "Hashed_Password": hashed_password,
                }
                # La logique pour ajouter à la base de données réelle irait ici.

                st.success(
                    f"✅ Utilisateur **{nom}** ({role}) ajouté avec succès ! Mot de passe haché et prêt à être stocké."
                )
                st.balloons()

    st.markdown("---")

    # --- Section : Liste des utilisateurs ---
    st.subheader("👥 Liste actuelle des utilisateurs")

    search_query = st.text_input("Rechercher un utilisateur par nom ou email", "")
    if search_query:
        filtered_df = df_users[
            df_users.apply(
                lambda row: search_query.lower()
                in row.astype(str).str.lower().to_string(),
                axis=1,
            )
        ]
    else:
        filtered_df = df_users

    st.dataframe(filtered_df, use_container_width=True)

    # --- Section : Actions sur un utilisateur existant ---
    st.markdown("---")
    st.subheader("🔧 Modifier ou supprimer un utilisateur")

    with st.form("action_utilisateur"):
        selected_user = st.selectbox(
            "Sélectionnez un utilisateur",
            df_users["Email"].tolist(),
            format_func=lambda x: f"{x} ({df_users[df_users['Email'] == x]['Rôle'].iloc[0]})",
        )

        action = st.radio(
            "Action",
            [
                "Modifier le rôle",
                "Réinitialiser le mot de passe",
                "Supprimer l'utilisateur",
            ],
        )

        if action == "Modifier le rôle":
            user_current_role = df_users[df_users["Email"] == selected_user][
                "Rôle"
            ].iloc[0]
            roles_list = [
                "midwife",
                "nurse",
                "doctor",
                "admin",
                "patient",
                "stagiaire",
                "etudiante",
                "doctorante",
            ]
            new_role = st.selectbox(
                "Nouveau rôle",
                roles_list,
                index=roles_list.index(user_current_role),
            )

        if action == "Supprimer l'utilisateur":
            confirm_delete = st.checkbox(
                "Je confirme la suppression de cet utilisateur."
            )
            if not confirm_delete:
                st.warning("Veuillez cocher la case pour confirmer la suppression.")

        action_submit = st.form_submit_button("Confirmer l'action")

        if action_submit:
            if action == "Modifier le rôle":
                st.success(
                    f"✅ Rôle de l'utilisateur **{selected_user}** mis à jour en **{new_role}**."
                )
            elif action == "Réinitialiser le mot de passe":
                # Envoi d'un lien de réinitialisation sécurisé par e-mail
                st.warning(
                    f"⚠️ Une procédure de réinitialisation de mot de passe a été envoyée à **{selected_user}**."
                )
            elif action == "Supprimer l'utilisateur":
                if confirm_delete:
                    # Logique de suppression ici
                    st.error(f"❌ L'utilisateur **{selected_user}** a été supprimé.")
                else:
                    st.error("❌ Suppression annulée : la confirmation est requise.")


if __name__ == "__main__":
    render()
