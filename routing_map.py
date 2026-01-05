import streamlit as st


# --- Modules publics ---
def render_home():
    st.markdown("## 🏠 Accueil")


def render_mission():
    st.markdown("Notre mission")


def render_vision():
    st.markdown("Notre vision")


def render_qui_sommes_nous():
    st.markdown("Quisommes-nous ?")


def render_team():
    st.markdown("Notre équipe")


def render_contact():
    st.markdown("Nous joindre")


def render_faq():
    st.markdown("Foire aux questions")


def render_about():
    st.markdown("## 👥 Qui sommes-nous ?\nBienvenue dans notre espace de présentation.")


# --- Expression libre : Les Papotines ---
def render_papotines():
    st.markdown("## 🗣️ Les Papotines")
    st.info("Partagez vos coups de cœur, blagues, annonces ou confidences.")
    with st.form("form_papotines"):
        pseudo = st.text_input("👩‍💼 Votre prénom ou pseudo")
        thème = st.selectbox("🎨 Thème", ["Blague", "Annonce", "Coup de cœur", "Autre"])
        message = st.text_area("💬 Votre message")
        publier = st.form_submit_button("📣 Publier")
        if publier and message:
            st.success("Papotine publiée 💖")
            st.markdown(f"**{pseudo or 'Anonyme'}** a partagé un(e) *{thème}* :")
            st.markdown(f"> {message}")


# --- Liens utiles ---
def render_links():
    st.markdown("## 🔗 Liens utiles")
    st.info("Ressources pour s’informer, se former, ou explorer.")

    if "liens_utiles" not in st.session_state:
        st.session_state.liens_utiles = []

    with st.form("form_liens_utiles"):
        titre = st.text_input("📌 Titre du lien")
        url = st.text_input("🌐 URL complète")
        catégorie = st.selectbox(
            "📂 Catégorie",
            [
                "Revue de presse",
                "Publication scientifique",
                "Site gouvernemental",
                "Autoformation / Tutoriel",
                "Autre",
            ],
        )
        description = st.text_area("📝 Description du contenu")
        soumis = st.form_submit_button("📥 Ajouter le lien")

        if soumis and url:
            st.session_state.liens_utiles.append(
                {
                    "Titre": titre or "Lien sans titre",
                    "URL": url,
                    "Catégorie": catégorie,
                    "Description": description,
                }
            )
            st.success("Lien ajouté avec succès !")

    st.markdown("### 📚 Liens enregistrés")
    filtre = st.selectbox(
        "🔎 Filtrer par catégorie",
        ["Toutes"] + list({l["Catégorie"] for l in st.session_state.liens_utiles}),
    )
    liens_filtrés = (
        st.session_state.liens_utiles
        if filtre == "Toutes"
        else [l for l in st.session_state.liens_utiles if l["Catégorie"] == filtre]
    )

    for lien in liens_filtrés:
        st.markdown(f"**{lien['Titre']}** ({lien['Catégorie']})")
        st.markdown(f"[Accéder au lien]({lien['URL']})")
        st.markdown(f"> {lien['Description']}")
        st.markdown("---")


# --- Archives : Agora ---
def render_agora():
    st.markdown("## 💬 Agora (archives)")
    st.info("Exprimez-vous librement : anecdotes, blagues, ventes, coups de cœur…")


# --- Bandeau de navigation publique ---
def render_top_strip():
    st.markdown("### 🌐 Navigation publique")
    cols = st.columns(10)
    top_items = [
        ("🏠 HOME", "top_home"),
        ("🎯 Mission", "top_mission"),
        ("📦 Vision", "top_vision"),
        ("📦 Équipe", "top_team"),
        ("❓ FAQ", "top_faq"),
        ("📬 Contact", "top_contact"),
        ("👥 Qui-sommes-nous ?", "top_about"),
        ("🗣️ Les Papotines", "top_papotines"),
    ]
    for i, (label, key) in enumerate(top_items):
        with cols[i]:
            st.button(label, key=key)


# --- ROUTING_MAP exportable ---
ROUTING_MAP = {
    "top_home": render_home,
    "top_mission": render_mission,
    "top_vision": render_vision,
    "top_faq": render_faq,
    "top_contact": render_contact,
    "top_about": render_about,
    "top_papotines": render_papotines,
    "top_links": render_links,
}
