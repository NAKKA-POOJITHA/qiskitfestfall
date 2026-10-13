"""
QuantumCure AI - Page 7: Reports & Analytics
Export centre allowing download of real metrics CSV, predictions CSV, JSON summaries,
and scientific high-resolution ROC and confusion matrix visualizations.
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
    page_title="Reports & Analytics — QuantumCure AI",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Export")

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: baseline; gap: 10px;">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #25324A;">Reports & Analytics Export</h1>
        <span class="badge-neutral" style="font-size: 0.8rem;">Data & Artifact Exports</span>
    </div>
    <p style="margin-top: 4px; font-size: 0.95rem; color: #64748B;">
        Review comprehensive experimental outputs and download genuine verified research artifacts.
    </p>
</div>
""", unsafe_allow_html=True)

res_dir = Path("results")
metrics_csv = res_dir / "metrics.csv"
metrics_json = res_dir / "metrics.json"
preds_csv = res_dir / "predictions.csv"
roc_png = res_dir / "roc_curves.png"
cm_png = res_dir / "confusion_matrices.png"
audit_md = res_dir / "data_audit_report.md"
config_json = res_dir / "experiment_config.json"

# Section 1: Benchmark Table
st.markdown("### Model Benchmark Comparison Table")
if metrics_csv.exists():
    df_metrics = pd.read_csv(metrics_csv)
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)
else:
    st.warning("No saved metrics found.")

st.markdown("---")

# Section 2: Direct Download Action Centre
st.markdown("### Export Artifacts")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="qc-card">
        <h4 style="margin: 0 0 6px 0; color: #25324A;">Tabular Metrics (CSV)</h4>
        <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">Held-out evaluation metrics across all 3 models.</p>
    </div>
    """, unsafe_allow_html=True)
    if metrics_csv.exists():
        with open(metrics_csv, "rb") as f:
            st.download_button("📥 Download metrics.csv", data=f, file_name="quantumcure_metrics.csv", mime="text/csv")

with c2:
    st.markdown("""
    <div class="qc-card">
        <h4 style="margin: 0 0 6px 0; color: #25324A;">Patient Predictions (CSV)</h4>
        <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">Patient-level held-out predictions & scores.</p>
    </div>
    """, unsafe_allow_html=True)
    if preds_csv.exists():
        with open(preds_csv, "rb") as f:
            st.download_button("📥 Download predictions.csv", data=f, file_name="quantumcure_predictions.csv", mime="text/csv")

with c3:
    st.markdown("""
    <div class="qc-card">
        <h4 style="margin: 0 0 6px 0; color: #25324A;">Experiment Summary (JSON)</h4>
        <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">Machine-readable metrics and metadata.</p>
    </div>
    """, unsafe_allow_html=True)
    if metrics_json.exists():
        with open(metrics_json, "rb") as f:
            st.download_button("📥 Download metrics.json", data=f, file_name="quantumcure_metrics.json", mime="application/json")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Image Downloads
c4, c5 = st.columns(2)
with c4:
    if roc_png.exists():
        st.markdown("#### High-Resolution ROC Curves")
        st.image(str(roc_png), use_container_width=True)
        with open(roc_png, "rb") as f:
            st.download_button("📥 Download ROC Plot (PNG)", data=f, file_name="quantumcure_roc_curves.png", mime="image/png")

with c5:
    if cm_png.exists():
        st.markdown("#### Confusion Matrix Diagnostic Breakdown")
        st.image(str(cm_png), use_container_width=True)
        with open(cm_png, "rb") as f:
            st.download_button("📥 Download Confusion Matrix (PNG)", data=f, file_name="quantumcure_confusion_matrices.png", mime="image/png")

# Audit Report Viewer
st.markdown("---")
st.markdown("### Clinical Dataset Audit Report Viewer")
if audit_md.exists():
    with open(audit_md, "r", encoding="utf-8") as f:
        audit_content = f.read()
    with st.expander("📄 View Full Data Audit Report (Markdown)", expanded=False):
        st.markdown(audit_content)
