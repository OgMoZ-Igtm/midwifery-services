import importlib
import streamlit as st

DOCTOR_FORMS = [
    "modules.forms_doctor.doctor_birth_care_plan_form",
    "modules.forms_doctor.doctor_cesarean_operative_report_form",
    "modules.forms_doctor.doctor_fetal_anomaly_assessment_form",
    "modules.forms_doctor.doctor_final_discharge_prescriptions_form",
    "modules.forms_doctor.doctor_inter_specialities_consultation_request_form",
    "modules.forms_doctor.doctor_ultrasound_report_form",
    "modules.forms_doctor.doctor_supervision_form",
    "modules.forms_doctor.doctor_due_date_calculator_form",
]


def test_import_and_render(module_name: str):
    try:
        module = importlib.import_module(module_name)
        st.success(f"✅ Import réussi : {module_name}")
        render_functions = [
            attr
            for attr in dir(module)
            if attr.startswith("render_") and attr.endswith("_form")
        ]
        if render_functions:
            st.write(f"➡️ Fonctions de rendu trouvées : {render_functions}")
        else:
            st.warning(f"Aucune fonction render_*_form trouvée dans {module_name}")
    except Exception as e:
        st.error(f"❌ Erreur lors du test de {module_name}: {e}")


def main():
    st.title("=== Tests des formulaires DOCTOR ===")
    for form_module in DOCTOR_FORMS:
        test_import_and_render(form_module)


if __name__ == "__main__":
    main()
