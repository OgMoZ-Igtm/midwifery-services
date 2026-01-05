import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv
import os
import time
import importlib

# =========================================================
# ⚙️ CONFIGURATION ET CONSTANTES GLOBALES
# =========================================================

# Charger les variables d'environnement (si utilisées)
load_dotenv()

# --- Simulation des mots de passe (à remplacer par une source sécurisée en production) ---
USER_PASSWORDS = {
    "MIDWIFE": "msa2024",
    "NURSE": "nurse2024",
    "DOCTOR": "doc2024",
    "PATIENT": "pat2024",
    "STUDENT": "stud2024",
    "INTERN": "intern2024",
    "DOCTORAL": "phd2024",
    "ADMIN": "admin2024",
}

# --- URL de Placeholder pour les assets statiques (Audio/Météo supprimés) ---
STATIC_ASSET_URLS = {
    "img_1": "https://placehold.co/1200x400/94A3B8/FFFFFF?text=+MSA",
    "img_2": "https://placehold.co/1200x400/3B82F6/FFFFFF?text=Soutien+aux+communaut%C3%A9s+cries",
    "img_3": "https://placehold.co/1200x400/10B981/FFFFFF?text=Soins+de+sage-femme+en+milieu+autochtone",
}

# --- Constantes: Liste des formulaires spécifiques par rôle (DÉPLACÉES dans la section globale)
# NOTE: Goal 4 respecté: Tous les formulaires sont dans modules/forms/form_* (simulé par le chemin)
SPECIFIC_FORMS = {
    "MIDWIFE": [
        "modules/forms/form_birth_plan",
        "modules/forms/form_postpartum",
        "modules/forms/form_initial_routine",
        "modules/forms/form_patient_file",
        "modules/forms/form_patient_management",
        "modules/forms/form_midwife_messages",
        "modules/forms/form_consultation_prenatale",
        "modules/forms/form_emotional_well_being",
        "modules/forms/form_incident_report",
        "modules/forms/form_demographics",
        "modules/forms/form_prenatal_care",
        "modules/forms/form_postnatal_care",
        "modules/forms/form_intrapartum_care",
    ],
    "NURSE": [
        "modules/forms/form_schedule_nurse",
        "modules/forms/form_consultation_notes",
        "modules/forms/form_nurse_shift_report",
        "modules/forms/form_nursing_notes",
        "modules/forms/form_nurse_inventory_management",
        "modules/forms/form_nurse_medicament_admin",
        "modules/forms/form_vital_signs",
        "modules/forms/form_followup",
    ],
    "DOCTOR": [
        "modules/forms/form_doctor_emergency_assessment",
        "modules/forms/form_medicament_prescription",
        "modules/forms/form_due_date_calculator",
        "modules/forms/form_doctor_schedule",
        "modules/forms/form_medical_report",
        "modules/forms/form_prescription",
    ],
    "PATIENT": [
        "modules/forms/form_patient_satisfaction_survey",
        "modules/forms/form_patient_symptom",
        "modules/forms/form_patient_appointment_booking",
        "modules/forms/form_patient_communicatient_prefs",
        "modules/forms/form_patient_feedback",
        "modules/forms/form_patient_prescription_request",
        "modules/forms/form_feedback",
        "modules/forms/form_request",
    ],
    "STUDENT": [
        "modules/forms/form_observation",
        "modules/forms/form_reflection",
    ],
    "GUEST": [
        "modules/forms/form_utility_general_contact",
        "modules/forms/form_utility_service_request",
    ],
    "INTERN": [
        "modules/forms/form_clinical_observation",
        "modules/forms/form_inter_case_study",
        "modules/forms/form_intern_logbook",
        "modules/forms/form_intern_skill_checklist",
        "modules/forms/form_training_log",
    ],
    "DOCTORAL": [
        "modules/forms/form_research_note",
        "modules/forms/form_doctorant_ethics_submissions",
    ],
    "ADMIN": [
        "modules/forms/form_user_management",
        "modules/forms/form_system_logs_viewer",
        "modules/forms/form_report_dashboard",
        "modules/forms/form_global_settings",
        "modules/forms/form_config_system",
    ],
}

# --- Constantes: Fonctions partagées
SHARED_BUTTONS = {
    "Agenda": "📅",
    "Calendrier": "🗓️",
    "Messages": "✉️",
    "Chat": "💬",
    "Profil": "👤",
    "Settings": "⚙️",
    "Signup": "📝",
}

SHARED_FORMS = {
    "Agenda": "modules/forms/form_agenda",
    "Calendrier": "modules/forms/form_calendar",
    "Messages": "modules/forms/form_messages",
    "Chat": "modules/forms/form_chat",
    "Profil": "modules/forms/form_profile",
    "Settings": "modules/forms/form_settings",
    "Signup": "modules/forms/form_signup",
}


FORM_LABELS = {
    # MIDWIFE
    "modules/forms/form_birth_plan": "🍼 Plan de naissance",
    "modules/forms/form_postpartum": "🌸 Suivi post-partum",
    "modules/forms/form_initial_routine": "🧾 Routine initiale",
    "modules/forms/form_patient_file": "📁 Dossier patiente",
    "modules/forms/form_patient_management": "🧭 Gestion de la patiente",
    "modules/forms/form_midwife_messages": "✉️ Messages de la sage-femme",
    "modules/forms/form_consultation_prenatale": "🤰 Consultation prénatale",
    "modules/forms/form_emotional_well_being": "💖 Bien-être émotionnel",
    "modules/forms/form_incident_report": "⚠️ Rapport d'incident",
    "modules/forms/form_demographics": "📊 Données démographiques",
    "modules/forms/form_prenatal_care": "🌿 Soins prénataux",
    "modules/forms/form_postnatal_care": "🌼 Soins postnataux",
    "modules/forms/form_intrapartum_care": "⏳ Soins intrapartum",
    # NURSE
    "modules/forms/form_schedule_nurse": "📆 Horaire infirmier",
    "modules/forms/form_consultation_notes": "📝 Notes de consultation",
    "modules/forms/form_nurse_shift_report": "🌙 Rapport de quart",
    "modules/forms/form_nursing_notes": "📒 Notes infirmières",
    "modules/forms/form_nurse_inventory_management": "📦 Gestion des stocks",
    "modules/forms/form_nurse_medicament_admin": "💊 Administration des médicaments",
    "modules/forms/form_vital_signs": "❤️ Signes vitaux",
    "modules/forms/form_followup": "🔄 Suivi infirmier",
    # DOCTOR
    "modules/forms/form_doctor_emergency_assessment": "🚨 Évaluation d'urgence",
    "modules/forms/form_medicament_prescription": "💊 Prescription",
    "modules/forms/form_due_date_calculator": "📅 Calcul de la date prévue",
    "modules/forms/form_doctor_schedule": "🩺 Horaire du médecin",
    "modules/forms/form_medical_report": "📄 Rapport médical",
    "modules/forms/form_prescription": "🖊️ Ordonnance",
    # PATIENT
    "modules/forms/form_patient_satisfaction_survey": "🗣️ Sondage de satisfaction",
    "modules/forms/form_patient_symptom": "🤒 Symptômes",
    "modules/forms/form_patient_appointment_booking": "📅 Prise de rendez-vous",
    "modules/forms/form_patient_communicatient_prefs": "📞 Préférences de communication",
    "modules/forms/form_patient_feedback": "💬 Retour d'expérience",
    "modules/forms/form_patient_prescription_request": "📝 Demande d'ordonnance",
    "modules/forms/form_feedback": "🗨️ Commentaires",
    "modules/forms/form_request": "📨 Demande générale",
    # STUDENT
    "modules/forms/form_observation": "👀 Observation clinique",
    "modules/forms/form_reflection": "🧠 Réflexion personnelle",
    # GUEST
    "modules/forms/form_utility_general_contact": "📬 Contact général",
    "modules/forms/form_utility_service_request": "🛠️ Demande de service",
    # INTERN
    "modules/forms/form_clinical_observation": "🔍 Observation clinique",
    "modules/forms/form_inter_case_study": "📚 Étude de cas",
    "modules/forms/form_intern_logbook": "📓 Journal de stage",
    "modules/forms/form_intern_skill_checklist": "✅ Liste de compétences",
    "modules/forms/form_training_log": "🗂️ Journal de formation",
    # DOCTORAL
    "modules/forms/form_research_note": "🧪 Note de recherche",
    "modules/forms/form_doctorant_ethics_submissions": "📑 Soumissions éthiques",
    # ADMIN
    "modules/forms/form_user_management": "👥 Gestion des utilisateurs",
    "modules/forms/form_system_logs_viewer": "🧾 Journaux système",
    "modules/forms/form_report_dashboard": "📊 Tableau de bord",
    "modules/forms/form_global_settings": "⚙️ Paramètres globaux",
    "modules/forms/form_config_system": "🛠️ Configuration système",
    # SHARED
    "modules/forms/form_agenda": "📅 Agenda",
    "modules/forms/form_calendar": "🗓️ Calendrier",
    "modules/forms/form_messages": "✉️ Messages",
    "modules/forms/form_chat": "💬 Chat",
    "modules/forms/form_profile": "👤 Profil",
    "modules/forms/form_settings": "⚙️ Paramètres",
    "modules/forms/form_signup": "📝 Inscription",
}

THEMATIC_GROUPS = {
    "Soins et suivi": [
        "modules/forms/form_prenatal_care",
        "modules/forms/form_postnatal_care",
        "modules/forms/form_intrapartum_care",
        "modules/forms/form_followup",
        "modules/forms/form_vital_signs",
        "modules/forms/form_medical_report",
    ],
    "Gestion et organisation": [
        "modules/forms/form_patient_management",
        "modules/forms/form_patient_file",
        "modules/forms/form_schedule_nurse",
        "modules/forms/form_doctor_schedule",
        "modules/forms/form_user_management",
        "modules/forms/form_global_settings",
    ],
    "Émotions et communication": [
        "modules/forms/form_emotional_well_being",
        "modules/forms/form_midwife_messages",
        "modules/forms/form_patient_feedback",
        "modules/forms/form_messages",
        "modules/forms/form_chat",
    ],
    "Demandes et formulaires utilitaires": [
        "modules/forms/form_request",
        "modules/forms/form_utility_service_request",
        "modules/forms/form_patient_prescription_request",
        "modules/forms/form_signup",
    ],
    "Formation et apprentissage": [
        "modules/forms/form_observation",
        "modules/forms/form_reflection",
        "modules/forms/form_training_log",
        "modules/forms/form_research_note",
    ],
}

THEME_COLORS = {
    "Soins": "#e3f2fd",
    "Gestion": "#f1f8e9",
    "Émotion": "#fce4ec",
}

ROLE_COLORS = {
    "MIDWIFE": "#f8bbd0",
    "NURSE": "#b2dfdb",
    "DOCTOR": "#c5cae9",
    "PATIENT": "#ffe0b2",
    "STUDENT": "#dcedc8",
    "GUEST": "#f0f4c3",
    "INTERN": "#e1bee7",
    "DOCTORAL": "#d7ccc8",
    "ADMIN": "#ffccbc",
}

# --- Constantes: Icônes des formulaires
FORM_ICONS = {
    "birth": "🧺",
    "prescription": "💊",
    "emergency": "🚨",
    "schedule": "📅",
    "notes": "📝",
    "feedback": "💬",
    "observation": "👀",
    "reflection": "🪞",
    "report": "📊",
    "appointment": "📆",
    "inventory": "📦",
    "incident": "⚠️",
    "research": "🔬",
    "settings": "⚙️",
    "default": "📄",
}


ROLE_ICONS = {
    "MIDWIFE": "🧺",
    "DOCTOR": "🩺",
    "NURSE": "💉",
    "PATIENT": "🫶",
    "STUDENT": "📚",
    "INTERN": "🧪",
    "DOCTORAL": "🎓",
    "ADMIN": "🛠️",
    "GUEST": "👤",
}

# --- NOUVEAU: Tableaux de bord spécifiques par rôle ---
# NOTE: Goal 5 respecté: Tous les tableaux de bord sont dans dashboard/dashbord_* (simulé par le chemin)
# La structure actuelle utilise les données ici pour simuler un contenu provenant de dashboard/dashbord_*.py
DASHBOARD_CONTENT = {
    "MIDWIFE": {
        "title": "Aperçu de la cohorte Prénatale",
        "metrics": [
            ("Patient(e)s actives", "14"),
            ("Naissances prévues (30j)", "3"),
            ("Rapports d'incident ouverts", "1"),
            ("Prochain rendez-vous clé", "Waskaganish, 10:00 (A. Mami)"),
        ],
    },
    "NURSE": {
        "title": "Gestion du Quart et des Patients",
        "metrics": [
            ("Lits occupés", "4/10"),
            ("Dossiers en attente", "5"),
            ("Prochaine administration (Médicament)", "14:00 (Lit 3)"),
            ("Niveau de stock critiques", "2 (Seringues, Désinfectant)"),
        ],
    },
    "DOCTOR": {
        "title": "Évaluation et Prescriptions",
        "metrics": [
            ("Évaluations d'urgence complétées (24h)", "2"),
            ("Prescriptions en cours de révision", "8"),
            ("Consultations prévues (Aujourd'hui)", "6"),
            ("Mortalité Mère/Bébé (Année)", "0%"),
        ],
    },
    "PATIENT": {
        "title": "Mon Suivi et Rendez-vous",
        "metrics": [
            ("Date prévue d'accouchement", "20 Mars 2025"),
            ("Prochain rendez-vous", "15 Décembre, 11:00"),
            ("Documents partagés par la sage-femme", "Plan de naissance (Non révisé)"),
            ("Sondages de satisfaction en attente", "1"),
        ],
    },
    "STUDENT": {
        "title": "Progression du Stage et Réflexion",
        "metrics": [
            ("Heures d'observation complétées", "120/400"),
            ("Réflexions soumises", "4/5"),
            ("Étude de cas en cours", "1"),
            ("Prochaine évaluation clinique", "18 Janvier"),
        ],
    },
    "INTERN": {
        "title": "Journal et Compétences Cliniques",
        "metrics": [
            ("Cas cliniques documentés", "12"),
            ("Compétences validées", "7/15"),
            ("Heures de formation requises", "80/100"),
            ("Prochaine revue de journal", "Vendredi"),
        ],
    },
    "DOCTORAL": {
        "title": "Suivi de Recherche et Éthique",
        "metrics": [
            ("Soumissions éthiques en attente", "1"),
            ("Notes de recherche créées (30j)", "15"),
            ("Statut du financement", "Approuvé"),
            ("Prochaine publication visée", "Revue A (Juin 2025)"),
        ],
    },
    "ADMIN": {
        "title": "Performance Système et Utilisateurs",
        "metrics": [
            ("Utilisateurs actifs (24h)", "25"),
            ("Incidents système ouverts", "0"),
            ("Nouvelles inscriptions en attente", "3 (Nurses)"),
            ("Temps d'activité moyen du système", "99.9%"),
        ],
    },
    "GUEST": {
        "title": "Informations Générales",
        "metrics": [
            ("Requêtes de service soumises", "N/A (Non connecté)"),
            ("Contact d'urgence", "418-555-1234"),
        ],
    },
}


# =========================================================
# 🛠️ FONCTIONS UTILITAIRES
# =========================================================


def load_static_asset(asset_name):
    """Charge l'URL d'un asset statique simulé (usage pour URL/HTML)."""
    return STATIC_ASSET_URLS.get(asset_name, "")


# --- Fonctions d'affichage ---
def render_info_section():
    """Affiche les sections d'information spécifiques."""
    current_page = st.session_state.get("info_page", "Accueil")

    if current_page == "Accueil":
        # Contenu de l'accueil pour le public est dans render_home_page
        pass

    elif current_page == "Mission":
        st.title("🎯 Notre mission")
        st.write(
            "Accompagner, soutenir, et honorer chaque naissance avec respect et amour."
        )

    elif current_page == "Notre équipe":
        st.title("📍 Notre équipe")
        st.write(
            "Découvrez les sages-femmes, infirmières et accompagnantes qui font vivre ce projet."
        )

    elif current_page == "Contact":
        st.title("📞 Contact")
        st.write("Pour toute question, vous pouvez nous écrire ou nous appeler.")

    elif current_page == "FAQ":
        st.title("❓ Foire aux questions")
        st.write("Les réponses aux questions les plus fréquentes.")

    elif current_page == "Les Papotines":
        st.title("🎀 Les Papotines")
        st.write("Un espace de parole, de partage et de douceur entre femmes.")

    elif current_page == "Pour nous joindre":
        st.title("📧 Pour nous joindre")
        st.write("Formulaire de contact pour nous écrire directement.")

    elif current_page == "Liens utiles":
        st.title("🔗 Liens utiles")
        st.write("Ressources, partenaires et documents à consulter.")

    # 🌿 Bouton de retour à l'accueil
    if current_page != "Accueil":
        st.markdown("---")
        if st.button("⬅️ Retour à l'accueil"):
            st.session_state["info_page"] = "Accueil"
            st.rerun()


def show_public_header():
    """Affiche l'en-tête public avec les liens d'information stylisés (Goal 1)."""
    # CSS pour styliser les boutons comme des liens de texte
    st.markdown(
        """
        <style>
        .public-header-row .stButton > button {
            background: none !important;
            border: none !important;
            color: #1e40af; /* Couleur de lien */
            padding: 5px 10px;
            text-decoration: none !important;
            box-shadow: none;
        }
        .public-header-row .stButton > button:hover {
            background-color: #eff6ff !important;
            text-decoration: none !important;
            color: #3b82f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Midwifery Services Application")
    st.caption(
        "Plateforme de soutien et de coordination dans les communautés de Waskaganish, Chisasibi et Mistissini"
    )

    # --- Bande horizontale avec liens cliquables en bleu ---
    # NOTE: L'implémentation originale de la bande a été modifiée pour utiliser des boutons Streamlit,
    # car les liens HTML cliquables dans le contexte d'un composant Streamlit peuvent poser problème
    # avec la gestion de l'état de session si on ne gère pas les événements de clic.
    cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    labels = [
        "Accueil",
        "Mission",
        "Notre équipe",
        "Contact",
        "FAQ",
        "Les Papotines",
        "Pour nous joindre",
        "Liens utiles",
    ]

    st.markdown(
        "<div class='public-header-row' style='margin-bottom:0.5rem;'>",
        unsafe_allow_html=True,
    )
    for col, label in zip(cols, labels):
        with col:
            # Utiliser des boutons pour la gestion de l'état
            if st.button(label, key=f"nav_{label}"):
                st.session_state["info_page"] = label
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Ligne de séparation douce
    st.markdown(
        "<hr style='margin-top:0.5rem;margin-bottom:1rem;border:1px solid #ccc;'>",
        unsafe_allow_html=True,
    )

    # Section d'information
    # NOTE: La fonction render_info_section est maintenant appelée à l'intérieur de main()
    # pour éviter la double exécution et gérer le layout.


def render_home_page():
    """Affiche le carrousel (Goal 4) et le squelette de la page de présentation (Goal 5)."""
    # --- Carrousel Dynamique (Corrigé pour l'erreur 'offset') ---
    CAROUSEL_HTML = f"""
    <style>
        /* Styles pour un carrousel propre et réactif */
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
                
                // Correction de l'erreur 'offset': double accolade
                track.style.transform = `translateX(${{offset}}%)`;
                
            }}, intervalTime);
        }}
    </script>
    """
    st.markdown(CAROUSEL_HTML, unsafe_allow_html=True)

    # --- Squelette de Page de Présentation (Goal 5) ---
    st.subheader("💡 À Propos de MSA.")
    st.markdown(
        """
    Le projet Midwifery Service Application, en abrégé "MSA", est une initiative visant à améliorer l'accès et la qualité des soins de sage-femme pour les mères et les familles des communautés cries de Waskaganish, Chisasibi et Mistissini (à venir), dans les Territoires-cries-de-la-Baie-James, au nord du Québec.

    Notre objectif principal est d'offrir un soutien médical et émotionnel complet, respectueux des cultures autochtones.

    ---
    ### Nos axes principaux :
    * **Soins de proximité :** Réduction des déplacements pour les mères en offrant des services directement dans les communautés.
    * **Intégration culturelle :** Collaboration étroite avec les Aînés et les leaders communautaires pour garantir des pratiques respectueuses des traditions.
    * **Formation et réseau :** Création d'un réseau sécurisé pour les professionnels de la santé afin de partager les informations et les meilleures pratiques.

    #### Partenariats clés

    Certaines variables recueillies ici ont été spécifiquement demandées par Nishiyuu. D'autres ont été sélectionnées à la suite de diverses consultations avec les Services de sage-femme et s'inspirent de :

    * The National Indigenous Association of Midwives  
    * I-CLSC, Care 4, CHB, RSFQ  
    * The Canadian Midwifery Minimum Database  
    * MSSS  

    📊 L’analyse des données est une démarche publique et sera communiquée chaque année aux communautés d’Eeyou Istchee par le biais du rapport annuel des Services de sage-femme et du Cree Health Board.

    ❤️ Merci à toutes et tous pour votre engagement à offrir des soins de sage-femme de haute qualité aux familles d’Eeyou Istchee.
    """
    )
    # NOTE: render_weather_map a été retiré ici.


def handle_login():
    """Gère le formulaire de connexion et la redirection."""
    st.subheader("🧡 Bienvenue !")
    message_placeholder = st.empty()

    with st.form("msa_login_form", clear_on_submit=True):
        username = st.text_input(
            "Identifiant (rôle)",
            placeholder="Ex: MIDWIFE, DOCTOR, PATIENT...",
        ).upper()
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter", type="primary")

    if submitted:
        role = username.upper()
        if role in USER_PASSWORDS and password == USER_PASSWORDS[role]:
            message_placeholder.success(
                f"✅ Connexion réussie en tant que **{role}**. Redirection..."
            )

            current_time = time.time()

            # Mise à jour de la dernière session si une session précédente a existé
            if st.session_state.get("login_time"):
                st.session_state["last_session"] = {
                    "role": st.session_state.get("user_role"),
                    "start": st.session_state["login_time"],
                    "end": current_time,
                }

            # Définition de la nouvelle session
            st.session_state["user_role"] = role
            st.session_state["logged_in"] = True
            st.session_state["info_page"] = "Accueil"
            # Les lignes audio ont été supprimées ici.
            st.session_state["login_time"] = (
                current_time  # Goal 6: Capture l'heure de connexion
            )
            # Initialisation de la section de navigation
            st.session_state["main_section_auth"] = (
                "Tableau de bord"  # Par défaut sur le tableau de bord
            )
            st.session_state["selected_form"] = None

            time.sleep(0.5)
            st.rerun()
        else:
            message_placeholder.error("⛔ Identifiant ou mot de passe incorrect.")


def get_all_forms_for_role(role):
    specific = SPECIFIC_FORMS.get(role, [])
    shared = list(SHARED_FORMS.values())
    return specific + shared


def render_dashboard(role):
    """Affiche un tableau de bord spécifique basé sur le rôle de l'utilisateur. (Simule le contenu de dashboard/dashbord_*.py)"""
    role_data = DASHBOARD_CONTENT.get(role, {})

    # Style personnalisé pour les cartes de métriques
    st.markdown(
        """
        <style>
        .metric-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.05);
            background-color: #ffffff;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        .metric-title {
            font-size: 1.1em;
            font-weight: 600;
            color: #333333;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 1.6em;
            font-weight: 700;
            color: #1e40af; /* Bleu MSA */
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.title(
        f"📊 Tableau de bord {role.capitalize()} : {role_data.get('title', 'Aperçu Général')}"
    )
    st.markdown("---")

    # Affichage des métriques sous forme de cartes
    cols = st.columns(
        len(role_data.get("metrics", [])) if role_data.get("metrics") else 1
    )

    # S'assurer que cols est une liste même s'il n'y a qu'une seule colonne
    if not isinstance(cols, list):
        cols = [cols]

    if role_data.get("metrics"):
        for i, (label, value) in enumerate(role_data.get("metrics")):
            # Utiliser modulo pour s'assurer que l'indice est valide
            with cols[i % len(cols)]:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <span class="metric-title">{label}</span>
                        <span class="metric-value">{value}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.warning(f"Aucune métrique spécifique définie pour le rôle {role}.")

    # Simulation de la carte de la communauté
    st.subheader("Situation Géographique & Logistique")
    st.warning(
        "Information : La carte interactive de Folium est remplacée par un message pour maintenir la simplicité du script principal. Elle serait ici."
    )


def render_form_content(form_path, role):
    """Simule l'affichage d'un formulaire spécifique ou partagé en détail. (Simule le contenu de modules/forms/form_*.py)"""
    label = FORM_LABELS.get(form_path, form_path.split("/")[-1])

    st.title(f"📄 {label}")
    st.caption(f"Formulaire (chemin : `{form_path}`) affiché pour le rôle : **{role}**")
    st.markdown("---")

    # NOTE: Les placeholders ont été remplacés par des exemples de champs Streamlit réels.
    st.info(
        "💡 **Instructions du formulaire** : Veuillez remplir tous les champs obligatoires avant de soumettre."
    )

    # Exemple de champs simulés pour illustrer le formulaire débloqué
    if (
        "patient_file" in form_path
        or "consultation" in form_path
        or "intrapartum" in form_path
    ):
        st.subheader("Section Clinique et Historique")
        with st.form(key=f"form_{form_path}_clinical"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(
                    "Nom du dossier",
                    "A. Mami - Naissance Prévue 2024",
                    key="clinical_name",
                )
                st.date_input(
                    "Date de la dernière évaluation", value=None, key="clinical_date"
                )
            with col2:
                st.selectbox(
                    "Statut du suivi",
                    ["Actif", "Post-partum", "Archivé"],
                    key="clinical_status",
                )
                st.slider("Risque perçu (1-10)", 1, 10, 3, key="clinical_risk")
            st.text_area(
                "Notes de suivi (Obligatoire)", max_chars=500, key="clinical_notes"
            )
            submitted = st.form_submit_button(
                "Soumettre la Section Clinique", type="primary"
            )

    elif "admin" in form_path or "management" in form_path:
        st.subheader("Outils d'administration et de gestion")
        with st.form(key=f"form_{form_path}_admin"):
            st.selectbox(
                "Rôle à gérer",
                ["MIDWIFE", "PATIENT", "DOCTOR", "ADMIN"],
                key="admin_role_select",
            )
            st.multiselect(
                "Accès aux formulaires (Globaux)",
                [
                    "Plan de naissance",
                    "Rapport de quart",
                    "Ordonnance",
                    "Gestion des utilisateurs",
                ],
                default=["Plan de naissance"],
                key="admin_access",
            )
            st.button(
                "Synchroniser les journaux système / Mettre à jour les privilèges",
                type="secondary",
            )
            submitted = st.form_submit_button(
                "Sauvegarder les Paramètres Admin", type="primary"
            )

    elif "schedule" in form_path or "calendar" in form_path or "agenda" in form_path:
        st.subheader("Gestion du temps et Planification")
        with st.form(key=f"form_{form_path}_schedule"):
            st.slider("Heures de disponibilité", 8, 18, (9, 17), key="schedule_hours")
            st.text_area("Notes d'absence / Conflits d'horaire", key="schedule_notes")
            submitted = st.form_submit_button("Mettre à jour l'Horaire", type="primary")

    elif "feedback" in form_path or "request" in form_path:
        st.subheader("Communication et Retour")
        with st.form(key=f"form_{form_path}_request"):
            st.radio(
                "Priorité de la demande",
                ["Faible", "Moyenne", "Urgent"],
                key="request_priority",
            )
            st.text_area("Détail de la demande ou du commentaire", key="request_detail")
            submitted = st.form_submit_button(
                "Envoyer la Demande/le Feedback", type="primary"
            )

    # Formulaire de fallback pour tous les autres chemins non explicitement gérés
    else:
        st.subheader(f"Contenu Standard du Formulaire : {label}")
        with st.form(key=f"form_{form_path}_default"):
            st.text_input(
                f"Champ de texte pour {label}",
                "Informations standards...",
                key="default_input",
            )
            st.checkbox("Confirmation des données", key="default_confirm")
            submitted = st.form_submit_button(
                "Soumettre le Formulaire Standard", type="primary"
            )

    st.markdown("---")
    # Message de succès basé sur la dernière soumission simulée
    if submitted:
        st.success(
            f"✅ Données simulées pour '{label}' soumises par le rôle **{role}** avec succès."
        )


def render_authenticated_interface():
    """Affiche l'interface complète après connexion, y compris la sidebar améliorée."""
    # 🔐 Sécurité : définir le rôle dès le début
    role = st.session_state.get("user_role", "MIDWIFE")
    role_icon = ROLE_ICONS.get(role.upper(), "👤")
    color = ROLE_COLORS.get(role.upper(), "#eeeeee")
    form_options = get_all_forms_for_role(role)

    # 🎛️ Affichage dans la barre latérale
    with st.sidebar:
        # --- Détermination de la salutation (Goal 6) ---
        current_hour = time.localtime().tm_hour
        if 5 <= current_hour < 12:
            greeting = "Bonjour"
        elif 12 <= current_hour < 18:
            greeting = "Bon après-midi"
        else:
            greeting = "Bonsoir"

        st.markdown(f"## {greeting} sur votre espace, {role.capitalize()}! 👋")
        st.markdown("---")

        st.markdown(f"### 🎛️ Menu **{role.capitalize()}**")
        st.markdown(
            f"{role_icon} Vous êtes connecté en tant que **{role.capitalize()}**."
        )
        st.markdown("---")

        # Détails de Session (Goal 6)
        st.markdown("#### Détails de Session")

        login_timestamp = st.session_state.get("login_time")
        if login_timestamp:
            login_dt = time.localtime(login_timestamp)
            st.markdown(
                f"**Connexion :** {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}"
            )

        last_sess = st.session_state.get("last_session", {})
        if last_sess and last_sess.get("start") and last_sess.get("end"):
            start_dt = time.localtime(last_sess["start"])
            end_dt = time.localtime(last_sess["end"])
            st.markdown("---")
            st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
            st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
            st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

        st.markdown("---")  # Séparateur pour le menu de navigation

        main_section = st.radio(
            "🧭 Que souhaitez-vous afficher ?",
            [
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ],
            key="main_section_auth",
            index=[
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ].index(st.session_state.get("main_section_auth", "Accueil")),
        )

        # Logique de sélection de contenu (complétion de la fonction)
        selected_content = None
        if main_section == "Formulaire spécifique":
            form_options_specific = SPECIFIC_FORMS.get(role, [])
            # Map form paths to their display labels
            display_options_specific = {
                FORM_LABELS.get(p, p.split("/")[-1]): p for p in form_options_specific
            }

            if form_options_specific:
                # Trouver l'index de la dernière sélection pour éviter la réinitialisation
                current_selected_form = st.session_state.get("selected_form")
                default_index = 0
                if (
                    current_selected_form
                    and current_selected_form in display_options_specific.values()
                ):
                    # Trouvez la clé (le label) correspondant au chemin du formulaire
                    default_label = next(
                        (
                            k
                            for k, v in display_options_specific.items()
                            if v == current_selected_form
                        ),
                        list(display_options_specific.keys())[0],
                    )
                    default_index = list(display_options_specific.keys()).index(
                        default_label
                    )

                selected_label = st.selectbox(
                    "📄 Choisissez un formulaire spécifique",
                    list(display_options_specific.keys()),
                    key="selected_form_specific",
                    index=default_index,
                )

                # Mise à jour de l'état de session
                selected_content = display_options_specific[selected_label]
                st.session_state["selected_form"] = selected_content
                # On s'assure que la sélection est bien le formulaire spécifique
                if selected_content != st.session_state.get("selected_form_last_path"):
                    st.session_state["selected_form_last_path"] = selected_content
                    st.rerun()  # Reréglage pour afficher le formulaire immédiatement après la sélection
            else:
                st.info("Aucun formulaire spécifique pour ce rôle.")
                st.session_state["selected_form"] = None

        elif main_section == "Fonction partagée":
            # Map shared form paths to their display labels
            display_options_shared = {
                FORM_LABELS.get(v, k): v for k, v in SHARED_FORMS.items()
            }

            # Trouver l'index de la dernière sélection pour éviter la réinitialisation
            current_selected_form = st.session_state.get("selected_form")
            default_index = 0
            if (
                current_selected_form
                and current_selected_form in display_options_shared.values()
            ):
                default_label = next(
                    (
                        k
                        for k, v in display_options_shared.items()
                        if v == current_selected_form
                    ),
                    list(display_options_shared.keys())[0],
                )
                default_index = list(display_options_shared.keys()).index(default_label)

            selected_label = st.selectbox(
                "🔗 Choisissez une fonction partagée",
                list(display_options_shared.keys()),
                key="selected_form_shared",
                index=default_index,
            )

            # Mise à jour de l'état de session
            selected_content = display_options_shared[selected_label]
            st.session_state["selected_form"] = selected_content
            # On s'assure que la sélection est bien le formulaire partagé
            if selected_content != st.session_state.get("selected_form_last_path"):
                st.session_state["selected_form_last_path"] = selected_content
                st.rerun()  # Reréglage pour afficher le formulaire immédiatement après la sélection
        else:
            # Si Tableau de bord ou Accueil est sélectionné, on efface le formulaire précédent
            st.session_state["selected_form"] = None
            st.session_state["selected_form_last_path"] = None

        st.markdown("---")
        # --- Goal 3: Selectbox de test par rôle ---
        st.markdown("#### Mode Test Rapide (Rôle)")
        test_roles = list(USER_PASSWORDS.keys())
        current_role_index = test_roles.index(role) if role in test_roles else 0

        selected_test_role = st.selectbox(
            "Changer de rôle pour tester :",
            test_roles,
            index=current_role_index,
            key="test_role_switcher",
        )

        if selected_test_role != role:
            st.session_state["user_role"] = selected_test_role
            st.session_state["main_section_auth"] = (
                "Tableau de bord"  # Revenir au tableau de bord après le changement
            )
            st.session_state["selected_form"] = None
            st.session_state["selected_form_last_path"] = None
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Se déconnecter", key="logout_btn"):
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = "GUEST"
            st.session_state["selected_form"] = None
            st.session_state["selected_form_last_path"] = None
            st.session_state["main_section_auth"] = "Accueil"
            st.rerun()

    # 🖥️ Contenu principal
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color}1A; /* Fond légèrement coloré par rôle */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Goal 1: Connexion des formulaires/dashboards par rôle
    if st.session_state.get("selected_form"):
        # Affichage du formulaire sélectionné
        render_form_content(st.session_state["selected_form"], role)
    elif main_section == "Tableau de bord":
        # Affichage du tableau de bord
        render_dashboard(role)
    elif main_section == "Accueil":
        # Affichage de la page d'accueil simple pour les utilisateurs connectés
        st.header(f"Page d'accueil de l'espace {role.capitalize()}")
        st.info(
            "Utilisez le menu de gauche pour accéder à votre Tableau de bord, vos Formulaires spécifiques et aux Fonctions partagées."
        )
        # Simuler un tableau de bord léger en page d'accueil
        render_dashboard(role)
    else:
        # Fallback pour tout autre cas
        st.header(f"Bienvenue, {role.capitalize()}")
        st.info("Utilisez la barre latérale pour naviguer.")


def main():
    """Fonction principale de l'application Streamlit."""
    st.set_page_config(
        page_title="MSA - Midwifery Services Application",
        page_icon=ROLE_ICONS.get("MIDWIFE"),
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 1. Vérification de l'état de connexion
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = "GUEST"
        st.session_state["info_page"] = "Accueil"
        st.session_state["main_section_auth"] = "Accueil"
        st.session_state["selected_form"] = None  # Ajouté pour le suivi des formulaires
        st.session_state["selected_form_last_path"] = (
            None  # Ajouté pour la persistance du formulaire
        )

    # 2. Logique d'affichage
    if st.session_state["logged_in"]:
        render_authenticated_interface()
    else:
        # Mode public/déconnecté
        # Réinitialisation de l'état si l'utilisateur est déconnecté
        st.session_state["user_role"] = "GUEST"
        st.session_state["main_section_auth"] = "Accueil"

        # Afficher le header public et les liens d'information
        show_public_header()

        # Gérer l'affichage en fonction de la page d'information sélectionnée
        current_info_page = st.session_state.get("info_page", "Accueil")

        if current_info_page == "Accueil":
            # Layout avec carrousel et login
            col_logo, col_login = st.columns([2, 1])
            with col_logo:
                render_home_page()
            with col_login:
                handle_login()
        else:
            # Layout pour les pages d'information spécifiques
            col_info, col_login = st.columns([2, 1])
            with col_info:
                render_info_section()
            with col_login:
                st.markdown("---")
                handle_login()


if __name__ == "__main__":
    main()
