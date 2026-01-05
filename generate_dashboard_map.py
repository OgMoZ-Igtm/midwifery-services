# ⚠️ import cassé : os

DASHBOARD_DIR = "modules/forms/dashboards"
output_path = "modules/forms/dashboard_map.py"

dashboard_map = {}
imports = []

for filename in os.listdir(DASHBOARD_DIR):
    if filename.startswith("dashboard_") and filename.endswith(".py"):
        role = filename.replace("dashboard_", "").replace(".py", "")
        alias = f"run_{role}"
        module_path = f"modules.forms.dashboards.{filename[:-3]}"
        imports.append(f"from {module_path} import run as {alias}")
        dashboard_map[role] = alias

with open(output_path, "w", encoding="utf-8") as f:
    f.write("# 🔄 Auto-generated dashboard map\n\n")
    for line in imports:
        f.write(line + "\n")
    f.write("\nDASHBOARD_MAP = {\n")
    for role, alias in dashboard_map.items():
        f.write(f'    "{role}": {alias},\n')
    f.write("}\n")

print("✅ DASHBOARD_MAP généré dans dashboard_map.py")
