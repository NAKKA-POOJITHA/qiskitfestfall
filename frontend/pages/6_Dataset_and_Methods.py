"""
QuantumCure AI - Page 6: Dataset & Methods
Comprehensive methodological transparency, dataset citations, software version audit,
and clinical feature dictionary.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import json
import streamlit as st
import pandas as pd

from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Dataset & Methods — QuantumCure AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Case History")

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: baseline; gap: 10px;">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #25324A;">Dataset & Methodology</h1>
        <span class="badge-neutral" style="font-size: 0.8rem;">Provenance & Protocol</span>
    </div>
    <p style="margin-top: 4px; font-size: 0.95rem; color: #64748B;">
        Comprehensive documentation of clinical data sources, preprocessing transformations, and experimental parameters.
    </p>
</div>
""", unsafe_allow_html=True)

# Load data audit and feature dictionary
res_dir = Path("results")
proc_dir = Path("dataset/processed")
audit_file = res_dir / "data_audit.json"
dict_file = proc_dir / "feature_dictionary.json"
config_file = res_dir / "experiment_config.json"

audit_data = {}
if audit_file.exists():
    with open(audit_file, "r") as f:
        audit_data = json.load(f)

feat_dict = {}
if dict_file.exists():
    with open(dict_file, "r") as f:
        feat_dict = json.load(f)

# Grid Layout: Overview Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Patients", f"{audit_data.get('records_count', 1058)} Records")
with c2:
    st.metric("Usable Predictive Features", "5 Clinical Features")
with c3:
    st.metric("Held-Out Test Cohort", "212 Patients (20%)")
with c4:
    st.metric("Primary Benchmark", "100 Train / 212 Test")

# Methodology Details
st.markdown("### Clinical Dataset Metadata & Licensing")
st.markdown("""
<div class="qc-card">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 0.88rem;">
        <div>
            <strong>Dataset Name:</strong> BCNB (Breast Cancer Nodal / Biopsy Clinical Dataset)<br>
            <strong>Primary Repository:</strong> The Cancer Imaging Archive (TCIA) / Nature Scientific Data<br>
            <strong>License:</strong> Creative Commons Attribution 4.0 International (CC BY 4.0)<br>
            <strong>Target Variable:</strong> Axillary Lymph Node Status (<code>ALN status</code>)
        </div>
        <div>
            <strong>Class 0 (Negative):</strong> N0 (655 patients, 61.91%)<br>
            <strong>Class 1 (Positive):</strong> N+(1-2) and N+(>2) (403 patients, 38.09%)<br>
            <strong>Target Leakage Mitigation:</strong> Strictly excluded <code>Number of lymph node metastases</code><br>
            <strong>Partition Protocol:</strong> Patient-level Stratified Split (Seed = 42)
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Dictionary Table
st.markdown("### Selected Predictor Feature Dictionary")
table_data = []
for fname, meta in feat_dict.items():
    table_data.append({
        "Feature Name": fname,
        "Variable Type": meta["type"],
        "Clinical Units": meta["units"],
        "Description": meta["description"],
        "Oncological Significance": meta["clinical_significance"]
    })
st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

# Software Version & Dependency Environment
st.markdown("### Computational Environment & Software Versions")
st.markdown("""
<div class="qc-card">
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; font-size: 0.85rem; color: #25324A;">
        <div>
            • <strong>Python Version:</strong> 3.13.5<br>
            • <strong>Qiskit Framework:</strong> 2.1.2<br>
            • <strong>Qiskit Machine Learning:</strong> 0.9.1
        </div>
        <div>
            • <strong>scikit-learn:</strong> 1.8.0<br>
            • <strong>XGBoost:</strong> 3.4.1<br>
            • <strong>Streamlit:</strong> 1.45+
        </div>
        <div>
            • <strong>Quantum Circuit:</strong> ZZFeatureMap (5 Qubits)<br>
            • <strong>Fidelity Engine:</strong> Exact Statevector Simulation<br>
            • <strong>Imputation:</strong> Training-fold Median
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Known Limitations
st.markdown("### Known Scientific & Methodological Limitations")
st.markdown("""
<div class="qc-card" style="font-size: 0.85rem; color: #64748B; line-height: 1.6;">
    1. <strong>Single-Center Clinical Cohort:</strong> BCNB originated from a single major medical center. External geographic generalizability remains unverified.<br>
    2. <strong>Tabular Predictor Subset:</strong> This clinical tabular prototype utilizes clinicopathological indices. Full multi-modal integration with whole-slide histopathology and radiological imaging is reserved for subsequent versions.<br>
    3. <strong>NISQ Feature Mapping:</strong> Fixed ZZ feature maps without variational quantum parameter optimization were tested; trainability and barren plateau analysis for higher-depth ansatzes represent active research areas.
</div>
""", unsafe_allow_html=True)
