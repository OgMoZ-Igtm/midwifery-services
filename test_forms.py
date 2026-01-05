# test_forms.py
import streamlit as st
import importlib
import inspect
import pandas as pd
import pathlib


# ============================================================================
# 📋 Détection automatique des modules de formulaires
# ============================================================================
def discover_form_modules(base_path="modules"):
    modules = {}
    base = pathlib.Path(base_path)
    for role_dir in base.glob("forms_*"):  # ex: forms_midwife, forms_doctor...
        role = role_dir.name.replace("forms_", "").upper()
        modules[role] = []
        for py_file in role_dir.glob("*_form.py"):
            # Construire le chemin importable : modules.forms_midwife.form_postnatal_care
            rel_path = py_file.relative_to(base).with_suffix("")
            module_name = ".".join([base_path] + list(rel_path.parts))
            modules[role].append(module_name)
    return modules


FORM_MODULES = discover_form_modules()


# ============================================================================
# 🔍 Fonction de diagnostic
# ============================================================================
def diagnose_module(module_name):
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        return {"module": module_name, "status": "❌ ImportError", "details": str(e)}

    has_render_form = hasattr(mod, "render_form") and inspect.isfunction(
        mod.render_form
    )
    render_functions = [
        name
        for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if name.startswith("render_") and name != "render_form"
    ]

    if not has_render_form and not render_functions:
        return {"module": module_name, "status": "❌ Aucun render_form ni render_*"}
    elif not has_render_form:
        return {
            "module": module_name,
            "status": "⚠️ Pas de render_form",
            "details": f"Wrappers: {render_functions}",
        }
    elif not render_functions:
        return {
            "module": module_name,
            "status": "⚠️ Pas de render_*",
            "details": "Seulement render_form",
        }
    else:
        return {
            "module": module_name,
            "status": "✅ OK",
            "details": f"Wrappers: {render_functions}",
        }


# ============================================================================
# 🚀 Interface Streamlit
# ============================================================================
st.title("🔎 Diagnostic et test automatique des formulaires")

results_all = []

for role, modules in FORM_MODULES.items():
    st.header(f"{role} Forms")
    for module_name in modules:
        res = diagnose_module(module_name)
        res["role"] = role
        results_all.append(res)

        st.write(f"- {res['module']} → {res['status']}")
        if "details" in res:
            st.caption(res["details"])

        # Bouton pour tester visuellement
        if res["status"].startswith("✅") or res["status"].startswith("⚠️"):
            try:
                mod = importlib.import_module(module_name)
                render_functions = [
                    name
                    for name, obj in inspect.getmembers(mod, inspect.isfunction)
                    if name.startswith("render_") and name != "render_form"
                ]
                for fn_name in render_functions:
                    if st.button(f"▶️ Tester {fn_name}", key=f"{module_name}_{fn_name}"):
                        getattr(mod, fn_name)()
            except Exception as e:
                st.error(f"Erreur lors du test de {module_name}: {e}")

# ============================================================================
# 📤 Export CSV
# ============================================================================
df = pd.DataFrame(results_all)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Exporter diagnostic en CSV", csv, file_name="diagnostic_forms.csv"
)
