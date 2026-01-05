import streamlit as st
import time

# =========================================================
# 1. CONFIGURATION ET DONNÉES STATIQUES (Non modifiée)
# ... (le code de configuration est le même) ...
# =========================================================


# Placeholder pour les modules de formulaire non inclus dans cet exemple
class FormPlaceholder:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def render(self):
        st.header(f"✨ Page : {self.title} ✨")
        st.info(f"Ceci est le contenu détaillé de la page : **{self.description}**.")
        st.markdown("---")
        st.image(
            "https://via.placeholder.com/600x300?text=Contenu+de+la+page",
            caption=self.title,
        )


form_home = FormPlaceholder(
    "Accueil", "Bienvenue dans l’espace de la maïeutique numérique."
)
form_mission = FormPlaceholder(
    "Mission", "Soutenir les familles et les professionnel·les avec amour."
)
form_vision = FormPlaceholder("Vision", "Un monde où chaque naissance est honorée.")
form_contact = FormPlaceholder(
    "Contact", "Écrivez-nous pour toute question ou collaboration."
)
form_equipe = FormPlaceholder(
    "Notre équipe", "Les visages et les cœurs derrière le projet."
)
form_faq = FormPlaceholder("FAQ", "Réponses aux questions les plus fréquentes.")
form_links = FormPlaceholder("Liens utiles", "Ressources et partenaires de confiance.")
form_nous_joindre = FormPlaceholder(
    "Pour nous joindre", "Envoyez-nous un message doux."
)
form_papotines = FormPlaceholder(
    "Les Papotines", "Partagez vos coups de cœur, blagues et confidences."
)


# # Registre pour les formulaires Publics (utilisé pour la navigation/menu)
# # Seules les entrées avec un module placeholder sont listées ici pour cet exemple
# ,
#     "Mission": {
#         "module": form_mission,
#         "icon": "🎯",
#         "color": "#FDE2B9",
#         "description": "Soutenir les familles et les professionnel·les avec amour et enracinement culturel.",
#         "is_public": True,
#     },
#     "Vision": {
#         "module": form_vision,
#         "icon": "🌈",
#         "color": "#D3C0F9",
#         "description": "Un monde où chaque naissance est honorée.",
#         "is_public": True,
#     },
#     "Contact": {
#         "module": form_contact,
#         "icon": "✉️",
#         "color": "#FFD1DC",
#         "description": "Écrivez-nous pour toute question ou collaboration.",
#         "is_public": True,
#     },
#     "Notre équipe": {
#         "module": form_equipe,
#         "icon": "🧑‍🤝‍🧑",
#         "color": "#C1E1C1",
#         "description": "Les visages et les cœurs derrière le projet.",
#         "is_public": True,
#     },
#     "FAQ": {
#         "module": form_faq,
#         "icon": "❓",
#         "color": "#FFFACD",
#         "description": "Réponses aux questions les plus fréquentes.",
#         "is_public": True,
#     },
#     "Liens utiles": {
#         "module": form_links,
#         "icon": "🔗",
#         "color": "#E6E6FA",
#         "description": "Ressources et partenaires de confiance.",
#         "is_public": True,
#     },
#     "Pour nous joindre": {
#         "module": form_nous_joindre,
#         "icon": "📞",
#         "color": "#F5DEB3",
#         "description": "Envoyez-nous un message doux.",
#         "is_public": True,
#     },
#     "Les Papotines": {
#         "module": form_papotines,
#         "icon": "🧵",
#         "color": "#FFB6C1",
#         "description": "Partagez vos coups de cœur, blagues et confidences.",
#         "is_public": True,
#     },
# }


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

    # --- Squelette de Page de Présentation ---
    st.subheader("💡 À Propos de MSA.")
    st.markdown(
        """
    Le projet **Midwifery Service Application**, en abrégé "**MSA**", est une initiative visant à améliorer l'accès et la qualité des soins de sage-femme pour les mères et les familles des communautés cries.
    Notre objectif principal est d'offrir un soutien médical et émotionnel complet, respectueux des cultures autochtones.
    
    ---
    ### Nos axes principaux :
    * **Soins de proximité :** Réduction des déplacements pour les mères.
    * **Intégration culturelle :** Collaboration étroite avec les Aînés.
    * **Formation et réseau :** Partage des informations et des meilleures pratiques.
    
    ❤️ Merci à toutes et tous pour votre engagement.
    """
    )


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
    # CSS pour styliser les boutons (maintenu pour le style, mais l'alignement se fait par colonnes)
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

    st.title("Midwifery Services Application")
    st.caption(
        "Plateforme de soutien et de coordination dans les communautés de Waskaganish, Chisasibi et Mistissini (à venir)."
    )


from modules.public.form_registry import form_registry

# --- BANDE HORIZONTALE OBLIGATOIRE (avec st.columns) ---

# Filtrer les formulaires publics
public_forms = {
    name: entry for name, entry in form_registry.items() if entry["role"] == "public"
}

labels = list(public_forms.keys())

# Crée un nombre de colonnes égal au nombre de liens
cols = st.columns(len(labels))

# Boucle pour placer chaque bouton dans sa propre colonne
st.markdown("<div class='public-header-row'>", unsafe_allow_html=True)

for col, label in zip(cols, labels):
    with col:
        if st.button(label, key=f"nav_pub_{label}"):
            st.session_state["info_page"] = label
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Ligne de séparation douce
st.markdown(
    "<hr style='margin-top:0.5rem;margin-bottom:1rem;border:1px solid #ccc;'>",
    unsafe_allow_html=True,
)


from modules.public.form_registry import form_registry


def render_info_section():
    """
    Affiche les sections d'information spécifiques basées sur st.session_state["info_page"].
    Ce contenu est destiné à la partie publique.
    """
    current_page = st.session_state.get("info_page", "Accueil")

    # Filtrer les formulaires publics
    public_forms = {
        name: entry
        for name, entry in form_registry.items()
        if entry["role"] == "public"
    }

    if current_page in public_forms:
        form_data = public_forms[current_page]

        # Affichage du titre, icône et description (si disponibles)
        icon = getattr(form_data["module"], "ICON", "📄")
        description = getattr(form_data["module"], "DESCRIPTION", "Formulaire public")

        st.title(f"{icon} {current_page}")
        st.write(f"*{description}*")

        # Appel à la fonction de rendu spécifique
        form_data["render"]()

    else:
        st.error(f"Page d'information publique '{current_page}' non trouvée.")


# =========================================================
# 3. FONCTION PRINCIPALE DE L'INTERFACE
# =========================================================


def main_public_interface():
    """
    Fonction principale pour l'interface publique (avant connexion).
    Structure : HEADER (bande horizontale)
                CONTENT (2/3) | LOGIN (1/3)
    """
    # 1. Initialisation de l'état si nécessaire
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = "Accueil"  # Page par défaut

    # Si l'utilisateur est connecté, on quitte l'interface publique
    if st.session_state["logged_in"]:
        st.success(
            f"Bienvenue, **{st.session_state['user_role']}**! Vous êtes connecté(e)."
        )
        st.button(
            "Déconnexion", on_click=lambda: st.session_state.clear() and st.rerun()
        )
        st.header("Tableau de bord de l'utilisateur")
        st.write("Ceci est l'espace sécurisé. Le contenu du dashboard irait ici.")
        return

    # 2. 🌟 AFFICHAGE DE L'EN-TÊTE PUBLIC (BANDE HORIZONTALE EN HAUT)
    # Ceci se fait AVANT la définition des colonnes, donc il occupe toute la largeur supérieure.
    render_public_header()

    # 3. DISPOSITION EN COLONNES POUR LE CONTENU ET LA CONNEXION (SOUS L'EN-TÊTE)
    # Colonne de gauche (2/3) pour le contenu public, Colonne de droite (1/3) pour la connexion
    content_col, login_col = st.columns([2, 1])

    # --- Colonne de Gauche : Contenu Public (Mission, Vision, etc.) ---
    with content_col:
        render_info_section()

    # --- Colonne de Droite : Formulaire de Connexion ---
    with login_col:
        # Placeholder pour les messages de succès/erreur de connexion
        message_placeholder = st.empty()
        handle_login_form(message_placeholder)  # Contient la logique du formulaire

    # Bouton de retour à l'accueil
    current_page = st.session_state.get("info_page")
    if current_page != "Accueil" and not st.session_state["logged_in"]:
        with content_col:
            st.markdown("---")
            if st.button("⬅️ Retour à l'accueil", key="back_to_home_main"):
                st.session_state["info_page"] = "Accueil"
                st.rerun()


# =========================================================
# 4. POINT D'ENTRÉE DU SCRIPT (Non modifiée)
# =========================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="MSA - Midwifery Services Application",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    main_public_interface()
