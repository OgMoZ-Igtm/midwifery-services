import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Constantes pour les types de logs (Meilleures pratiques TI)
LOG_TYPES = ["INFO", "PATIENT", "ADMIN", "CRITIQUE", "ERREUR"]
LOG_COLORS = {
    "INFO": "blue",
    "PATIENT": "green",
    "ADMIN": "orange",
    "CRITIQUE": "red",
    "ERREUR": "red",
}


def init_system_log():
    """Initialise l'historique des logs de la session, y compris des exemples."""
    if "system_logs" not in st.session_state:
        # Structure de données de journal simple (pour une solution Firestore, ce serait une collection)
        st.session_state.system_logs = [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": "ADM_001",
                "type": "CRITIQUE",
                "message": "Naissance enregistrée : Patient 456 - Apgar 9/10.",
                "details": {"patient_id": "P456", "outcome": "Success"},
            },
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": "DR_JANE",
                "type": "PATIENT",
                "message": "Mise à jour du statut du travail pour Patient 123 : 4 cm de dilatation.",
                "details": {"patient_id": "P123", "status": "Active Labor"},
            },
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": "ADM_001",
                "type": "INFO",
                "message": "Rapport quotidien de l'unité généré.",
                "details": {},
            },
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": "SYSTEM",
                "type": "ERREUR",
                "message": "Échec de connexion au serveur d'imagerie médicale (MRI).",
                "details": {"error_code": "503", "component": "IMAGING_SVC"},
            },
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": "NUR_LISE",
                "type": "ADMIN",
                "message": "Connexion réussie au système à partir du poste de garde.",
                "details": {"session_id": "s89012"},
            },
        ]


def log_event(user_id: str, log_type: str, message: str, details: dict = None):
    """
    Ajoute un nouvel événement au journal du système.
    Dans une application réelle, cela écrirait dans Firestore.
    """
    new_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "type": log_type,
        "message": message,
        "details": details if details is not None else {},
    }
    # Insère au début pour que le plus récent soit en haut
    st.session_state.system_logs.insert(0, new_log)
    # L'utilisateur de ce module n'a pas besoin de faire rerender ici,
    # car il est appelé depuis d'autres actions.


def format_log_row(log_item: dict) -> str:
    """Formate une ligne de log avec des couleurs et des icônes pour la clarté."""
    log_type = log_item["type"]
    color = LOG_COLORS.get(log_type, "gray")

    # Choisir une icône (lucide-react est la librairie par défaut de Streamlit)
    if log_type == "CRITIQUE" or log_type == "ERREUR":
        icon = "🚨"
    elif log_type == "PATIENT":
        icon = "👶"  # Bébés pour les événements patients en obstétrique
    elif log_type == "ADMIN":
        icon = "🔑"
    else:
        icon = "ℹ️"

    details_str = f"({log_item['user_id']})"

    # Utilisation de Markdown et HTML pour une mise en forme riche
    markdown = f"""
    <div style="
        border-left: 5px solid {color}; 
        padding: 5px 10px; 
        margin-bottom: 5px; 
        background-color: #f9f9f9; 
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
    ">
        <div style="flex-grow: 1;">
            <span style="font-weight: bold; color: {color}; margin-right: 10px;">{icon} {log_type}</span>
            {log_item['message']} <span style="color: gray; font-size: 0.9em;">{details_str}</span>
        </div>
        <div style="color: #666; font-size: 0.8em; align-self: center;">
            {log_item['timestamp']}
        </div>
    </div>
    """
    return markdown


def render():
    """
    Rendu du tableau de bord d'administration des logs.
    """
    init_system_log()

    st.markdown("## ⚙️ Journal des événements Système (Obstétrique)")

    # ------------------ Barre de filtres et d'actions ------------------
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_types = st.multiselect(
            "Filtrer par Type d'événement",
            options=LOG_TYPES,
            default=LOG_TYPES,
            key="log_filter_types",
        )

    with col2:
        # Bouton factice pour la meilleure pratique d'exportation
        if st.button("Exporter le Journal (CSV)", help="Télécharge les logs filtrés."):
            st.warning(
                "Fonctionnalité d'exportation non implémentée, mais c'est une meilleure pratique."
            )

    # ------------------ Application du filtre ------------------

    # 1. Conversion de l'historique en DataFrame pour une manipulation facile
    df_logs = pd.DataFrame(st.session_state.system_logs)

    # 2. Filtrage
    if selected_types:
        df_filtered = df_logs[df_logs["type"].isin(selected_types)].copy()
    else:
        df_filtered = pd.DataFrame()  # Rien si aucun type n'est sélectionné

    st.metric(label="Nombre total d'événements", value=len(df_filtered))

    # ------------------ Affichage des Logs Filtrés ------------------
    st.markdown("### Événements Récents")

    if df_filtered.empty:
        st.info("Aucun événement correspondant aux filtres sélectionnés.")
    else:
        log_container = st.container(height=500, border=True)
        with log_container:
            # Afficher les logs formatés ligne par ligne
            for index, row in df_filtered.iterrows():
                # Streamlit n'a pas de composant 'log row' natif, on utilise du Markdown/HTML
                st.markdown(format_log_row(row.to_dict()), unsafe_allow_html=True)

    st.divider()
    st.caption("Le journal est trié du plus récent au plus ancien.")


# Exemple d'exécution du composant
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Journal Système Admin")

    # Exemple d'appel pour enregistrer un événement après 5 secondes
    if "test_log_added" not in st.session_state:
        st.session_state.test_log_added = False

    if not st.session_state.test_log_added:
        # Utilisation de time.sleep() pour simuler un événement asynchrone pour l'exemple
        # time.sleep(1)
        log_event(
            user_id="ADM_001",
            log_type="PATIENT",
            message="Nouvelle admission: Patiente M. Dubois - Dilatation 1 cm.",
            details={"patient_id": "P500", "arrival": "13:30"},
        )
        st.session_state.test_log_added = True
        # st.rerun() # Dérécommenter si exécuté dans un environnement Streamlit pur

    render()
