import os
import re
import ast

PACKS_DIR = "packs"
NAVIGATION_FILE = "utils/navigation.py"

# Ordre fixe
PACK_ORDER = [
    "ADMIN",
    "DOCTOR",
    "NURSE",
    "MIDWIFE",
    "PATIENT",
    "MESSAGES",
    "STUDENT",
    "DOCTORAL",
    "INTERN",
    "ORGANISATION",
]

# Permissions pack → rôles (même mapping que dans security.py)
PACK_PERMISSIONS = {
    "ADMIN": ["ADMIN"],
    "DOCTOR": ["DOCTOR", "ADMIN"],  # admin peut voir mais pas modifier
    "NURSE": ["NURSE", "MIDWIFE"],
    "MIDWIFE": ["MIDWIFE", "NURSE"],
    "PATIENT": ["PATIENT", "DOCTOR", "ADMIN"],
    "MESSAGES": [
        "ADMIN",
        "DOCTOR",
        "NURSE",
        "MIDWIFE",
        "PATIENT",
        "STUDENT",
        "DOCTORAL",
        "INTERN",
    ],
    "STUDENT": ["STUDENT"],
    "DOCTORAL": ["DOCTORAL"],
    "INTERN": ["INTERN"],
    "ORGANISATION": ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE"],
}


def sanitize_name(name):
    return os.path.splitext(name)[0].replace("_", " ")


def has_app_function(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
        return any(
            isinstance(node, ast.FunctionDef) and node.name == "app"
            for node in tree.body
        )
    except Exception:
        return False


def ensure_app_function(file_path):
    if not has_app_function(file_path):
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(
                "\n\n# Ajout automatique de la fonction app()\n"
                "def app():\n"
                "    import streamlit as st\n"
                f"    st.title('📄 {os.path.basename(file_path)}')\n"
                "    st.info('Page générée automatiquement, à compléter.')\n"
            )


def fix_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("navigation_controls", "display_menus")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def process_pack(pack_path):
    files = [
        f for f in os.listdir(pack_path) if f.endswith(".py") and not f.startswith("__")
    ]
    files.sort(key=lambda x: re.sub(r"^\d+_", "", x).lower())

    new_files = []
    for i, f in enumerate(files, start=1):
        prefix = f"{i:02d}_"
        base_name = re.sub(r"^\d+_", "", f)
        new_name = prefix + base_name

        old_path = os.path.join(pack_path, f)
        new_path = os.path.join(pack_path, new_name)

        if f != new_name:
            os.rename(old_path, new_path)
            print(f"✅ {f} → {new_name}")
            f = new_name
        else:
            print(f"⏩ Ignoré (déjà correct) : {f}")

        file_path = os.path.join(pack_path, f)
        fix_imports(file_path)
        ensure_app_function(file_path)

        new_files.append(f)

    return new_files


def update_navigation(all_packs):
    nav_code = [
        "import streamlit as st\n",
        "from utils.security import est_autorise\n",
        "\n",
        "def display_menus(role):\n",
        "    st.sidebar.title('📌 Navigation')\n",
        "\n",
    ]

    for pack in PACK_ORDER:
        if pack not in all_packs:
            continue

        files = all_packs[pack]
        nav_code.append(f"    if est_autorise(role, '{pack}'):\n")
        nav_code.append(
            f"        with st.sidebar.expander('📂 {pack.title()}', expanded=False):\n"
        )
        for f in files:
            page_name = sanitize_name(f)
            nav_code.append(
                f"            if st.button('{page_name}'):\n"
                f"                st.session_state.current_page = '{pack}.{f[:-3]}'\n"
                "                st.rerun()\n"
            )
        nav_code.append("\n")

    with open(NAVIGATION_FILE, "w", encoding="utf-8") as f:
        f.writelines(nav_code)

    print(f"✅ Navigation mise à jour dans {NAVIGATION_FILE}")


def main():
    all_packs = {}
    for pack in os.listdir(PACKS_DIR):
        pack_path = os.path.join(PACKS_DIR, pack)
        if os.path.isdir(pack_path):
            print(f"\n📦 Traitement du pack {pack}")
            new_files = process_pack(pack_path)
            all_packs[pack.upper()] = new_files
    update_navigation(all_packs)


if __name__ == "__main__":
    main()
