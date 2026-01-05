# -*- coding: utf-8 -*-
# Fichier : test_forms_midwife.py
# Objectif : Vérifier l'import et le rendu des formulaires MIDWIFE

import sys, os, importlib
import streamlit as st
from datetime import datetime

# ✅ Imports backend nécessaires
from modules.backend.supabase_utils import mock_or_insert
from modules.backend.supabase_core import supabase
from modules.backend.supabase_client import supabase
from modules.backend.form_decorator import register_form

# ✅ Ajout du chemin racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# ✅ Liste complète des modules MIDWIFE à tester
MIDWIFE_FORMS = [
    # Bloc 1
    "modules.forms_midwife.midwife_birth_plan_consent_form",
    "modules.forms_midwife.midwife_childbirth_form",
    "modules.forms_midwife.midwife_education_prevention_form",
    "modules.forms_midwife.midwife_daily_tasks_form",
    "modules.forms_midwife.midwife_demographics_form",
    "modules.forms_midwife.midwife_emotional_well_being_form",
    "modules.forms_midwife.midwife_follow_up_form",
    "modules.forms_midwife.midwife_incident_report_form",
    "modules.forms_midwife.midwife_initial_anamnesis_form",
    "modules.forms_midwife.midwife_initial_routine_form",
    "modules.forms_midwife.midwife_intrapartum_care_form",
    "modules.forms_midwife.midwife_messaging_form",
    "modules.forms_midwife.midwife_obstetrics_form",
    "modules.forms_midwife.midwife_nutrition_form",
    "modules.forms_midwife.midwife_patient_file_form",
    "modules.forms_midwife.midwife_patienta_alerts_form",
    "modules.forms_midwife.midwife_patient_management_form",
    "modules.forms_midwife.midwife_portogram_form",
    "modules.forms_midwife.midwife_post_partum_follow_up_form",
    "modules.forms_midwife.midwife_pregnancy_tracking_form",
    "modules.forms_midwife.midwife_prenatal_care_form",
    "modules.forms_midwife.midwife_postanata_care_form",
    "modules.forms_midwife.midwife_prenatal_consultation_form",
    "modules.forms_midwife.midwife_prenatal_follow_up_form",
    "modules.forms_midwife.midwife_profile_form",
    # Bloc 2
    "modules.forms_midwife.midwife_resume_data_recorded_form",
    "modules.forms_midwife.midwife_throughout_midwifery_care_form",
    "modules.forms_midwife.midwife_visit_history_form",
    "modules.forms_midwife.midwife_workshops_form",
]


def test_import_and_render(module_name: str):
    """Teste l'import et la présence des fonctions décorées dans un module donné."""
    try:
        module = importlib.import_module(module_name)
        st.success(f"✅ Import réussi : {module_name}")
        render_functions = [
            attr
            for attr in dir(module)
            if attr.startswith("render_") and attr.endswith("_form")
        ]
        if render_functions:
            st.write(f"➡️ Fonctions de rendu trouvées : {render_functions}")
        else:
            st.warning(f"Aucune fonction render_*_form trouvée dans {module_name}")
    except Exception as e:
        st.error(f"❌ Erreur lors du test de {module_name}: {e}")


def main():
    st.title("🧑‍🍼 Tests des formulaires MIDWIFE")
    st.markdown(
        "Ce panneau permet de diagnostiquer les modules sages-femmes disponibles dans le dashboard."
    )
    for form_module in MIDWIFE_FORMS:
        test_import_and_render(form_module)


# ==============================================================================
# 🧩 Wrapper décoré pour le dashboard
# ==============================================================================
@register_form(
    "Tests des formulaires MIDWIFE",
    role="MIDWIFE",
    icon="🧑‍🍼",
    description="Outil de diagnostic pour vérifier les formulaires sages-femmes disponibles",
)
def render_midwife_form_test_suite():
    main()


# ==============================================================================
# 🧪 Fonction de test autonome
# ==============================================================================
def render_form():
    """Fonction autonome pour lancer le test des formulaires MIDWIFE."""
    st.set_page_config(layout="wide", page_title="Test Formulaires MIDWIFE")
    main()


# --- Exécution pour test autonome ---
if __name__ == "__main__":
    render_form()
