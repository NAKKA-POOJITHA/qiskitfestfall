"""
QuantumCure AI - Page 2: Patient Prediction Lab
Interactive multi-model prediction lab matching Reference UI styling with blind held-out evaluation.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import pandas as pd
import numpy as np

from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar
from frontend.components.patient_form import render_patient_input_form
from backend.prediction_service import PredictionService

st.set_page_config(
    page_title="Patient Prediction Lab — QuantumCure AI",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Patient Cases")

# Top Header Bar matching Reference UI
st.markdown("""
<div class="top-header-bar">
    <div class="search-pill-container">
        <span style="color: #94A3B8; margin-right: 8px;">🔍</span>
        <input type="text" placeholder="Search case or patient ID..." style="border: none; outline: none; width: 100%; font-size: 0.88rem; color: #1E293B;">
        <span style="color: #64748B; cursor: pointer; font-size: 14px;">⚙️</span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <div class="action-icon-pill">
            <span>✉️</span>
        </div>
        <div class="action-icon-pill" style="position: relative;">
            <span>🔔</span>
            <span style="position: absolute; top: 6px; right: 8px; width: 8px; height: 8px; background: #EF4444; border-radius: 50%;"></span>
        </div>
        <div class="user-profile-pill">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" style="width: 30px; height: 30px; border-radius: 50%; object-fit: cover;">
            <div style="font-size: 0.82rem; line-height: 1.2;">
                <strong style="color: #1E293B; display: block;">Dr. Sarah Mitchell</strong>
                <span style="color: #64748B; font-size: 0.75rem;">@mitchell.oncology</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #1E293B; letter-spacing: -0.02em;">
            Patient Prediction Lab
        </h1>
        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748B;">
            Evaluate Quantum-kernel SVM, Classical RBF-SVM, and XGBoost on genuine held-out test records.
        </p>
    </div>
    <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
        <button class="btn-summary-ai">
            <span>⚡</span> Quantum Park
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# Initialize Prediction Service in Session State
if "pred_service" not in st.session_state:
    try:
        svc = PredictionService()
        svc.load_artifacts()
        st.session_state["pred_service"] = svc
    except Exception as e:
        st.error(f"Failed to load model artifacts: {e}. Please ensure models are trained via `python -m backend.train`.")
        st.stop()

svc = st.session_state["pred_service"]
test_df = svc.load_test_patients()

tab1, tab2 = st.tabs(["🔍 Blind Held-Out Patient Evaluation", "✍️ Custom Clinical Case Entry"])

with tab1:
    st.markdown("""
    <div class="ref-dashboard-card" style="margin-bottom: 1rem;">
        <h3 class="ref-card-title">Select Unseen Held-out Test Patient</h3>
        <p class="ref-card-subtitle">
            Choose from 212 real anonymized records from the BCNB test cohort. True nodal status is blinded initially.
        </p>
    """, unsafe_allow_html=True)

    if len(test_df) == 0:
        st.warning("No test patients available. Please run data preprocessing first.")
    else:
        patient_options = [
            f"Patient #{row['Patient ID']} — Age: {int(row['orig_Age'])} yrs | Tumour: {row['orig_Tumour_Size']} cm | Grade: {int(row['orig_Histological_grade']) if not pd.isna(row['orig_Histological_grade']) else '2'}"
            for _, row in test_df.iterrows()
        ]

        selected_idx = st.selectbox(
            "Select Anonymized Patient Record:",
            range(len(patient_options)),
            format_func=lambda i: patient_options[i]
        )

        selected_patient = test_df.iloc[selected_idx]
        actual_target = int(selected_patient["target"])
        actual_aln_label = selected_patient["ALN status"]

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Tumour Diameter", f"{selected_patient['orig_Tumour_Size']} cm")
        with col2:
            st.metric("Patient Age", f"{int(selected_patient['orig_Age'])} yrs")
        with col3:
            grade_val = int(selected_patient['orig_Histological_grade']) if not pd.isna(selected_patient['orig_Histological_grade']) else 2
            st.metric("Histological Grade", f"Grade {grade_val}")
        with col4:
            st.metric("ER Receptor", str(selected_patient['orig_ER']))
        with col5:
            st.metric("HER2 Receptor", str(selected_patient['orig_HER2']))

        st.markdown("</div>", unsafe_allow_html=True)

        patient_input = {
            "Tumour Size(cm)": float(selected_patient["orig_Tumour_Size"]),
            "Age(years)": float(selected_patient["orig_Age"]),
            "Histological grading": float(grade_val),
            "ER": str(selected_patient["orig_ER"]),
            "HER2": str(selected_patient["orig_HER2"])
        }

        patient_key = f"pt_{selected_patient['Patient ID']}"
        if "reveal_state" not in st.session_state:
            st.session_state["reveal_state"] = {}

        if st.button("🚀 Run Multi-Model Prediction", key=f"btn_predict_{patient_key}", type="primary"):
            st.session_state[f"pred_{patient_key}"] = svc.predict_patient(patient_input)

        if f"pred_{patient_key}" in st.session_state:
            res = st.session_state[f"pred_{patient_key}"]
            q_res = res["quantum_svm"]
            c_res = res["classical_svm"]
            x_res = res["xgboost"]
            agr = res["agreement"]

            st.markdown("### Multi-Model Predictions")
            c1, c2, c3 = st.columns(3)

            with c1:
                q_label = "N+ (Metastasis)" if q_res["prediction"] == 1 else "N0 (Negative)"
                st.markdown(f"""
                <div class="ref-kpi-card" style="border-top: 4px solid #8B5CF6;">
                    <div class="kpi-floating-badge" style="background: #F3E8FF; color: #8B5CF6;">⚛️</div>
                    <div class="kpi-title">Quantum-kernel SVM</div>
                    <div class="kpi-value" style="font-size: 1.5rem; color: #8B5CF6;">{q_label}</div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-top: 8px;">
                        Calibrated Probability: <strong>{q_res['probability']*100:.1f}%</strong><br>
                        Raw Decision Score: <code>{q_res['decision_score']:+.4f}</code><br>
                        Max Training Fidelity: <code>{q_res['max_training_fidelity']:.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                c_label = "N+ (Metastasis)" if c_res["prediction"] == 1 else "N0 (Negative)"
                st.markdown(f"""
                <div class="ref-kpi-card" style="border-top: 4px solid #14B8A6;">
                    <div class="kpi-floating-badge" style="background: #E6FFFA; color: #14B8A6;">🧠</div>
                    <div class="kpi-title">Classical RBF-SVM</div>
                    <div class="kpi-value" style="font-size: 1.5rem; color: #14B8A6;">{c_label}</div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-top: 8px;">
                        Calibrated Probability: <strong>{c_res['probability']*100:.1f}%</strong><br>
                        Raw Decision Score: <code>{c_res['decision_score']:+.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                x_label = "N+ (Metastasis)" if x_res["prediction"] == 1 else "N0 (Negative)"
                st.markdown(f"""
                <div class="ref-kpi-card" style="border-top: 4px solid #FF7A59;">
                    <div class="kpi-floating-badge" style="background: #FFE8E0; color: #FF7A59;">🤖</div>
                    <div class="kpi-title">XGBoost Classifier</div>
                    <div class="kpi-value" style="font-size: 1.5rem; color: #FF7A59;">{x_label}</div>
                    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-top: 8px;">
                        Predicted Probability: <strong>{x_res['probability']*100:.1f}%</strong><br>
                        Tree Ensemble Majority
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            if agr["unanimous"]:
                st.markdown(f"""
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 12px 16px; font-size: 0.9rem; color: #166534;">
                    ✅ <strong>Unanimous Model Consensus:</strong> All 3 models agree on <strong>{agr['majority_label']}</strong>.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 12px 16px; font-size: 0.9rem; color: #92400E;">
                    ⚠️ <strong>Model Divergence:</strong> Split prediction. {agr['models_positive']} model(s) predict N+ while {agr['models_negative']} model(s) predict N0.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            reveal_clicked = st.button("🔓 Reveal Actual Pathological Result", key=f"reveal_{patient_key}")
            if reveal_clicked:
                st.session_state["reveal_state"][patient_key] = True

            if st.session_state["reveal_state"].get(patient_key, False):
                actual_text = "N+ (Metastasis Present)" if actual_target == 1 else "N0 (No Metastasis)"
                q_correct = (q_res["prediction"] == actual_target)
                c_correct = (c_res["prediction"] == actual_target)
                x_correct = (x_res["prediction"] == actual_target)

                st.markdown(f"""
                <div class="ref-dashboard-card" style="border: 2px solid #8B5CF6; background: #FAF5FF; margin-top: 15px;">
                    <div class="ref-card-header">
                        <div>
                            <h4 class="ref-card-title">Verified Ground-Truth Pathological Outcome</h4>
                            <div class="ref-card-subtitle">Official BCNB Staging: {actual_aln_label}</div>
                        </div>
                        <span class="status-pill-{'positive' if actual_target==1 else 'negative'}">{actual_text}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; font-size: 0.9rem;">
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px 14px;">
                            Quantum-kernel SVM: {'✅ Correct' if q_correct else '❌ Incorrect'}
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px 14px;">
                            Classical RBF-SVM: {'✅ Correct' if c_correct else '❌ Incorrect'}
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px 14px;">
                            XGBoost: {'✅ Correct' if x_correct else '❌ Incorrect'}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h3 class="ref-card-title">Manual Patient Case Entry</h3>
        <p class="ref-card-subtitle">
            Enter hypothetical clinicopathological markers to evaluate real-time multi-model inference.
        </p>
    """, unsafe_allow_html=True)
    manual_form_values = render_patient_input_form()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⚡ Run Multi-Model Inference", key="btn_manual_predict", type="primary"):
        manual_res = svc.predict_patient(manual_form_values)
        if not manual_res["success"]:
            st.error("Validation error: " + ", ".join(manual_res["errors"]))
        else:
            q_m = manual_res["quantum_svm"]
            c_m = manual_res["classical_svm"]
            x_m = manual_res["xgboost"]

            st.markdown("### Custom Case Diagnostic Estimates")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="ref-kpi-card" style="border-top: 4px solid #8B5CF6;">
                    <div class="kpi-floating-badge" style="background: #F3E8FF; color: #8B5CF6;">⚛️</div>
                    <div class="kpi-title">Quantum-kernel SVM</div>
                    <div class="kpi-value" style="font-size: 1.5rem; color: #8B5CF6;">{q_m['label']}</div>
                    <div style="font-size: 0.85rem; color: #64748B; margin-top: 8px;">
                        Calibrated Probability: <strong>{q_m['probability']*100:.1f}%</strong><br>
                        Mean Quantum Fidelity: <code>{q_m['mean_training_fidelity']:.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="ref-kpi-card" style="border-top: 4px solid #14B8A6;">
                    <div class="kpi-floating-badge" style="background: #E6FFFA; color: #14B8A6;">🧠</div>
                    <div class="kpi-title">Classical RBF-SVM</div>
                    <div class="kpi-value" style="font-size: 1.5rem; color: #14B8A6;">{c_m['label']}</div>
                    <div style="font-size: 0.85rem; color: #64748B; margin-top: 8px;">
                        Calibrated Probability: <strong>{c_m['probability']*100:.1f}%</strong><br>
                        Decision Score: <code>{c_m['decision_score']:+.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="ref-kpi-card" style="border-top: 4px solid #FF7A59;">
                    <div class="kpi-floating-badge" style="background: #FFE8E0; color: #FF7A59;">🤖</div>
                    <div class="kpi-title">XGBoost</div>
                    <div class="kpi-value" style="font-size: 1.5rem; color: #FF7A59;">{x_m['label']}</div>
                    <div style="font-size: 0.85rem; color: #64748B; margin-top: 8px;">
                        Estimated Probability: <strong>{x_m['probability']*100:.1f}%</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
