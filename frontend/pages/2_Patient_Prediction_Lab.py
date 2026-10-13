"""
QuantumCure AI - Page 2: Patient Prediction Lab
Supports two distinct workflows:
- Workflow A: Enter Features Manually (interactive clinical input form, validation, presets, reset)
- Workflow B: Select Test Sample (real held-out 212-patient BCNB cohort, blinded target, reveal outcome)
- Multi-model evaluation across Quantum Kernel SVM, Classical RBF-SVM, and XGBoost
- Real inference execution, agreement indicator, and zero emojis
"""

import sys
import time
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import pandas as pd
import numpy as np

from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar
from frontend.components.patient_form import render_patient_input_form
from backend.prediction_service import PredictionService

st.set_page_config(
    page_title="Patient Prediction Lab — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Prediction Lab")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Patient Prediction Lab
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Run Quantum Kernel SVM, Classical RBF-SVM, and XGBoost on custom clinical entries or verified held-out test cases.
        </p>
    </div>
    <div style="display: flex; gap: 10px;">
        <a href="/Model_Comparison_Lab" target="_self" style="text-decoration: none;">
            <button class="btn-summary-ai">
                <span>Model Comparison Lab →</span>
            </button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Prediction Service in Session State
if "pred_service" not in st.session_state:
    try:
        svc = PredictionService()
        svc.load_artifacts()
        st.session_state["pred_service"] = svc
    except Exception as e:
        st.error(f"Failed to load model artifacts: {e}. Please ensure models are trained via backend pipeline.")
        st.stop()

svc = st.session_state["pred_service"]
test_df = svc.load_test_patients()

# Session Prediction History state
if "prediction_history" not in st.session_state:
    st.session_state["prediction_history"] = []

# Segmented control: Workflow A (Manual) | Workflow B (Held-Out Sample)
tab_manual, tab_heldout = st.tabs(["Enter Features Manually", "Select Test Sample (Held-Out Evaluation)"])

# ==============================================================================
# WORKFLOW A: ENTER FEATURES MANUALLY
# ==============================================================================
with tab_manual:
    st.markdown("""
    <div class="ref-dashboard-card" style="margin-bottom: 1.25rem;">
        <h3 class="ref-card-title">Manual Clinical Case Entry</h3>
        <p class="ref-card-subtitle">
            Input verified clinicopathological markers to evaluate real-time multi-model inference. Ground truth is not available for hypothetical entries.
        </p>
    """, unsafe_allow_html=True)

    manual_input_values = render_patient_input_form()
    st.markdown("</div>", unsafe_allow_html=True)

    col_btn_m, _ = st.columns([1, 4])
    with col_btn_m:
        run_manual = st.button("Run Prediction", key="btn_run_manual", type="primary", use_container_width=True)

    if run_manual:
        start_t = time.perf_counter()
        m_output = svc.predict_patient(manual_input_values)
        latency_ms = (time.perf_counter() - start_t) * 1000
        m_output["latency_ms"] = latency_ms
        st.session_state["latest_manual_pred"] = m_output

        # Add to session history
        st.session_state["prediction_history"].append({
            "Timestamp": time.strftime("%H:%M:%S"),
            "Patient ID": "Manual Entry",
            "Tumour (cm)": manual_input_values["Tumour Size(cm)"],
            "Age": int(manual_input_values["Age(years)"]),
            "Grade": int(manual_input_values["Histological grading"]),
            "Quantum Pred": m_output["quantum_svm"]["label"],
            "Quantum Score": f"{m_output['quantum_svm']['decision_score']:+.3f}",
            "Classical Pred": m_output["classical_svm"]["label"],
            "Classical Score": f"{m_output['classical_svm']['decision_score']:+.3f}",
            "XGBoost Pred": m_output["xgboost"]["label"],
            "XGBoost Prob": f"{m_output['xgboost']['probability']*100:.1f}%",
            "Consensus": m_output["agreement"]["majority_label"]
        })

    if "latest_manual_pred" in st.session_state:
        res = st.session_state["latest_manual_pred"]
        if not res["success"]:
            st.error("Validation error: " + ", ".join(res.get("errors", [])))
        else:
            q_res = res["quantum_svm"]
            c_res = res["classical_svm"]
            x_res = res["xgboost"]
            agr = res["agreement"]

            st.markdown("### Multi-Model Inference Results")
            c1, c2, c3 = st.columns(3)

            # Card 1: Quantum SVM (Purple #7965E8)
            with c1:
                st.markdown(f"""
                <div class="model-card-quantum">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span class="model-badge-quantum">Quantum Kernel</span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Status: Completed</span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-bottom: 0.35rem;">Qiskit ZZFeatureMap SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #7965E8; margin-bottom: 0.75rem;">{q_res['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6; border-top: 1px solid #F0EDFF; padding-top: 8px;">
                        Calibrated Probability: <strong style="color: #25324A;">{q_res['probability']*100:.1f}%</strong><br>
                        Raw Decision Margin: <code>{q_res['decision_score']:+.4f}</code><br>
                        Mean Training Fidelity: <code>{q_res['mean_training_fidelity']:.4f}</code><br>
                        Execution: <strong>Qiskit Statevector Simulator</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Technical Quantum Parameters", expanded=False):
                    st.caption("Qubits: 5 | Reps: 2 | Entanglement: Linear | Scaled Coordinates: " + str(res["scaled_features"]))

            # Card 2: Classical RBF-SVM (Teal #18A999)
            with c2:
                st.markdown(f"""
                <div class="model-card-rbf">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span class="model-badge-rbf">Classical Baseline</span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Status: Completed</span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-bottom: 0.35rem;">Classical RBF-SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #18A999; margin-bottom: 0.75rem;">{c_res['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6; border-top: 1px solid #E7F8F5; padding-top: 8px;">
                        Calibrated Probability: <strong style="color: #25324A;">{c_res['probability']*100:.1f}%</strong><br>
                        Raw Decision Margin: <code>{c_res['decision_score']:+.4f}</code><br>
                        Support Vectors: <strong>728</strong><br>
                        Kernel: <strong>Radial Basis Function (gamma=0.5)</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Technical RBF Parameters", expanded=False):
                    st.caption("C: 2.0 | gamma: 0.5 | Scaling: MinMaxScaler([0, pi]) | Probability Calibration: Platt Sigmoid")

            # Card 3: XGBoost (Coral #F08A78)
            with c3:
                st.markdown(f"""
                <div class="model-card-xgb">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span class="model-badge-xgb">Ensemble Baseline</span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Status: Completed</span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-bottom: 0.35rem;">XGBoost Classifier</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #F08A78; margin-bottom: 0.75rem;">{x_res['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6; border-top: 1px solid #FFF0EC; padding-top: 8px;">
                        Predicted Probability: <strong style="color: #25324A;">{x_res['probability']*100:.1f}%</strong><br>
                        Number of Estimators: <strong>50 Trees</strong><br>
                        Max Depth: <strong>3</strong> (learning_rate: 0.05)<br>
                        Inference Latency: <strong>{res.get('latency_ms', 4.2):.1f} ms</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Technical XGBoost Parameters", expanded=False):
                    st.caption("Trees: 50 | Max Depth: 3 | Split Criteria: Gain / Hist | Base Score: 0.5")

            # Agreement Box & Disclaimer
            st.markdown(f"""
            <div style="background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 12px; padding: 14px 18px; margin-top: 14px;">
                <div style="font-weight: 700; color: #92400E; font-size: 0.9rem;">
                    Model Consensus: {agr['majority_label']} ({agr['models_positive']} of 3 models predict N+)
                </div>
                <div style="font-size: 0.78rem; color: #78350F; margin-top: 4px;">
                    Exploratory manual prediction: No histological biopsy ground truth exists for hypothetical inputs. Model agreement does not establish ground-truth clinical validity.
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# WORKFLOW B: SELECT TEST SAMPLE (BLIND PROTOCOL)
# ==============================================================================
with tab_heldout:
    st.markdown("""
    <div class="ref-dashboard-card" style="margin-bottom: 1.25rem;">
        <h3 class="ref-card-title">Select Held-Out Test Patient</h3>
        <p class="ref-card-subtitle">
            Select an unseen patient record from the 212 held-out BCNB test cohort. True pathological lymph node status is blinded during prediction.
        </p>
    """, unsafe_allow_html=True)

    if len(test_df) == 0:
        st.warning("No test patients available. Please verify dataset files.")
    else:
        patient_options = [
            f"Patient #{int(row['Patient ID'])} | Tumour: {row['orig_Tumour_Size']} cm | Age: {int(row['orig_Age'])} yrs | Grade {int(row['orig_Histological_grade']) if not pd.isna(row['orig_Histological_grade']) else 2} | ER {row['orig_ER']} | HER2 {row['orig_HER2']}"
            for _, row in test_df.iterrows()
        ]

        selected_idx = st.selectbox(
            "Select Anonymized Patient Record:",
            range(len(patient_options)),
            format_func=lambda i: patient_options[i]
        )

        selected_patient = test_df.iloc[selected_idx]
        patient_id = int(selected_patient["Patient ID"])
        actual_target = int(selected_patient["target"])
        actual_aln_label = str(selected_patient["ALN status"])
        grade_val = int(selected_patient['orig_Histological_grade']) if not pd.isna(selected_patient['orig_Histological_grade']) else 2

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Primary Tumour Size", f"{selected_patient['orig_Tumour_Size']} cm")
        with col2:
            st.metric("Patient Age", f"{int(selected_patient['orig_Age'])} yrs")
        with col3:
            st.metric("Histological Grade", f"Grade {grade_val}")
        with col4:
            st.metric("Estrogen Receptor (ER)", str(selected_patient['orig_ER']))
        with col5:
            st.metric("HER2 Status", str(selected_patient['orig_HER2']))

        st.markdown("</div>", unsafe_allow_html=True)

        patient_input = {
            "Tumour Size(cm)": float(selected_patient["orig_Tumour_Size"]),
            "Age(years)": float(selected_patient["orig_Age"]),
            "Histological grading": float(grade_val),
            "ER": str(selected_patient["orig_ER"]),
            "HER2": str(selected_patient["orig_HER2"])
        }

        patient_key = f"pt_{patient_id}"

        col_btn_h, _ = st.columns([1, 4])
        with col_btn_h:
            run_clicked_h = st.button("Run All Models on Sample", key=f"btn_run_{patient_key}", type="primary", use_container_width=True)

        if run_clicked_h:
            start_t = time.perf_counter()
            prediction_output = svc.predict_patient(patient_input)
            latency_ms = (time.perf_counter() - start_t) * 1000
            prediction_output["latency_ms"] = latency_ms
            st.session_state[f"pred_{patient_key}"] = prediction_output

            # Add to history
            st.session_state["prediction_history"].append({
                "Timestamp": time.strftime("%H:%M:%S"),
                "Patient ID": f"#{patient_id}",
                "Tumour (cm)": selected_patient["orig_Tumour_Size"],
                "Age": int(selected_patient["orig_Age"]),
                "Grade": grade_val,
                "Quantum Pred": prediction_output["quantum_svm"]["label"],
                "Quantum Score": f"{prediction_output['quantum_svm']['decision_score']:+.3f}",
                "Classical Pred": prediction_output["classical_svm"]["label"],
                "Classical Score": f"{prediction_output['classical_svm']['decision_score']:+.3f}",
                "XGBoost Pred": prediction_output["xgboost"]["label"],
                "XGBoost Prob": f"{prediction_output['xgboost']['probability']*100:.1f}%",
                "Consensus": prediction_output["agreement"]["majority_label"]
            })

        if f"pred_{patient_key}" in st.session_state:
            res_h = st.session_state[f"pred_{patient_key}"]
            q_h = res_h["quantum_svm"]
            c_h = res_h["classical_svm"]
            x_h = res_h["xgboost"]
            agr_h = res_h["agreement"]

            st.markdown("### Model Predictions Comparison")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="model-card-quantum">
                    <span class="model-badge-quantum">Quantum Kernel</span>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-top: 6px;">Qiskit ZZFeatureMap SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #7965E8; margin: 6px 0;">{q_h['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Calibrated Probability: <strong>{q_h['probability']*100:.1f}%</strong><br>
                        Decision Margin: <code>{q_h['decision_score']:+.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="model-card-rbf">
                    <span class="model-badge-rbf">Classical Baseline</span>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-top: 6px;">Classical RBF-SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #18A999; margin: 6px 0;">{c_h['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Calibrated Probability: <strong>{c_h['probability']*100:.1f}%</strong><br>
                        Decision Margin: <code>{c_h['decision_score']:+.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="model-card-xgb">
                    <span class="model-badge-xgb">Ensemble Baseline</span>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-top: 6px;">XGBoost Classifier</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #F08A78; margin: 6px 0;">{x_h['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Predicted Probability: <strong>{x_h['probability']*100:.1f}%</strong><br>
                        Status: Completed ({res_h.get('latency_ms', 4.5):.1f} ms)
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Blind Protocol: Reveal Button
            reveal_key = f"reveal_{patient_id}"
            if reveal_key not in st.session_state:
                st.session_state[reveal_key] = False

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if not st.session_state[reveal_key]:
                if st.button("Reveal Actual Outcome", key=f"btn_rev_{patient_id}"):
                    st.session_state[reveal_key] = True
                    st.rerun()
            else:
                q_correct = (q_h["prediction"] == actual_target)
                c_correct = (c_h["prediction"] == actual_target)
                x_correct = (x_h["prediction"] == actual_target)

                st.markdown(f"""
                <div class="ground-truth-box">
                    <h4 style="margin: 0; color: #25324A; font-size: 1.1rem; font-weight: 800;">
                        Verified Ground-Truth Pathological Outcome
                    </h4>
                    <p style="margin: 4px 0 12px 0; font-size: 0.84rem; color: #64748B;">
                        Anonymized Patient #{patient_id} Pathology Staging:
                        <strong style="color: #25324A;">{actual_aln_label}</strong>
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
                        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 16px;">
                            <span style="color: #64748B; font-size: 0.76rem; display: block;">Quantum Kernel SVM</span>
                            <strong style="color: {'#18A999' if q_correct else '#E11D48'}; font-size: 1rem;">
                                {'Correct Prediction' if q_correct else 'Misclassified'}
                            </strong>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 16px;">
                            <span style="color: #64748B; font-size: 0.76rem; display: block;">Classical RBF-SVM</span>
                            <strong style="color: {'#18A999' if c_correct else '#E11D48'}; font-size: 1rem;">
                                {'Correct Prediction' if c_correct else 'Misclassified'}
                            </strong>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 16px;">
                            <span style="color: #64748B; font-size: 0.76rem; display: block;">XGBoost Classifier</span>
                            <strong style="color: {'#18A999' if x_correct else '#E11D48'}; font-size: 1rem;">
                                {'Correct Prediction' if x_correct else 'Misclassified'}
                            </strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# SECTION: SESSION PREDICTION HISTORY
# ==============================================================================
st.markdown("---")
st.markdown("### Session Prediction History")
st.caption("Temporary session-level audit trail. No patient data is permanently stored on external servers.")

if st.session_state["prediction_history"]:
    hist_df = pd.DataFrame(st.session_state["prediction_history"])
    st.dataframe(hist_df, use_container_width=True)

    col_h1, col_h2, _ = st.columns([1, 1, 3])
    with col_h1:
        if st.button("Clear History"):
            st.session_state["prediction_history"] = []
            st.rerun()
    with col_h2:
        csv_data = hist_df.to_csv(index=False).encode("utf-8")
        st.download_button("Export History CSV", data=csv_data, file_name="prediction_history.csv", mime="text/csv")
else:
    st.info("No predictions executed in current session yet. Run a manual entry or select a test sample above.")
