import os
import re

DECORATOR_PATTERN = re.compile(r"^@(\w+)")
FUNCTION_PATTERN = re.compile(r"^def (\w+)\(")

def auto_fix_decorators(base_path):
    report = []
    print("🧹 Correction automatique des décorateurs orphelins...\n")

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                new_lines = []
                skip_next = False
                for i, line in enumerate(lines):
                    if skip_next:
                        skip_next = False
                        continue

                    match = DECORATOR_PATTERN.match(line.strip())
                    if match:
                        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                        if not next_line.startswith("def "):
                            report.append(f"❌ Supprimé `@{match.group(1)}` dans {path}, ligne {i+1}")
                            continue  # skip this decorator line
                    new_lines.append(line)

                # Écriture si modification
                if len(new_lines) != len(lines):
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)

    with open("decorator_auto_fix_report.md", "w", encoding="utf-8") as f:
        f.write("# 🧾 Rapport de correction automatique des décorateurs\n\n")
        for line in report:
            f.write(f"{line}\n")

    print("✅ Correction terminée. Rapport : `decorator_auto_fix_report.md`")

if __name__ == "__main__":
    auto_fix_decorators("modules")
