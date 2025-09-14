import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# Connexion à la base
conn = sqlite3.connect("consultations.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(page_title="Espace Administrateur", page_icon="🧑‍💼", layout="wide")
st.title("🧑‍💼 Tableau de bord Administrateur")

st.sidebar.title("🔙 Navigation")
st.sidebar.page_link("main.py", label="Retour à l'accueil", icon="🏠")

# --- Filtres pour les demandes ---
st.subheader("📋 Toutes les demandes de consultation")
statut_filter = st.selectbox("Filtrer par statut", ["Tous", "En attente", "Traité"])
priorite_filter = st.selectbox("Filtrer par priorité", ["Toutes", "Urgent", "Normal"])

query = "SELECT * FROM demandes"
conditions = []
if statut_filter != "Tous":
    conditions.append(f"statut = '{statut_filter}'")
if priorite_filter != "Toutes":
    conditions.append(f"priorite = '{priorite_filter}'")
if conditions:
    query += " WHERE " + " AND ".join(conditions)

df = pd.read_sql_query(query, conn)
df["date_demande"] = pd.to_datetime(df["date_demande"])
st.dataframe(df.set_index("id"), use_container_width=True)

# --- Statistiques globales ---
st.markdown("---")
st.subheader("📈 Statistiques des demandes")
stats = pd.read_sql_query(
    "SELECT statut, COUNT(*) as total FROM demandes GROUP BY statut", conn
)
st.bar_chart(stats.set_index("statut"))

# --- Journal d’audit ---
st.markdown("---")
st.subheader("📜 Journal d’audit")

try:
    audit_df = pd.read_csv("data/audit_log.csv")
    audit_df["timestamp"] = pd.to_datetime(audit_df["timestamp"])

    # Filtres dynamiques
    users = ["Tous"] + sorted(audit_df["user"].unique().tolist())
    event_types = ["Tous"] + sorted(audit_df["event_type"].unique().tolist())

    selected_user = st.selectbox("👤 Filtrer par utilisateur", users)
    selected_event = st.selectbox("📌 Filtrer par type d'événement", event_types)
    date_range = st.date_input("📅 Filtrer par date", [])

    filtered_df = audit_df.copy()
    if selected_user != "Tous":
        filtered_df = filtered_df[filtered_df["user"] == selected_user]
    if selected_event != "Tous":
        filtered_df = filtered_df[filtered_df["event_type"] == selected_event]
    if len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df["timestamp"] >= start) & (filtered_df["timestamp"] <= end)
        ]

    st.dataframe(
        filtered_df.sort_values("timestamp", ascending=False), use_container_width=True
    )

    # Message de confirmation
    if not filtered_df.empty:
        last_event = filtered_df.sort_values("timestamp", ascending=False).iloc[0]
        st.success(
            f"✅ Dernier événement : **{last_event['event_type']}** par **{last_event['user']}**"
        )
    else:
        st.info("Aucun événement correspondant aux filtres.")

    # Export CSV
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📤 Exporter les logs filtrés en CSV",
        data=csv_data,
        file_name="audit_logs_export.csv",
        mime="text/csv",
    )

    # 📊 Graphique des événements par type
    st.markdown("---")
    st.subheader("📊 Répartition des événements par type")
    event_stats = filtered_df["event_type"].value_counts()
    st.bar_chart(event_stats)

    # 📊 Graphique des événements par jour
    st.subheader("📆 Événements par jour")
    daily_stats = filtered_df["timestamp"].dt.date.value_counts().sort_index()
    st.line_chart(daily_stats)

except FileNotFoundError:
    st.warning("⚠️ Aucun journal d’audit trouvé.")
