"""
QuantumCure AI - Research Dashboard View
Complies with Master Prompt Parts 2 & 6:
- Strict Light Theme with specified palette
- Prominent Research Prototype Disclaimer
- Zero emojis across the entire page
- Replaces unrelated hospital statistics with verified BCNB cancer research data:
  1. 4 Verified KPI metric cards (1,058 BCNB Cohort, Quantum SVM, Classical RBF-SVM, XGBoost)
  2. Diagnostic ROC Curves & AUROC Rankings on held-out test cohort
  3. BCNB Cohort Nodal Status Distribution & Computational Cost Comparison
  4. Real Held-Out Test Patient Evaluation Table (Patient IDs, true status, multi-model outputs)
"""

import json
from pathlib import Path
import streamlit as st
import pandas as pd

from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar
from frontend.components.metric_cards import render_metric_cards
from frontend.components.charts import (
    create_bcnb_class_distribution_chart,
    create_interactive_roc_curves,
    create_auroc_bar_chart,
    create_runtime_comparison_chart
)


def load_saved_results(results_dir="results"):
    """Loads saved metrics, predictions, and configurations."""
    res_path = Path(results_dir)
    metrics_file = res_path / "metrics.json"
    preds_file = res_path / "predictions.csv"
    config_file = res_path / "experiment_config.json"

    metrics_list = None
    preds_df = None
    config = None

    if metrics_file.exists():
        try:
            with open(metrics_file, "r", encoding="utf-8") as f:
                metrics_list = json.load(f)
        except Exception:
            pass

    if preds_file.exists():
        try:
            preds_df = pd.read_csv(preds_file)
        except Exception:
            pass

    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    return {
        "metrics_list": metrics_list,
        "preds_df": preds_df,
        "config": config
    }


def render_research_dashboard():
    """Renders the scientifically rigorous medical AI research dashboard."""
    apply_light_theme(st)
    render_sidebar(active_tab="Dashboard")

    # Mandatory Prominent Clinical Disclaimer
    render_disclaimer_banner(st)

    # Top Header Bar (clean SVGs, zero emojis)
    st.markdown("""
    <div class="top-header-bar">
        <div class="search-pill-container">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" placeholder="Search patient ID or biomarker..." style="border: none; outline: none; width: 100%; font-size: 0.86rem; color: #25324A; background: transparent;">
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <a href="/Patient_Prediction_Lab" target="_self" style="text-decoration: none;">
                <div class="action-icon-pill" title="Prediction Lab">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2v6a2 2 0 0 0 2 2h6"></path>
                        <path d="M4 15V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1"></path>
                    </svg>
                </div>
            </a>
            <a href="/Model_Comparison_Lab" target="_self" style="text-decoration: none;">
                <div class="action-icon-pill" title="Model Comparison">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="20" x2="18" y2="10"></line>
                        <line x1="12" y1="20" x2="12" y2="4"></line>
                        <line x1="6" y1="20" x2="6" y2="14"></line>
                    </svg>
                </div>
            </a>
            <div class="user-profile-pill">
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #F0EDFF; color: #7965E8; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.78rem;">
                    QC
                </div>
                <div style="font-size: 0.82rem; line-height: 1.2;">
                    <strong style="color: #25324A; display: block;">QuantumCure Research</strong>
                    <span style="color: #64748B; font-size: 0.74rem;">BCNB Oncology Task</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Page Title Row
    st.markdown("""
    <div class="page-title-row">
        <div>
            <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
                Research Dashboard
            </h1>
            <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
                Axillary lymph node metastasis prediction: Quantum Kernel SVM vs Classical RBF-SVM and XGBoost.
            </p>
        </div>
        <div style="display: flex; gap: 10px;">
            <a href="/Patient_Prediction_Lab" target="_self" style="text-decoration: none;">
                <button class="btn-summary-ai">
                    <span>Patient Prediction Lab →</span>
                </button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load saved metrics and predictions
    data = load_saved_results()
    metrics_list = data["metrics_list"]
    preds_df = data["preds_df"]

    # 1. Row of 4 KPI Metric Cards
    render_metric_cards(metrics_list)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 2. Middle Row: Diagnostic ROC Curves (Left) & AUROC Ranking (Right)
    col_roc, col_bar = st.columns([1.5, 1])

    with col_roc:
        st.markdown("""
        <div class="ref-dashboard-card">
            <div class="ref-card-header">
                <div>
                    <h3 class="ref-card-title">Model Discrimination Performance</h3>
                    <div class="ref-card-subtitle">Overlaid ROC curves evaluated on 212 held-out BCNB patients</div>
                </div>
                <a href="/Model_Comparison_Lab" target="_self" style="text-decoration: none;">
                    <span class="pill-filter-btn">Full Comparison Lab →</span>
                </a>
            </div>
        """, unsafe_allow_html=True)
        if preds_df is not None:
            fig_roc = create_interactive_roc_curves(preds_df)
            st.plotly_chart(fig_roc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bar:
        st.markdown("""
        <div class="ref-dashboard-card">
            <div class="ref-card-header">
                <div>
                    <h3 class="ref-card-title">AUROC Ranking</h3>
                    <div class="ref-card-subtitle">Discriminative power comparison</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if metrics_list:
            fig_bar = create_auroc_bar_chart(metrics_list)
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3. Third Row: BCNB Class Distribution & Computational Latency
    col_cohort, col_latency = st.columns([1, 1.3])

    with col_cohort:
        st.markdown("""
        <div class="ref-dashboard-card">
            <div class="ref-card-header">
                <div>
                    <h3 class="ref-card-title">BCNB Cohort Nodal Status</h3>
                    <div class="ref-card-subtitle">1,058 Verified Clinical Biopsies</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig_donut = create_bcnb_class_distribution_chart()
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_latency:
        st.markdown("""
        <div class="ref-dashboard-card">
            <div class="ref-card-header">
                <div>
                    <h3 class="ref-card-title">Computational Latency & Runtime</h3>
                    <div class="ref-card-subtitle">Training time and per-patient inference latency</div>
                </div>
                <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
                    <span class="pill-filter-btn">Quantum Heatmap →</span>
                </a>
            </div>
        """, unsafe_allow_html=True)
        if metrics_list:
            fig_runtime = create_runtime_comparison_chart(metrics_list)
            st.plotly_chart(fig_runtime, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 4. Bottom Row: Verified Held-Out Test Cohort Patient Table (Scientific Integrity)
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h3 class="ref-card-title">Held-Out Test Cohort Predictions (Sample of 10 Patients)</h3>
                <div class="ref-card-subtitle">True pathological lymph node status vs Multi-Model predictions</div>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="/Patient_Prediction_Lab" target="_self" style="text-decoration: none;">
                    <span class="pill-filter-btn">Run Blind Patient Evaluation →</span>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if preds_df is not None:
        sample_df = preds_df.head(10).copy()

        table_html = """
        <table class="ref-patient-table">
            <thead>
                <tr>
                    <th>Patient ID</th>
                    <th>Actual ALN Status</th>
                    <th>Quantum SVM Output</th>
                    <th>Classical RBF-SVM</th>
                    <th>XGBoost</th>
                    <th>Model Consensus</th>
                </tr>
            </thead>
            <tbody>
        """

        for _, row in sample_df.iterrows():
            pid = int(row["Patient ID"])
            gt_class = str(row["Ground Truth Class"])
            q_class = str(row["Quantum_kernel_SVM_Class"])
            q_score = float(row["Quantum_kernel_SVM_Score"])
            c_class = str(row["Classical_RBF_SVM_Class"])
            c_score = float(row["Classical_RBF_SVM_Score"])
            x_class = str(row["XGBoost_Class"])
            x_score = float(row["XGBoost_Score"])

            # Consensus logic
            preds = [q_class, c_class, x_class]
            if preds.count("N+") == 3 or preds.count("N0") == 3:
                consensus_pill = '<span class="status-pill-released" style="background:#E7F8F5; color:#18A999;">Unanimous</span>'
            else:
                consensus_pill = '<span class="status-pill-released" style="background:#FEF3C7; color:#B45309;">Majority (2 vs 1)</span>'

            gt_pill = '<span class="status-pill-positive">N+ Metastasis</span>' if gt_class == "N+" else '<span class="status-pill-negative">N0 Negative</span>'

            table_html += f"""
            <tr class="ref-patient-row">
                <td><strong style="color: #25324A;">Patient #{pid}</strong></td>
                <td>{gt_pill}</td>
                <td><span style="color: #7965E8; font-weight: 700;">{q_class}</span> <span style="font-size: 0.75rem; color: #64748B;">({q_score:.3f})</span></td>
                <td><span style="color: #18A999; font-weight: 700;">{c_class}</span> <span style="font-size: 0.75rem; color: #64748B;">({c_score:.3f})</span></td>
                <td><span style="color: #F08A78; font-weight: 700;">{x_class}</span> <span style="font-size: 0.75rem; color: #64748B;">({x_score:.3f})</span></td>
                <td>{consensus_pill}</td>
            </tr>
            """

        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
