import streamlit as st
import pandas as pd



# Simulation de données patient.
# Le mot de passe (cliquez sur "Déverrouiller l'accès" après l'avoir rentré)
PROFILE_PASSWORD = "patientview"

import streamlit as st

# Liste des options valides pour la situation maritale
OPTIONS_SITUATION_MARITALE = [
    "Mariée",
    "Divorcée",
    "Célibataire",
    "Union libre",
    "Refuse de se prononcer",
]


# Fonction de validation
def est_situation_valide(situation):
    return situation in OPTIONS_SITUATION_MARITALE


# Interface utilisateur
st.title("Formulaire du Patient")

nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
age = st.number_input("Âge", min_value=0, max_value=120, step=1)
lieu = st.text_input("Lieu de résidence")
nombre_enfants = st.number_input("Nombre d'enfants", min_value=0, step=1)

# Sélection de la situation maritale
situation_maritale = st.selectbox("Situation maritale", OPTIONS_SITUATION_MARITALE)

# Validation automatique
if est_situation_valide(situation_maritale):
    st.success(f"Situation maritale sélectionnée : {situation_maritale}")
else:
    st.error("Situation maritale invalide.")

# Affichage des données si tout est rempli
if st.button("Valider"):
    if nom and prenom and age and lieu:
        st.write("✅ Données du patient :")
        st.json(
            {
                "Nom": nom,
                "Prénom": prenom,
                "Âge": age,
                "Lieu de résidence": lieu,
                "Nombre d'enfants": nombre_enfants,
                "Situation maritale": situation_maritale,
            }
        )
    else:
        st.warning("Veuillez remplir tous les champs obligatoires.")


def dashboard_administrateur():
    """Tableau de bord pour l'Administrateur."""
    st.header("Tableau de Bord Administrateur ⚙️")
    st.markdown(
        """
    Ceci est la vue d'administration. Vous avez accès à toutes les configurations
    et à la gestion des utilisateurs et des accès.
    """
    )
    st.warning("Fonctionnalité de gestion centralisée en cours de développement.")
    st.write(f"Bienvenue, **{st.session_state.username}**.")


def dashboard_sage_femme():
    """
    Tableau de bord pour la Sage-Femme, incluant le profil patient verrouillé.
    """

    st.header("Tableau de Bord Sage-Femme 🤰")
    st.markdown(f"Bienvenue, **{st.session_state.username}**.")
    st.markdown(
        """
    Aperçu rapide des patientes nécessitant une attention immédiate.
    """
    )

    st.divider()

    # --- 3. Profil du patient sous menu dépliant ouvrable par mot de passe ---

    # Définir une clé d'état pour la visibilité du profil
    if "patient_profile_unlocked" not in st.session_state:
        st.session_state.patient_profile_unlocked = False

    st.subheader("Dossier Patient Actif : Sophie DUPONT")

    # Utilisation d'un expander pour masquer le contenu
    with st.expander(
        "Accéder au **Profil Confidentiel** (Mot de Passe Requis)",
        expanded=st.session_state.patient_profile_unlocked,
    ):

        # Le formulaire apparaît uniquement si le profil est verrouillé
        if not st.session_state.patient_profile_unlocked:
            with st.form("profile_access_form", clear_on_submit=True):
                st.info(
                    "Veuillez entrer le mot de passe pour accéder aux informations personnelles."
                )
                password_input = st.text_input(
                    "Mot de passe du Profil", type="password", key="profile_pass"
                )
                submit_profile = st.form_submit_button(
                    "Déverrouiller l'accès", type="primary", width='stretch'
                )

                if submit_profile:
                    if password_input == PROFILE_PASSWORD:
                        st.session_state.patient_profile_unlocked = True
                        st.success(
                            "Accès autorisé. Le profil est maintenant visible. Cliquez sur l'expander pour cacher."
                        )
                        st.rerun()  # Re-rendre pour afficher le contenu immédiatement
                    else:
                        st.error("Mot de passe incorrect pour accéder au profil.")

        # --- Affichage du profil détaillé si déverrouillé ---
        if st.session_state.patient_profile_unlocked:

            st.markdown("### Informations Personnelles Confidentielles")

            # Afficher les données patient
            data = PATIENT_DATA.get("current_patient", {})

            if data:
                # Préparation des données pour l'affichage
                profile_df = pd.DataFrame(data.items(), columns=["Champ", "Valeur"])

                # Stylisation et affichage des données
                st.table(profile_df.set_index("Champ"))

            else:
                st.warning(
                    "Aucune donnée patient n'est associée à cet utilisateur de démonstration."
                )

            # Bouton pour refermer et verrouiller
            if st.button("Verrouiller le Profil", key="lock_profile"):
                st.session_state.patient_profile_unlocked = False
                st.toast("Profil confidentiel verrouillé.", icon="🔒")
                st.rerun()


def dashboard_infirmier():
    """Tableau de bord pour l'Infirmier."""
    st.header("Tableau de Bord Infirmier/Infirmière 💉")
    st.markdown(f"Bienvenue, **{st.session_state.username}**.")
    st.markdown(
        """
    Cette page affiche les tâches quotidiennes, les rappels de médication,
    et les informations vitales des patients.
    """
    )
    st.success("Toutes les tâches pour aujourd'hui sont complètes.")


# def render_dashboard(role)
def dashboard_page(role):
    """
    Fonction centrale pour diriger l'utilisateur vers le bon tableau de bord
    en fonction de son rôle.
    """

    # Mapping des rôles vers les fonctions de tableau de bord
    role_map = {
        "Administrateur": dashboard_administrateur,
        "Sage-Femme": dashboard_sage_femme,
        "Infirmier": dashboard_infirmier,
    }

    # Vérifie si le rôle existe et appelle la fonction correspondante
    if role in role_map:
        role_map[role]()
    else:
        st.error(f"Rôle non reconnu: **{role}**. Veuillez contacter l'assistance.")
