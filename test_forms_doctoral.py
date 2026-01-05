# -*- coding: utf-8 -*-
# Fichier : test_forms_doctoral.py
# Objectif : Vérifier l'import et le rendu des formulaires DOCTORAL

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

# ✅ Liste complète des modules DOCTORAL à tester
DOCTORAL_FORMS = [
    "modules.forms_doctoral.doctoral_data_extraction_form",
    "modules.forms_doctoral.doctoral_research_consent_form",
    "modules.forms_doctoral.doctoral_thesis_report_form",
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
    st.title("📘 Tests des formulaires DOCTORAL")
    st.markdown(
        "Ce panneau permet de diagnostiquer les modules doctoraux disponibles dans le dashboard."
    )
    for form_module in DOCTORAL_FORMS:
        test_import_and_render(form_module)


# ==============================================================================
# 🧩 Wrapper décoré pour le dashboard
# ==============================================================================
@register_form(
    "Tests des formulaires DOCTORAL",
    role="DOCTORAL",
    icon="📘",
    description="Outil de diagnostic pour vérifier les formulaires doctoraux disponibles",
)
def render_doctoral_form_test_suite():
    main()


# ==============================================================================
# 🧪 Fonction de test autonome
# ==============================================================================
def render_form():
    """Fonction autonome pour lancer le test des formulaires DOCTORAL."""
    st.set_page_config(layout="wide", page_title="Test Formulaires DOCTORAL")
    main()


# --- Exécution pour test autonome ---
if __name__ == "__main__":
    render_form()
