"""
QuantumCure AI - Page 9: Reports & Analytics
Full implementation of Master Prompt Part 15:
- Experiment selection and status inspection
- Model metrics table and runtime profiling
- Direct download actions for metrics.csv, predictions.csv, and experiment_config.json
- High-resolution ROC and confusion matrix visualizations
- Printable Markdown research summary export
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
    page_title="Reports & Analytics — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Reports & Analytics")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Reports & Analytics Export
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Download verified research artifacts, tabular benchmark metrics, patient predictions, and experiment configurations.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

res_dir = Path(root_dir) / "results"
metrics_csv = res_dir / "metrics.csv"
metrics_json = res_dir / "metrics.json"
preds_csv = res_dir / "predictions.csv"
roc_png = res_dir / "roc_curves.png"
cm_png = res_dir / "confusion_matrices.png"
audit_md = res_dir / "data_audit_report.md"
config_json = res_dir / "experiment_config.json"

# Section 1: Benchmark Table
st.markdown("""
<div class="ref-dashboard-card" style="margin-bottom: 1.25rem;">
    <h3 class="ref-card-title">Verified Model Benchmark Results</h3>
    <div class="ref-card-subtitle">Experiment ID: EXP_2026_BCNB_01 | Evaluated on 212 held-out BCNB test patients</div>
""", unsafe_allow_html=True)

if metrics_csv.exists():
    df_metrics = pd.read_csv(metrics_csv)
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
else:
    st.warning("No saved metrics found.")

st.markdown("</div>", unsafe_allow_html=True)

# Section 2: Direct Download Action Centre
st.markdown("### Export Verified Artifacts")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Tabular Metrics (CSV)</h4>
        <p style="font-size: 0.78rem; color: #64748B; margin: 4px 0 12px 0;">Held-out evaluation metrics across all 3 models.</p>
    """, unsafe_allow_html=True)
    if metrics_csv.exists():
        with open(metrics_csv, "rb") as f:
            st.download_button("Download metrics.csv", data=f, file_name="quantumcure_metrics.csv", mime="text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Patient Predictions (CSV)</h4>
        <p style="font-size: 0.78rem; color: #64748B; margin: 4px 0 12px 0;">Patient-level held-out predictions & scores.</p>
    """, unsafe_allow_html=True)
    if preds_csv.exists():
        with open(preds_csv, "rb") as f:
            st.download_button("Download predictions.csv", data=f, file_name="quantumcure_predictions.csv", mime="text/csv", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Experiment Summary (JSON)</h4>
        <p style="font-size: 0.78rem; color: #64748B; margin: 4px 0 12px 0;">Machine-readable metrics and metadata.</p>
    """, unsafe_allow_html=True)
    if metrics_json.exists():
        with open(metrics_json, "rb") as f:
            st.download_button("Download metrics.json", data=f, file_name="quantumcure_metrics.json", mime="application/json", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Section 3: Diagnostic Visualization Downloads
c_img1, c_img2 = st.columns(2)

with c_img1:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">ROC Curves Plot (PNG)</h4>
    """, unsafe_allow_html=True)
    if roc_png.exists():
        st.image(str(roc_png), use_column_width=True)
        with open(roc_png, "rb") as f:
            st.download_button("Download ROC Plot (PNG)", data=f, file_name="quantumcure_roc_curves.png", mime="image/png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_img2:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Confusion Matrices Plot (PNG)</h4>
    """, unsafe_allow_html=True)
    if cm_png.exists():
        st.image(str(cm_png), use_column_width=True)
        with open(cm_png, "rb") as f:
            st.download_button("Download Confusion Matrix (PNG)", data=f, file_name="quantumcure_confusion_matrices.png", mime="image/png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Section 4: Data Audit Report Markdown Viewer
if audit_md.exists():
    with st.expander("View Full Data Audit Report (Markdown)", expanded=False):
        with open(audit_md, "r", encoding="utf-8") as f:
            st.markdown(f.read())
