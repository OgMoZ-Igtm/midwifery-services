# BANNER_INJECTED
import streamlit as st
import pandas as pd
import numpy as np


if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="👑 Tableau de bord Admin", page_icon="👑")
    st.title("👑 Tableau de bord Administrateur")

    st.success(
        f"Bonjour {st.session_state.username}, voici votre cockpit de supervision 🌐"
    )

    st.subheader("📊 Statistiques générales")
    st.metric("Utilisateurs actifs", 128)
    st.metric("Formulaires soumis aujourd’hui", 42)
    st.metric("Messages échangés", 87)

    st.subheader("📁 Accès rapide")
    st.button("🔐 Logs de sécurité")
    st.button("📬 Messagerie interne")
    st.button("📦 Organisation")
    st.button("📚 Modules étudiants")
    st.button("🩺 Modules médicaux")

    st.subheader("🧭 Navigation complète")
    st.markdown(
        "Utilisez la barre latérale pour accéder à tous les modules disponibles."
    )
    st.set_page_config(layout="wide")  # Utilise toute la largeur de l'écran

    st.title("Tableau de bord administratif en obstétrique 📈")
    st.subheader("Aperçu rapide des données cliniques et administratives.")

    # Section des métriques principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Utilisateurs actifs", 58, "10% d'augmentation")
    col2.metric("🍼 Naissances suivies", 124, "5 naissances cette semaine")
    col3.metric("🤰 Patients enregistrés", 245, "12 nouvelles inscriptions")
    col4.metric("📩 Messages envoyés", 1345, "45% de réponses")

    st.markdown("---")

    # Section des graphiques
    st.markdown("### Statistiques et graphiques 📊")

    # Graphique des naissances par mois
    st.markdown("#### Naissances par mois")
    births_data = pd.DataFrame(
        {
            "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil"],
            "Nombre de naissances": [25, 30, 45, 40, 55, 60, 75],
        }
    )
    st.bar_chart(births_data.set_index("Mois"))

    # Graphique de répartition des patients par âge
    st.markdown("#### Répartition des patients par tranche d'âge")
    age_groups = pd.DataFrame(
        {
            "Tranche d'âge": ["<20", "20-25", "26-30", "31-35", "36-40", ">40"],
            "Nombre de patients": [15, 60, 85, 55, 20, 10],
        }
    )
    st.line_chart(age_groups.set_index("Tranche d'âge"))

    st.markdown("---")

    # Section des rapports et des listes
    st.markdown("### Rapports et listes détaillés 🔍")

    # Rapport utilisateur avec un expander
    with st.expander("Gérer les utilisateurs"):
        st.write("Liste des 10 derniers utilisateurs inscrits :")
        user_list = pd.DataFrame(
            {
                "Nom": [
                    "Marie L.",
                    "Jean C.",
                    "Sophie P.",
                    "Luc A.",
                    "Chloé B.",
                    "Thomas R.",
                    "Anaïs S.",
                    "David L.",
                    "Émilie G.",
                    "François D.",
                ],
                "Rôle": [
                    "Admin",
                    "Médecin",
                    "Infirmière",
                    "Médecin",
                    "Infirmière",
                    "Admin",
                    "Médecin",
                    "Infirmière",
                    "Médecin",
                    "Admin",
                ],
                "Dernière connexion": [
                    "2025-09-06",
                    "2025-09-05",
                    "2025-09-06",
                    "2025-09-04",
                    "2025-09-06",
                    "2025-09-06",
                    "2025-09-05",
                    "2025-09-06",
                    "2025-09-05",
                    "2025-09-06",
                ],
            }
        )
        st.table(user_list)

    # Rapport patients avec un expander
    with st.expander("Accéder aux dossiers patients"):
        st.write("État de suivi des 50 patients les plus récents.")
        patient_data = {
            "ID Patient": np.arange(1001, 1051),
            "Date d'inscription": pd.to_datetime(
                pd.Series(
                    np.random.choice(pd.date_range("2025-01-01", "2025-09-06"), 50)
                )
            ),
            "Statut": np.random.choice(
                ["En cours", "Terminé", "En attente"], 50, p=[0.7, 0.2, 0.1]
            ),
        }
        patients_df = pd.DataFrame(patient_data)
        st.dataframe(patients_df)


# Pour exécuter le code en tant que script principal

if __name__ == "__main__":
    render()
