# logger.py

import sqlite3
import logging
import os
from datetime import datetime

# 📁 Crée le dossier de logs s'il n'existe pas
os.makedirs("logs", exist_ok=True)

# 🛠️ Configuration du logger principal
logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,  # Change à INFO ou WARNING selon le besoin
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# 🔍 Fonctions de journalisation standard
def log_debug(message):
    logging.debug(message)


def log_info(message):
    logging.info(message)


def log_warning(message):
    logging.warning(message)


def log_error(message):
    logging.error(message)


# 🧾 Journalisation dans la base SQLite
def log_user_action(email, role, action):
    """Journalise une action réussie dans la table 'logs'."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            role TEXT,
            action TEXT,
            timestamp TEXT
        )
    """
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO logs (email, role, action, timestamp) VALUES (?, ?, ?, ?)",
        (email, role, action, timestamp),
    )

    conn.commit()
    conn.close()


def log_alert(email, role, message):
    """Journalise une alerte (tentative échouée, anomalie)."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    """
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO alerts (email, role, message, timestamp) VALUES (?, ?, ?, ?)",
        (email, role, message, timestamp),
    )

    conn.commit()
    conn.close()


# 🗂️ Journalisation des accès dans un fichier texte
def log_access(username, role, page):
    """Enregistre les accès dans un fichier texte lisible."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/access_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {username} | {role} | {page}\n")


def log_action(email, role, action):
    print("✅ log_action de logger.py appelée")
    print(f"📌 log_user_action appelée avec : {email}, {role}, {action}")
