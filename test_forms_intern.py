# -*- coding: utf-8 -*-
# Fichier : test_forms_intern.py
# Objectif : Vérifier l'import et le rendu des formulaires INTERN

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

# ✅ Liste complète des modules INTERN à tester
INTERN_FORMS = [
    "modules.forms_intern.intern_daily_progress_soap_form",
    "modules.forms_intern.intern_dashboard_logbook_ob_form",
    "modules.forms_intern.intern_delivery_exams_follow_up_ob_form",
    "modules.forms_intern.intern_delivery_report_ob_form",
    "modules.forms_intern.intern_draft_order_ob_form",
    "modules.forms_intern.intern_initial_assessment_ob_form",
    "modules.forms_intern.intern_skill_checklist_form",
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
    st.title("🩺 Tests des formulaires INTERN")
    st.markdown(
        "Ce panneau permet de diagnostiquer les modules internes disponibles dans le dashboard."
    )
    for form_module in INTERN_FORMS:
        test_import_and_render(form_module)


# ==============================================================================
# 🧩 Wrapper décoré pour le dashboard
# ==============================================================================
@register_form(
    "Tests des formulaires INTERN",
    role="INTERN",
    icon="🩺",
    description="Outil de diagnostic pour vérifier les formulaires internes disponibles",
)
def render_intern_form_test_suite():
    main()


# ==============================================================================
# 🧪 Fonction de test autonome
# ==============================================================================
def render_form():
    """Fonction autonome pour lancer le test des formulaires INTERN."""
    st.set_page_config(layout="wide", page_title="Test Formulaires INTERN")
    main()


# --- Exécution pour test autonome ---
if __name__ == "__main__":
    render_form()
