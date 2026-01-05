# form_config.py
# Ce fichier définit la structure de navigation (FORM_MAP) pour chaque rôle.
# Les clés sont les noms affichés dans la sidebar, et les valeurs sont
# les clés de routage correspondantes définies dans routing_map.py.

# --- Modules Partagés (Nouveaux) ---
SHARED_MODULES = {
    "🗓️ Agenda": "agenda",
    "📅 Calendrier": "calendar",
    "💬 Messagerie": "messages",
    "👤 Mon Profil": "profile",
    "⚙️ Paramètres": "settings",
}

# --- Définition des Cartes de Formulaires (FORM_MAP) ---
FORM_MAP = {
    # 1. Rôle Administrateur
    "admin": {
        "🛠️ Tableau de Bord Admin": "admin_dashboard",
        "📜 Logs Système": "logs",
        "🔍 Accès aux Données": "data_access",
        **SHARED_MODULES,  # Ajout des modules partagés
    },
    # 2. Rôle Sage-femme
    "midwife": {
        "👩‍⚕️ Tableau de Bord Sage-femme": "midwife_dashboard",
        "👶 Formulaire Postnatal": "postnatal_form",
        "📅 Historique Patient": "patient_history",
        "📆 Prise de RDV": "appointment_booking",
        **SHARED_MODULES,
    },
    # 3. Rôle Médecin
    "doctor": {
        "🩺 Tableau de Bord Médecin": "doctor_dashboard",
        "📝 Formulaire générique": "form",
        "📅 Historique Patient": "patient_history",
        "📆 Prise de RDV": "appointment_booking",
        **SHARED_MODULES,
    },
    # 4. Rôle Étudiant
    "student": {
        "🎓 Tableau de Bord Étudiant": "student_dashboard",
        "👁️ Module d'Observation": "observation",
        "🚀 Découverte de l'application": "app_tour",
        **SHARED_MODULES,
    },
    # 5. Rôle Patient
    "patient": {
        "🧍 Tableau de Bord Patient": "patient_dashboard",
        "📆 Prise de RDV": "appointment_booking",
        "📅 Historique Patient": "patient_history",
        **SHARED_MODULES,
    },
    # 6. Rôle Invité (Guest)
    "guest": {
        "🙋 Bienvenue Invité": "guest_welcome",
        "👀 Tableau de Bord Invité": "guest_dashboard",
    },
    # 7. Rôle Doctorant
    "doctoral": {
        "📚 Tableau de Bord Doctorant": "doctoral_dashboard",
        "🔍 Accès aux Données": "data_access",
        **SHARED_MODULES,
    },
    # 8. Rôle Stagiaire
    "intern": {
        "🧪 Tableau de Bord Stagiaire": "intern_dashboard",
        "👁️ Module d'Observation": "observation",
        **SHARED_MODULES,
    },
    # 9. Rôle Étudiant
    "intern": {
        "🧪 Tableau de Bord Stagiaire": "intern_dashboard",
        "👁️ Module d'Observation": "observation",
        **SHARED_MODULES,
    },
    # Rôle par Défaut (Utilisé si le rôle n'est pas trouvé)
    "default": {
        "🧭 Tableau de Bord par défaut": "default_dashboard",
        "📝 Formulaire générique": "form",
        **SHARED_MODULES,
    },
}
