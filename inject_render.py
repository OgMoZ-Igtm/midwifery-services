import os

BASE_DIR = "packs"


def format_title(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ")
    return name.title()


def inject_render_function(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "def render(" in content:
        print(f"✅ {file_path} contient déjà render()")
        return

    title = format_title(os.path.basename(file_path))
    render_code = f"""
def render():
    import streamlit as st
    st.title("📄 {title}")
    st.info("Ce formulaire n’a pas encore été implémenté.")
"""

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + render_code.strip() + "\n")

    print(f"✨ render() injecté dans {file_path}")


def scan_and_inject():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                inject_render_function(file_path)


if __name__ == "__main__":
    scan_and_inject()
