# 📋 audit_forms_modules.py — Diagnostic des modules de formulaires

import os
import ast
import traceback

BASE_DIR = "modules/forms"


def audit_python_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source, filename=path)
        return None  # OK
    except Exception as e:
        return f"{type(e).__name__} in {path}: {e}"


def audit_forms_modules():
    print("🔍 Audit des modules de formulaires...\n")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                error = audit_python_file(full_path)
                if error:
                    print(f"⚠️ {error}")
    print("\n✅ Audit terminé.")


if __name__ == "__main__":
    audit_forms_modules()
