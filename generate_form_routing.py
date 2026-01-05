import os

BASE_DIR = "modules/forms"
ROLES = ["midwife", "nurse", "admin", "public"]  # adapte selon tes rôles


def collect_render_functions():
    imports = []
    routing_map = []
    for role in ROLES:
        role_path = os.path.join(BASE_DIR, role)
        if not os.path.isdir(role_path):
            continue
        for filename in os.listdir(role_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                import_path = f"modules.forms.{role}.{module_name}"
                alias = f"render_{module_name}"
                imports.append(f"from {import_path} import render_form as {alias}")
                routing_map.append(f'    "{module_name}": {alias},')
    return imports, routing_map


if __name__ == "__main__":
    imports, routing_map = collect_render_functions()

    print("# ✅ Lignes d'import")
    print("\n".join(imports))
    print("\n# ✅ ROUTING_MAP")
    print("ROUTING_MAP = {\n" + "\n".join(routing_map) + "\n}")
