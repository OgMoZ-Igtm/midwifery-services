import os
import re

ROOT_DIR = "modules"
TARGET_EXT = ".py"
SUPABASE_PATTERNS = [
    r"supabase\.table\(",
    r"supabase\.select\(",
    r"supabase\.insert\(",
    r"supabase\.update\(",
    r"supabase\.delete\(",
    r"supabase\.execute\(",
]
GUARD_BLOCK = (
    'if not supabase:\n    st.warning("⚠️ Supabase est désactivé.")\n    return\n'
)

modified_files = []


def inject_guard_in_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    injected = False
    inside_function = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("def ") and stripped.endswith(":"):
            inside_function = True
            new_lines.append(line)
            continue

        if inside_function and any(re.search(p, stripped) for p in SUPABASE_PATTERNS):
            indent = line[: len(line) - len(stripped)]
            new_lines.append(f"{indent}{GUARD_BLOCK}")
            injected = True
            inside_function = False
            new_lines.append(line)
        else:
            new_lines.append(line)

    if injected:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        modified_files.append(path)
        print(f"✅ Bloc injecté dans : {path}")


def scan_and_inject():
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(TARGET_EXT):
                path = os.path.join(root, file)
                inject_guard_in_file(path)


def generate_report():
    print("\n📋 Rapport des fichiers modifiés :")
    for path in modified_files:
        print(f"🌿 {path}")
    print(
        f"\n✅ Total : {len(modified_files)} fichiers protégés contre Supabase désactivé."
    )


# 📝 Génération du rapport pour le tableau Streamlit
with open("inject_supabase_guard_report.txt", "w", encoding="utf-8") as f:
    for path in modified_files:
        f.write(f"🌿 {path}\n")


if __name__ == "__main__":
    scan_and_inject()
    generate_report()
