import streamlit as st
import bcrypt
import re
import sqlite3
import os
import json
import time
from datetime import datetime, timedelta

# --- Fonctions utilitaires ---

# Crée le répertoire 'data' si il n'existe pas.
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def create_users_table():
    """Crée la table des utilisateurs si elle n'existe pas."""
    conn = sqlite3.connect(os.path.join(DATA_DIR, "users.db"))
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def load_persistent_data():
    """
    Charge les données de la dernière connexion et de verrouillage
    depuis un fichier JSON. Les dates sont converties en objets datetime.
    """
    login_data_path = os.path.join(DATA_DIR, "user_data.json")
    if os.path.exists(login_data_path):
        with open(login_data_path, "r") as f:
            data = json.load(f)
            # Conversion des chaînes de date ISO en objets datetime
            for email, user_info in data.items():
                if (
                    "last_login" in user_info
                    and user_info["last_login"] != "non enregistrée"
                ):
                    user_info["last_login"] = datetime.fromisoformat(
                        user_info["last_login"]
                    )
                if "locked_out_until" in user_info and user_info["locked_out_until"]:
                    user_info["locked_out_until"] = datetime.fromisoformat(
                        user_info["locked_out_until"]
                    )
            return data
    return {}


def save_persistent_data(data):
    """
    Sauvegarde les données de la dernière connexion et de verrouillage
    dans un fichier JSON. Les objets datetime sont convertis en chaînes de date ISO.
    """
    login_data_path = os.path.join(DATA_DIR, "user_data.json")
    data_to_save = data.copy()
    for email, user_info in data_to_save.items():
        if "last_login" in user_info and isinstance(user_info["last_login"], datetime):
            user_info["last_login"] = user_info["last_login"].isoformat()
        if "locked_out_until" in user_info and isinstance(
            user_info["locked_out_until"], datetime
        ):
            user_info["locked_out_until"] = user_info["locked_out_until"].isoformat()

    with open(login_data_path, "w") as f:
        json.dump(data_to_save, f, indent=4)


def verifier_robustesse_mdp(password):
    """Vérifie la robustesse du mot de passe."""
    if len(password) < 8:
        return "Le mot de passe doit contenir au moins 8 caractères."
    if not re.search(r"[A-Z]", password):
        return "Le mot de passe doit contenir au moins une lettre majuscule."
    if not re.search(r"[a-z]", password):
        return "Le mot de passe doit contenir au moins une lettre minuscule."
    if not re.search(r"\d", password):
        return "Le mot de passe doit contenir au moins un chiffre."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Le mot de passe doit contenir au moins un caractère spécial."
    return None


# --- Fonction principale de l'interface ---


def login_form():
    """Affiche l'interface de connexion et d'inscription."""

    for key, default in {
        "logged_in": False,
        "user_info": None,
        "last_login": "non enregistrée",
        "role": "GUEST",
        "login_ui_rendered": False,
        "prenom": "Guest",
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    if "persistent_user_data" not in st.session_state:
        st.session_state["persistent_user_data"] = load_persistent_data()

    create_users_table()

    st.title("Page de Connexion / Inscription")

    # Choix du formulaire
    choix_form = st.radio(
        "Choisir une option :", ["Connexion", "Inscription"], key="choix_form_radio"
    )

    if not st.session_state.get("logged_in"):
        if choix_form == "Connexion":
            with st.form(key="form_connexion"):
                email = st.text_input("Adresse courriel")
                password = st.text_input("Mot de passe", type="password")
                submit_login = st.form_submit_button("Se connecter")

                if submit_login:
                    now = datetime.now()
                    user_data = st.session_state["persistent_user_data"].get(email, {})
                    locked_until = user_data.get("locked_out_until")

                    if locked_until and now < locked_until:
                        wait_time = int((locked_until - now).total_seconds())
                        st.error(
                            f"❌ Trop de tentatives échouées. Réessayez dans {wait_time} secondes."
                        )
                    else:
                        if email == "test@example.com" and password == "Test1234!":
                            user = {"prenom": "TestUser", "role": "ADMIN"}
                        else:
                            user = None

                        if user:
                            user_data["failed_attempts"] = 0
                            st.session_state["logged_in"] = True
                            st.session_state["user_info"] = user
                            st.session_state["role"] = user["role"]
                            st.session_state["prenom"] = user["prenom"]

                            last_login = user_data.get("last_login", "non enregistrée")
                            st.session_state["last_login"] = (
                                last_login.strftime("%A %d %B %Y à %H:%M")
                                if isinstance(last_login, datetime)
                                else last_login
                            )

                            user_data["last_login"] = now
                            st.session_state["persistent_user_data"][email] = user_data
                            save_persistent_data(
                                st.session_state["persistent_user_data"]
                            )

                            st.success(f"✅ Connexion réussie, {user['prenom']}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            user_data["failed_attempts"] = (
                                user_data.get("failed_attempts", 0) + 1
                            )
                            if user_data["failed_attempts"] >= 3:
                                user_data["locked_out_until"] = now + timedelta(
                                    minutes=5
                                )
                                st.error(
                                    "❌ Trop de tentatives échouées. Compte verrouillé pour 5 minutes."
                                )
                            else:
                                st.error("❌ Email ou mot de passe incorrect.")

                            st.session_state["persistent_user_data"][email] = user_data
                            save_persistent_data(
                                st.session_state["persistent_user_data"]
                            )

        elif choix_form == "Inscription":
            with st.form(key="form_inscription"):
                prenom = st.text_input("Votre prénom")
                email_reg = st.text_input("Adresse courriel")
                password_reg = st.text_input("Mot de passe", type="password")
                password_confirm = st.text_input(
                    "Confirmer le mot de passe", type="password"
                )
                role_reg = st.selectbox(
                    "Rôle",
                    [
                        "PATIENT",
                        "MIDWIFEE",
                        "NURSE",
                        "DOCTOR",
                        "ADMIN",
                        "STUDENT",
                        "INTERN",
                        "DOCTORAL",
                    ],
                )
                submit_reg = st.form_submit_button("S'inscrire")

                if submit_reg:
                    if (
                        not prenom
                        or not email_reg
                        or not password_reg
                        or not password_confirm
                    ):
                        st.warning("⚠️ Tous les champs sont obligatoires.")
                    elif password_reg != password_confirm:
                        st.error("❌ Les mots de passe ne correspondent pas.")
                    else:
                        erreur_mdp = verifier_robustesse_mdp(password_reg)
                        if erreur_mdp:
                            st.error(f"❌ {erreur_mdp}")
                        else:
                            try:
                                conn = sqlite3.connect(
                                    os.path.join(DATA_DIR, "users.db")
                                )
                                cursor = conn.cursor()
                                mot_de_passe_hash = bcrypt.hashpw(
                                    password_reg.encode("utf-8"), bcrypt.gensalt()
                                ).decode()
                                cursor.execute(
                                    """
                                    INSERT INTO users (prenom, email, mot_de_passe_hash, role)
                                    VALUES (?, ?, ?, ?)
                                    """,
                                    (prenom, email_reg, mot_de_passe_hash, role_reg),
                                )
                                conn.commit()

                                st.session_state["logged_in"] = True
                                st.session_state["prenom"] = prenom
                                st.session_state["role"] = role_reg
                                st.session_state["user_info"] = {
                                    "prenom": prenom,
                                    "role": role_reg,
                                }

                                st.success(
                                    "✅ Compte créé avec succès. Redirection en cours..."
                                )
                                time.sleep(1)
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("⚠️ Cet email est déjà utilisé.")
                            except Exception as e:
                                st.error(
                                    f"❌ Erreur lors de la création du compte : {e}"
                                )
                            finally:
                                conn.close()
    else:
        st.success(
            f"Vous êtes déjà connecté(e), {st.session_state.get('prenom', 'Guest')}!"
        )
        st.write("Vous pouvez ajouter d'autres éléments d'interface utilisateur ici.")

        if st.button("Se déconnecter"):
            for key in ["logged_in", "user_info", "last_login", "role", "prenom"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
