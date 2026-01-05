from modules.public.form_registry import form_registry

public_forms = {
    name: entry
    for name, entry in form_registry.items()
    if entry.get("role") == "PUBLIC"
}

import streamlit as st
import time

# =========================================================
# 1. CONFIGURATION ET DONNÉES STATIQUES (Non modifiée)
# ... (le code de configuration est le même) ...
# =========================================================

from modules.public.form_home import form_home
from modules.public.form_mission import form_mission
from modules.public.form_vision import form_vision
from modules.public.form_contact import form_contact
from modules.public.form_equipe import form_equipe
from modules.public.form_faq import form_faq
from modules.public.form_links import form_links
from modules.public.form_nous_joindre import form_nous_joindre
from modules.public.form_papotines import form_les_papotines
from modules.public.form_qui_sommes_nous import form_qui_sommes_nous

# =========================================================
# 2. REGISTRE PUBLIC (utilisé pour la navigation/menu)
# =========================================================
PUBLIC_FORMS_REGISTRY = {
    "Accueil": {
        "module": form_home,
        "icon": "🏠",
        "color": "#AEDFF7",
        "description": "Midwifery Services Application.",
        "is_public": True,
    },
    "Mission": {
        "module": form_mission,
        "icon": "🎯",
        "color": "#FDE2B9",
        "description": "Soutenir les familles et les professionnel·les avec amour et enracinement culturel.",
        "is_public": True,
    },
    "Vision": {
        "module": form_vision,
        "icon": "🌈",
        "color": "#D3C0F9",
        "description": "Un monde où chaque naissance est honorée.",
        "is_public": True,
    },
    "Contact": {
        "module": form_contact,
        "icon": "✉️",
        "color": "#FFD1DC",
        "description": "Écrivez-nous pour toute question ou collaboration.",
        "is_public": True,
    },
    "Notre équipe": {
        "module": form_equipe,
        "icon": "🧑‍🤝‍🧑",
        "color": "#C1E1C1",
        "description": "Les visages et les cœurs derrière le projet.",
        "is_public": True,
    },
    "FAQ": {
        "module": form_faq,
        "icon": "❓",
        "color": "#FFFACD",
        "description": "Réponses aux questions les plus fréquentes.",
        "is_public": True,
    },
    "Liens utiles": {
        "module": form_links,
        "icon": "🔗",
        "color": "#E6E6FA",
        "description": "Ressources et partenaires de confiance.",
        "is_public": True,
    },
    "Pour nous joindre": {
        "module": form_nous_joindre,
        "icon": "📞",
        "color": "#F5DEB3",
        "description": "Envoyez-nous un message doux.",
        "is_public": True,
    },
    "Les Papotines": {
        "module": form_les_papotines,
        "icon": "🧵",
        "color": "#FFB6C1",
        "description": "Partagez vos coups de cœur, blagues et confidences.",
        "is_public": True,
    },
}


# Utilisateurs pour l'exemple de connexion
USER_PASSWORDS = {
    "MIDWIFE": "pass123",
    "DOCTOR": "secure456",
    "ADMIN": "superadmin",
}

STATIC_ASSET_URLS = {
    "img_1": "https://via.placeholder.com/900x400?text=Image+1+du+Carrousel",
    "img_2": "https://via.placeholder.com/900x400?text=Image+2+du+Carrousel",
    "img_3": "https://via.placeholder.com/900x400?text=Image+3+du+Carrousel",
}

# =========================================================
# 2. FONCTIONS UTILITAIRES (HELPERS) (Non modifiée)
# ... (le code des helpers est le même) ...
# =========================================================


def load_static_asset(asset_name):
    """Charge l'URL d'un asset statique simulé (usage pour URL/HTML)."""
    return STATIC_ASSET_URLS.get(asset_name, "")


def render_bebe_experience():
    """Affiche l'animation du nouveau-né et le son (version simulée pour l'audio)."""
    st.markdown(
        """
        <div style="border: 2px solid #ffb6c1; border-radius: 12px; padding: 1rem; background-color: #fff0f5;">
            <h3 style="color:#d63384;">👶 Le souffle de la vie</h3>
            <div id="typewriter" style="font-size:1.1rem; font-family:monospace; color:#333;"></div>
        </div>
        <script>
        const text = "Un nouveau-né pleure doucement... et le monde s’éveille avec tendresse.";
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                document.getElementById("typewriter").innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        // Utilisation d'un drapeau pour éviter l'exécution multiple dans Streamlit
        if (document.getElementById("typewriter") && !document.getElementById("typewriter").getAttribute("data-typed")) {
            typeWriter();
            document.getElementById("typewriter").setAttribute("data-typed", "true");
        }
        </script>
    """,
        unsafe_allow_html=True,
    )
    # L'audio réel nécessiterait un fichier accessible
    # st.audio(audio_path, format="audio/mp3")


def render_home_page():
    """Affiche le carrousel et le squelette de la page de présentation."""
    # --- Carrousel Dynamique (HTML/JS simulé) ---
    CAROUSEL_HTML = f"""
    <style>
        .carousel-container {{
            overflow: hidden;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }}
        .carousel-track {{
            display: flex;
            transition: transform 1s ease-in-out;
            width: 300%;
        }}
        .carousel-item {{
            min-width: 33.33%;
            box-sizing: border-box;
        }}
        .carousel-item img {{
            width: 100%;
            height: 400px;
            display: block;
            object-fit: cover;
            border-radius: 8px;
        }}
    </style>
    <div class="carousel-container">
        <div class="carousel-track" id="msa-carousel-track">
            <div class="carousel-item"><img src="{load_static_asset('img_1')}" alt="Image 1"></div>
            <div class="carousel-item"><img src="{load_static_asset('img_2')}" alt="Image 2"></div>
            <div class="carousel-item"><img src="{load_static_asset('img_3')}" alt="Image 3"></div>
        </div>
    </div>
    <script>
        const track = document.getElementById('msa-carousel-track');
        if (track && !window.msaCarouselInterval) {{
            let currentIdx = 0;
            const totalItems = 3;
            const intervalTime = 6000;

            window.msaCarouselInterval = setInterval(() => {{
                currentIdx = (currentIdx + 1) % totalItems;
                const offset = -currentIdx * 100 / totalItems;

                track.style.transform = `translateX(${{offset}}%)`;
            }}, intervalTime);
        }}
    </script>
    """
    st.markdown(CAROUSEL_HTML, unsafe_allow_html=True)


def handle_login_form(message_placeholder):
    """
    Affiche et gère le formulaire de connexion.
    Utilise une DIV stylisée pour encadrer les champs comme demandé.
    """
    # CSS pour styliser le bloc de connexion
    st.markdown(
        """
        <style>
        .login-box {
            padding: 20px;
            border-radius: 15px;
            border: 3px solid #FFD1DC; /* Bordure rose douce */
            background-color: #FFF0F5; /* Fond rose très clair */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .login-box .stTextInput > div > div > input, .login-box .stButton > button {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🏠 Bienvenue dans MSA !❤️")

        with st.form("msa_login_form", clear_on_submit=True):
            st.markdown(
                """
                <p style="font-size:1rem; color:#d63384; font-style:italic;">
                Veuillez utiliser votre rôle et votre mot de passe.
                </p>
                """,
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Identifiant (rôle)",
                placeholder="Ex: MIDWIFE, DOCTOR, ADMIN...",
            ).upper()

            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter", type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        role = username.upper()
        if role in USER_PASSWORDS and password == USER_PASSWORDS[role]:
            message_placeholder.success(
                f"✅ Connexion réussie en tant que **{role}**. Redirection..."
            )
            # Mise à jour de l'état de la session pour la connexion
            st.session_state["user_role"] = role
            st.session_state["logged_in"] = True
            st.session_state["info_page"] = "Tableau de bord"
            time.sleep(0.5)
            st.rerun()
        else:
            message_placeholder.error("⛔ Identifiant ou mot de passe incorrect.")


def render_public_header():
    """Affiche l'en-tête public avec les liens d'information stylisés en bande horizontale."""

    # --- CSS pour styliser les boutons ---
    st.markdown(
        """
        <style>
        .public-header-row .stButton > button {
            background: none !important;
            border: none !important;
            color: #1e40af; /* Bleu lien */
            padding: 5px 10px;
            text-decoration: none !important;
            box-shadow: none;
            margin: 0; /* Important: enlever les marges si possible */
            width: 100%; /* S'assurer que le bouton prend la largeur de sa colonne */
        }
        .public-header-row .stButton > button:hover {
            background-color: #eff6ff !important;
            text-decoration: underline !important;
            color: #3b82f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Titre et sous-titre ---
    st.title("Midwifery Services Application")
    st.caption(
        "Plateforme de soutien et de coordination dans les communautés de Waskaganish, "
        "Chisasibi et Mistissini (à venir)."
    )

    # --- Génération dynamique des boutons ---
    labels = list(PUBLIC_FORMS_REGISTRY.keys())

    if labels:
        cols = st.columns(len(labels))
        st.markdown("<div class='public-header-row'>", unsafe_allow_html=True)
        for i, (col, label) in enumerate(zip(cols, labels)):
            with col:
                # ✅ Ajout de l'index pour garantir l'unicité
                if st.button(label, key=f"nav_pub_{i}_{label}"):
                    st.session_state["info_page"] = label
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Aucun formulaire public disponible pour l'instant.")


# --- BANDE HORIZONTALE OBLIGATOIRE (avec st.columns) ---
labels = list(PUBLIC_FORMS_REGISTRY.keys())

if labels:
    cols = st.columns(len(labels))
    st.markdown("<div class='public-header-row'>", unsafe_allow_html=True)
    for col, label in zip(cols, labels):
        with col:
            if st.button(label, key=f"nav_pub_{label}"):
                st.session_state["info_page"] = label
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Aucun formulaire public disponible pour l'instant.")


def render_info_section():
    current_page = st.session_state.get("info_page", "Accueil")

    if current_page not in PUBLIC_FORMS_REGISTRY:
        st.error(f"Page d'information publique '{current_page}' non trouvée.")
        return

    form_data = PUBLIC_FORMS_REGISTRY[current_page]
    module_ref = form_data.get("module")

    # En-tête
    st.title(f"{form_data.get('icon', '')} {current_page}")
    if form_data.get("description"):
        st.write(f"*{form_data['description']}*")

    # Debug visible
    # st.caption(f"Module type: {type(module_ref).__name__}")

    # Appel sécurisé
    if callable(module_ref):
        module_ref()  # vrai wrapper décoré, e.g., form_accueil()
    elif hasattr(module_ref, "render") and callable(module_ref.render):
        module_ref.render()  # ancien placeholder compatible
        st.warning(
            "Cette page utilise encore un placeholder (render). Remplacez par la fonction décorée."
        )
    else:
        st.error(
            "Le module n'est ni une fonction ni un objet avec render(). Vérifiez le registre et les imports."
        )


def main_public_interface():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = "Accueil"

    if st.session_state.get("logged_in", False):
        st.success(f"Bienvenue, **{st.session_state.get('user_role', 'invité')}**!")
        st.button("Déconnexion", on_click=lambda: st.session_state.clear())
        st.header("Tableau de bord de l'utilisateur")
        st.write("Ceci est l'espace sécurisé. Le contenu du dashboard irait ici.")
        return

    # ✅ Appel unique
    render_public_content()


def render_public_content():
    # ✅ définir les colonnes ici
    content_col, login_col = st.columns([2, 1])

    # 🟦 Colonne gauche : contenu public
    with content_col:
        page = st.session_state.get("info_page", "Accueil")
        page_config = PUBLIC_FORMS_REGISTRY.get(page)

        if page_config and "module" in page_config:
            page_config["module"]()  # appelle la fonction de rendu
        else:
            st.warning(f"Page '{page}' non définie.")

        # ✅ Bouton retour à l'accueil (placé dans la colonne gauche)
        current_page = st.session_state.get("info_page", "Accueil")
        if current_page != "Accueil" and not st.session_state.get("logged_in", False):
            st.markdown("---")
            if st.button("⬅️ Retour à l'accueil", key="back_to_home_main"):
                st.session_state["info_page"] = "Accueil"
                st.rerun()

    # 🟦 Colonne droite : login + vidéo/audio
    with login_col:
        message_placeholder = st.empty()
        handle_login_form(message_placeholder)

        st.markdown("---")
        subcol, _ = st.columns([2, 1])
        with subcol:
            st.markdown("#### 🎥 Vidéo explicative")
            st.video("static/mov_bbb.mp4")

            st.subheader("")
            try:
                with open("static/exemple.mp3", "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            except FileNotFoundError:
                st.error("")

        # ✅ Menu dépliant avec identifiants de test (cachés par défaut)
        with st.expander("Identifiants de test (rôles et mots de passe)"):
            test_credentials = {
                "MIDWIFE": "msa2024",
                "NURSE": "nurse2024",
                "DOCTOR": "doc2024",
                "PATIENT": "pat2024",
                "STUDENT": "stud2024",
                "INTERN": "intern2024",
                "DOCTORAL": "phd2024",
                "ADMIN": "admin2024",
            }
            for role, pwd in test_credentials.items():
                st.write(f"**{role}** → `{pwd}`")


# =========================================================
# 4. POINT D'ENTRÉE DU SCRIPT
# =========================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="MSA - Midwifery Services Application",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    main_public_interface()
