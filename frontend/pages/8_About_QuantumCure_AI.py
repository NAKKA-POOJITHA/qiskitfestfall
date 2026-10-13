"""
QuantumCure AI - Page 8: About QuantumCure AI & Multi-Cancer Roadmap
Strategic vision, multi-cancer expansion roadmap, system architecture, and clinical ethics.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="About QuantumCure AI — Multi-Cancer Roadmap",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar()

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: baseline; gap: 10px;">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #25324A;">About QuantumCure AI</h1>
        <span class="badge-quantum" style="font-size: 0.8rem;">Multi-Cancer Vision</span>
    </div>
    <p style="margin-top: 4px; font-size: 0.95rem; color: #64748B;">
        Investigating quantum kernel algorithms for precision oncology through empirical, reproducible benchmarking.
    </p>
</div>
""", unsafe_allow_html=True)

# Strategic Vision Card
st.markdown("""
<div class="qc-card">
    <h3 style="margin: 0 0 10px 0; color: #25324A; font-size: 1.2rem;">Project Vision & Architecture</h3>
    <p style="color: #64748B; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0;">
        QuantumCure AI was architected from first principles to bridge theoretical quantum machine learning algorithms with practical oncology research. 
        Rather than generating decorative quantum circuits or artificial metrics, the system implements end-to-end data audits, rigorous target leakage controls, 
        genuine Qiskit statevector phase simulations, and identical held-out test evaluations against industry-standard classical machine learning models.
    </p>
</div>
""", unsafe_allow_html=True)

# Multi-Cancer Roadmap
st.markdown("### Multi-Cancer Research Expansion Roadmap")
st.markdown("""
<p style="font-size: 0.85rem; color: #64748B; margin-bottom: 1rem;">
    Each cancer prediction challenge requires its own validated dataset, biological target formulation, and independently trained models. 
    Status tags reflect the strict current state of implementation.
</p>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="qc-card" style="border-top: 4px solid #18A999; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #25324A; font-size: 1rem;">Breast Cancer (BCNB)</strong>
            <span class="badge-classical">IMPLEMENTED</span>
        </div>
        <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 12px;">
            <strong>Target:</strong> Axillary Lymph Node Metastasis (N0 vs N+)<br>
            <strong>Cohort:</strong> 1,058 Real Patient Records<br>
            <strong>Features:</strong> 5 Clinicopathological Markers<br>
            <strong>Status:</strong> Trained, Verified, Deployed
        </div>
        <p style="font-size: 0.8rem; color: #10786C; background: #E7F8F5; padding: 6px 10px; border-radius: 6px; margin: 0;">
            Active working prototype running live Qiskit 2.1.2 ZZFeatureMap calculations.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="qc-card" style="border-top: 4px solid #F08A78; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #25324A; font-size: 1rem;">Lung Cancer (TCGA-LUAD)</strong>
            <span class="badge-xgboost">DATASET NEEDED</span>
        </div>
        <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 12px;">
            <strong>Target:</strong> <em>EGFR</em> / <em>KRAS</em> Mutation Status<br>
            <strong>Cohort:</strong> Genomic RNA-Seq & Clinical<br>
            <strong>Features:</strong> High-dimensional Expression Vectors<br>
            <strong>Status:</strong> Planned Next Phase
        </div>
        <p style="font-size: 0.8rem; color: #C2410C; background: #FFF0EC; padding: 6px 10px; border-radius: 6px; margin: 0;">
            Awaiting raw TCGA GDC data ingestion pipeline. No models currently exist for this task.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="qc-card" style="border-top: 4px solid #7965E8; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #25324A; font-size: 1rem;">Colorectal (TCGA-COAD)</strong>
            <span class="badge-quantum">PLANNED</span>
        </div>
        <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 12px;">
            <strong>Target:</strong> Microsatellite Instability (MSI-H vs MSS)<br>
            <strong>Cohort:</strong> Clinical + Molecular Staging<br>
            <strong>Features:</strong> DNA Mismatch Repair Panel<br>
            <strong>Status:</strong> Conceptual Design
        </div>
        <p style="font-size: 0.8rem; color: #563ED6; background: #F0EDFF; padding: 6px 10px; border-radius: 6px; margin: 0;">
            Future planned study into quantum kernels for genomic instability classification.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Ethical AI & Responsible Use Statement
st.markdown("### Ethical AI, Safety, and Governance")
st.markdown("""
<div class="clinical-disclaimer" style="font-size: 0.88rem; line-height: 1.6;">
    <strong>Mandatory Ethical Governance Framework:</strong><br>
    • <strong>No Unsubstantiated Quantum Supremacy Claims:</strong> We report measured performance accurately, including instances where classical models match or exceed quantum kernels.<br>
    • <strong>Privacy Preservation:</strong> Patient data is strictly anonymized; administrative identifiers are isolated from predictive feature sets.<br>
    • <strong>Non-Clinical Status:</strong> Machine learning predictions represent statistical associations and must not be used to direct medical intervention without institutional clinical review board approvals.
</div>
""", unsafe_allow_html=True)
