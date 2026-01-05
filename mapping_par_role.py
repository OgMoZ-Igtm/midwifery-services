SPECIFIC_FORMS_MAPPING = {
    "MIDWIFE": {
        "Soins Prénatals": "form_prenatal_care",
        "Soins Postnatals": "form_postnatal_care",
    },
    "ADMIN": {
        "Gestion Utilisateurs": "form_user_management",
        "Journal Système": "form_system_log",
    },
    "DOCTOR": {
        "Rapport Médical": "form_medical_report",
        "Prescription": "form_prescription",
    },
    # NOUVEAUX RÔLES AJOUTÉS
    "NURSE": {
        "Saisie de Soins": "form_care_entry",
        "Inventaire Médicaments": "form_medication_inventory",
        "Contrôle des Signes Vitaux": "form_vitals_check",
    },
    "PATIENT": {
        "Consultation de Mon Dossier": "form_personal_record",
        "Demande de Rendez-vous": "form_appointment_request",
        "Questionnaire de Santé": "form_health_questionnaire",
    },
    "INTERN": {
        "Rapport de Cas Clinique": "form_clinical_case_report",
        "Journal de Bord (Stage)": "form_internship_log",
        "Demande d'Accès Supervision": "form_supervision_access",
    },
    "GUEST": {
        "Information Publique Maternité": "form_public_maternity_info",
        "Formulaire de Contact": "form_contact",
        "Accès Documentation": "form_public_documentation",
    },
    "DOCTORAL": {
        "Gestion Projet de Recherche": "form_research_project_management",
        "Saisie de Données d'Étude": "form_study_data_entry",
        "Rapport d'Avancement Thèse": "form_thesis_progress_report",
    },
    "STUDENT": {
        "Modules de Formation E-learning": "form_training_modules",
        "Feuille de Présence/Heures": "form_attendance_hours",
        "Auto-Évaluation Compétences": "form_skills_self_assessment",
    },
}
