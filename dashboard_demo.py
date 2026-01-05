import streamlit as st
import time

# --- Simulations de données ---
role = st.session_state.get("user_role", "MIDWIFE")
role_icon = "🧑‍⚕️" if role == "MIDWIFE" else "🛠️"

SPECIFIC_FORMS = {
    "MIDWIFE": [
        "forms_midwife/form_prenatal_care",
        "forms_midwife/form_postnatal_care",
    ],
    "ADMIN": ["forms_admin/form_user_management"],
}

SHARED_FORMS = {
    "Agenda": "forms_shared/form_agenda",
    "Profil": "forms_shared/form_profile",
}

SHARED_BUTTONS = {
    "Agenda": "Agenda",
    "Profil": "Profil",
}

FORM_LABELS = {
    "forms_midwife/form_prenatal_care": "Soins prénataux",
    "forms_midwife/form_postnatal_care": "Suivi postnatal",
    "forms_admin/form_user_management": "Gestion utilisateurs",
    "forms_shared/form_agenda": "Agenda partagé",
    "forms_shared/form_profile": "Profil utilisateur",
}

THEMATIC_GROUPS = {
    "Soins": ["forms_midwife/form_prenatal_care", "forms_midwife/form_postnatal_care"],
    "Configuration": ["forms_admin/form_user_management"],
    "Partagé": ["forms_shared/form_agenda", "forms_shared/form_profile"],
}

# --- Barre latérale décorée ---
with st.sidebar:
    st.markdown("## 🌿 Navigation sacrée")
    st.markdown("#### Détails de Session")

    login_timestamp = st.session_state.get("login_time")
    if login_timestamp:
        login_dt = time.localtime(login_timestamp)
        st.markdown(
            f"<span style='color:#A7D8DE'><strong>Connexion :</strong> {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}</span>",
            unsafe_allow_html=True,
        )

    last_sess = st.session_state.get("last_session", {})
    if last_sess and last_sess.get("start") and last_sess.get("end"):
        start_dt = time.localtime(last_sess["start"])
        end_dt = time.localtime(last_sess["end"])
        st.markdown("---")
        st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
        st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
        st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

    st.markdown("---")
    main_section = st.radio(
        "🧭 Que souhaitez-vous afficher ?",
        ["Accueil", "Tableau de bord", "Formulaire spécifique", "Fonction partagée"],
        key="main_section_auth",
        index=[
            "Accueil",
            "Tableau de bord",
            "Formulaire spécifique",
            "Fonction partagée",
        ].index(st.session_state.get("main_section_auth", "Accueil")),
    )

    selected_content_key = None
    if main_section == "Formulaire spécifique":
        form_options_specific = SPECIFIC_FORMS.get(role, [])
        display_options_specific = {
            FORM_LABELS.get(p, p.split("/")[-1]): p for p in form_options_specific
        }

        if form_options_specific:
            selected_label = st.selectbox(
                "📄 Choisissez un formulaire",
                list(display_options_specific.keys()),
                key="specific_form_select",
            )
            selected_content_key = display_options_specific.get(selected_label)
        else:
            st.info("Aucun formulaire spécifique pour ce rôle.")
    elif main_section == "Fonction partagée":
        selected_label = st.selectbox(
            "🌐 Fonction partagée",
            list(SHARED_BUTTONS.keys()),
            key="shared_func_select",
        )
        selected_content_key = SHARED_FORMS.get(selected_label)

    st.session_state["selected_form"] = selected_content_key

    st.markdown("---")
    if st.button("🚪 Déconnexion", key="logout_button", type="primary"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["info_page"] = "Accueil"
        st.session_state["selected_form"] = None
        st.session_state["last_session"] = {
            "role": role,
            "start": st.session_state["login_time"],
            "end": time.time(),
        }
        st.session_state["login_time"] = None
        st.rerun()

# --- Corps principal ---
main_section = st.session_state.get("main_section_auth", "Accueil")
selected_content_key = st.session_state.get("selected_form")

st.markdown(f"### {role_icon} Formulaires pour le rôle : **{role.capitalize()}**")

for theme, paths in THEMATIC_GROUPS.items():
    filtered = [
        p
        for p in paths
        if p in SPECIFIC_FORMS.get(role, []) + list(SHARED_FORMS.values())
    ]
    if filtered:
        with st.expander(f"📂 {theme}", expanded=False):
            for form_path in filtered:
                label = FORM_LABELS.get(form_path, form_path.split("/")[-1])
                color = "#F0F8FF" if "prenatal" in form_path else "#FBE9E7"

                st.markdown(
                    f"<div style='background-color:{color}; padding:10px; border-radius:8px; margin-bottom:10px'>"
                    f"<strong>{label}</strong><br>"
                    f"<em>Chemin :</em> {form_path}<br>"
                    f"<button style='margin-top:5px'>Ouvrir</button>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
