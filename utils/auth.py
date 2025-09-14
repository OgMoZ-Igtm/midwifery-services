import sqlite3
import time
import streamlit as st
from functools import wraps  # Important pour les décorateurs !


def get_user_role(username):
    """Récupère le rôle d'un utilisateur depuis la base de données."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def has_permission(username, page):
    """Vérifie si un utilisateur a la permission d'accéder à une page."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT can_access FROM permissions WHERE username = ? AND page = ?",
        (username, page),
    )
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1


def authenticated():
    """Vérifie l'état d'authentification de l'utilisateur."""
    return st.session_state.get("authenticated", False)


def logout():
    """Déconnecte l'utilisateur et réinitialise la session."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None
    st.info("Déconnexion réussie ! Redirection vers la page de connexion.")
    time.sleep(1)
    st.rerun()
