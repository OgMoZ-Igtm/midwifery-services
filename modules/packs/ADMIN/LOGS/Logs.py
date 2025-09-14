import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import time


def render():
    page_admin_logs()
    # Ajout de l'actualisation automatique toutes les 30 secondes
    time.sleep(30)
    st.rerun()


def page_admin_logs():
    """
    Affiche la page des logs pour l'administrateur,
    gérant l'historique des connexions et déconnexions.
    Cette fonction gère la récupération, le filtrage et la visualisation des données,
    et nécessite des privilèges d'administrateur pour y accéder.
    """
    st.set_page_config(page_title="📜 Journal des accès", page_icon="📜", layout="wide")
    st.title("📜 Journal des accès")
    st.markdown("Recherchez et analysez l'historique d'accès de votre application.")

    # Vérification des permissions
    # L'accès est limité au rôle 'admin' pour des raisons de sécurité.
    if st.session_state.get("role") != "admin":
        st.warning("⛔ Accès réservé aux administrateurs.")
        st.stop()

    # Connexion à la base de données (peut être remplacé par une base de données réelle)
    @st.cache_resource
    def get_db_connection():
        conn = sqlite3.connect("users.db")
        return conn

    conn = get_db_connection()
    cursor = conn.cursor()

    # Création de la table 'logs' si elle n'existe pas
    # Ajout d'une colonne 'ip' pour la détection de menaces
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            role TEXT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip TEXT
        )
        """
    )
    conn.commit()

    # Chargement des données des logs
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)

    if df.empty:
        st.info("Aucun log trouvé.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # --- Affichage des Toasts et des métriques après le chargement des données ---
    st.toast("📡 Surveillance des connexions en cours...", icon="🔍")

    # Détection des tentatives de connexion échouées (force brute)
    failures = df[df["action"].str.contains("échec", case=False, na=False)]
    now = datetime.now()
    time_limit = now - timedelta(minutes=10)
    recent_failures = failures[failures["timestamp"] >= time_limit]
    if len(recent_failures) >= 3:
        st.toast("⚠️ Tentatives de connexion suspectes détectées", icon="🚨")

    # Calcul des connexions du jour pour la métrique
    df_daily = df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")
    st.sidebar.metric(
        "Connexions aujourd’hui",
        df_daily["count"].iloc[-1] if not df_daily.empty else 0,
    )

    # --- Section des alertes de sécurité ---
    st.subheader("🚨 Surveillance de Sécurité")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    # Détection des tentatives de connexion échouées (force brute)
    with col1:
        if len(recent_failures) >= 5:
            st.error(
                "⚠️ Tentative de force brute ? Plus de 5 échecs récents de connexion détectés."
            )
        else:
            st.success("✅ Aucun échec de connexion suspect détecté.")

    # Détection des rôles inhabituels
    with col2:
        valid_roles = {"admin", "doctor", "nurse", "midwife", "patient", "student"}
        unusual_connections = df[~df["role"].isin(valid_roles)]
        if not unusual_connections.empty:
            st.warning(
                f"🚨 Connexions inhabituelles détectées ({len(unusual_connections)})."
            )
        else:
            st.success("✅ Tous les rôles sont valides.")

    # Détection d'IPs non reconnues (simulation)
    with col3:
        if "ip" in df.columns:
            known_ips = df["ip"].mode().tolist()  # IP la plus fréquente
            unusual_ips = df[~df["ip"].isin(known_ips)]
            if not unusual_ips.empty:
                st.warning(f"🚨 Connexions depuis des IPs inhabituelles détectées.")
            else:
                st.success("✅ Aucune IP suspecte détectée.")

    # --- Filtres en barre latérale ---
    st.sidebar.header("🔎 Options de Filtrage")
    st.sidebar.markdown("---")

    # Filtres
    roles = ["Tout"] + sorted(df["role"].dropna().unique().tolist())
    actions = ["Tout"] + sorted(df["action"].dropna().unique().tolist())

    role_filter = st.sidebar.selectbox("🎭 Rôle", roles)
    action_filter = st.sidebar.selectbox("⚡ Action", actions)

    # Barre de recherche pour l'email
    search_email = st.sidebar.text_input("Rechercher par email", "")

    # Filtre de date
    df["date"] = df["timestamp"].dt.date
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range = st.sidebar.date_input("📅 Plage de dates", [min_date, max_date])

    # Application des filtres
    filtered_df = df.copy()
    if role_filter != "Tout":
        filtered_df = filtered_df[filtered_df["role"] == role_filter]
    if action_filter != "Tout":
        filtered_df = filtered_df[filtered_df["action"] == action_filter]
    if search_email:
        filtered_df = filtered_df[
            filtered_df["email"].str.contains(search_email, case=False, na=False)
        ]
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["date"] >= date_range[0])
            & (filtered_df["date"] <= date_range[1])
        ]

    st.markdown("---")

    # --- Métriques Clés et Statistiques ---
    st.subheader("📈 Aperçu des logs")
    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)

    with col_metrics1:
        st.metric("Total d'actions", len(filtered_df))
    with col_metrics2:
        st.metric("Utilisateurs uniques", filtered_df["email"].nunique())
    with col_metrics3:
        last_action_time = filtered_df["timestamp"].max()
        st.metric(
            "Dernière action",
            (
                last_action_time.strftime("%H:%M:%S le %Y-%m-%d")
                if pd.notna(last_action_time)
                else "N/A"
            ),
        )

    # --- Tableau de données et visualisations ---
    st.subheader("📚 Données des Logs")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📊 Visualisations interactives")
    st.markdown("---")

    # Graphique des actions par jour
    daily_actions = (
        filtered_df.groupby(filtered_df["timestamp"].dt.date)
        .size()
        .reset_index(name="count")
    )
    fig1 = px.bar(daily_actions, x="timestamp", y="count", title="📅 Activité par jour")
    fig1.update_layout(xaxis_title="Date", yaxis_title="Nombre d'actions")
    st.plotly_chart(fig1, use_container_width=True)

    # Graphique de répartition des actions
    col_viz1, col_viz2 = st.columns(2)
    with col_viz1:
        role_counts = filtered_df["role"].value_counts().reset_index()
        role_counts.columns = ["role", "count"]
        fig2 = px.pie(
            role_counts, values="count", names="role", title="🎭 Répartition par rôle"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_viz2:
        action_counts = filtered_df["action"].value_counts().reset_index()
        action_counts.columns = ["action", "count"]
        fig3 = px.bar(
            action_counts, x="action", y="count", title="⚡ Actions les plus fréquentes"
        )
        fig3.update_layout(xaxis_title="Action", yaxis_title="Nombre")
        st.plotly_chart(fig3, use_container_width=True)

    # Exportation des données
    st.markdown("---")
    st.subheader("📤 Exporter les données")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Télécharger le fichier CSV",
        data=csv,
        file_name="logs_filtrés.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    render()
