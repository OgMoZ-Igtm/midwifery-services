# utils/security.py
"""
🎯 Gère les rôles et permissions d’accès aux packs.
Le nouveau modèle de permissions liste les rôles autorisés par pack.
Cela simplifie la gestion et renforce la sécurité.
"""
import streamlit as st
from datetime import datetime
import os

# ------------------------
# Définition des permissions (nouveau modèle)
# ------------------------

# Règle métier :
# - Chaque pack liste explicitement les rôles qui peuvent y accéder.
# - Un pack non listé ici est considéré comme ayant une permission vide (aucun accès).
# - Les rôles sont en majuscules pour garantir la cohérence.

PACK_PERMISSIONS = {
    # 'ADMIN' est le seul pack accessible uniquement par les admins
    "ADMIN": ["ADMIN"],
    # 'DOCTOR' est pour les DOCTOR et les ADMIN
    "DOCTOR": ["ADMIN", "DOCTOR"],
    # 'NURSE' est accessible par un groupe plus large
    "NURSE": ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE"],
    "MIDWIFE": ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE"],
    # 'PATIENT' est un pack central accessible par de nombreux rôles
    "PATIENT": ["ADMIN", "DOCTOR", "NURSE", "PATIENT", "MIDWIFE"],
    # Les packs spécifiques à l'apprentissage sont partagés entre les rôles concernés
    "STUDENT": ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE", "STUDENT"],
    "DOCTORAL": ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE", "DOCTORAL"],
    "INTERN": ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE", "INTERN"],
    # 'MESSAGES' est accessible par tous les utilisateurs connectés
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
    # Le pack 'ORGANISATION' est EXCLUSIVEMENT réservé à l'ADMIN
    "ORGANISATION": ["ADMIN"],
}

# --- Journal d'audit (pour la traçabilité) ---
AUDIT_LOG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "logs", "audit.log"
)


def log_audit_event(user: str, event_type: str, details: str):
    """Enregistre un événement dans deux journaux : texte et CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = (
        f"[{timestamp}] User: {user} | Event: {event_type} | Details: {details}\n"
    )

    # Journal texte
    log_dir = os.path.dirname(AUDIT_LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(AUDIT_LOG_FILE, "a") as log_file:
        log_file.write(log_message)

    # Journal CSV pour l'interface admin
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "audit_log.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "user", "event_type", "details"])
    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, user, event_type, details])


# ------------------------
# Fonctions utilitaires
# ------------------------


def est_autorise(role: str, pack: str, username: str) -> bool:
    """
    Vérifie si un rôle donné a le droit d’accéder à un pack.
    Un événement d'audit est enregistré pour chaque tentative d'accès.
    """
    role = role.upper()
    pack = pack.upper()

    is_allowed = role in PACK_PERMISSIONS.get(pack, [])

    # Enregistrer l'événement d'audit
    if is_allowed:
        log_audit_event(
            username,
            "Access Granted",
            f"User accessed pack '{pack}' with role '{role}'",
        )
    else:
        log_audit_event(
            username,
            "Access Denied",
            f"User tried to access pack '{pack}' with insufficient role '{role}'",
        )

    return is_allowed


def get_packs_for_role(role: str):
    """
    Retourne la liste des packs accessibles pour un rôle donné.
    """
    role = role.upper()
    if role == "GUEST":
        return []

    packs_autorises = []
    for pack, roles_autorises in PACK_PERMISSIONS.items():
        if role in roles_autorises:
            packs_autorises.append(pack)

    return packs_autorises


def afficher_badge_securite(role: str, pack: str):
    """
    Affiche un badge de sécurité indiquant l'accès autorisé ou refusé.
    Cette fonction est essentielle pour le débogage et l'expérience utilisateur.
    """
    allowed_roles = PACK_PERMISSIONS.get(pack, [])

    st.markdown(f"**Permissions pour le pack `{pack}` :**")
    if role in allowed_roles:
        st.success(f"✅ Accès autorisé pour le rôle **{role}**")
        st.info(f"Rôles autorisés pour ce pack : {', '.join(allowed_roles)}")
    else:
        st.error(f"❌ Accès refusé pour le rôle **{role}**")
        st.warning(
            f"Seuls les rôles suivants peuvent y accéder : {', '.join(allowed_roles)}"
        )
