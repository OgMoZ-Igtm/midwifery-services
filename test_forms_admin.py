# -*- coding: utf-8 -*-
# Fichier : test_forms_admin.py
# Objectif : Vérifier l'import et le rendu des formulaires ADMIN

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

# ✅ Liste complète des modules ADMIN à tester
ADMIN_FORMS = [
    "modules.forms_admin.admin_access_audit_log_form",
    "modules.forms_admin.admin_model_configuration_form",
    "modules.forms_admin.admin_statistical_report_form",
    "modules.forms_admin.admin_user_role_management_form",
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
    st.title("🛠️ Tests des formulaires ADMIN")
    st.markdown(
        "Ce panneau permet de diagnostiquer les modules administratifs disponibles dans le dashboard."
    )
    for form_module in ADMIN_FORMS:
        test_import_and_render(form_module)


# ==============================================================================
# 🧩 Wrapper décoré pour le dashboard
# ==============================================================================
@register_form(
    "Tests des formulaires ADMIN",
    role="ADMIN",
    icon="🛡️",
    description="Outil de diagnostic pour vérifier les formulaires administratifs disponibles",
)
def render_admin_form_test_suite():
    main()


# ==============================================================================
# 🧪 Fonction de test autonome
# ==============================================================================
def render_form():
    """Fonction autonome pour lancer le test des formulaires ADMIN."""
    st.set_page_config(layout="wide", page_title="Test Formulaires ADMIN")
    main()


# --- Exécution pour test autonome ---
if __name__ == "__main__":
    render_form()
