# ⚠️ import cassé : os
# ⚠️ import cassé : re


def scan_streamlit_files(base_path="modules"):
    rerun_issues = []
    session_state_issues = []
    button_key_issues = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()

                # 🔄 Rerun sans condition
                if "st.rerun()" in code:
                    if not re.search(
                        r"if\s+st\.button\(.+?\):\s+.*?st\.rerun\(\)", code, re.DOTALL
                    ):
                        rerun_issues.append(path)

                # 🧠 Session state écrasé
                session_state_matches = re.findall(
                    r"st\.session_state\.(\w+)\s*=", code
                )
                for var in session_state_matches:
                    if f'if "{var}" not in st.session_state' not in code:
                        session_state_issues.append((path, var))

                # 🔘 Boutons sans clé
                button_matches = re.findall(r"st\.button\(([^)]+)\)", code)
                for match in button_matches:
                    if "key=" not in match:
                        button_key_issues.append((path, match))

    return rerun_issues, session_state_issues, button_key_issues


def print_report():
    rerun_issues, session_state_issues, button_key_issues = scan_streamlit_files()

    print("🔄 Rerun sans condition :")
    for path in rerun_issues:
        print(f"  - {path}")

    print("\n🧠 Session state écrasé sans vérification :")
    for path, var in session_state_issues:
        print(f"  - {path} → `{var}`")

    print("\n🔘 Boutons sans clé :")
    for path, btn in button_key_issues:
        print(f"  - {path} → {btn}")


if __name__ == "__main__":
    print_report()
