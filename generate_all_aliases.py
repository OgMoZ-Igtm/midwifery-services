# generate_all_aliases.py
# ⚠️ import cassé : os

MODULES_DIR = "modules"
PAGES_DIR = "pages"

os.makedirs(PAGES_DIR, exist_ok=True)

for root, _, files in os.walk(MODULES_DIR):
    for file in files:
        if file.startswith("form_") and file.endswith(".py"):
            module_path = os.path.join(root, file)
            import_path = module_path.replace("/", ".").replace(".py", "")
            alias_path = os.path.join(PAGES_DIR, file)

            alias_code = f"""# Auto-generated alias for Streamlit
from {import_path} import render_form

render_form()
"""

            with open(alias_path, "w", encoding="utf-8") as f:
                f.write(alias_code)

print("✅ Tous les alias ont été générés dans le dossier pages/")
