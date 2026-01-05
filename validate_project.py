import ast
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FILES_TO_VALIDATE = ["constants.py", "utils.py", "App_New_Version.py"]

FORBIDDEN_IN_CONSTANTS = [
    "st.",
    "streamlit",
    "requests",
    "def ",
    "import ",
    "from ",
    "=",
    "get(",
]


def check_undefined_variables(tree, filename):
    errors = []
    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined.add(target.id)
        elif isinstance(node, ast.Name):
            if (
                isinstance(node.ctx, ast.Load)
                and node.id not in defined
                and not isinstance(node.ctx, ast.Store)
            ):
                errors.append(
                    f"[{filename}] ❌ Variable '{node.id}' used before definition (line {node.lineno})"
                )
    return errors


def check_forbidden_constants_code(filepath):
    errors = []
    if "constants.py" in filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                for forbidden in FORBIDDEN_IN_CONSTANTS:
                    if forbidden in line and not line.strip().startswith("#"):
                        errors.append(
                            f"[constants.py] ❌ Forbidden usage '{forbidden}' on line {i}: {line.strip()}"
                        )
    return errors


def validate_file(filepath):
    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
        errors += check_undefined_variables(tree, filepath)
        errors += check_forbidden_constants_code(filepath)
    except Exception as e:
        errors.append(f"[{filepath}] ❌ Parsing error: {e}")
    return errors


def run_validation():
    all_errors = []
    for filename in FILES_TO_VALIDATE:
        path = os.path.join(PROJECT_ROOT, filename)
        if os.path.exists(path):
            all_errors += validate_file(path)
        else:
            all_errors.append(f"[{filename}] ⚠️ File not found.")
    return all_errors


def main():
    all_errors = []
    for filename in FILES_TO_VALIDATE:
        path = os.path.join(PROJECT_ROOT, filename)
        if os.path.exists(path):
            all_errors += validate_file(path)
        else:
            all_errors.append(f"[{filename}] ⚠️ File not found.")
    if all_errors:
        print("🚨 Problèmes détectés :")
        for err in all_errors:
            print(err)
    else:
        print(
            "✅ Aucun problème détecté. Ton projet est propre comme un ciel d’hiver à Waskaganish."
        )


if __name__ == "__main__":
    main()
