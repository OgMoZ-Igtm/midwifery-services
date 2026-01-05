from modules.public.form_registry import form_registry

linked_forms = {
    name: entry for name, entry in form_registry.items() if entry.get("is_extended", False)
}

import json

# 📜 Dictionnaire des formulaires par rôle
,
    "form_postpartum": {
        "title": "Suivi postnatal",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_postpartum",
    },
    "form_initial_routine": {
        "title": "Routine initiale",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_initial_routine",
    },
    "form_patient_file": {
        "title": "Dossier patiente",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_patient_file",
    },
    "form_patient_management": {
        "title": "Gestion patiente",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_patient_management",
    },
    "form_midwife_messages": {
        "title": "Messages sage-femme",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_midwife_messages",
    },
    "form_consultation_prenatale": {
        "title": "Consultation prénatale",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_consultation_prenatale",
    },
    "form_emotional_well_being": {
        "title": "Bien-être émotionnel",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_emotional_well_being",
    },
    "form_incident_report": {
        "title": "Rapport d'incident",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_incident_report",
    },
    "form_demographics": {
        "title": "Démographie",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_demographics",
    },
    "form_prenatal_care": {
        "title": "Soins prénataux",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_prenatal_care",
    },
    "form_postnatal_care": {
        "title": "Soins postnataux",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_postnatal_care",
    },
    "form_intrapartum_care": {
        "title": "Soins intrapartum",
        "role": "MIDWIFE",
        "module": "modules.forms_midwife.form_intrapartum_care",
    },
    # 🧑‍⚕️ NURSE
    "form_schedule_nurse": {
        "title": "Horaire infirmier",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_schedule_nurse",
    },
    "form_consultation_notes": {
        "title": "Notes de consultation",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_consultation_notes",
    },
    "form_nurse_shift_report": {
        "title": "Rapport de quart",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_nurse_shift_report",
    },
    "form_nursing_notes": {
        "title": "Notes infirmières",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_nursing_notes",
    },
    "form_nurse_inventory_management": {
        "title": "Inventaire",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_nurse_inventory_management",
    },
    "form_nurse_medicament_admin": {
        "title": "Administration médicaments",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_nurse_medicament_admin",
    },
    "form_vital_signs": {
        "title": "Signes vitaux",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_vital_signs",
    },
    "form_followup": {
        "title": "Suivi",
        "role": "NURSE",
        "module": "modules.forms_nurse.form_followup",
    },
    # 🛡️ ADMIN
    "form_user_management": {
        "title": "Gestion utilisateurs",
        "role": "ADMIN",
        "module": "modules.forms_admin.form_user_management",
    },
    "form_system_logs_viewer": {
        "title": "Logs système",
        "role": "ADMIN",
        "module": "modules.forms_admin.form_system_logs_viewer",
    },
    "form_report_dashboard": {
        "title": "Rapports",
        "role": "ADMIN",
        "module": "modules.forms_admin.form_report_dashboard",
    },
    "form_global_settings": {
        "title": "Paramètres globaux",
        "role": "ADMIN",
        "module": "modules.forms_admin.form_global_settings",
    },
    "form_config_system": {
        "title": "Configuration système",
        "role": "ADMIN",
        "module": "modules.forms_admin.form_config_system",
    },
}

# 🛠️ Enrichissement du dictionnaire avec les noms de fonctions
for key, config in LINKED_FORMS_EXTENDED.items():
    module_path = config.get("module")
    if not module_path:
        continue

    module_name = module_path.split(".")[-1]
    config["render"] = f"render_{module_name}"
    config["validate"] = f"validate_{module_name}"

# 💾 Sauvegarde dans un fichier JSON
with open("enriched_registry.json", "w") as f:
    json.dump(LINKED_FORMS_EXTENDED, f, indent=4)

print("✅ Dictionnaire enrichi avec les fonctions render/validate")
