import streamlit as st
import datetime
import pandas as pd
from utils.security import afficher_badge_securite


def render():
    """
    Formulaire de saisie pour la documentation des soins intrapartum.
    """

    # Affichage du badge de sécurité pour le rôle pertinent (ex: DOCTOR ou MIDWIFE)
    st.markdown(afficher_badge_securite("DOCTOR"), unsafe_allow_html=True)

    st.title("🤰 Formulaire de soins intrapartum")
    st.info(
        "Documentez le suivi du travail, les événements cliniques et les résultats de la naissance."
    )

    with st.form(key="intrapartum_form"):
        # --- Section 1: Informations d'admission ---
        st.subheader("1. Admission et état initial")
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input(
                "ID Patient", max_chars=10, help="ID unique de la patiente"
            )
            gravida = st.number_input(
                "Gravida (Nb. de grossesses)", min_value=0, step=1
            )
            para = st.number_input("Para (Nb. d'accouchements)", min_value=0, step=1)

        with col2:
            date_admission = st.date_input(
                "Date d'admission", value=datetime.date.today()
            )
            time_admission = st.time_input("Heure d'admission")
            gestational_age = st.text_input(
                "Âge gestationnel (semaines + jours)", placeholder="ex: 39+2"
            )

        st.markdown("---")

        # --- Section 2: Suivi du travail ---
        st.subheader("2. Suivi de la progression du travail")
        col_cervix, col_fetal = st.columns(2)

        with col_cervix:
            st.markdown("**Progression cervicale**")
            cervical_dilation = st.slider(
                "Dilatation (cm)", min_value=0, max_value=10, value=0
            )
            cervical_effacement = st.slider(
                "Effacement (%)", min_value=0, max_value=100, value=0
            )
            fetal_station = st.selectbox(
                "Station fœtale", ["-3", "-2", "-1", "0", "+1", "+2", "+3"]
            )

        with col_fetal:
            st.markdown("**Monitorage fœtal**")
            fetal_heart_rate = st.number_input(
                "Rythme cardiaque fœtal (bpm)",
                min_value=50,
                max_value=200,
                step=1,
                value=140,
            )
            fetal_monitor_type = st.radio(
                "Méthode de monitorage", ["Intermittent", "Continu"]
            )

            st.markdown("**Contractions utérines**")
            contraction_frequency = st.number_input(
                "Fréquence (en 10 min)", min_value=0, step=1
            )
            contraction_duration = st.number_input(
                "Durée (secondes)", min_value=0, step=1
            )

        st.markdown("---")

        # --- Section 3: Événements et interventions ---
        st.subheader("3. Événements et interventions")
        st.checkbox(
            "Rupture de la membrane (SROM)", help="Spontaneous Rupture of Membranes"
        )
        st.checkbox(
            "Rupture de la membrane (AROM)", help="Artificial Rupture of Membranes"
        )

        col_interventions, col_meds = st.columns(2)
        with col_interventions:
            st.multiselect(
                "Interventions",
                [
                    "Pose de cathéter",
                    "Amniotomie",
                    "Pose de forceps",
                    "Ventouse obstétricale",
                    "Autre...",
                ],
            )
        with col_meds:
            st.multiselect(
                "Médications",
                [
                    "Oxytocine",
                    "Anesthésie épidurale",
                    "Analgésie IV",
                    "Antibiotiques",
                    "Autre...",
                ],
            )

        st.text_area(
            "Notes sur les interventions",
            placeholder="Détails sur les interventions ou médications administrées...",
        )

        st.markdown("---")

        # --- Section 4: Résultats de la naissance ---
        st.subheader("4. Résultats de la naissance")
        col_birth_details, col_baby_stats = st.columns(2)

        with col_birth_details:
            time_birth = st.time_input("Heure de la naissance")
            birth_type = st.selectbox(
                "Type d'accouchement",
                [
                    "Vaginal spontané",
                    "Césarienne",
                    "Assisté par forceps",
                    "Assisté par ventouse",
                ],
            )

        with col_baby_stats:
            birth_weight = st.number_input(
                "Poids à la naissance (kg)", min_value=0.5, step=0.1
            )
            apgar_1min = st.number_input(
                "Score Apgar (1 min)", min_value=0, max_value=10, step=1
            )
            apgar_5min = st.number_input(
                "Score Apgar (5 min)", min_value=0, max_value=10, step=1
            )

        st.text_area(
            "Observations cliniques et notes de naissance",
            placeholder="Notes détaillées sur le travail et l'accouchement...",
            height=150,
        )

        # Bouton de soumission du formulaire
        submit_button = st.form_submit_button("✅ Enregistrer les données intrapartum")

    if submit_button:
        # Traitement des données soumises
        if not patient_id:
            st.error("❌ Le champ 'ID Patient' est obligatoire.")
        else:
            st.success("🎉 Données intrapartum enregistrées avec succès!")
            st.balloons()

            # Affichage des données soumises pour vérification
            st.subheader("📝 Récapitulatif")
            data = {
                "ID Patient": [patient_id],
                "Dilatation": [cervical_dilation],
                "Effacement": [cervical_effacement],
                "Station Fœtale": [fetal_station],
                "Poids du bébé": [fetal_heart_rate],
                "APGAR 1 min": [apgar_1min],
                "APGAR 5 min": [apgar_5min],
            }
            df = pd.DataFrame(data)
            st.dataframe(
                df.T, use_container_width=True
            )  # Utilise la vue transposée pour une meilleure lisibilité


# Assurez-vous d'avoir ce bloc pour que la page s'exécute correctement
if __name__ == "__main__":
    render()
