# ⚠️ import cassé : os

BASE_PATH = "modules/forms"
roles = {
    "admin": {
        "form_admin_rapport": [
            "📊 Rapport de performance",
            "st.text_input('Nom du service')",
            "st.date_input('Période couverte')",
            "st.text_area('Observations générales')",
        ]
    },
    "midwife": {
        "form_suivi_postnatal": [
            "👶 Suivi postnatal",
            "st.text_input('Nom de la patiente')",
            "st.date_input('Date de l’accouchement')",
            "st.radio('État général', ['Bon', 'Fatiguée', 'À surveiller'])",
        ]
    },
    "nurse": {
        "form_soins_postnatals": [
            "💉 Soins postnatals",
            "st.text_input('Nom de la patiente')",
            "st.checkbox('Pansement changé')",
            "st.slider('Douleur (0-10)', 0, 10)",
        ]
    },
    "student": {
        "form_cas_clinique": [
            "🎓 Cas clinique",
            "st.text_input('Titre du cas')",
            "st.text_area('Description')",
            "st.selectbox('Type de pathologie', ['Prééclampsie', 'Hémorragie', 'Travail prolongé'])",
        ]
    },
    "doctor": {
        "form_prescription_obstetrique": [
            "🩺 Prescription obstétrique",
            "st.text_input('Nom de la patiente')",
            "st.text_area('Prescription')",
            "st.date_input('Date de prescription')",
        ]
    },
}

shared_forms = {
    "form_demande_rdv": [
        "📅 Demande de rendez-vous",
        "st.text_input('Nom')",
        "st.date_input('Date souhaitée')",
        "st.selectbox('Motif', ['Consultation', 'Suivi', 'Urgence'])",
    ],
    "form_signalement": [
        "🚨 Signalement",
        "st.text_input('Nom du déclarant')",
        "st.text_area('Description du problème')",
        "st.radio('Urgence', ['Faible', 'Modérée', 'Élevée'])",
    ],
    "form_feedback": [
        "💬 Feedback",
        "st.text_input('Nom (optionnel)')",
        "st.text_area('Commentaire')",
        "st.slider('Satisfaction (0-10)', 0, 10)",
    ],
}


def create_form(path, title, components):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("import streamlit as st\n\n")
        f.write("def render_form():\n")
        f.write(f'    st.header("{title}")\n')
        for comp in components[1:]:
            f.write(f"    {comp}\n")
        f.write("\n")
        f.write("def display_render():\n")
        f.write("    render_form()\n")
    print(f"✅ Créé : {path}")


def generate_role_forms():
    for role, forms in roles.items():
        role_path = os.path.join(BASE_PATH, f"forms_{role}")
        for form_name, components in forms.items():
            path = os.path.join(role_path, f"{form_name}.py")
            create_form(path, components[0], components)


def generate_shared_forms():
    shared_path = os.path.join(BASE_PATH, "forms_shared")
    for form_name, components in shared_forms.items():
        if form_name == "form_messagerie":
            continue  # déjà implémenté
        path = os.path.join(shared_path, f"{form_name}.py")
        create_form(path, components[0], components)


if __name__ == "__main__":
    generate_role_forms()
    generate_shared_forms()
