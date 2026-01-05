# Fichier : dashboard/dashboard_admin.py

# =========================================================================
# 📦 IMPORTS
# =========================================================================
# Bibliothèques Streamlit et Data Science
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Utilitaires internes
from modules.backend.supabase_utils import mock_or_fetch
from modules.backend.form_decorator import register_form
from modules.public.dashboard_renderer import render_dashboard_for_role
from modules.public.form_registry import get_forms_for_role


# =========================================================================
# ⚙️ CONFIGURATION & CONSTANTES
# =========================================================================
ROLE = "ADMIN"
ICON = "🛡️"

FORM_REGISTER_ICONS = {
    "ADMIN": "🛡️",
    "MIDWIFE": "🧑‍🍼",
    "DOCTOR": "👨‍⚕️",
    "NURSE": "🩹",
    "PATIENT": "🫂",
    "DOCTORAL": "🧠",
    "INTERN": "📘",
    "STUDENT": "🎓",
    "GUEST": "🪶",
}

# =========================================================================
# 📊 DONNÉES SIMULÉES PAR RÔLE (Pour les visualisations)
# =========================================================================
roles_data = {
    "MIDWIFE": {
        "formulaires": [
            "form_prenatal_care",
            "form_postnatal_care",
            "form_intrapartum_care",
            "form_midwife_throughout_midwifery_care",
            "form_consultation_prenatale",
            "form_postpartum_follow_up",
            "form_partogram",
            "form_prenatal_follow_up",
            "form_birth_plan_consent",
            "form_childbirth",
            "form_contact_info",
            "form_midwife_daily_tasks",
            "form_midwife_demographics",
            "form_midwife_education_prevention",
            "form_emotional_well_being",
            "form_follow_up",
            "form_incident_report",
            "form_initial_anamnesis",
            "form_initial_routine",
            "form_midwife_messages",
            "form_nutrition",
            "form_patient_file",
            "form_patient_management",
            "form_patients_alerts",
            "form_resume_data_recorded",
            "form_visit_history",
            "form_workshops",
        ],
        "remplis": [
            42,
            38,
            33,
            29,
            45,
            31,
            25,
            40,
            15,
            20,
            18,
            55,
            30,
            22,
            19,
            37,
            10,
            28,
            23,
            12,
            35,
            48,
            50,
            14,
            26,
            39,
            17,
        ],
        "completion": [
            84,
            76,
            66,
            75,
            80,
            70,
            60,
            85,
            55,
            65,
            58,
            90,
            78,
            62,
            59,
            79,
            50,
            74,
            63,
            52,
            77,
            88,
            89,
            54,
            68,
            81,
            57,
        ],
    },
    "DOCTOR": {
        "formulaires": [
            "form_birth_care_plan",
            "form_cesarean_operative_report",
            "form_fetal_anomaly_assessment",
            "form_final_discharge_prescriptions",
            "form_inter_specialities_consultation_request",
            "form_ultrasond_report",
            "form_supervision",
            "form_due_date_calculator",
        ],
        "remplis": [51, 44, 48, 30, 25, 40, 55, 45],
        "completion": [88, 72, 80, 65, 60, 75, 90, 85],
    },
    "NURSE": {
        "formulaires": [
            "form_administration_record",
            "form_admission_discharge_checklist",
            "form_patient_education_postpartum",
            "form_postpartum_care_record",
            "form_vital_signs",
            "form_evolution_notes",
            "form_fetal_monotoring_pain_assessment",
        ],
        "remplis": [60, 52, 47, 40, 65, 55, 45],
        "completion": [92, 78, 70, 75, 95, 85, 80],
    },
    "PATIENT": {
        "formulaires": [
            "form_appointment_booking",
            "form_appointment_followup",
            "form_communication_prefs",
            "form_feedback",
            "form_messaging",
            "form_obstetric_informed_consent",
            "form_pre_consultation_questionnaire",
            "form_pregnancy_log",
            "form_prescription_request",
            "form_satisfaction_survey",
            "form_symptom_logs",
        ],
        "remplis": [36, 42, 39, 30, 25, 20, 35, 45, 18, 50, 28],
        "completion": [75, 88, 82, 70, 65, 60, 78, 85, 55, 90, 68],
    },
    "DOCTORAL": {
        "formulaires": [
            "form_data_extraction",
            "form_research_consent",
            "form_thesis_report",
        ],
        "remplis": [24, 18, 30],
        "completion": [80, 72, 88],
    },
    "INTERN": {
        "formulaires": [
            "form_daily_progress_soap",
            "form_dashboard_logbook_ob",
            "form_delivery_exams_follow_up_ob",
            "form_delivery_report_ob",
            "form_draft_order_ob",
            "form_initial_assessment_ob",
            "form_skill_checklist",
        ],
        "remplis": [40, 32, 36, 25, 30, 45, 28],
        "completion": [85, 78, 82, 60, 65, 90, 70],
    },
    "STUDENT": {
        "formulaires": [
            "form_clinical_observations_ob",
            "form_ob_dashboard",
            "form_supervision_ob",
            "form_competency_evaluations_ob",
            "form_course_feedback",
            "form_case_study",
            "form_stage_request",
        ],
        "remplis": [34, 40, 29, 35, 42, 38, 30],
        "completion": [78, 85, 70, 80, 88, 82, 75],
    },
    # DONNÉES GUEST AJOUTÉES ICI
    "GUEST": {
        "formulaires": [
            "form_public_education_ressources",
            "form_utility_service_request",
            "form_workshop_registration_portal",
        ],
        "remplis": [22, 35, 18],
        "completion": [70, 82, 60],
    },
    # DONNÉES ADMIN AJOUTÉES ICI
    "ADMIN": {
        "formulaires": (
            # Formulaires spécifiques Admin
            [
                "form_access_audit_log",
                "form_model_configuration",
                "form_statistical_report",
                "form_user_role_management",
            ]
            # + Tous les formulaires des autres rôles
            + roles_data["MIDWIFE"]["formulaires"]
            + roles_data["DOCTOR"]["formulaires"]
            + roles_data["NURSE"]["formulaires"]
            + roles_data["PATIENT"]["formulaires"]
            + roles_data["DOCTORAL"]["formulaires"]
            + roles_data["INTERN"]["formulaires"]
            + roles_data["STUDENT"]["formulaires"]
            + roles_data["GUEST"]["formulaires"]
        ),
        "remplis": (
            [48, 36, 42, 55]  # propres à Admin
            + roles_data["MIDWIFE"]["remplis"]
            + roles_data["DOCTOR"]["remplis"]
            + roles_data["NURSE"]["remplis"]
            + roles_data["PATIENT"]["remplis"]
            + roles_data["DOCTORAL"]["remplis"]
            + roles_data["INTERN"]["remplis"]
            + roles_data["STUDENT"]["remplis"]
            + roles_data["GUEST"]["remplis"]
        ),
        "completion": (
            [95, 88, 90, 97]  # propres à Admin
            + roles_data["MIDWIFE"]["completion"]
            + roles_data["DOCTOR"]["completion"]
            + roles_data["NURSE"]["completion"]
            + roles_data["PATIENT"]["completion"]
            + roles_data["DOCTORAL"]["completion"]
            + roles_data["INTERN"]["completion"]
            + roles_data["STUDENT"]["completion"]
            + roles_data["GUEST"]["completion"]
        ),
    },
}


# =========================================================================
# ⚙️ FONCTIONS UTILITAIRES
# =========================================================================


def create_dashboard_dataframe(data):
    """Crée et retourne le DataFrame consolidé pour le dashboard."""
    all_rows = []
    for role, role_data in data.items():
        for i in range(len(role_data["formulaires"])):
            # Construction du nom de formulaire plus propre
            form_name_raw = role_data["formulaires"][i]
            form_name_display = (
                form_name_raw.replace("form_", "").replace("_", " ").title()
            )

            all_rows.append(
                {
                    "Rôle": role,
                    "Formulaire": form_name_display,
                    "Module Interne": f"modules.forms_{role.lower()}.{form_name_raw}",
                    "Remplis": (
                        role_data["remplis"][i] if i < len(role_data["remplis"]) else 0
                    ),
                    "Taux de complétion (%)": (
                        role_data["completion"][i]
                        if i < len(role_data["completion"])
                        else 0
                    ),
                }
            )
    return pd.DataFrame(all_rows)


def form_dashboard_admin():
    """Tableau de bord pour le rôle Admin, incluant les statistiques et le registre."""

    st.title(f"{ICON} Tableau de bord {ROLE}")
    st.markdown("Vue panoramique sur tous les rôles et leurs indicateurs clés.")

    # Rendu dynamique du dashboard (implique des KPI venant d'une autre fonction)
    render_dashboard_for_role(ROLE)

    # 1. Rendu du Tableau de bord Statistique
    df = create_dashboard_dataframe(roles_data)

    st.subheader("Synthèse des Formulaires par Rôle")
    st.dataframe(
        df,
        use_container_width=True,
        column_order=["Rôle", "Formulaire", "Remplis", "Taux de complétion (%)"],
    )

    # 📈 Visualisation globale - Formulaires remplis
    fig = px.bar(
        df.sort_values(by="Remplis", ascending=False).head(20),  # Top 20
        x="Formulaire",
        y="Remplis",
        color="Rôle",
        title="🛡️ Top 20 des formulaires remplis",
        height=600,
    )
    fig.update_layout(xaxis={"categoryorder": "total descending"})
    st.plotly_chart(fig, use_container_width=True)

    # 📉 Comparaison des taux de complétion - Box plot
    fig2 = px.box(
        df,
        x="Rôle",
        y="Taux de complétion (%)",
        color="Rôle",
        title="📊 Distribution des taux de complétion par rôle",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 🔥 Heatmap de corrélation globale
    try:
        pivot = df.pivot_table(
            index="Module Interne",  # Utiliser le chemin complet comme index
            values=["Remplis", "Taux de complétion (%)"],
            aggfunc="mean",
        )

        # Calculer la corrélation uniquement si plus de 1 colonne numérique existe
        if pivot.shape[1] > 1:
            corr = pivot.corr(numeric_only=True)
            plt.style.use("ggplot")
            fig3, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, cbar=True)
            ax.set_title("Heatmap de corrélation (Remplis vs. Taux de complétion)")
            st.pyplot(fig3)
        else:
            st.info(
                "Heatmap non affichée : seulement une colonne numérique dans les données agrégées."
            )

    except ValueError:
        st.warning(
            "Impossible de calculer la Heatmap (données non numériques ou manquantes)."
        )

    # 📤 Exportation
    st.markdown("---")
    st.subheader("Options d'Exportation")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Exporter les statistiques en CSV",
        csv,
        file_name="admin_dashboard_stats.csv",
    )

    # 📦 Formulaires dynamiques (Liste basée sur le registre)
    st.markdown("---")
    st.markdown("## 📋 Audit: Formulaires enregistrés pour le rôle ADMIN")
    forms = get_forms_for_role(ROLE.lower())
    if forms:
        for name, config in forms.items():
            icon = config.get("icon", ICON)
            title = config.get("title", name)
            st.markdown(f"- {icon} **{title}** (`{name}`)")
    else:
        st.warning(
            "Aucun formulaire spécifique n'est actuellement enregistré pour le rôle ADMIN."
        )


# ==============================================================================
# 🧩 ENREGISTREMENT DU FORMULAIRE (via décorateur)
# ==============================================================================
@register_form(
    "Dashboard Admin",
    role="ADMIN",
    icon=ICON,
    description="Tableau de bord pour le rôle Admin avec vue panoramique et audit des modules",
)
def render_dashboard_admin():
    """Fonction de rendu principale pour le dashboard (enregistrée)."""
    form_dashboard_admin()


# ==============================================================================
# 🧪 FONCTION DE TEST AUTONOME
# ==============================================================================
def render_form():
    """Fonction autonome pour lancer le dashboard Admin."""
    st.set_page_config(layout="wide", page_title="Dashboard Admin Démo")

    # NOTE: Dans un environnement Streamlit complet, l'enregistrement doit avoir
    # eu lieu au préalable. Ici, on appelle directement la fonction principale.
    form_dashboard_admin()


# --- Exécution autonome ---
if __name__ == "__main__":
    # La fonction `render_dashboard_admin()` est celle qui sera utilisée
    # dans le cadre de l'application Streamlit principale, mais pour
    # l'exécution locale de ce fichier, on utilise `render_form()`.
    render_form()
