import streamlit as st
import importlib
import inspect
import pandas as pd
import pathlib


# ============================================================================
# 📋 Détection automatique des modules de formulaires
# ============================================================================
def discover_form_modules(base_path="modules"):
    """
    Découvre et liste les modules de formulaires basés sur la structure du dossier.
    Ex: modules/forms_midwife/form_postnatal_care.py
    """
    modules = {}
    base = pathlib.Path(base_path)
    # Cherche les dossiers de rôle (ex: forms_midwife)
    for role_dir in base.glob("forms_*"):
        role = role_dir.name.replace("forms_", "").upper()
        modules[role] = []
        # Cherche les fichiers de formulaire (ex: *_form.py)
        for py_file in role_dir.glob("*_form.py"):
            # Construit le chemin d'importation : modules.forms_midwife.form_postnatal_care
            rel_path = py_file.relative_to(base).with_suffix("")
            # Utilise .as_posix() pour s'assurer que les séparateurs sont des points sur tous les OS
            module_name = ".".join([base_path] + list(rel_path.parts))
            modules[role].append(module_name)
    return modules


FORM_MODULES = discover_form_modules()


# ============================================================================
# 🔍 Fonction de diagnostic
# ============================================================================
def diagnose_module(module_name):
    """Diagnostique la présence des fonctions attendues dans un module."""
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        # Erreur d'importation fatale
        return {"module": module_name, "status": "❌ ImportError", "details": str(e)}

    # Vérifie la présence de render_form
    has_render_form = hasattr(mod, "render_form") and inspect.isfunction(
        mod.render_form
    )

    # Liste toutes les fonctions 'wrapper' render_*
    render_functions = [
        name
        for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if name.startswith("render_") and name != "render_form"
    ]

    details = (
        f"Wrappers: {', '.join(render_functions) if render_functions else 'Aucun'}"
    )

    # Détermine le statut
    if not has_render_form and not render_functions:
        status = "❌ Aucun render_form ni render_*"
    elif not has_render_form:
        status = "⚠️ Pas de render_form"
    elif not render_functions:
        status = "⚠️ Pas de render_*"
        details = "Seulement render_form"
    else:
        status = "✅ OK"

    return {
        "module": module_name,
        "status": status,
        "details": details,
        "render_functions": render_functions,  # Ajout pour l'étape de test
    }


# ============================================================================
# 🚀 Interface Streamlit
# ============================================================================
st.set_page_config(layout="wide")
st.title("🔎 Diagnostic et test automatique des formulaires")
st.markdown("---")

results_all = []

for role, modules in FORM_MODULES.items():
    st.header(f"🗂️ Rôle : {role}")
    col1, col2 = st.columns([1, 4])  # 1 pour le module, 4 pour les détails et tests

    # Tableau pour afficher les résultats
    df_role_results = []

    for module_name in modules:
        res = diagnose_module(module_name)
        res["role"] = role
        results_all.append(res)

        # Affichage du diagnostic dans la première colonne
        with col1:
            st.markdown(f"**{res['module'].split('.')[-1]}**")
            st.markdown(f"`{res['status']}`", help=res.get("details", ""))

        # Section de test visuel dans la deuxième colonne
        with col2:
            # Nous extrayons toujours les fonctions pour le test
            render_functions_to_test = res.get("render_functions", [])

            if render_functions_to_test:
                try:
                    # Tente d'importer le module pour les tests, seulement si des fonctions render existent
                    mod = importlib.import_module(module_name)

                    # Conteneur pour les boutons de test
                    button_cols = st.columns(len(render_functions_to_test) + 1)

                    # Stocker la fonction sélectionnée
                    selected_fn = None

                    # Génère un bouton pour chaque fonction render_*
                    for i, fn_name in enumerate(render_functions_to_test):
                        with button_cols[i]:
                            if st.button(
                                f"▶️ Test {fn_name}", key=f"{module_name}_{fn_name}"
                            ):
                                selected_fn = fn_name

                    # Si une fonction a été sélectionnée, on l'appelle dans un expander
                    if selected_fn:
                        st.subheader(f"Test en cours: `{selected_fn}`")
                        st.info(
                            f"Le formulaire `{module_name}` est affiché ci-dessous dans le contexte de `{selected_fn}`."
                        )

                        # Utiliser un conteneur pour isoler l'affichage du formulaire
                        with st.expander("Affichage du formulaire", expanded=True):
                            # Appel de la fonction de rendu (le cœur du test)
                            getattr(mod, selected_fn)()
                        st.markdown("---")

                except Exception as e:
                    st.error(
                        f"Erreur fatale lors de l'exécution du test pour {module_name}: {e}"
                    )
            else:
                st.caption(res.get("details", "Pas de fonctions 'render' à tester."))

        st.markdown("---")  # Séparateur visuel entre les modules

st.markdown("## 📊 Récapitulatif Global")

# ============================================================================
# 📤 Export CSV
# ============================================================================
if results_all:
    df = pd.DataFrame(results_all)
    # Nettoyer les colonnes avant l'affichage/export
    df = df.drop(columns=["render_functions"], errors="ignore")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Exporter diagnostic en CSV", csv, file_name="diagnostic_forms.csv"
    )
else:
    st.warning(
        "Aucun module de formulaire trouvé dans le dossier 'modules' (forms_*/*_form.py)."
    )
