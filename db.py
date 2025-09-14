import sqlite3
import streamlit as st
import bcrypt
import os
import datetime

# Définition du chemin de la base de données
DB_NAME = "users.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)


# Utilise le décorateur st.cache_resource pour mettre en cache la connexion SQLite
@st.cache_resource
def get_db_connection():
    """
    Crée et met en cache une connexion à la base de données SQLite.
    La connexion est créée une seule fois pour toutes les exécutions de l'application,
    la rendant sûre pour les threads de Streamlit.
    """
    # L'argument check_same_thread=False est nécessaire pour permettre à Streamlit
    # d'utiliser la connexion depuis différents threads.
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """
    Créer toutes les tables nécessaires si elles n'existent pas déjà.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table des utilisateurs
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            mot_de_passe_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'GUEST',
            last_login TIMESTAMP
        );
    """
    )

    # Table des logs d'accès
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            access_time TEXT NOT NULL,
            user_role TEXT NOT NULL
        );
    """
    )

    # Tables pour les stages étudiants
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT,
            stage_site TEXT,
            superviseur TEXT,
            activites TEXT,
            heures INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Tables pour les évaluations
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT,
            stage_nom TEXT,
            note_superviseur INTEGER,
            auto_eval INTEGER,
            commentaires TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Tables pour les projets doctorants
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS doctoral_research (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctoral_email TEXT,
            titre TEXT,
            directeur TEXT,
            domaine TEXT,
            resume TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Tables pour les publications doctorants
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS doctoral_publications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctoral_email TEXT,
            titre TEXT,
            journal TEXT,
            annee INTEGER,
            lien TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    conn.commit()


# =========================
# FONCTIONS D'INTERACTION DB
# =========================


def verify_user(email, password):
    """Vérifie les informations de l'utilisateur et retourne son prénom et son rôle."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT prenom, mot_de_passe_hash, role FROM users WHERE email=?", (email,)
    )
    user_data = cursor.fetchone()
    if user_data:
        prenom, hashed_password, role = user_data
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return {"prenom": prenom, "role": role}
    return None


def log_access(email, role):
    """Enregistre l'accès de l'utilisateur."""
    conn = get_db_connection()
    cursor = conn.cursor()
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO access_log (email, access_time, user_role) VALUES (?, ?, ?)",
        (email, access_time, role),
    )
    conn.commit()


def get_access_logs():
    """Récupère tous les logs d'accès."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, access_time, user_role FROM access_log ORDER BY access_time DESC"
    )
    logs = cursor.fetchall()
    return logs


def insert_log(email, role, action):
    """Enregistre un événement dans la table des logs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (email, role, action) VALUES (?, ?, ?)", (email, role, action)
    )
    conn.commit()


def insert_user(prenom, email, password_hash, role):
    """Insère un nouvel utilisateur dans la base de données."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (prenom, email, mot_de_passe_hash, role) VALUES (?, ?, ?, ?)",
        (prenom, email, password_hash, role),
    )
    conn.commit()


def insert_student_practice(student_email, stage_site, superviseur, activites, heures):
    """Insère un nouveau journal de stage pour un étudiant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO student_practice (student_email, stage_site, superviseur, activites, heures)
        VALUES (?, ?, ?, ?, ?)
    """,
        (student_email, stage_site, superviseur, activites, heures),
    )
    conn.commit()


def insert_student_evaluation(
    student_email, stage_nom, note_superviseur, auto_eval, commentaires
):
    """Insère une nouvelle évaluation de stage pour un étudiant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO student_evaluations (student_email, stage_nom, note_superviseur, auto_eval, commentaires)
        VALUES (?, ?, ?, ?, ?)
    """,
        (student_email, stage_nom, note_superviseur, auto_eval, commentaires),
    )
    conn.commit()


def insert_doctoral_research(doctoral_email, titre, directeur, domaine, resume):
    """Insère un nouveau projet de recherche pour un doctorant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO doctoral_research (doctoral_email, titre, directeur, domaine, resume)
        VALUES (?, ?, ?, ?, ?)
    """,
        (doctoral_email, titre, directeur, domaine, resume),
    )
    conn.commit()


def insert_doctoral_publication(doctoral_email, titre, journal, annee, lien):
    """Insère une nouvelle publication pour un doctorant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO doctoral_publications (doctoral_email, titre, journal, annee, lien)
        VALUES (?, ?, ?, ?, ?)
    """,
        (doctoral_email, titre, journal, annee, lien),
    )
    conn.commit()
