import streamlit as st
import importlib
import os

def load_form_functions(module_path):
    form_funcs = {}
    try:
        for filename in os.listdir(module_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{module_path.replace('/', '.')}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    if attr.startswith("render_"):
                        form_funcs[attr] = getattr(module, attr)
    except Exception:
        pass
    return form_funcs

def render_sidebar_forms():
    role = st.session_state.permissions.get("role", "guest")
    specific_path = f"modules/forms/forms_{role}"
    shared_path = "modules/forms/forms_shared"

    specific_forms = load_form_functions(specific_path)
    shared_forms = load_form_functions(shared_path)

    selected_specific = st.sidebar.selectbox("📌 Formulaires spécifiques", list(specific_forms.keys()))
    selected_shared = st.sidebar.selectbox("🤝 Formulaires partagés", list(shared_forms.keys()))

    st.markdown("## Formulaire sélectionné")
    if selected_specific:
        specific_forms[selected_specific]()
    if selected_shared:
        shared_forms[selected_shared]()