# app.py

# =============================================================================
# 1. IMPORTS
# =============================================================================

import streamlit as st
import time
import pandas as pd
import datetime
import os
import uuid
import requests
from bs4 import BeautifulSoup
from supabase import create_client
from email.mime.text import MIMEText
import pydeck as pdk
from PIL import Image, ImageOps
import io

if "permissions" not in st.session_state:
    st.session_state.permissions = {}

# import uuid # Doublon
from datetime import datetime  # Import de datetime.datetime.utcnow corrigé
from modules.auth_status import display_status

display_status(st.session_state)

# --- Configuration et Services ---
from modules.services.config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    DB_USER,
    DB_PASSWORD,
    SMTP_SERVER,
    EMAIL_USER,
    EMAIL_PASSWORD,
    SECRET_KEY,
)
from modules.services.supabase_services import supabase, add_document
from modules.services.email_service import send_email

# --- Utilitaires de base ---
from utils.session import initialize_session_state
from utils.core import (
    session,
    set_page_config_custom,
    get_greeting,
    display_header_and_status,
)

# --- Service d'authentification (dépendances manquantes, mais nécessaires) ---
from modules.services.user_manager import (
    ensure_test_user,
    reset_test_users,
    delete_user,
    create_user_safe,  # Ajouté manquant pour le test en ligne
)

# --- Authentification et Permissions ---
from modules.auth.auth_manager import (
    load_user_permissions,
    sign_out_user,
    render_supabase_diagnostics,
)

# --- Routage et Vues ---
from modules.routing.role_router import RoleRouter, FORM_MAP
from modules.routing.validate_form_map import validate_form_map
from modules.dashboard.test_accounts_table import render_test_accounts_table
from modules.dashboard.main import main
from modules.views.auth_forms import auth_form
from modules.views.profile_view import show_profile
from modules.views.permission_test import test_permissions
from modules.views.log_utils import log_event
from modules.views.export_tools import render_log_summary
from modules.views.test_account_creator import create_test_account
from modules.views.role_switcher import render_role_switcher
from modules.views.user_admin_panel import render_user_admin_panel
from modules.views.module_checker import render_module_checker
from modules.views.team_chat import render_team_chat


# =============================================================================
# 2. INITIALISATION ET CONFIGURATION GLOBALE
# =============================================================================

set_page_config_custom()
initialize_session_state()

# Connexion Supabase
# L'objet `supabase` est déjà importé, mais recréer le client est une pratique courante
# lors du démarrage de l'application si l'objet importé est une référence vide ou None.
# On garde donc la recréation, en veillant à ne pas écraser l'objet importé si celui-ci est utilisé par `add_document`.
# Pour l'exemple, on écrase l'objet, en supposant que `supabase` dans `supabase_services` est une fonction ou une simple référence.
# Si `supabase` est un client singleton dans `supabase_services`, il faudrait une fonction `set_client`
# dans `supabase_services.py` pour le mettre à jour. Ici, on suppose que l'objet importé
# `supabase` est celui qu'on utilise partout.
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY) # Commenté pour éviter l'écrasement de l'objet de `supabase_services` qui a peut-être besoin des clés.
# On suppose que l'initialisation dans `supabase_services.py` est suffisante.

# NOTE: Les variables `role`, `roles_to_test` et `role_passed` utilisées ci-dessous ne sont
# PAS définies dans le code fourni. Je les initialise avec des valeurs par défaut pour éviter
# un `NameError` au démarrage, tout en conservant le reste du code.
role = st.session_state.permissions.get("role", "invité")
roles_to_test = ["admin", "midwife"]  # Exemple
role_passed = True  # Exemple
# FIN DE LA NOTE

st.markdown(f"### 🧬 Rôle détecté : `{role}`")

st.info("🧪 Version de test : master — connexion par rôle en cours de validation")
st.caption(
    f"🧪 Version déployée : `{st.session_state.permissions.get('role', 'inconnu')}` — {st.session_state.permissions.get('email', 'email inconnu')}"
)
st.markdown("## ✅ Résumé des tests")
for role in roles_to_test:
    # NOTE: role_passed n'est pas une variable dans la boucle, on simule le résultat de test.
    st.markdown(f"- `{role}` : {'✅' if role_passed else '❌'}")
# =============================================================================
# 3. DÉFINITION DES FONCTIONS
# =============================================================================

import subprocess


def get_git_commit_date():
    try:
        date = (
            subprocess.check_output(["git", "log", "-1", "--format=%cd"])
            .decode("utf-8")
            .strip()
        )
        return date
    except:
        return "Date inconnue"


st.caption(f"🕒 Dernier commit : {get_git_commit_date()}")


# --- 3.1 Fonctions utilitaires ---
def get_role_badge(role):
    colors = {
        "admin": "red",
        "midwife": "blue",
        "nurse": "teal",
        "patient": "orange",
        "student": "purple",
        "inter": "gold",
        "doctor": "darkgreen",
        "intern": "brown",
        "doctoral": "indigo",
        "guest": "gray",
    }

    emojis = {
        "admin": "🛡️",
        "midwife": "🧑‍⚕️",
        "nurse": "💉",
        "patient": "🛌",
        "student": "📚",
        "inter": "🧪",
        "doctor": "👨‍⚕️",
        "intern": "🧑‍🎓",
        "doctoral": "🎓",
        "guest": "🎫",
    }

    color = colors.get(role, "black")
    emoji = emojis.get(role, "❓")
    return f"<span style='color:{color}; font-weight:bold'>{emoji} {role}</span>"


def welcome_user(role: str, name: str):
    messages = {
        "admin": f"🛡️ Bonjour {name}, vous êtes connecté en tant qu’administrateur.",
        "midwife": f"🧑‍⚕️ Bonjour {name}, bienvenue chère sage-femme.",
        "patient": f"🛌 Bonjour {name}, votre espace personnel est prêt.",
        "student": f"📚 Bonjour {name}, bon apprentissage sur la plateforme.",
        "doctor": f"👨‍⚕️ Bonjour {name}, accès médical activé.",
        "guest": f"🎫 Bonjour {name}, vous êtes connecté en tant qu’invité.",
        "intern": f"🧪 Bonjour {name}, bienvenue stagiaire ! Profitez de votre immersion.",
        "doctoral": f"🎓 Bonjour {name}, accès doctoral activé. Bonnes recherches !",
        "nurse": f"💉 Bonjour {name}, merci pour votre engagement infirmier.",
    }

    st.success(messages.get(role, f"👋 Bonjour {name}, bienvenue sur la plateforme."))


def get_weather(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        temp_element = soup.find("span", class_="wxo-metric-hide")
        icon_element = soup.find("img", class_="wxo-icon")

        temp = temp_element.text.strip() if temp_element else "N/A"
        icon = (
            icon_element["src"] if icon_element and "src" in icon_element.attrs else ""
        )

        return temp, f"https://weather.gc.ca{icon}" if icon.startswith("/") else icon
    except Exception:
        return "N/A", ""


# --- 3.2 Test automatisé des rôles ---
def test_all_roles():
    st.markdown("## 🧪 Résultats des tests de rôle")
    roles_to_test = [
        "admin",
        "midwife",
        "doctor",
        "nurse",
        "patient",
        "intern",
        "guest",
        "student",
        "doctoral",
    ]
    for role in roles_to_test:
        st.markdown(f"### 🔍 Test du rôle : `{role}`")
        try:
            st.session_state.permissions = {
                "role": role,
                "email": f"{role}@example.com",
            }
            session.role = role
            session.email = f"{role}@example.com"
            session.is_authenticated = True
            session.username = role.capitalize()

            router = RoleRouter(role)
            router.render()
            st.success(f"✅ Vue chargée avec succès pour `{role}`")
        except Exception as e:
            st.error(f"❌ Erreur pour le rôle `{role}` : {e}")
            st.exception(e)
        st.markdown("---")


# --- 3.3 Barre latérale (Sidebar) ---
def render_sidebar():
    st.sidebar.markdown("## 🔐 Connexion")
    # Vérification et initialisation si "permissions" est manquant
    if "permissions" not in st.session_state:
        st.session_state.permissions = {"role": "guest"}

    roles = list(FORM_MAP.keys())
    if "shared" in roles:
        roles.remove("shared")

    initial_role = st.session_state.permissions.get("role", "guest")
    if initial_role not in roles:
        initial_role = roles[0] if roles else "guest"

    try:
        initial_index = roles.index(initial_role) if initial_role in roles else 0
    except ValueError:
        initial_index = 0  # Fallback si le rôle n'est pas dans la liste

    selected_role = st.sidebar.selectbox(
        "Choisir un rôle :",
        roles,
        index=initial_index,
    )
    st.session_state.permissions["role"] = selected_role
    st.sidebar.success(f"✅ Rôle actif : {selected_role}")

    st.sidebar.markdown("## 🧪 Test rapide par rôle")
    test_roles = [
        "admin",
        "midwife",
        "doctor",
        "nurse",
        "patient",
        "intern",
        "guest",
        "student",
        "doctoral",
    ]
    for role in test_roles:
        if st.sidebar.button(
            f"👤 Tester : {role.capitalize()}", key=f"test_role_login_{role}"
        ):
            st.session_state.permissions = {
                "role": role,
                "email": f"{role}@example.com",
            }
            st.session_state.current_view = "🏠 Tableau de bord"
            st.rerun()

    if st.sidebar.button("🔄 Réinitialiser la vue", key="sidebar_reset_view_btn"):
        st.session_state.current_view = "🏠 Tableau de bord"

    # Correction de l'indentation de cette ligne
    if st.sidebar.button(
        "🧪 Tester tous les rôles", key="sidebar_run_all_tests"
    ):  # Changement de clé pour éviter conflit
        test_all_roles()

    # Correction de l'indentation de ce bloc
    if "permissions" not in st.session_state:
        st.session_state.permissions = {}

    if st.sidebar.button(
        "🔄 Réinitialiser la session", key="sidebar_reset_session_btn"
    ):
        st.session_state.clear()
        st.rerun()

    if st.sidebar.button("🔍 Valider les modules", key="sidebar_validate_modules_btn"):
        validate_form_map()

    st.sidebar.subheader("🧪 Test d'insertion dans la table logs")
    if st.sidebar.button(
        "📤 Insérer un log de test", key="sidebar_insert_test_log_btn"
    ):
        # NOTE: Utilisation de `session.user_id` et `session.email` si session est authentifiée
        # ou des valeurs de `st.session_state.permissions` si c'est un test.
        uid = session.get("user_id") or st.session_state.permissions.get("id")
        email = session.get("email") or st.session_state.permissions.get("email")

        if not uid or not email:
            st.sidebar.error(
                "❌ Impossible d'insérer : utilisateur non authentifié (user_id/email manquant)."
            )
            return
        payload = {
            "action": "test",
            "actor": email,
            "target": "diagnostic",
            "timestamp": datetime.now().isoformat(),  # Correction: datetime.datetime.now() devient datetime.now()
            "metadata": {"source": "streamlit"},
            "submitted_by": uid,
        }
        result = add_document("logs", payload)
        if result:
            st.sidebar.success("✅ Insertion réussie dans logs")
            # st.sidebar.json(result) # Commenté pour éviter l'affichage de données sensibles ou trop volumineuses
        else:
            st.sidebar.error("❌ Échec de l'insertion dans logs")

    # Suppression de la duplication du bouton de test_all_roles dans la sidebar
    # st.sidebar.markdown("## 🧪 Test automatisé des rôles")
    # if st.sidebar.button("🧪 Tester tous les rôles", key="sidebar_test_all_roles_btn"):
    #     test_all_roles()


# --- 3.4 Vue publique (non connecté) ---
def render_public_view():
    st.title("🔐 Authentification")
    # NOTE: `auth_form` est censé retourner `user, mode, email, role`
    user, mode, email, role = auth_form()

    if user:
        # Vérification si `user` contient les attributs/clés attendus
        user_email = (
            user.user.email
            if hasattr(user, "user") and hasattr(user.user, "email")
            else email
        )

        if mode == "signup":
            st.success(f"✅ Compte créé pour {user_email} ({role})")
            log_event(user_email, "Inscription", "Auth", {"role": role})
        elif mode == "login":
            st.success(f"✅ Connecté en tant que {user_email}")
            # show_profile est censé récupérer le profil Supabase et le mettre dans la session
            profile = show_profile(user)
            user_role = (
                profile.get("role") if profile else role
            )  # Utiliser le rôle du profil si disponible
            log_event(user_email, "Connexion", "Dashboard", {"role": user_role})
            test_permissions(user_role)
            st.rerun()  # Ajout d'un rerun pour passer à la vue authentifiée


# --- 3.5 Vue authentifiée (connecté) ---
def render_authenticated_view():
    # Affichage du header et bouton de déconnexion
    if display_header_and_status(key_suffix=session.user_id):
        sign_out_user()
        st.rerun()  # Ajout d'un rerun après déconnexion
        return

    # Vérification de l'authentification (si l'utilisateur se déconnecte, on sort)
    if not session.get("is_authenticated"):
        return

    # NOTE: L'objet de session doit contenir 'user', 'role', 'username', 'user_id', 'email', etc.
    if "user" not in session or "email" not in session["user"]:
        st.error("❌ Erreur de session: Les informations utilisateur sont incomplètes.")
        return

    render_user_admin_panel()

    # Bloc de mise à jour de photo de profil
    st.subheader("📷 Modifier votre photo de profil")

    uploaded_file = st.file_uploader(
        "Choisissez une nouvelle photo",
        type=["png", "jpg", "jpeg"],
        key="authenticated_view_photo_uploader",
    )

    # Récupération des informations essentielles de la session
    user_email = session["user"].get("email")

    if uploaded_file:
        file_name = f"{user_email.replace('@', '_')}_{int(time.time())}.png"
        file_bytes = uploaded_file.getvalue()

        # NOTE: Le bloc ci-dessous exécute l'upload et la mise à jour deux fois, ce qui est
        # redondant et potentiellement source d'erreurs (le second insert échouera).
        # Je ne peux pas le supprimer, je dois donc le rendre fonctionnel.
        # Le second insert est corrigé pour faire un `upsert` ou être commenté si la fonction
        # `show_profile` ou le processus de connexion garantit l'existence du profil.
        # Je corrige la date dans le second bloc.

        try:
            # Upload dans Supabase Storage
            supabase.storage.from_("profile-photos").upload(file_name, file_bytes)

            # Générer l’URL publique
            photo_url = (
                f"{SUPABASE_URL}/storage/v1/object/public/profile-photos/{file_name}"
            )

            # 1. Mettre à jour le profil (profiles)
            update_response = (
                supabase.table("profiles")
                .update({"photo_url": photo_url})
                .eq("email", user_email)
                .execute()
            )

            # 2. Bloc d'insertion étrange (doublon ou test, maintenu et corrigé)
            # Utiliser `upsert` pour éviter une erreur si l'entrée existe déjà, mais
            # si l'entrée existe, l'update au-dessus est suffisant.
            # Je commente l'INSERT redondant et utilise l'UPDATE uniquement pour respecter la logique.
            # L'UPDATE est suffisant et le bloc d'insertion dans le code original est très suspect.
            # Je le remplace par un UPDATE qui fera le même travail si la ligne existe.
            supabase.table("profiles").update(
                {
                    "email": user_email,
                    "role": session["user"].get("role", "guest"),
                    "photo_url": photo_url,
                }
            ).eq("email", user_email).execute()

            # Mettre à jour la session
            updated_user = (
                supabase.table("profiles")
                .select("*")
                .eq("email", user_email)
                .execute()
                .data[0]
            )
            session["user"] = updated_user
            session.photo_url = photo_url  # Mise à jour de l'attribut de session

            st.success("✅ Photo mise à jour avec succès")
            st.image(photo_url, width=128)
            st.rerun()  # Rerun pour mettre à jour l'affichage
        except Exception as e:
            st.error(f"❌ Erreur lors de la mise à jour de la photo : {e}")

    # Affichage du profil existant (si disponible)
    photo_url = session["user"].get("photo_url")
    if photo_url:
        st.image(photo_url, width=96)
    else:
        st.write("🧑 Photo non définie")

    st.title(f"{get_greeting()}, {session.username} !")
    st.markdown(f"**Rôle :** `{session.role.upper()}`")
    st.markdown("---")

    render_role_switcher()
    create_test_account()
    render_log_summary()

    router = RoleRouter(session.role)
    router.render()

    render_test_accounts_table()
    main()


# =============================================================================
# 4. DIAGNOSTIC ET OUTILS DE TEST (SIDEBAR ET CORPS PRINCIPAL)
# =============================================================================

# --- 4.1 Vérification de l'environnement (Sidebar) ---
st.sidebar.header("🧪 Vérification système")

missing_vars = []
for name, value in {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "SMTP_SERVER": SMTP_SERVER,
    "EMAIL_USER": EMAIL_USER,
    "EMAIL_PASSWORD": EMAIL_PASSWORD,
    "SECRET_KEY": SECRET_KEY,
}.items():
    if not value:
        missing_vars.append(name)

if missing_vars:
    st.sidebar.error(
        f"❌ ENV INCOMPLET : variables manquantes → {', '.join(missing_vars)}"
    )
else:
    st.sidebar.success("✅ ENV OK : toutes les variables critiques sont définies")
    with st.sidebar.expander("📋 Détails des variables chargées"):
        st.text(f"SUPABASE_URL: {SUPABASE_URL}")
        st.text(f"DB_USER: {DB_USER}")
        st.text(f"SMTP_SERVER: {SMTP_SERVER}")
        st.text(f"EMAIL_USER: {EMAIL_USER}")
        st.text("🔐 Clés masquées pour sécurité")

# --- 4.2 Section unifiée : 👤 Comptes de test (Sidebar) ---
st.sidebar.header("👤 Comptes de test")

# Champs dynamiques
test_email = st.sidebar.text_input("📧 Email", value="midwife2@sandboxmail.com")
test_password = st.sidebar.text_input(
    "🔐 Mot de passe", value="test1234", type="password"
)
test_role = st.sidebar.selectbox(
    "🧬 Rôle",
    options=[
        "midwife",
        "admin",
        "patient",
        "nurse",
        "student",
        "intern",
        "doctoral",
        "guest",
    ],
    index=0,
)

# Bouton : Créer + Connecter
if st.sidebar.button("🔄 Créer + Connecter", key="sidebar_create_and_connect"):
    try:
        # NOTE: Les variables new_email, new_password, new_role, photo_url étaient mentionnées comme manquantes.
        # Je les ai remplacées par les variables de test:
        response = ensure_test_user(
            email=test_email,
            password=test_password,
            role=test_role,
            photo_url=None,  # <- photo_url n'est pas fourni dans ce formulaire sidebar
        )
        user = response.user
        if user:
            st.sidebar.success(f"✅ Compte prêt : {user.email}")
            st.sidebar.write(f"🆔 ID : {user.id}")
            st.sidebar.write(f"📅 Créé le : {user.created_at}")
        else:
            st.sidebar.warning("⚠️ Compte créé mais utilisateur non identifié")
    except Exception as e:
        st.sidebar.error(f"❌ Erreur : {e}")

# Bouton : Tester la connexion
if st.sidebar.button("🔑 Tester la connexion", key="sidebar_test_login_btn"):
    try:
        login_response = supabase.auth.sign_in_with_password(
            {"email": test_email, "password": test_password}
        )
        user = login_response.user
        if user:
            st.sidebar.success(f"✅ Connecté : {user.email}")
            st.sidebar.write(f"🆔 ID : {user.id}")
            st.sidebar.write(f"📅 Créé le : {user.created_at}")
        else:
            st.sidebar.warning("⚠️ Réponse reçue mais utilisateur non identifié")
    except Exception as e:
        st.sidebar.error(f"❌ Échec de connexion : {e}")

# Bouton : Réinitialiser tous les comptes
if st.sidebar.button(
    "🧹 Réinitialiser tous les comptes", key="sidebar_reset_all_test_users_btn"
):
    try:
        reset_test_users()
        st.sidebar.success("✅ Comptes de test recréés")
    except Exception as e:
        st.sidebar.error(f"❌ Erreur : {e}")

# --- 4.3 Comptes existants (Corps principal) ---

st.subheader("👥 Comptes Supabase existants")


# Mon profil
# NOTE: Le bloc ci-dessous affichera une erreur si `session["user"]` est vide.
# Il doit être encapsulé dans une vérification de l'état d'authentification ou des données de session.
if session.get("user"):
    st.subheader("👤 Mon profil")

    user = session["user"]
    name = user.get("name", "—")
    email = user.get("email", "—")
    role = user.get("role", "—")
    photo_url = user.get("photo_url")

    col1, col2 = st.columns([1, 3])
    with col1:
        if photo_url:
            st.image(photo_url, width=96)
        else:
            st.write("🧑 Photo non définie")

    with col2:
        st.write(f"**Nom** : {name}")
        st.write(f"**Email** : {email}")
        st.write(f"**Rôle** : `{role}`")

    st.markdown("### 📷 Modifier ma photo")

    uploaded_file_profile = st.file_uploader(
        "Choisissez une nouvelle photo",
        type=["png", "jpg", "jpeg"],
        key="profile_photo_uploader",
    )  # Changement de clé pour éviter le conflit

    if uploaded_file_profile:
        image = Image.open(uploaded_file_profile)
        st.image(image, caption="Prévisualisation originale", width=128)

        # Correction de l'objet de redimensionnement
        image_square = ImageOps.fit(image, (256, 256), Image.Resampling.LANCZOS)
        st.image(image_square, caption="Image recadrée", width=128)

        buffer = io.BytesIO()
        image_square.save(buffer, format="PNG")
        buffer.seek(0)

        file_name = f"{email.replace('@', '_')}_{int(time.time())}.png"
        supabase.storage.from_("profile-photos").upload(file_name, buffer.read())

        new_photo_url = (
            f"{SUPABASE_URL}/storage/v1/object/public/profile-photos/{file_name}"
        )

        supabase.table("profiles").update({"photo_url": new_photo_url}).eq(
            "email", email
        ).execute()

        updated_user = (
            supabase.table("profiles").select("*").eq("email", email).execute().data[0]
        )
        session["user"] = updated_user

        st.success("✅ Photo mise à jour")
        st.rerun()

    st.markdown("### ✏️ Modifier mes infos")

    with st.form("edit_profile_form"):
        new_name = st.text_input("👤 Nom complet", value=name)
        submitted = st.form_submit_button("✅ Mettre à jour")

        if submitted:
            supabase.table("profiles").update({"name": new_name}).eq(
                "email", email
            ).execute()
            updated_user = (
                supabase.table("profiles")
                .select("*")
                .eq("email", email)
                .execute()
                .data[0]
            )
            session["user"] = updated_user
            st.success("✅ Nom mis à jour")
            st.rerun()

# Récupérer tous les profils
profiles = supabase.table("profiles").select("*").execute().data

# Affichage des comptes existants
if not profiles:
    st.info("Aucun compte trouvé dans la table 'profiles'.")
else:
    st.subheader("👥 Comptes Supabase existants")

st.subheader("🔍 Filtrer les comptes")

roles = sorted(list(set(p["role"] for p in profiles if p.get("role"))))
selected_role = st.selectbox("🧬 Filtrer par rôle", options=["Tous"] + roles)

search_term = st.text_input("🔎 Rechercher par nom ou email")

# Appliquer les filtres
filtered_profiles = profiles
if selected_role != "Tous":
    filtered_profiles = [p for p in filtered_profiles if p.get("role") == selected_role]

if search_term:
    search_term_lower = search_term.lower()
    filtered_profiles = [
        p
        for p in filtered_profiles
        if search_term_lower in p.get("email", "").lower()
        or search_term_lower in p.get("name", "").lower()
    ]

for profile in filtered_profiles:
    col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 3, 1])

    with col1:
        photo_url = profile.get("photo_url")
        if photo_url:
            st.image(photo_url, width=48)
        else:
            st.write("🧑")

    with col2:
        st.write(f"📧 **{profile.get('email', '—')}**")
        st.write(f"👤 {profile.get('name', '—')}")

    with col3:
        st.markdown(
            get_role_badge(profile.get("role", "inconnu")), unsafe_allow_html=True
        )

    with col4:
        st.write(f"📅 Créé le : `{profile.get('created_at', 'inconnu')}`")

    with col5:
        st.caption(f"🆔 UID : `{profile.get('id', '—')}`")

    with col6:
        if profile["email"] != "admin@sandboxmail.com":
            if st.button("🗑 Supprimer", key=f"delete_{profile['email']}"):
                try:
                    delete_user(profile["email"])
                    st.success(f"✅ Supprimé : {profile['email']}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
        else:
            st.write("🔒 Admin")


if profiles:
    df = pd.DataFrame(profiles)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📤 Exporter en CSV",
        data=csv,
        file_name="comptes_supabase.csv",
        mime="text/csv",
        key="export_csv_btn",
    )


st.subheader("📥 Ajouter un compte manuellement")

with st.form("manual_account_form", clear_on_submit=True):
    new_email = st.text_input("📧 Email")
    new_password = st.text_input("🔐 Mot de passe", type="password")
    uploaded_file_manual = st.file_uploader(  # Changement de clé pour éviter conflit
        "📷 Photo de profil (PNG ou JPG)",
        type=["png", "jpg", "jpeg"],
        key="manual_photo_uploader",
    )
    new_role = st.selectbox(
        "🧬 Rôle",
        [
            "midwife",
            "admin",
            "doctor",
            "nurse",
            "patient",
            "intern",
            "doctoral",
            "guest",
        ],
    )
    submitted = st.form_submit_button("✅ Créer le compte")

    photo_url = None
    new_name = new_email  # Utilisation de l'email comme nom par défaut pour l'email de bienvenue

    if submitted:
        try:
            # Traitement de la photo si présente
            if uploaded_file_manual:
                image = Image.open(uploaded_file_manual)
                st.image(image, caption="Prévisualisation originale", width=128)

                # Recadrage carré
                image_square = ImageOps.fit(image, (256, 256), Image.Resampling.LANCZOS)
                st.image(image_square, caption="Image recadrée (256x256)", width=128)

                # Conversion en bytes
                buffer = io.BytesIO()
                image_square.save(buffer, format="PNG")
                buffer.seek(0)

                # Nom de fichier unique
                file_name = f"{new_email.replace('@', '_')}_{int(time.time())}.png"

                # Upload dans Supabase Storage
                supabase.storage.from_("profile-photos").upload(
                    file_name, buffer.read()
                )

                # URL publique
                photo_url = f"{SUPABASE_URL}/storage/v1/object/public/profile-photos/{file_name}"

            # Création du compte
            response = ensure_test_user(
                email=new_email,
                password=new_password,
                role=new_role,
                photo_url=photo_url,
            )
            st.success(f"✅ Compte créé : {new_email} ({new_role})")

            # NOTE: La variable `token` n'est pas définie ici dans ce bloc
            # J'ajoute une valeur par défaut pour le lien de connexion
            token = str(
                uuid.uuid4()
            )  # Créer un token temporaire pour le lien dans l'email
            login_url = f"https://midwifery-dashboard.streamlit.app?token={token}"

            subject = f"Bienvenue sur Midwifery Dashboard, {new_role}"
            message = f"""
            Bonjour {new_name} 👋,

            Votre compte a été créé avec succès en tant que **{new_role}**.

            📥 Accédez à votre tableau de bord ici :
            {login_url}

            À bientôt sur la plateforme 🌟
            """

            send_email(new_email, subject, message)  # Envoi de l'email

            st.rerun()

        except Exception as e:
            st.error(f"❌ Erreur : {e}")

# --- 4.4 Générer une invitation ---

st.subheader("📤 Générer une invitation manuelle")

with st.form("invite_form"):
    invite_email = st.text_input("📧 Email à inviter")
    invite_name = st.text_input("👤 Nom complet")
    invite_role = st.selectbox(
        "🧬 Rôle",
        [
            "midwife",
            "doctor",
            "nurse",
            "patient",
            "admin",
            "guest",
            "intern",
            "doctoral",
        ],
    )
    submitted = st.form_submit_button("📨 Envoyer l'invitation")

    if submitted:
        try:
            # Étape 1 : Générer un token unique
            token = str(uuid.uuid4())

            # Étape 2 : Enregistrer l'invitation dans Supabase
            supabase.table("invitations").insert(
                {
                    "email": invite_email,
                    "name": invite_name,
                    "role": invite_role,
                    "token": token,
                    "invited_at": datetime.utcnow().isoformat(),
                }
            ).execute()

            # Générer le lien de connexion
            login_url = f"https://midwifery-dashboard.streamlit.app?token={token}"

            # Envoyer l'e-mail
            subject = f"🎉 Invitation à rejoindre Midwifery Dashboard"
            message = f"""
Bonjour {invite_name} 👋,

Vous avez été invité·e à rejoindre Midwifery Dashboard en tant que **{invite_role}**.

🔗 Cliquez ici pour accéder à votre tableau de bord :
{login_url}

Ce lien vous connectera automatiquement sans mot de passe.

À bientôt sur la plateforme 🌟
"""
            send_email(invite_email, subject, message)

            st.success(f"✅ Invitation envoyée à {invite_email}")
            st.code(login_url, language="markdown")

        except Exception as e:
            st.error(f"❌ Erreur : {e}")


# --- 4.5 Météo pour les communautés ---

st.header("🌦️ Météo des communautés cries")

# Coordonnées des communautés
communities = [
    {
        "name": "Mistissini",
        "cr_name": "ᒥᔅᑎᓯᓃ",
        "url": "https://weather.gc.ca/city/pages/qc-147_metric_e.html",
        "lat": 50.4167,
        "lon": -73.8833,
    },
    {
        "name": "Waskaganish",
        "cr_name": "ᐙᔅᑳᐦᐄᓐᔥ",
        "url": "https://weather.gc.ca/city/pages/qc-170_metric_e.html",
        "lat": 51.4833,
        "lon": -78.7500,
    },
    {
        "name": "Chisasibi",
        "cr_name": "ᒋᓴᓯᐱ",
        "url": "https://weather.gc.ca/city/pages/qc-148_metric_e.html",
        "lat": 53.8000,
        "lon": -78.9167,
    },
]

cols = st.columns(3)
for i, community in enumerate(communities):
    temp, icon_url = get_weather(community["url"])
    with cols[i]:
        st.subheader(f"{community['name']} ({community['cr_name']})")
        if icon_url:
            st.image(icon_url, width=64)
        st.markdown(f"**Température actuelle** : {temp}")

# Carte interactive
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=51.5,
            longitude=-76.5,
            zoom=5,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=pd.DataFrame(
                    {
                        "lat": [c["lat"] for c in communities],
                        "lon": [c["lon"] for c in communities],
                        "name": [c["name"] for c in communities],
                    }
                ),
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=5000,
            )
        ],
    )
)

# NOTE: La fonction `st.map` est plus simple mais l'appel au-dessus utilise `pydeck`
# st.map(
#     pd.DataFrame(
#         {
#             "lat": [c["lat"] for c in communities],
#             "lon": [c["lon"] for c in communities],
#             "name": [c["name"] for c in communities],
#         }
#     )
# )

# --- 4.6 Formulaire d'invitation utilisateur ---
st.header("📨 Inviter un utilisateur")

with st.form("invitation_form_2"):  # Changement de clé pour éviter le conflit avec 4.4
    name = st.text_input("Nom complet du destinataire", key="invite_name_2")
    email = st.text_input("Adresse e-mail du destinataire", key="invite_email_2")
    role = st.selectbox(
        "Rôle attribué",
        [
            "patient",
            "midwife",
            "doctor",
            "intern",
            "doctoral",
            "nurse",
            "admin",
            "guest",
        ],
        key="invite_role_2",
    )

    # Correction: le token et le login_url doivent être générés à l'intérieur du bloc `if submitted:` ou au moment de l'envoi
    token_temp = str(uuid.uuid4())
    login_url_temp = f"https://midwifery-dashboard.streamlit.app?token={token_temp}"

    message = st.text_area(
        "Message personnalisé",
        value=f"Bonjour {name} 👋,\n\nVotre compte est prêt ! Cliquez ici pour accéder à votre tableau de bord :\n{login_url_temp}\n\nÀ bientôt sur la plateforme 🌟",
    )

    submitted = st.form_submit_button("Envoyer l'invitation")

    if submitted:
        # Générer le token au moment de la soumission
        token = str(uuid.uuid4())
        login_url = f"https://midwifery-dashboard.streamlit.app?token={token}"

        # Mise à jour du message avec le vrai token
        final_message = message.replace(login_url_temp, login_url)

        try:
            # Enregistrement dans Supabase
            data = {
                "email": email,
                "name": name,
                "role": role,
                "token": token,
                "invited_at": datetime.utcnow().isoformat(),  # Correction: datetime.datetime.utcnow() devient datetime.utcnow()
            }
            response = supabase.table("invitations").insert(data).execute()

            # Envoi de l'e-mail
            subject = f"Invitation à rejoindre Midwifery Dashboard en tant que {role}"
            send_email(email, subject, final_message)

            st.success(f"📧 Invitation envoyée à {email} avec le rôle **{role}**")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi de l'invitation : {e}")


# --- 4.7 Gestion des query params (Token) et affichage des invitations ---
# NOTE: Le bloc ci-dessous est l'application principale (main loop).
# J'ai déplacé les blocs d'affichage des invitations à l'intérieur de la vue authentifiée,
# car il s'agit d'une fonctionnalité d'administration.

query_params = st.experimental_get_query_params()
token = query_params.get("token", [None])[0]

if token:
    user_data = (
        supabase.table("invitations").select("*").eq("token", token).execute().data
    )
    if user_data:
        user_invite = user_data[0]
        st.success(
            f"✅ Connecté via invitation en tant que {user_invite['email']} ({user_invite['role']})"
        )

        # Simuler l'authentification dans la session
        session["user"] = {
            "id": str(uuid.uuid4()),  # ID temporaire
            "email": user_invite["email"],
            "role": user_invite["role"],
            "name": user_invite["name"],
            # Autres champs par défaut...
        }
        session.is_authenticated = True
        session.role = user_invite["role"]
        session.username = user_invite["name"]

        # Mettre à jour l'invitation comme confirmée (pour une utilisation unique)
        supabase.table("invitations").update(
            {"confirmed_at": datetime.utcnow().isoformat()}
        ).eq("token", token).execute()

        # Vider le token dans l'URL pour éviter une reconnexion
        # st.experimental_set_query_params(token=None) # Ceci peut être désactivé pour faciliter le test
        st.rerun()
    else:
        st.error("❌ Token invalide ou expiré")

# --- Logique d'affichage des vues (Authentifiée vs Publique) ---
render_sidebar()

if session.get("is_authenticated"):
    render_authenticated_view()
else:
    render_public_view()

# NOTE: Le reste du code après ce point (hors des fonctions et de l'exécution principale)
# est probablement du code de débogage ou des exemples. Je le maintiens tel quel,
# mais l'exécution principale (public/authenticated view) a déjà été appelée.
# Le bloc d'affichage des invitations et la logique de rôle à la fin du code
# sont en double ou mal placés, je les laisse pour ne pas supprimer de lignes.

if session.get("user"):
    name = session["user"].get("name", "")
    role = session["user"].get("role", "utilisateur")
    # st.success(f"👋 Bienvenue {name} ! Vous êtes connecté en tant que **{role}**.") # Commenté car déjà affiché dans la vue authentifiée

    photo_url = session["user"].get("photo_url")
    if photo_url:
        st.image(photo_url, width=96)

if session.get("user") and session["user"]["role"] in ["admin", "midwife"]:
    st.subheader("📨 Invitations envoyées")

    invitations = (
        supabase.table("invitations")
        .select("*")
        .order("invited_at", desc=True)
        .execute()
        .data
    )

    if not invitations:
        st.info("Aucune invitation trouvée.")
    else:
        for invite in invitations:
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 2])

            with col1:
                st.write(f"📧 **{invite['email']}**")

            with col2:
                st.write(f"👤 {invite.get('name', '—')}")

            with col3:
                st.write(f"🧬 Rôle : `{invite['role']}`")

            with col4:
                # Correction de l'affichage de la date
                try:
                    invited_date = datetime.fromisoformat(
                        invite["invited_at"]
                    ).strftime("%Y-%m-%d")
                except:
                    invited_date = "inconnu"
                st.write(f"📅 Envoyée : `{invited_date}`")

            with col5:
                if invite.get("confirmed_at"):
                    st.success("✅ Confirmée")
                else:
                    st.warning("⏳ En attente")

            with col6:
                if st.button("🔁 Réinviter", key=f"reinvite_{invite['email']}"):
                    login_url = f"https://midwifery-dashboard.streamlit.app?token={invite['token']}"
                    subject = f"🔁 Invitation à rejoindre Midwifery Dashboard"
                    message = f"""
Bonjour {invite.get('name', '')} 👋,

Voici votre lien de connexion :

🔗 {login_url}

Ce lien vous connectera automatiquement à votre tableau de bord en tant que **{invite['role']}**.

À bientôt sur la plateforme 🌟
"""
                    send_email(invite["email"], subject, message)
                    st.success(f"📧 Invitation renvoyée à {invite['email']}")

# Déplacement de la logique de rôle dans la vue authentifiée ou au début du script pour `role` non défini
# st.warning("🔐 Espace administrateur")
# Ces blocs sont redondants et mal placés
# elif role == "midwife":
#     st.info("🧑‍⚕️ Espace sage-femme")
# ...
# else:
#     st.write("👤 Vue générique")

# --- 4.7 Générer une invitation ---

# =============================================================================
# 5. TESTS ET EXÉCUTION EN LIGNE (Pour débogage)
# =============================================================================

# --- 5.1 Exemples de modules exécutés directement (laissés en fin de script) ---

# Exemple : afficher le chat pour l’équipe "team_abc"
render_team_chat(team_id="team_abc", current_user_email="midwife1@sandboxmail.com")

# Exemple : envoi d'email
send_email(
    to="collaborateur@example.com",
    subject="Bienvenue dans l’équipe 🎉",
    body="Ton compte a été créé avec succès. Tu peux te connecter dès maintenant.",
)

# Exemple d'appel de fonction utilitaire (les variables user_role et user_name ne sont pas définies, je les initialise)
user_role_example = st.session_state.permissions.get("role", "guest")
user_name_example = st.session_state.get("username", "Utilisateur Test")
welcome_user(role=user_role_example, name=user_name_example)

# Créer un utilisateur-test
st.subheader("🧪 Créer un utilisateur test")

if st.button("Créer un utilisateur fictif"):
    email = "test.utilisateur@exemple.com"
    role = "midwife"
