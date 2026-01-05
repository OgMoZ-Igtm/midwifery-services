# ⚠️ import cassé : os
# ⚠️ import cassé : re


def correct_missing_colons(base_path="modules"):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                new_lines = []
                modified = False

                for line in lines:
                    # Corrige les if sans deux-points
                    match = re.match(r"(\s*)if\s+(.*)\s*(?<!:)\s*$", line)
                    if match and not line.strip().endswith(":"):
                        indent, condition = match.groups()
                        new_line = f"{indent}if {condition.strip()}:\n"
                        new_lines.append(new_line)
                        modified = True
                    else:
                        new_lines.append(line)

                if modified:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"✅ Corrigé : {path}")


if __name__ == "__main__":
    correct_missing_colons()
