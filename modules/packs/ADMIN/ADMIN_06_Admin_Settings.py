# BANNER_INJECTED
import streamlit as st
import pandas as pd

from utils.security import afficher_badge_securite

# Ne pas appeler la fonction ici. L'appeler dans la fonction render() pour un meilleur contrôle.
# afficher_badge_securite("ADMIN")

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour la configuration
    des paramètres du système par l'administrateur.
    """
    st.set_page_config(page_title="Paramètres du Système", page_icon="⚙️", layout="wide")

    # Correction de la ligne de code :
    # 1. On appelle la fonction en lui passant le pack "ADMIN".
    # 2. On utilise st.markdown() avec le paramètre unsafe_allow_html=True pour afficher
    #    le badge de sécurité qui est une chaîne de caractères HTML.
    afficher_badge_securite("ADMIN", "ADMIN")

    st.title("⚙️ Paramètres du système")
    st.info(
        "Cette page permet de configurer les options de sécurité et de gestion des données du système."
    )

    with st.form(key="system_settings_form"):

        # --- Section 1: Sécurité du compte et de l'accès ---
        st.subheader("1. Sécurité du compte et de l'accès 🔒")
        col1_sec, col2_sec = st.columns(2)

        with col1_sec:
            enable_2fa = st.checkbox(
                "Activer la double authentification (2FA)",
                help="Les utilisateurs devront fournir un second code de vérification à la connexion.",
            )
            force_password_update = st.checkbox(
                "Forcer la mise à jour des mots de passe tous les 90 jours",
                help="Les utilisateurs seront invités à changer leur mot de passe périodiquement.",
            )
            lock_account_attempts = st.number_input(
                "Nombre d'échecs de connexion avant verrouillage",
                min_value=3,
                max_value=10,
                step=1,
                value=5,
                help="Le compte sera verrouillé après ce nombre de tentatives infructueuses.",
            )

        with col2_sec:
            session_timeout = st.number_input(
                "Délai d'expiration de la session (en minutes)",
                min_value=15,
                step=15,
                value=60,
                help="Déconnexion automatique après cette période d'inactivité.",
            )
            password_complexity = st.selectbox(
                "Niveau de complexité des mots de passe",
                ["Faible", "Moyen", "Élevé"],
                help="Exige des caractères spéciaux, des majuscules, et des chiffres.",
            )
            enable_ip_whitelist = st.checkbox(
                "Activer la liste blanche d'IP pour les administrateurs",
                help="Les administrateurs ne peuvent se connecter que depuis des adresses IP approuvées.",
            )

        st.markdown("---")

        # --- Section 2: Gestion des données et confidentialité ---
        st.subheader("2. Gestion des données et confidentialité 🩺")
        col1_data, col2_data = st.columns(2)

        with col1_data:
            allow_csv_export = st.checkbox(
                "Autoriser l’export CSV des données patients",
                help="Permet aux utilisateurs autorisés de télécharger des données au format CSV.",
            )
            data_retention_period = st.number_input(
                "Période de rétention des logs (en jours)",
                min_value=30,
                step=30,
                value=90,
                help="Les logs de connexion et d'activité seront conservés pendant cette période.",
            )
            enable_anonymization = st.checkbox(
                "Anonymiser les données patient non-essentielles",
                help="Remplace les identifiants directs par des pseudonymes dans les rapports analytiques.",
            )

        with col2_data:
            audit_log_access = st.checkbox(
                "Journaliser les accès aux dossiers patients sensibles",
                help="Enregistre chaque accès aux informations les plus confidentielles.",
            )
            automatic_data_deletion = st.number_input(
                "Suppression des dossiers après (années)",
                min_value=0,
                max_value=20,
                step=1,
                value=10,
                help="Supprime automatiquement les dossiers des patients inactifs après cette période (0 pour désactiver).",
            )
            backup_frequency = st.selectbox(
                "Fréquence des sauvegardes de la base de données",
                ["Quotidien", "Hebdomadaire", "Mensuel"],
                help="Définit la fréquence des sauvegardes automatiques pour la récupération des données.",
            )

        st.markdown("---")

        # --- Section 3: Personnalisation de l'interface ---
        st.subheader("3. Personnalisation de l'interface 🎨")
        theme_option = st.selectbox(
            "Thème de l'application",
            ["Clair", "Sombre"],
            help="Change le thème visuel de l'interface utilisateur.",
        )

        # Bouton de sauvegarde
        submit_button = st.form_submit_button("💾 Sauvegarder les paramètres")

    if submit_button:
        # Ici, vous ajouteriez la logique de sauvegarde des paramètres
        st.success("✅ Paramètres du système sauvegardés avec succès!")
        st.balloons()


if __name__ == "__main__":
    render()
