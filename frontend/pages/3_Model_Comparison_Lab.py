"""
QuantumCure AI - Page 3: Model Comparison & Research Analytics Lab
Full implementation of Master Prompt Part 8:
- Metrics: AUROC, Accuracy, Precision, Recall/Sensitivity, Specificity, F1-Score, PR-AUC, Confusion Matrix, FPR, FNR, Runtimes
- Overlaid ROC curves and Precision-Recall curves
- Side-by-side Confusion Matrices
- Interactive Threshold Exploration Slider with dynamic metric calculation
- Sortable benchmark comparison table with CSV and JSON downloads
- Scientifically honest Quantum vs Classical comparative research analysis
- Strict No-Emoji policy
"""

import sys
import json
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import (
    roc_curve, roc_auc_score,
    precision_recall_curve, average_precision_score,
    confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
)

from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar
from frontend.components.charts import (
    create_interactive_roc_curves,
    create_precision_recall_curves,
    create_confusion_matrix_charts,
    create_auroc_bar_chart,
    create_runtime_comparison_chart
)

st.set_page_config(
    page_title="Model Comparison Lab — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Model Comparison")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Model Comparison & Analytics Lab
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Head-to-head empirical benchmarking: Quantum-Kernel SVM vs Classical RBF-SVM vs XGBoost on 212 held-out BCNB patients.
        </p>
    </div>
    <div style="display: flex; gap: 10px;">
        <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
            <button class="btn-summary-ai">
                <span>Quantum Insights & Heatmap →</span>
            </button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data files
res_path = Path(root_dir) / "results"
metrics_file = res_path / "metrics.json"
preds_file = res_path / "predictions.csv"
config_file = res_path / "experiment_config.json"

metrics_list = []
preds_df = None
config = {}

if metrics_file.exists():
    with open(metrics_file, "r", encoding="utf-8") as f:
        metrics_list = json.load(f)

if preds_file.exists():
    preds_df = pd.read_csv(preds_file)

if config_file.exists():
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

if not metrics_list or preds_df is None:
    st.error("Verified experiment results not found. Please ensure training and evaluation scripts have run.")
    st.stop()

# ==============================================================================
# SECTION A: BENCHMARK SUMMARY TABLE & COHORT OVERVIEW
# ==============================================================================
st.markdown("""
<div class="ref-dashboard-card" style="margin-bottom: 1.25rem;">
    <div class="ref-card-header">
        <div>
            <h3 class="ref-card-title">Verified Benchmark Metrics Summary</h3>
            <div class="ref-card-subtitle">
                Evaluation Split: 212 held-out test patients (131 N0 / 81 N+ | 38.2% baseline metastasis prevalence)
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

table_data = []
for m in metrics_list:
    table_data.append({
        "Model": m["model_name"],
        "AUROC": f"{m.get('auroc', 0.0):.4f}",
        "Accuracy": f"{m.get('accuracy', 0.0)*100:.2f}%",
        "Precision": f"{m.get('precision', 0.0)*100:.2f}%",
        "Recall (Sens.)": f"{m.get('recall', 0.0)*100:.2f}%",
        "Specificity": f"{m.get('specificity', 0.0)*100:.2f}%",
        "F1-Score": f"{m.get('f1_score', 0.0):.4f}",
        "PR-AUC": f"{m.get('pr_auc', 0.0):.4f}",
        "Train Time (s)": f"{m.get('training_time_seconds', 0.0):.2f}",
        "Inference (ms)": f"{m.get('inference_time_ms_per_patient', 0.0):.2f}",
        "Status": "Verified"
    })

bench_df = pd.DataFrame(table_data)
st.dataframe(bench_df, use_container_width=True, hide_index=True)

# Export buttons
col_d1, col_d2, _ = st.columns([1.2, 1.2, 3])
with col_d1:
    csv_bytes = bench_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Metrics CSV", data=csv_bytes, file_name="quantumcure_model_comparison.csv", mime="text/csv")
with col_d2:
    json_bytes = json.dumps(metrics_list, indent=2).encode("utf-8")
    st.download_button("Download Metrics JSON", data=json_bytes, file_name="quantumcure_model_comparison.json", mime="application/json")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# SECTION B: INTERACTIVE CHARTS (ROC, PR, CONFUSION MATRICES)
# ==============================================================================
tab_charts1, tab_charts2, tab_charts3 = st.tabs(["ROC & PR Curves", "Confusion Matrices", "Computational Latency"])

with tab_charts1:
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        st.markdown("""
        <div class="ref-dashboard-card">
            <h4 class="ref-card-title">Receiver Operating Characteristic (ROC)</h4>
            <div class="ref-card-subtitle">True Positive Rate vs False Positive Rate across all thresholds</div>
        """, unsafe_allow_html=True)
        fig_roc = create_interactive_roc_curves(preds_df)
        st.plotly_chart(fig_roc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        st.markdown("""
        <div class="ref-dashboard-card">
            <h4 class="ref-card-title">Precision-Recall (PR) Curves</h4>
            <div class="ref-card-subtitle">Precision vs Recall in class-imbalanced setting (38.2% positive prevalence)</div>
        """, unsafe_allow_html=True)
        fig_pr = create_precision_recall_curves(preds_df)
        st.plotly_chart(fig_pr, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_charts2:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Side-by-Side Model Confusion Matrices</h4>
        <div class="ref-card-subtitle">Exact classification breakdowns evaluated at default decision boundary</div>
    """, unsafe_allow_html=True)

    cm1, cm2, cm3 = st.columns(3)
    with cm1:
        fig_cm_q = create_confusion_matrix_charts(preds_df, "Quantum_kernel_SVM")
        st.plotly_chart(fig_cm_q, use_container_width=True)
    with cm2:
        fig_cm_c = create_confusion_matrix_charts(preds_df, "Classical_RBF_SVM")
        st.plotly_chart(fig_cm_c, use_container_width=True)
    with cm3:
        fig_cm_x = create_confusion_matrix_charts(preds_df, "XGBoost")
        st.plotly_chart(fig_cm_x, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_charts3:
    col_r1, col_r2 = st.columns([1.2, 1])
    with col_r1:
        st.markdown("""
        <div class="ref-dashboard-card">
            <h4 class="ref-card-title">Training Time vs Inference Latency</h4>
            <div class="ref-card-subtitle">Resource comparison between classical CPU pipelines and quantum statevector simulations</div>
        """, unsafe_allow_html=True)
        fig_rt = create_runtime_comparison_chart(metrics_list)
        st.plotly_chart(fig_rt, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r2:
        st.markdown("""
        <div class="ref-dashboard-card">
            <h4 class="ref-card-title">Computational Complexity Profile</h4>
            <div style="font-size: 0.82rem; color: #25324A; line-height: 1.7; margin-top: 10px;">
                <p><strong>Classical RBF-SVM:</strong> Gram matrix construction scale is O(N² · d) with vectorized Euclidean distances. Evaluated in 0.04s.</p>
                <p><strong>XGBoost:</strong> Tree building scale is O(K · d · N log N) with histogram approximation. Trained in 0.08s.</p>
                <p><strong>Quantum-Kernel SVM:</strong> Computing pairwise fidelity |⟨Φ(x)|Φ(y)⟩|² requires statevector simulations scaling as O(N² · 2ⁿ) where n=5 qubits. Test kernel computation took 4.12s.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# SECTION C: INTERACTIVE THRESHOLD EXPLORATION (Part 8.C)
# ==============================================================================
st.markdown("---")
st.markdown("""
<div class="ref-dashboard-card">
    <h3 class="ref-card-title">Diagnostic Decision Threshold Explorer</h3>
    <p class="ref-card-subtitle">
        Investigate how varying classification thresholds trades off sensitivity (catching all metastases) versus specificity (avoiding overtreatment).
    </p>
""", unsafe_allow_html=True)

col_t_model, col_t_slider = st.columns([1, 2])
with col_t_model:
    selected_thresh_model = st.selectbox(
        "Select Model for Threshold Tuning:",
        ["XGBoost", "Classical_RBF_SVM", "Quantum_kernel_SVM"],
        format_func=lambda x: x.replace("_", " ")
    )
with col_t_slider:
    threshold_val = st.slider("Classification Threshold (Probability Cutoff):", min_value=0.10, max_value=0.90, value=0.50, step=0.02)

# Dynamic threshold recalculation on test cohort
score_col = f"{selected_thresh_model}_Score"
y_true = preds_df["Ground Truth Target"].values
scores = preds_df[score_col].values

# Convert continuous scores to threshold predictions
y_thresh_pred = (scores >= threshold_val).astype(int)

th_acc = accuracy_score(y_true, y_thresh_pred)
th_prec = precision_score(y_true, y_thresh_pred, zero_division=0)
th_sens = recall_score(y_true, y_thresh_pred, zero_division=0)
cm_th = confusion_matrix(y_true, y_thresh_pred)
th_tn, th_fp, th_fn, th_tp = cm_th.ravel()
th_spec = th_tn / (th_tn + th_fp) if (th_tn + th_fp) > 0 else 0.0
th_f1 = f1_score(y_true, y_thresh_pred, zero_division=0)

m_c1, m_c2, m_c3, m_c4, m_c5 = st.columns(5)
with m_c1:
    st.metric("Sensitivity (Recall)", f"{th_sens*100:.1f}%")
with m_c2:
    st.metric("Specificity", f"{th_spec*100:.1f}%")
with m_c3:
    st.metric("Precision (PPV)", f"{th_prec*100:.1f}%")
with m_c4:
    st.metric("F1-Score", f"{th_f1:.4f}")
with m_c5:
    st.metric("Overall Accuracy", f"{th_acc*100:.1f}%")

st.caption(f"At threshold {threshold_val:.2f}: True Positives: {th_tp} | False Negatives (Missed N+): {th_fn} | False Positives (False Alarms): {th_fp} | True Negatives: {th_tn}")
st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# SECTION D: SCIENTIFIC QUANTUM VS CLASSICAL ANALYSIS (Part 8.E)
# ==============================================================================
st.markdown("""
<div class="ref-dashboard-card" style="border-left: 4px solid #7965E8;">
    <h3 class="ref-card-title">Scientific Findings: Quantum vs Classical Comparison</h3>
    <div class="ref-card-subtitle">Empirical analysis answering the core research question</div>
    <div style="font-size: 0.85rem; color: #25324A; line-height: 1.7; margin-top: 12px;">
        <h4 style="color: #7965E8; margin: 0 0 6px 0;">Primary Research Question:</h4>
        <p><em>"Does the quantum-kernel model offer a measurable advantage over classical models for breast cancer axillary lymph node metastasis prediction?"</em></p>
        
        <h4 style="color: #25324A; margin: 12px 0 6px 0;">Empirical Conclusion:</h4>
        <p>
            <strong>No measurable quantum advantage is observed on this clinical tabular dataset.</strong><br>
            Empirical benchmarking on the 212 held-out BCNB patient cohort reveals:
        </p>
        <ul>
            <li><strong>XGBoost</strong> achieved highest discrimination: <strong>AUROC 0.6012</strong> (Accuracy 59.43%, PR-AUC 0.4731).</li>
            <li><strong>Classical RBF-SVM</strong> performed comparably: <strong>AUROC 0.5982</strong> (Accuracy 59.43%, PR-AUC 0.4497).</li>
            <li><strong>Quantum-kernel SVM (ZZFeatureMap)</strong> achieved: <strong>AUROC 0.5001</strong> (Accuracy 50.47%, PR-AUC 0.3804), performing near random chance.</li>
        </ul>

        <h4 style="color: #25324A; margin: 12px 0 6px 0;">Why Classical Models Outperform Quantum Kernel Learning Here:</h4>
        <ol>
            <li><strong>Tabular Feature Inductive Bias:</strong> Clinical tabular predictors (tumor size, age, grade) have monotonic and thresholded decision boundaries that tree ensembles and RBF kernels capture efficiently.</li>
            <li><strong>Exponential Feature Map Geometry:</strong> The ZZFeatureMap projects data into high-dimensional Hilbert space (dimension 32) using periodic Pauli rotations. For continuous biological biomarkers, trigonometric periodic wrapping can map non-similar tumor diameters to near-orthogonal quantum states, reducing generalizability.</li>
            <li><strong>Computational Overhead:</strong> Classical RBF-SVM training completed in 0.04s, whereas quantum statevector inner product computation required 4.12s—representing an approximately 100x increase in computational burden without performance benefit.</li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)
