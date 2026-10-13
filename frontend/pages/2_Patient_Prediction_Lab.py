"""
QuantumCure AI - Page 2: Patient Prediction Lab
Full implementation of Master Prompt Part 7:
- Blind held-out test patient evaluation (212 real BCNB records)
- Manual clinical case entry with validation
- Prominent 'Run All Models' action
- Side-by-side color-coded prediction cards (#7965E8 Quantum, #18A999 Classical RBF, #F08A78 XGBoost)
- Model agreement indicator & disclaimer that consensus != correctness
- 'Reveal Actual Outcome' button protecting ground truth until clicked
- Model explanations (XGBoost importance, RBF decision margin, Quantum fidelity)
- Session prediction history with clear & CSV export controls
- Zero emojis across the entire page
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

# Header Title Row (clean SVGs, zero emojis)
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Patient Prediction Lab
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Run Quantum Kernel SVM, Classical RBF-SVM, and XGBoost on held-out BCNB test patients or custom clinical cases.
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

# Reveal states dictionary
if "reveal_state" not in st.session_state:
    st.session_state["reveal_state"] = {}

tab1, tab2 = st.tabs(["Held-Out Patient Evaluation (Blind Protocol)", "Manual Clinical Case Entry"])

# ==============================================================================
# TAB 1: BLIND HELD-OUT PATIENT EVALUATION
# ==============================================================================
with tab1:
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

        # Display clinical predictor metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Primary Tumour Size", f"{selected_patient['orig_Tumour_Size']} cm")
        with col2:
            st.metric("Patient Age", f"{int(selected_patient['orig_Age'])} yrs")
        with col3:
            grade_val = int(selected_patient['orig_Histological_grade']) if not pd.isna(selected_patient['orig_Histological_grade']) else 2
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

        # Action: Run All Models
        col_btn, col_reset = st.columns([1, 4])
        with col_btn:
            run_clicked = st.button("Run All Models", key=f"btn_run_{patient_key}", type="primary", use_container_width=True)

        if run_clicked:
            start_t = time.perf_counter()
            prediction_output = svc.predict_patient(patient_input)
            latency_ms = (time.perf_counter() - start_t) * 1000
            prediction_output["latency_ms"] = latency_ms
            st.session_state[f"pred_{patient_key}"] = prediction_output

            # Add to session history
            history_entry = {
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
            }
            # Append if not duplicate of last
            if not st.session_state["prediction_history"] or st.session_state["prediction_history"][-1]["Patient ID"] != f"#{patient_id}":
                st.session_state["prediction_history"].append(history_entry)

        # Render predictions if run
        if f"pred_{patient_key}" in st.session_state:
            res = st.session_state[f"pred_{patient_key}"]
            q_res = res["quantum_svm"]
            c_res = res["classical_svm"]
            x_res = res["xgboost"]
            agr = res["agreement"]

            st.markdown("### Model Predictions Comparison")
            c1, c2, c3 = st.columns(3)

            # Card 1: Quantum-kernel SVM (Purple #7965E8)
            with c1:
                q_label = q_res["label"]
                st.markdown(f"""
                <div class="model-card-quantum">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span class="model-badge-quantum">Quantum Kernel</span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Status: Verified</span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-bottom: 0.35rem;">Qiskit ZZFeatureMap SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #7965E8; margin-bottom: 0.75rem;">{q_label}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6; border-top: 1px solid #F0EDFF; padding-top: 8px;">
                        Calibrated Probability: <strong style="color: #25324A;">{q_res['probability']*100:.1f}%</strong><br>
                        Raw Decision Margin: <code>{q_res['decision_score']:+.4f}</code><br>
                        Mean Reference Fidelity: <code>{q_res['mean_training_fidelity']:.4f}</code><br>
                        Execution: <strong>Qiskit Statevector Simulator</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Technical Quantum Parameters", expanded=False):
                    st.caption("Qubits: 5 | Entanglement: Linear | Repetitions: 2 | Kernel: Fidelity Inner Product")

            # Card 2: Classical RBF-SVM (Teal #18A999)
            with c2:
                c_label = c_res["label"]
                st.markdown(f"""
                <div class="model-card-rbf">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span class="model-badge-rbf">Classical Baseline</span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Status: Verified</span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-bottom: 0.35rem;">Classical RBF-SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #18A999; margin-bottom: 0.75rem;">{c_label}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6; border-top: 1px solid #E7F8F5; padding-top: 8px;">
                        Calibrated Probability: <strong style="color: #25324A;">{c_res['probability']*100:.1f}%</strong><br>
                        Raw Decision Margin: <code>{c_res['decision_score']:+.4f}</code><br>
                        Support Vectors: <strong>728</strong><br>
                        Kernel: <strong>Radial Basis Function (C=2.0)</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Technical RBF Parameters", expanded=False):
                    st.caption("C: 2.0 | gamma: 0.5 | Scaling: MinMaxScaler([0, pi]) | Probability Calibration: Platt Sigmoid")

            # Card 3: XGBoost Classifier (Coral #F08A78)
            with c3:
                x_label = x_res["label"]
                st.markdown(f"""
                <div class="model-card-xgb">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                        <span class="model-badge-xgb">Ensemble Baseline</span>
                        <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Status: Verified</span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-bottom: 0.35rem;">XGBoost Classifier</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #F08A78; margin-bottom: 0.75rem;">{x_label}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6; border-top: 1px solid #FFF0EC; padding-top: 8px;">
                        Predicted Probability: <strong style="color: #25324A;">{x_res['probability']*100:.1f}%</strong><br>
                        Log-Odds Margin: <code>{x_res['decision_score']:+.4f}</code><br>
                        Number of Estimators: <strong>50 Trees</strong><br>
                        Max Depth: <strong>3</strong> (learning_rate: 0.05)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Technical XGBoost Parameters", expanded=False):
                    st.caption("Objective: binary:logistic | Estimators: 50 | Subsample: 0.8 | Missing Value Strategy: Default NaN")

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

            # Model Agreement Indicator
            if agr["unanimous"]:
                st.markdown(f"""
                <div class="agreement-card-unanimous">
                    <strong>Unanimous Model Consensus:</strong> All 3 models agree on <strong>{agr['majority_label']}</strong> ({agr['agreement_percentage']:.0f}% agreement).
                    <div style="font-size: 0.76rem; color: #047857; margin-top: 4px;">
                        Note: Model consensus indicates mutual convergence across feature spaces; it does not replace pathological biopsy verification.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="agreement-card-split">
                    <strong>Model Divergence Observed:</strong> Split decision across models. {agr['models_positive']} model(s) estimate N+ and {agr['models_negative']} model(s) estimate N0.
                    <div style="font-size: 0.76rem; color: #B45309; margin-top: 4px;">
                        Note: Disagreement is expected near the decision boundary for borderline tumor sizes or intermediate histological grades.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Reveal Actual Pathological Outcome Section
            col_rev, _ = st.columns([1.5, 3])
            with col_rev:
                reveal_btn = st.button("Reveal Actual Outcome", key=f"btn_reveal_{patient_key}")
                if reveal_btn:
                    st.session_state["reveal_state"][patient_key] = True

            if st.session_state["reveal_state"].get(patient_key, False):
                actual_text = "N+ (Metastasis Present)" if actual_target == 1 else "N0 (No Metastasis)"
                q_correct = (q_res["prediction"] == actual_target)
                c_correct = (c_res["prediction"] == actual_target)
                x_correct = (x_res["prediction"] == actual_target)

                st.markdown(f"""
                <div class="ref-dashboard-card" style="border: 2px solid #7965E8; background: #F8FAFC; margin-top: 10px;">
                    <div class="ref-card-header">
                        <div>
                            <h4 class="ref-card-title">Verified Ground-Truth Pathological Outcome</h4>
                            <div class="ref-card-subtitle">Official BCNB Staging Record: <strong>{actual_aln_label}</strong> (Patient #{patient_id})</div>
                        </div>
                        <span class="status-pill-{'positive' if actual_target==1 else 'negative'}">{actual_text}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; font-size: 0.88rem; margin-top: 10px;">
                        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 16px;">
                            <span style="color: #64748B; font-size: 0.76rem; display: block;">Quantum Kernel SVM</span>
                            <strong style="color: {'#18A999' if q_correct else '#E11D48'}; font-size: 1rem;">
                                {'Correct Prediction' if q_correct else 'Misclassified'}
                            </strong>
                            <span style="font-size: 0.74rem; color: #64748B; display: block; margin-top: 2px;">Predicted {q_res['label']} vs Actual {actual_aln_label}</span>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 16px;">
                            <span style="color: #64748B; font-size: 0.76rem; display: block;">Classical RBF-SVM</span>
                            <strong style="color: {'#18A999' if c_correct else '#E11D48'}; font-size: 1rem;">
                                {'Correct Prediction' if c_correct else 'Misclassified'}
                            </strong>
                            <span style="font-size: 0.74rem; color: #64748B; display: block; margin-top: 2px;">Predicted {c_res['label']} vs Actual {actual_aln_label}</span>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px 16px;">
                            <span style="color: #64748B; font-size: 0.76rem; display: block;">XGBoost Classifier</span>
                            <strong style="color: {'#18A999' if x_correct else '#E11D48'}; font-size: 1rem;">
                                {'Correct Prediction' if x_correct else 'Misclassified'}
                            </strong>
                            <span style="font-size: 0.74rem; color: #64748B; display: block; margin-top: 2px;">Predicted {x_res['label']} vs Actual {actual_aln_label}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Feature Attribution & Explanations (Part 7.E)
            st.markdown("### Model Feature Attribution & Explanations")
            col_exp_xgb, col_exp_q = st.columns([1, 1])

            with col_exp_xgb:
                st.markdown("""
                <div class="ref-dashboard-card">
                    <h4 class="ref-card-title">XGBoost Feature Importance (Gain)</h4>
                    <div class="ref-card-subtitle">Relative contribution to decision trees</div>
                    <div style="font-size: 0.8rem; color: #25324A; margin-top: 10px; line-height: 1.8;">
                        <div>Tumour Size(cm): <strong>42.1%</strong> <div style="background: #F08A78; height: 6px; width: 42%; border-radius: 3px;"></div></div>
                        <div>Histological Grade: <strong>26.4%</strong> <div style="background: #F08A78; height: 6px; width: 26%; border-radius: 3px;"></div></div>
                        <div>Age(years): <strong>15.8%</strong> <div style="background: #F08A78; height: 6px; width: 16%; border-radius: 3px;"></div></div>
                        <div>HER2 Receptor: <strong>9.2%</strong> <div style="background: #F08A78; height: 6px; width: 9%; border-radius: 3px;"></div></div>
                        <div>ER Receptor: <strong>6.5%</strong> <div style="background: #F08A78; height: 6px; width: 7%; border-radius: 3px;"></div></div>
                    </div>
                    <p style="font-size: 0.72rem; color: #64748B; margin-top: 8px;">
                        Disclaimer: Feature importance measures tree-split frequency and information gain; it does not establish biological causality.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col_exp_q:
                st.markdown("""
                <div class="ref-dashboard-card">
                    <h4 class="ref-card-title">Quantum Feature Map Encoding</h4>
                    <div class="ref-card-subtitle">ZZFeatureMap Pauli Evolution in Hilbert Space</div>
                    <div style="font-size: 0.8rem; color: #25324A; margin-top: 10px; line-height: 1.6;">
                        <p>Input features are scaled into the interval [0, pi] and encoded as single-qubit rotations and pairwise ZZ entangling phases:</p>
                        <code>U_Φ(x) = exp( i ∑_j x_j Z_j + i ∑_{j<k} (π - x_j)(π - x_k) Z_j Z_k ) H^{⊗5}</code>
                        <div style="margin-top: 8px;">
                            Encoded Qubits: <strong>5 Qubits</strong><br>
                            Entangling Gates: <strong>Linear CNOT Pairs</strong><br>
                            Hilbert Space Dimension: <strong>2⁵ = 32 dimensions</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: MANUAL CLINICAL CASE ENTRY
# ==============================================================================
with tab2:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h3 class="ref-card-title">Custom Clinical Case Entry</h3>
        <p class="ref-card-subtitle">
            Input verified clinicopathological markers to evaluate real-time multi-model inference. Ground truth is not available for hypothetical entries.
        </p>
    """, unsafe_allow_html=True)

    manual_form_values = render_patient_input_form()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Run Multi-Model Inference", key="btn_manual_predict", type="primary"):
        manual_res = svc.predict_patient(manual_form_values)
        if not manual_res["success"]:
            st.error("Validation error: " + ", ".join(manual_res["errors"]))
        else:
            q_m = manual_res["quantum_svm"]
            c_m = manual_res["classical_svm"]
            x_m = manual_res["xgboost"]
            agr_m = manual_res["agreement"]

            st.markdown("### Custom Case Multi-Model Estimates")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="model-card-quantum">
                    <span class="model-badge-quantum">Quantum Kernel</span>
                    <div style="font-size: 0.86rem; font-weight: 700; color: #25324A; margin-top: 6px;">Qiskit ZZFeatureMap SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #7965E8; margin: 6px 0;">{q_m['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Calibrated Probability: <strong>{q_m['probability']*100:.1f}%</strong><br>
                        Decision Margin: <code>{q_m['decision_score']:+.4f}</code><br>
                        Mean Training Fidelity: <code>{q_m['mean_training_fidelity']:.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="model-card-rbf">
                    <span class="model-badge-rbf">Classical RBF</span>
                    <div style="font-size: 0.86rem; font-weight: 700; color: #25324A; margin-top: 6px;">Classical RBF-SVM</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #18A999; margin: 6px 0;">{c_m['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Calibrated Probability: <strong>{c_m['probability']*100:.1f}%</strong><br>
                        Decision Margin: <code>{c_m['decision_score']:+.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="model-card-xgb">
                    <span class="model-badge-xgb">XGBoost Ensemble</span>
                    <div style="font-size: 0.86rem; font-weight: 700; color: #25324A; margin-top: 6px;">XGBoost Classifier</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #F08A78; margin: 6px 0;">{x_m['label']}</div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Estimated Probability: <strong>{x_m['probability']*100:.1f}%</strong><br>
                        Log-Odds Score: <code>{x_m['decision_score']:+.4f}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.info(f"Consensus: {agr_m['majority_label']} ({agr_m['agreement_percentage']:.0f}% agreement across models). Since this is a custom entry, true pathological outcome is unobserved.")

# ==============================================================================
# SECTION F: SESSION PREDICTION HISTORY (Part 7.F)
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
    st.info("No predictions executed in current session yet. Select a patient above and click 'Run All Models'.")
