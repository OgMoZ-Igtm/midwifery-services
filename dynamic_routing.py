import importlib
import os


def load_public_render_functions():
    base_path = "modules.forms.public"
    folder = os.path.join("modules", "forms", "public")
    routing_map = {}

    for filename in os.listdir(folder):
        if filename.startswith("form_") and filename.endswith(".py"):
            module_name = filename[:-3]
            import_path = f"{base_path}.{module_name}"
            try:
                module = importlib.import_module(import_path)
                func = getattr(module, "render", None)
                if callable(func):
                    routing_map[module_name] = func
            except Exception as e:
                print(f"⚠️ Erreur d'import {module_name} : {e}")

    return routing_map


# Et, après le lancement :
# Dans chaque fichier public _ form_faq, form_links.py
# def render():
#     import streamlit as st
#     st.markdown("## 📚 FAQ")
#     st.info("Voici les questions les plus fréquentes...")


# Ce script Python va :
# - Créer la nouvelle structure forms/specific/…
# - Déplacer les fichiers existants dans les bons dossiers
# - Supprimer les fichiers redondants (forms_admin.py, .pyc, etc.)
# - Te laisser un log clair des actions effectuée
