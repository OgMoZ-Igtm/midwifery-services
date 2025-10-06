import subprocess
import streamlit as st


def get_git_branch():
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode()
            .strip()
        )
    except Exception:
        return "inconnu"


def get_last_commit():
    try:
        return (
            subprocess.check_output(
                ["git", "log", "-1", "--pretty=format:%h • %s (%cr)"]
            )
            .decode()
            .strip()
        )
    except Exception:
        return "aucun commit"


def display_deployment_status():
    branch = get_git_branch()
    commit = get_last_commit()
    role = (
        st.session_state.permissions.get("role", "non défini")
        if "permissions" in st.session_state
        else "non défini"
    )
    st.caption(f"🚀 Branche : `{branch}` — 🧬 Commit : {commit} — 🔐 Rôle : `{role}`")
