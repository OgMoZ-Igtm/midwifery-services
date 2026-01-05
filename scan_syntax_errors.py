import os
import ast

ROOT_DIR = "modules"
TARGET_EXT = ".py"
errors = []


def scan_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
    except SyntaxError as e:
        errors.append((path, f"{e.msg} (ligne {e.lineno})"))
    except Exception as e:
        errors.append((path, str(e)))


def scan_all():
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(TARGET_EXT):
                scan_file(os.path.join(root, file))


if __name__ == "__main__":
    scan_all()
    print("\n📋 Fichiers avec erreurs de syntaxe ou d'import :")
    for path, err in errors:
        print(f"❌ {path} → {err}")
    print(f"\n🔢 Total : {len(errors)} fichiers à corriger.")
