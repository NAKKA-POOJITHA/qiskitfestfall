"""
QuantumCure AI - Page 10: Multi-Cancer Research Registry
Full implementation of Master Prompt Part 16:
- Extensible cancer research task registry
- Initial task: BCNB Breast Cancer Axillary Lymph Node Metastasis (Active, Verified, Trained)
- Future tasks: TCGA-LUAD Lung Adenocarcinoma, TCGA-COAD Colorectal MSI (Strictly marked as 'Planned')
- Task-specific schemas, targets, and datasets preventing model reuse cross-cancer
- Strict No-Emoji policy
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Multi-Cancer Registry — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Multi-Cancer Registry")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Multi-Cancer Research Registry
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Extensible multi-task oncology registry. Each cancer challenge operates with its own verified dataset, biological target, and trained models.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Strategic Scientific Integrity Notice
st.markdown("""
<div style="background: #F0EDFF; border: 1px solid #D8D1F8; border-left: 4px solid #7965E8; border-radius: 10px; padding: 10px 16px; margin-bottom: 1.25rem; font-size: 0.82rem; color: #25324A; line-height: 1.5;">
    <strong>Task Separation Protocol:</strong> In accordance with scientific integrity rules (Master Prompt Part 16), models trained on breast cancer clinicopathological markers (BCNB) are never reused for other tumor types.
    Prospective cancer tasks are clearly marked as <strong>Planned</strong> until independent raw data, labels, and retraining pipelines are validated.
</div>
""", unsafe_allow_html=True)

# Registry Cards
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="ref-dashboard-card" style="border-top: 3px solid #18A999; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #25324A; font-size: 1rem;">Breast Cancer (BCNB)</strong>
            <span class="status-pill-released" style="background:#E7F8F5; color:#18A999;">ACTIVE / VERIFIED</span>
        </div>
        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 12px; line-height: 1.6;">
            <strong>Target:</strong> Axillary Lymph Node Metastasis (N0 vs N+)<br>
            <strong>Cohort:</strong> 1,058 Real Patients (846 Train / 212 Test)<br>
            <strong>Features:</strong> 5 Clinicopathological Biomarkers<br>
            <strong>Models:</strong> RBF-SVM, XGBoost, Qiskit ZZFeatureMap SVM<br>
            <strong>Best Model:</strong> XGBoost (AUROC: 0.6012)
        </div>
        <div style="font-size: 0.76rem; color: #0F8275; background: #E7F8F5; padding: 8px 10px; border-radius: 8px;">
            Active deployed task with live inference and complete audit trail.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="ref-dashboard-card" style="border-top: 3px solid #F08A78; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #25324A; font-size: 1rem;">Lung Cancer (TCGA-LUAD)</strong>
            <span class="status-pill-released" style="background:#FEF3C7; color:#B45309;">PLANNED</span>
        </div>
        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 12px; line-height: 1.6;">
            <strong>Target:</strong> <em>EGFR</em> / <em>KRAS</em> Oncogenic Driver Mutation<br>
            <strong>Cohort:</strong> Genomic RNA-Seq & Clinical Follow-up<br>
            <strong>Features:</strong> High-dimensional Transcriptomic Vectors<br>
            <strong>Models:</strong> Awaiting Task Ingestion Pipeline<br>
            <strong>Quantum Approach:</strong> Projected Quantum Kernel (PQK)
        </div>
        <div style="font-size: 0.76rem; color: #B45309; background: #FFFBEB; padding: 8px 10px; border-radius: 8px;">
            Awaiting raw TCGA GDC genomic ingestion. No trained models exist for this task.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="ref-dashboard-card" style="border-top: 3px solid #7965E8; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #25324A; font-size: 1rem;">Colorectal Cancer (TCGA-COAD)</strong>
            <span class="status-pill-released" style="background:#FEF3C7; color:#B45309;">PLANNED</span>
        </div>
        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 12px; line-height: 1.6;">
            <strong>Target:</strong> Microsatellite Instability (MSI-H vs MSS)<br>
            <strong>Cohort:</strong> Histopathology Whole Slide Images & RNA-Seq<br>
            <strong>Features:</strong> Multi-modal Feature Embeddings<br>
            <strong>Models:</strong> In Architecture Planning<br>
            <strong>Quantum Approach:</strong> Quantum Convolutional Neural Network
        </div>
        <div style="font-size: 0.76rem; color: #B45309; background: #FFFBEB; padding: 8px 10px; border-radius: 8px;">
            Roadmap milestone for multi-modal quantum classification. Currently non-active.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Technical Task Specification Table
st.markdown("### Cancer Research Task Specifications")
tasks_spec = [
    {
        "Cancer Domain": "Breast (BCNB)",
        "Biological Target": "Axillary Nodal Metastasis (ALN)",
        "Feature Space": "5 Tabular Biomarkers",
        "Sample Size": "1,058 Biopsies",
        "Algorithm Family": "ZZFeatureMap QSVM vs RBF vs XGB",
        "Implementation Status": "Active & Verified"
    },
    {
        "Cancer Domain": "Lung (TCGA-LUAD)",
        "Biological Target": "Somatic Driver Mutations (EGFR/KRAS)",
        "Feature Space": "Transcriptomic Gene Counts",
        "Sample Size": "585 Patients (TCGA)",
        "Algorithm Family": "Dimension-reduced Quantum PCA + QSVM",
        "Implementation Status": "Planned (Awaiting Data)"
    },
    {
        "Cancer Domain": "Colorectal (TCGA-COAD)",
        "Biological Target": "Mismatch Repair Defect (MSI)",
        "Feature Space": "WSI Patch Features + RNA",
        "Sample Size": "458 Patients (TCGA)",
        "Algorithm Family": "Quantum Graph Neural Network",
        "Implementation Status": "Planned (Research Proposal)"
    }
]

st.dataframe(pd.DataFrame(tasks_spec), use_container_width=True, hide_index=True)
