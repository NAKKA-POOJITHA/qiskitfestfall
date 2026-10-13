"""
QuantumCure AI - Interactive Patient Feature Form Component
Provides manual clinical feature entry with validation, example presets, and form reset.
"""

import streamlit as st


EXAMPLE_PRESETS = {
    "Select Example...": None,
    "Example 1: Low-Risk Case (T1N0, Grade 1, ER+, HER2-)": {
        "Tumour Size(cm)": 1.2,
        "Age(years)": 68,
        "Histological grading": 1.0,
        "ER": "Positive",
        "HER2": "Negative"
    },
    "Example 2: High-Risk Case (T3N+, Grade 3, ER-, HER2+)": {
        "Tumour Size(cm)": 4.8,
        "Age(years)": 42,
        "Histological grading": 3.0,
        "ER": "Negative",
        "HER2": "Positive"
    },
    "Example 3: Intermediate Equivocal Case (T2, Grade 2, ER+, HER2+)": {
        "Tumour Size(cm)": 2.8,
        "Age(years)": 58,
        "Histological grading": 2.0,
        "ER": "Positive",
        "HER2": "Positive"
    }
}


def render_patient_input_form():
    """
    Renders standardized input form for manual patient entry.
    Includes presets, reset control, and required field validation.
    """
    if "manual_form_data" not in st.session_state:
        st.session_state["manual_form_data"] = {
            "Tumour Size(cm)": 2.5,
            "Age(years)": 55,
            "Histological grading": 2.0,
            "ER": "Positive",
            "HER2": "Negative"
        }

    # Form Controls Bar: Load Presets & Reset Form
    ctrl_col1, ctrl_col2 = st.columns([3, 1])
    with ctrl_col1:
        selected_preset = st.selectbox(
            "Load Demonstration Clinical Preset:",
            options=list(EXAMPLE_PRESETS.keys()),
            help="Pre-loads verified demonstration patient profiles. Clearly identified as synthetic demonstration inputs."
        )
        if selected_preset and EXAMPLE_PRESETS[selected_preset] is not None:
            preset = EXAMPLE_PRESETS[selected_preset]
            st.session_state["manual_form_data"] = preset.copy()

    with ctrl_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Reset Form", use_container_width=True):
            st.session_state["manual_form_data"] = {
                "Tumour Size(cm)": 2.5,
                "Age(years)": 55,
                "Histological grading": 2.0,
                "ER": "Positive",
                "HER2": "Negative"
            }
            st.rerun()

    cur = st.session_state["manual_form_data"]

    col1, col2 = st.columns(2)
    with col1:
        tumour_size = st.number_input(
            "Primary Tumour Diameter (cm) *",
            min_value=0.1,
            max_value=15.0,
            value=float(cur["Tumour Size(cm)"]),
            step=0.1,
            help="Primary pathological diameter. Continuous numerical feature (BCNB cohort range: 0.5 - 5.5 cm)."
        )

        age = st.number_input(
            "Patient Age at Diagnosis (years) *",
            min_value=18,
            max_value=105,
            value=int(cur["Age(years)"]),
            step=1,
            help="Chronological age at primary diagnosis (BCNB cohort range: 22 - 89 years)."
        )

        grade_idx = int(cur["Histological grading"]) - 1
        grade = st.selectbox(
            "Nottingham Histological Grade *",
            options=[1.0, 2.0, 3.0],
            index=max(0, min(2, grade_idx)),
            format_func=lambda g: f"Grade {int(g)} ({'Well differentiated' if g==1 else ('Moderately differentiated' if g==2 else 'Poorly differentiated')})",
            help="Tubule formation, nuclear pleomorphism, and mitotic frequency grading."
        )

    with col2:
        er_idx = 0 if str(cur["ER"]).lower() == "positive" else 1
        er_status = st.selectbox(
            "Estrogen Receptor (ER) Status *",
            options=["Positive", "Negative"],
            index=er_idx,
            help="Immunohistochemistry nuclear staining positivity (>= 1%)."
        )

        her2_idx = 0 if str(cur["HER2"]).lower() == "positive" else 1
        her2_status = st.selectbox(
            "HER2 Receptor Status *",
            options=["Positive", "Negative"],
            index=her2_idx,
            help="Human Epidermal Growth Factor Receptor 2 amplification (IHC 3+ or ISH positive)."
        )

        st.caption("* Required clinical input field. All values are scaled into [0, pi] space before model inference.")

    return {
        "Tumour Size(cm)": tumour_size,
        "Age(years)": age,
        "Histological grading": grade,
        "ER": er_status,
        "HER2": her2_status
    }
