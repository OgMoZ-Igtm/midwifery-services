import streamlit as st
from datetime import datetime
from database import create_tables, nettoyer_sauvegardes, enregistrer_log, get_logs
import os
import pandas as pd


st.title("🛠️ Maintenance & Backups")
st.markdown(
    """
    This page allows you to manage the **maintenance of the Midwifery Services application**.  
    You can **reset tables**, **clean backups**, or **force deletion**.  
    """
)

# 🎛️ Maintenance options
force = st.checkbox("⚠️ Force delete ALL backups", value=False)
dry_run = st.checkbox("🧪 Simulation only (dry-run)", value=False)
log = st.checkbox("📝 Save actions in logs", value=True)
user = st.text_input("👤 User name", value=st.session_state.get("username", "system"))

# 📅 Date & Time
st.write(f"🕒 Action time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# 🚀 Start maintenance
if st.button("▶️ Run Maintenance"):
    create_tables()
    st.success("✅ Tables checked or created.")
    if log:
        enregistrer_log("Tables checked or created", user)

    folder = "sauvegardes"
    if not os.path.exists(folder):
        os.makedirs(folder)
        st.info("📁 Backup folder created.")
        if log:
            enregistrer_log("Backup folder created", user)

    files = os.listdir(folder)

    if force:
        if dry_run:
            st.warning("🧪 [Simulation] The following files would be deleted:")
            for f in files:
                st.write(f" - {f}")
            if log:
                enregistrer_log("Simulation: forced deletion of backups", user)
        else:
            for file in files:
                path = os.path.join(folder, file)
                if os.path.isfile(path):
                    os.remove(path)
            st.error("🧨 All backups deleted (forced mode).")
            if log:
                enregistrer_log("Forced deletion of all backups", user)
    else:
        if dry_run:
            st.warning("🧪 [Simulation] Files older than 7 days would be deleted.")
            if log:
                enregistrer_log("Simulation: cleaning old backups", user)
        else:
            nettoyer_sauvegardes()
            st.success("🧼 Old backups (>7 days) deleted.")
            if log:
                enregistrer_log("Cleaning old backups (>7 days)", user)

    st.success("✅ Maintenance completed.")
    if log:
        enregistrer_log("Maintenance completed", user)

# 📜 Logs history
st.markdown("---")
st.subheader("📜 Recent actions log")

try:
    logs = get_logs(limit=20)
    if logs:
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True)

        # ⬇️ Export button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download logs as CSV",
            data=csv,
            file_name=f"maintenance_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    else:
        st.info("ℹ️ No logs available.")
except Exception as e:
    st.error(f"Error loading logs: {e}")
