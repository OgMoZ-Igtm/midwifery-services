import os

BASE_DIR = "modules/forms"
ROLES = ["midwife", "nurse", "admin", "public"]  # adapte selon tes rôles

def collect_render_functions():
    imports = []
    for role in ROLES:
        role_path = os.path.join(BASE_DIR, role)
        if not os.path.isdir(role_path):
            continue
        for filename in os.listdir(role_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                import_path = f"modules.forms.{role}.{module_name}"
                imports.append(f"from {import_path} import render_form as render_{module_name}")
    return imports

if __name__ == "__main__":
    lines = collect_render_functions()
    print("\n".join(lines))
