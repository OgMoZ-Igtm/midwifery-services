# generate_page_aliases.py
# ⚠️ import cassé : os

MODULES_DIR = "modules/forms"
PAGES_DIR = "pages"

for root, _, files in os.walk(MODULES_DIR):
    for file in files:
        if file.startswith("form_") and file.endswith(".py"):
            module_path = os.path.join(root, file).replace("/", ".").replace(".py", "")
            alias_path = os.path.join(PAGES_DIR, file)
            with open(alias_path, "w", encoding="utf-8") as f:
                f.write(f"from {module_path} import render_form\n\nrender_form()\n")
