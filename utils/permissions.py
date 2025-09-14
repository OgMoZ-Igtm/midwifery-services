import pandas as pd

ROLES = {
    "ADMIN": {
        "can_view": ["ALL"],
        "can_edit": ["ALL"],
        "cannot_edit": ["DOCTOR", "PATIENT"],
    },
    "DOCTOR": {
        "can_view": ["DOCTOR", "PATIENT", "MESSAGES"],
        "can_edit": ["DOCTOR", "MESSAGES"],
    },
    "PATIENT": {"can_view": ["PATIENT", "MESSAGES"], "can_edit": ["MESSAGES"]},
    "MIDWIFE": {"can_view": ["MIDWIFE", "MESSAGES"], "can_edit": ["MESSAGES"]},
    "NURSE": {"can_view": ["NURSE", "MESSAGES", "PATIENT"], "can_edit": ["MESSAGES"]},
    "STUDENT": {"can_view": ["STUDENT", "MESSAGES"], "can_edit": ["MESSAGES"]},
    "DOCTORAL": {"can_view": ["DOCTORAL", "MESSAGES"], "can_edit": ["MESSAGES"]},
}


def can_access(role: str, section: str, action: str = "view") -> bool:
    role = role.upper()
    permissions = ROLES.get(role, {})

    if section == "MESSAGES":
        return True

    if action == "view":
        allowed = permissions.get("can_view", [])
        return "ALL" in allowed or section in allowed

    if action == "edit":
        if section in permissions.get("cannot_edit", []):
            return False
        allowed = permissions.get("can_edit", [])
        return "ALL" in allowed or section in allowed

    return False


def afficher_tableau_des_permissions():
    import streamlit as st

    data = []
    for role, droits in ROLES.items():
        data.append(
            {
                "Rôle": role,
                "Peut voir": ", ".join(droits.get("can_view", [])),
                "Peut éditer": ", ".join(droits.get("can_edit", [])),
                "Ne peut pas éditer": (
                    ", ".join(droits.get("cannot_edit", []))
                    if "cannot_edit" in droits
                    else "-"
                ),
            }
        )

    df = pd.DataFrame(data)
    st.dataframe(df)


def get_accessible_sections(role: str, action: str = "view") -> list:
    role = role.upper()
    permissions = ROLES.get(role, {})
    sections = permissions.get(f"can_{action}", [])
    return sorted(set(sections))
