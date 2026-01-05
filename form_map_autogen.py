import os

FORM_MAP = {
    "shared": {
        "🏠 Tableau de bord": "modules.forms.forms_shared.form_dashboard",
        "💬 Messagerie": "modules.forms.forms_shared.form_messages",
        "📅 Agenda": "modules.forms.forms_shared.form_calendar",
        "👤 Profil": "modules.forms.forms_shared.form_profile",
        "📊 Statistiques": "modules.forms.forms_shared.form_stats",
        "📝 Journal d'accès": "modules.forms.forms_shared.form_logs",
        "⚙️ Paramètres": "modules.forms.forms_shared.form_settings",
        "🔔 Notifications": "modules.forms.forms_shared.form_notifications",
        "➕ Création": "modules.forms.forms_shared.form_create",
    },
    "admin": {
        "🧾 Report Dashboard": "modules.forms.forms_admin.form_report_dashboard",
        "👥 Group Management": "modules.forms.forms_admin.form_group_management",
        "👥 Gestion des Utilisateurs": "modules.forms.forms_admin.form_admin_users",
        "⚙️ Paramètres Système": "modules.forms.forms_admin.form_config_system",
        "🗃️ Gestion des Données": "modules.forms.forms_admin.form_admin_data",
        "👤 User Management": "modules.forms.forms_admin.form_user_management",
        "🧩 Module Manager": "modules.forms.forms_admin.form_admin_module_manager",
        "🗑️ Log Deleter": "modules.forms.forms_admin.form_log_deleter",
        "🔐 Admin Roles": "modules.forms.forms_admin.form_admin_roles",
        "👤 User Management Supabase": "modules.forms.forms_admin.form_user_management_supabase",
        "🧭 Dashboard Modules": "modules.forms.forms_admin.form_admin_dashboard_modules",
        "📋 Admin Logs": "modules.forms.forms_admin.form_admin_logs",
        "📝 View Notes": "modules.forms.forms_admin.form_view_notes",
        "🔄 Update": "modules.forms.forms_admin.form_update",
        "🔐 Hashing": "modules.forms.forms_admin.form_hashing",
        "🔐 Admin Hashing": "modules.forms.forms_admin.form_admin_hashing",
        "📦 Pack Organisation": "modules.forms.forms_admin.form_pack_organisation",
        "📤 Export PDF": "modules.forms.forms_admin.form_export_pdf",
        "🧭 Admin Dashboard": "modules.forms.forms_admin.form_admin_dashboard",
        "🛠️ Éditeur de formulaires": "modules.dashboard.form_editor_admin",
    },
    "midwife": {
        "🧠 Emotional Well-being": "modules.forms.forms_midwife.form_emotional_well_being",
        "📈 Throughout Care": "modules.forms.forms_midwife.form_throughout_midwifery_care",
        "📄 Delivery Log": "modules.forms.forms_midwife.form_delivery_log",
        "👤 Demographics": "modules.forms.forms_midwife.form_demographics",
        "📊 Pregnancy Tracking": "modules.forms.forms_midwife.form_pregnancy_tracking",
        "🎓 Workshops": "modules.forms.forms_midwife.form_workshops",
        "🩺 Consultation": "modules.forms.forms_midwife.form_consultation_midwife",
        "📄 Birth Plan": "modules.forms.forms_midwife.form_birth_plan",
        "👩‍🍼 Postnatal Care": "modules.forms.forms_midwife.form_postnatal_care",
        "📁 Patient Data": "modules.forms.forms_midwife.form_patient_data",
        "📅 Medical Agenda": "modules.forms.forms_midwife.form_medical_agenda",
        "👶 Childbirth": "modules.forms.forms_midwife.form_childbirth",
        "🚨 Patient Alerts": "modules.forms.forms_midwife.form_patients_alerts",
        "🎓 Education & Prevention": "modules.forms.forms_midwife.form_education_prevention",
        "🥗 Nutrition": "modules.forms.forms_midwife.form_nutrition",
        "💬 Messages": "modules.forms.forms_midwife.form_messages",
        "🧭 Dashboard": "modules.forms.forms_midwife.form_midwife_dashboard",
        "📊 Prenatal Care": "modules.forms.forms_midwife.form_prenatal_care",
        "🩺 Intrapartum Care": "modules.forms.forms_midwife.form_intrapartum_care",
        "🔄 Follow-up": "modules.forms.forms_midwife.form_follow_up",
        "👤 Profile": "modules.forms.forms_midwife.form_profile",
    },
    "doctoral": {
        "📊 Research Project": "modules.forms.forms_doctoral.form_research_project",
        "📚 Thesis Tracking": "modules.forms.forms_doctoral.form_thesis_tracking",
        "🧑‍🏫 Supervision": "modules.forms.forms_doctoral.form_supervision",
        "📄 Publications": "modules.forms.forms_doctoral.form_publications",
        "🧭 Doctoral Dashboard": "modules.forms.forms_doctoral.form_doctoral_dashboard",
        "💬 Messages": "modules.forms.forms_doctoral.form_messages",
        "👤 Profile": "modules.forms.forms_doctoral.form_profile",
    },
    "doctor": {
        "📝 Medical Notes": "modules.forms.forms_doctor.form_medical_notes",
        "💊 Prescription": "modules.forms.forms_doctor.form_prescription",
        "💬 Messages": "modules.forms.forms_doctor.form_messages",
        "🧭 Doctor Dashboard": "modules.forms.forms_doctor.form_doctor_dashboard",
        "🔍 Diagnostic": "modules.forms.forms_doctor.form_diagnostic",
        "📥 Consultation Requests": "modules.forms.forms_doctor.form_consultation_requests",
        "📜 Patient History": "modules.forms.forms_doctor.form_patient_history",
        "📄 Page": "modules.forms.forms_doctor.form_page",
        "👤 Profile": "modules.forms.forms_doctor.form_profile",
        "📦 Supply": "modules.forms.forms_doctor.form_supply",
    },
    "student": {
        "🧭 Student Dashboard": "modules.forms.forms_student.form_student_dashboard",
        "📄 Internship Request": "modules.forms.forms_student.form_internship_request",
        "📚 Academic Tracking": "modules.forms.forms_student.form_academic_tracking",
        "📘 Courses": "modules.forms.forms_student.form_courses",
        "📝 Evaluations": "modules.forms.forms_student.form_evaluations",
        "💬 Messages": "modules.forms.forms_student.form_messages",
        "👤 Profile": "modules.forms.forms_student.form_profile",
    },
    "intern": {
        "📅 Daily Tasks": "modules.forms.forms_intern.form_daily_tasks",
        "🗣️ Feedback": "modules.forms.forms_intern.form_feedback",
        "🧭 Intern Dashboard": "modules.forms.forms_intern.form_intern_dashboard",
        "💬 Messages": "modules.forms.forms_intern.form_messages",
        "📘 Logbook": "modules.forms.forms_intern.form_intern_logbook",
        "📚 Resources": "modules.forms.forms_intern.form_resources",
        "👤 Profile": "modules.forms.forms_intern.form_profile",
    },
    "patient": {
        "📝 Self Report": "modules.forms.forms_patient.form_self_report",
        "📞 Contact Doctor": "modules.forms.forms_patient.form_contact_doctor",
        "📜 Visit History": "modules.forms.forms_patient.form_visit_history",
        "📅 Book Appointment": "modules.forms.forms_patient.form_book_appointment",
        "💬 Messages": "modules.forms.forms_patient.form_messages",
        "📤 Export PDF": "modules.forms.forms_patient.form_export_pdf",
        "🧭 Patient Dashboard": "modules.forms.forms_patient.form_patient_dashboard",
        "📄 View Records": "modules.forms.forms_patient.form_view_records",
        "👤 Profile": "modules.forms.forms_patient.form_profile",
    },
    "nurse": {
        "📦 Supply Request": "modules.forms.forms_nurse.form_supply_request",
        "❤️ Vital Signs": "modules.forms.forms_nurse.form_vital_signs",
        "📝 Nursing Notes": "modules.forms.forms_nurse.form_nursing_notes",
        "🧭 Nurse Dashboard": "modules.forms.forms_nurse.form_nurse_dashboard",
        "📊 Patient Monitoring": "modules.forms.forms_nurse.form_patient_monitoring",
        "💬 Messages": "modules.forms.forms_nurse.form_messages",
        "💊 Medication Management": "modules.forms.forms_nurse.form_medication_management",
        "📅 Schedule": "modules.forms.forms_nurse.form_schedule_nurse",
        "👤 Profile": "modules.forms.forms_nurse.form_profile",
    },
    "guest": {
        "🧭 Guest Dashboard": "modules.forms.forms_guest.form_guest_dashboard",
    },
}


BASE_PATH = "modules/forms"


def generate_form(path, title, role):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("import streamlit as st\n\n")
        f.write("def render_form():\n")
        f.write(f'    st.header("{title}")\n')

        # Champs réalistes selon le rôle
        if role == "midwife":
            f.write("    st.text_input('Nom de la patiente')\n")
            f.write("    st.date_input('Date de suivi')\n")
            f.write(
                "    st.radio('État général', ['Bon', 'Fatiguée', 'À surveiller'])\n"
            )
            f.write("    st.text_area('Observations cliniques')\n")
        elif role == "doctor":
            f.write("    st.text_input('Nom du patient')\n")
            f.write("    st.text_area('Diagnostic')\n")
            f.write("    st.text_area('Prescription')\n")
        elif role == "patient":
            f.write("    st.text_input('Nom')\n")
            f.write(
                "    st.selectbox('Motif de consultation', ['Douleur', 'Suivi', 'Autre'])\n"
            )
            f.write("    st.date_input('Date souhaitée')\n")
        elif role == "admin":
            f.write("    st.text_input('Nom du module')\n")
            f.write(
                "    st.selectbox('Type de gestion', ['Utilisateurs', 'Données', 'Sécurité'])\n"
            )
            f.write("    st.text_area('Instructions')\n")
        elif role == "student":
            f.write("    st.text_input('Nom de l’étudiant·e')\n")
            f.write(
                "    st.selectbox('Type de suivi', ['Cours', 'Stage', 'Évaluation'])\n"
            )
            f.write("    st.text_area('Commentaires')\n")
        elif role == "nurse":
            f.write("    st.text_input('Nom du patient')\n")
            f.write("    st.slider('Douleur (0-10)', 0, 10)\n")
            f.write("    st.checkbox('Médication administrée')\n")
        elif role == "shared":
            f.write("    st.text_input('Nom')\n")
            f.write("    st.text_area('Message ou paramètre')\n")
        else:
            f.write("    st.write('Ce formulaire est en cours de construction.')\n")

        f.write("\n")
        f.write("def display_render():\n")
        f.write("    render_form()\n")


def generate_all_forms():
    for role, forms in FORM_MAP.items():
        for title, module_path in forms.items():
            rel_path = module_path.replace(".", "/") + ".py"
            generate_form(rel_path, title, role)
            print(f"✅ Créé : {rel_path}")


if __name__ == "__main__":
    generate_all_forms()
