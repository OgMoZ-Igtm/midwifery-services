# -*- coding: utf-8 -*-
# Fichier : test_forms_student.py
# Objectif : Vérifier l'import et le rendu des formulaires STUDENT

import sys, os, importlib
import streamlit as st

# ✅ Ajout du chemin racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# ✅ Liste complète des modules STUDENT à tester
STUDENT_FORMS = [
    "modules.forms_student.student_academic_tracking_form",
    "modules.forms_student.student_case_study_form",
    "modules.forms_student.student_clinical_observations_ob_form",
    "modules.forms_student.student_competency_evaluations_ob_form",
    "modules.forms_student.student_course_feedback_form",
    "modules.forms_student.student_evaluations_form",
    "modules.forms_student.student_ob_dashboard_form",
    "modules.forms_student.student_stage_request_form",
    "modules.forms_student.student_supervision_ob_form",
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
    st.title("=== Tests des formulaires STUDENT ===")
    for form_module in STUDENT_FORMS:
        test_import_and_render(form_module)


if __name__ == "__main__":
    main()
