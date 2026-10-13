"""
QuantumCure AI - Interactive Patient Feature Form Component
"""

import streamlit as st


def render_patient_input_form(default_values=None):
    """
    Renders standardized input form for manual or pre-filled patient values.
    Returns dictionary with validated inputs or None.
    """
    defaults = default_values or {
        "Tumour Size(cm)": 2.5,
        "Age(years)": 52,
        "Histological grading": 2.0,
        "ER": "Positive",
        "HER2": "Negative"
    }

    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h4 style="margin: 0; color: #25324A; font-size: 1.05rem;">Clinical Feature Input Form</h4>
        <p style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">
            Input legitimate pre-operative clinicopathological features for multi-model inference.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        tumour_size = st.number_input(
            "Primary Tumour Diameter (cm)",
            min_value=0.1,
            max_value=15.0,
            value=float(defaults.get("Tumour Size(cm)", 2.5)),
            step=0.1,
            help="Maximum pathological or pre-operative ultrasound/MRI diameter of the primary breast lesion."
        )

        age = st.number_input(
            "Patient Age at Diagnosis (years)",
            min_value=18,
            max_value=105,
            value=int(defaults.get("Age(years)", 52)),
            step=1,
            help="Chronological age of patient in completed years."
        )

        grade = st.selectbox(
            "Nottingham Histological Grade",
            options=[1.0, 2.0, 3.0],
            index=int(defaults.get("Histological grading", 2.0)) - 1,
            format_func=lambda g: f"Grade {int(g)} ({'Well diff' if g==1 else ('Mod diff' if g==2 else 'Poorly diff')})",
            help="Tubule formation, nuclear pleomorphism, and mitotic frequency grading."
        )

    with col2:
        er_default_idx = 0 if str(defaults.get("ER", "Positive")).lower() == "positive" else 1
        er_status = st.selectbox(
            "Estrogen Receptor (ER) Status",
            options=["Positive", "Negative"],
            index=er_default_idx,
            help="Immunohistochemistry (IHC) nuclear staining threshold >= 1%."
        )

        her2_default_idx = 1 if str(defaults.get("HER2", "Negative")).lower() == "negative" else 0
        her2_status = st.selectbox(
            "HER2 Status (Amplification / IHC)",
            options=["Positive", "Negative"],
            index=her2_default_idx,
            help="HER2 status by IHC 3+ or ISH gene amplification."
        )

    return {
        "Tumour Size(cm)": tumour_size,
        "Age(years)": age,
        "Histological grading": grade,
        "ER": er_status,
        "HER2": her2_status
    }
