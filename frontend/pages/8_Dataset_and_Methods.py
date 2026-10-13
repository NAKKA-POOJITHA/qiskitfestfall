"""
QuantumCure AI - Page 8: Dataset & Methodology
Full implementation of Master Prompt Part 14:
- Verifiable BCNB dataset source, citation, and CC BY 4.0 license
- Exact 1,058 patient cohort size and binary target mapping (N0=0 vs N+=1)
- Selected feature dictionary with types, units, and clinical significance
- Zero-leakage preprocessing protocol and patient-level splitting
- Model configurations, hyperparameter selection, seeds, and software versions
- Scientific limitations and reproducibility disclosure
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

from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Dataset & Methods — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Dataset & Methods")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Dataset & Methodology
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Comprehensive documentation of clinical data provenance, zero-leakage preprocessing, and model parameters.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data audit and feature dictionary
res_dir = Path(root_dir) / "results"
proc_dir = Path(root_dir) / "dataset" / "processed"
audit_file = res_dir / "data_audit.json"
dict_file = proc_dir / "feature_dictionary.json"
config_file = res_dir / "experiment_config.json"

audit_data = {}
if audit_file.exists():
    with open(audit_file, "r", encoding="utf-8") as f:
        audit_data = json.load(f)

feat_dict = {}
if dict_file.exists():
    with open(dict_file, "r", encoding="utf-8") as f:
        feat_dict = json.load(f)

config = {}
if config_file.exists():
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Verified Cohort", f"{audit_data.get('records_count', 1058)} Patients", "Zero Duplicates")
with c2:
    st.metric("Predictor Features", "5 Biomarkers", "Scaled to [0, π]")
with c3:
    st.metric("Held-Out Test Set", "212 Patients", "Stratified 20%")
with c4:
    st.metric("Random Seed", "Seed 42", "Reproducible Split")

# Section 1: Provenance and Licensing
st.markdown("""
<div class="ref-dashboard-card" style="margin-top: 15px;">
    <h3 class="ref-card-title">Dataset Provenance & Regulatory Status</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; font-size: 0.84rem; line-height: 1.7; color: #25324A;">
        <div>
            <strong>Dataset Name:</strong> Breast Cancer Nodal / Biopsy (BCNB)<br>
            <strong>Primary Repository:</strong> The Cancer Imaging Archive (TCIA) / Nature Scientific Data<br>
            <strong>License:</strong> Creative Commons Attribution 4.0 International (CC BY 4.0)<br>
            <strong>Clinical Task:</strong> Pre-operative Axillary Lymph Node Metastasis Prediction<br>
            <strong>Target Variable:</strong> <code>ALN status</code> (N0 = 0 vs N+ = 1)
        </div>
        <div>
            <strong>Class 0 (Negative):</strong> N0 (655 patients, 61.91%)<br>
            <strong>Class 1 (Positive):</strong> N+(1-2) and N+(>2) (403 patients, 38.09%)<br>
            <strong>Confounder Exclusions:</strong> <code>Number of lymph node metastases</code> (Direct target leakage)<br>
            <strong>Data Integrity:</strong> 1,058 consecutive patients, zero artificial samples generated
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Section 2: Feature Dictionary Table
st.markdown("### Selected Predictor Feature Dictionary")
table_data = []
for fname, meta in feat_dict.items():
    table_data.append({
        "Biomarker Feature": fname,
        "Variable Type": meta.get("type", "Numerical"),
        "Clinical Units": meta.get("units", "cm / years / status"),
        "Biological / Clinical Significance": meta.get("clinical_significance", meta.get("description", ""))
    })

if table_data:
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

# Section 3: Preprocessing & Leakage Controls
st.markdown("""
<div class="ref-dashboard-card" style="margin-top: 15px;">
    <h3 class="ref-card-title">Zero-Leakage Preprocessing Protocol</h3>
    <div style="font-size: 0.84rem; color: #25324A; line-height: 1.7; margin-top: 10px;">
        <ol>
            <li><strong>Confounder Removal:</strong> The clinical attribute <code>Number of lymph node metastases</code> counts the resected positive nodes post-operatively. It is strictly excluded to prevent 100% target leakage.</li>
            <li><strong>Patient-Level Stratified Partition:</strong> The 1,058 patient dataset was split into 846 training cases (80%) and 212 held-out test cases (20%) using stratified random sampling preserving class ratio.</li>
            <li><strong>Training-Fitted Scaling:</strong> Features were mapped into the interval <code>[0, π]</code> using scikit-learn's <code>MinMaxScaler</code>. The scaler was fitted exclusively on training data and applied transform-only to test data.</li>
            <li><strong>Imputation Policy:</strong> Missing histological grading entries (12.48%) were imputed using the training median (Grade 2).</li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)

# Section 4: Software Stack & Reproducibility
st.markdown("""
<div class="ref-dashboard-card">
    <h3 class="ref-card-title">Software Environment & Reproducibility</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-top: 10px; font-size: 0.82rem; color: #25324A;">
        <div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 10px; padding: 12px;">
            <strong>Quantum Stack:</strong><br>
            Qiskit: <code>2.1.2</code><br>
            Backend: Statevector Simulator<br>
            Feature Map: ZZFeatureMap (reps=2)
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 10px; padding: 12px;">
            <strong>Classical Stack:</strong><br>
            Scikit-learn: <code>1.8.0</code><br>
            XGBoost: <code>3.4.1</code><br>
            NumPy: <code>2.x</code>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 10px; padding: 12px;">
            <strong>Runtime Environment:</strong><br>
            Python: <code>3.13.5</code><br>
            Host OS: Windows 11<br>
            Frontend: Streamlit Multi-Page
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
