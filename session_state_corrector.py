# ⚠️ import cassé : os
# ⚠️ import cassé : re


def correct_session_state_assignments(base_path="modules"):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                new_lines = []
                modified = False
                seen_vars = set()

                for i, line in enumerate(lines):
                    match = re.match(r"(\s*)st\.session_state\.(\w+)\s*=\s*(.+)", line)
                    if match:
                        indent, var, value = match.groups()
                        if var not in seen_vars:
                            seen_vars.add(var)
                            new_lines.append(
                                f'{indent}if "{var}" not in st.session_state:\n'
                            )
                            new_lines.append(
                                f"{indent}    st.session_state.{var} = {
                                    value.strip()}\n"
                            )
                            modified = True
                        else:
                            new_lines.append(line)  # déjà corrigé ailleurs
                    else:
                        new_lines.append(line)

                if modified:
                    with open(path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"✅ Corrigé : {path}")


if __name__ == "__main__":
    correct_session_state_assignments()
