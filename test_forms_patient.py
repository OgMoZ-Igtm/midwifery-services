# Fichier : test_forms_patient.py
import streamlit as st
import importlib
import inspect
import pandas as pd
import pathlib


# ============================================================================
# 📋 Détection automatique des modules de formulaires PATIENT
# ============================================================================
def discover_patient_modules(base_path="modules"):
    modules = []
    base = pathlib.Path(base_path)
    role_dir = base / "forms_patient"
    if role_dir.exists():
        for py_file in role_dir.glob("*_form.py"):
            rel_path = py_file.relative_to(base).with_suffix("")
            module_name = ".".join([base_path] + list(rel_path.parts))
            modules.append(module_name)
    return modules


PATIENT_MODULES = discover_patient_modules()


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
st.title("🔎 Diagnostic et test automatique des formulaires PATIENT")

results_all = []

for module_name in PATIENT_MODULES:
    res = diagnose_module(module_name)
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
    "📥 Exporter diagnostic en CSV", csv, file_name="diagnostic_forms_patient.csv"
)
