# generate_full_packs.py
import os

# === Définition des pages par pack ===
packs_structure = {
    "PATIENT": {
        "CarnetSante": """
import streamlit as st

def app():
    st.title("📖 Carnet de Santé")
    with st.form("carnet_sante"):
        vaccins = st.multiselect("💉 Vaccins reçus", ["BCG", "Polio", "Rougeole", "Covid-19"])
        allergies = st.text_area("Allergies connues")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Carnet mis à jour")
""",
        "Dossier": """
import streamlit as st

def app():
    st.title("🗂️ Dossier Médical")
    with st.form("dossier_patient"):
        nom = st.text_input("Nom complet")
        date_naissance = st.date_input("📅 Date de naissance")
        maladies = st.text_area("Antécédents médicaux")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Dossier sauvegardé")
""",
        "RendezVous": """
import streamlit as st

def app():
    st.title("📅 Rendez-vous")
    with st.form("rdv_patient"):
        date = st.date_input("Date du rendez-vous")
        motif = st.text_area("Motif du rendez-vous")
        submit = st.form_submit_button("Planifier")
        if submit: st.success("✅ Rendez-vous enregistré")
""",
    },
    "MIDWIFE": {
        "Demographics": """
import streamlit as st

def app():
    st.title("🧑‍🤰 Données démographiques")
    with st.form("demo_midwife"):
        nom = st.text_input("Nom")
        age = st.number_input("Âge", min_value=10, max_value=55)
        adresse = st.text_area("Adresse")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Données démographiques enregistrées")
""",
        "PrenatalCare": """
import streamlit as st

def app():
    st.title("🤰 Suivi Prénatal")
    with st.form("prenatal"):
        terme = st.number_input("Durée de grossesse (semaines)", 0, 42)
        tension = st.text_input("Tension artérielle")
        poids = st.number_input("Poids (kg)")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Suivi prénatal enregistré")
""",
        "IntrapartumCare": """
import streamlit as st

def app():
    st.title("🍼 Suivi Intrapartum")
    with st.form("intrapartum"):
        contractions = st.text_area("Observations des contractions")
        dilation = st.number_input("Dilatation (cm)", 0, 10)
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Données intrapartum enregistrées")
""",
        "PostNatalCare": """
import streamlit as st

def app():
    st.title("👩‍🍼 Suivi Postnatal")
    with st.form("postnatal"):
        allaitement = st.selectbox("Allaitement", ["Exclusif", "Mixte", "Non"])
        etat_maman = st.text_area("État de la mère")
        etat_bebe = st.text_area("État du bébé")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Suivi postnatal sauvegardé")
""",
        "ThroughoutCare": """
import streamlit as st

def app():
    st.title("📊 Suivi Continu")
    st.info("Suivi global de la grossesse et de l’accouchement")
""",
    },
    "MESSAGES": {
        "Inbox": """
import streamlit as st

def app():
    st.title("📥 Boîte de Réception")
    st.write("Ici s’afficheront les messages reçus.")
""",
        "Chat": """
import streamlit as st

def app():
    st.title("💬 Chat en direct")
    msg = st.text_input("Votre message")
    if st.button("Envoyer"): st.success("✅ Message envoyé")
""",
    },
    "STAGIAIRE": {
        "Journal": """
import streamlit as st

def app():
    st.title("📔 Journal de Stage")
    with st.form("journal_stage"):
        jour = st.date_input("📅 Date")
        activites = st.text_area("Activités réalisées")
        evaluation = st.slider("Évaluation du jour", 1, 10, 5)
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Journal de stage sauvegardé")
""",
        "Evaluation": """
import streamlit as st

def app():
    st.title("📝 Évaluation de Stage")
    with st.form("eval_stage"):
        note = st.slider("Note du tuteur", 1, 10, 5)
        commentaire = st.text_area("Commentaire du tuteur")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Évaluation enregistrée")
""",
    },
    "ETUDIANTE": {
        "Cours": """
import streamlit as st

def app():
    st.title("📚 Suivi des cours")
    with st.form("cours_etudiante"):
        cours = st.text_input("Cours suivi")
        notes = st.text_area("Notes personnelles")
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Cours enregistré")
""",
        "Suivi": """
import streamlit as st

def app():
    st.title("🎓 Suivi Étudiante")
    with st.form("suivi_etudiante"):
        questions = st.text_area("Questions pour le tuteur")
        progression = st.slider("Progression (%)", 0, 100, 0)
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Suivi enregistré")
""",
    },
    "DOCTORANTE": {
        "These": """
import streamlit as st

def app():
    st.title("📖 Suivi de Thèse")
    with st.form("these_doc"):
        sujet = st.text_input("Sujet de recherche")
        etape = st.selectbox("Étape actuelle", ["Revue", "Collecte", "Analyse", "Rédaction", "Soutenance"])
        submit = st.form_submit_button("Enregistrer")
        if submit: st.success("✅ Suivi de thèse enregistré")
""",
        "Publications": """
import streamlit as st

def app():
    st.title("📑 Publications & Communications")
    with st.form("pub_doc"):
        titre = st.text_input("Titre de la publication")
        conference = st.text_input("Conférence / Revue")
        date = st.date_input("📅 Date")
        submit = st.form_submit_button("Ajouter")
        if submit: st.success("✅ Publication ajoutée")
""",
    },
}


# === Générateur de fichiers ===
def generate_packs(base_dir="packs"):
    for pack, pages in packs_structure.items():
        pack_dir = os.path.join(base_dir, pack.upper())
        os.makedirs(pack_dir, exist_ok=True)

        for page, code in pages.items():
            filename = os.path.join(pack_dir, f"{page}.py")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code.strip())
            print(f"✅ {pack}/{page}.py créé")


if __name__ == "__main__":
    generate_packs()
    print("🎉 Tous les packs et leurs pages ont été générés avec succès")
