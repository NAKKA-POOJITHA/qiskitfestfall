"""
QuantumCure AI - Reference UI Dashboard View
Faithfully reproduces the top search/profile bar, 4 KPI cards,
stacked pill analytics chart, circular demographics donut, and medical statistics table from Image 1.
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar
from frontend.components.metric_cards import render_metric_cards
from frontend.components.charts import (
    create_pill_stacked_analytics_chart,
    create_circular_cohort_chart,
    create_interactive_roc_curves,
    create_auroc_bar_chart
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
    """Renders the dashboard replicating Reference Image 1."""
    apply_light_theme(st)
    render_sidebar()

    # Top Header Bar matching Image 1
    st.markdown("""
    <div class="top-header-bar">
        <div class="search-pill-container">
            <span style="color: #94A3B8; margin-right: 8px;">🔍</span>
            <input type="text" placeholder="Search patient or feature..." style="border: none; outline: none; width: 100%; font-size: 0.88rem; color: #1E293B;">
            <span style="color: #64748B; cursor: pointer; font-size: 14px;">⚙️</span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="action-icon-pill">
                <span>✉️</span>
            </div>
            <div class="action-icon-pill" style="position: relative;">
                <span>🔔</span>
                <span style="position: absolute; top: 6px; right: 8px; width: 8px; height: 8px; background: #EF4444; border-radius: 50%;"></span>
            </div>
            <div class="user-profile-pill">
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" style="width: 30px; height: 30px; border-radius: 50%; object-fit: cover;">
                <div style="font-size: 0.82rem; line-height: 1.2;">
                    <strong style="color: #1E293B; display: block;">Dr. Sarah Mitchell</strong>
                    <span style="color: #64748B; font-size: 0.75rem;">@mitchell.oncology</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Page Title Row matching Image 1
    st.markdown("""
    <div class="page-title-row">
        <div>
            <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #1E293B; letter-spacing: -0.02em;">
                Dashboard
            </h1>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748B;">
                Clinical oncology analytics, patient cases, and quantum machine learning metrics.
            </p>
        </div>
        <button class="btn-summary-ai" onclick="window.location.reload();">
            <span>✨</span> Summary With AI
        </button>
    </div>
    """, unsafe_allow_html=True)

    # Load saved metrics and predictions
    data = load_saved_results()
    metrics_list = data["metrics_list"]
    preds_df = data["preds_df"]

    # 1. Row of 4 KPI Metric Cards (Image 1 top row)
    render_metric_cards(metrics_list)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # 2. Middle Row: Stacked Pill Chart (Left) & Circular Donut (Right)
    col_analytics, col_demographics = st.columns([1.75, 1])

    with col_analytics:
        st.markdown("""
        <div class="ref-dashboard-card">
            <div class="ref-card-header">
                <div>
                    <h3 class="ref-card-title">AI Healthcare Department Analytics</h3>
                    <div class="ref-card-subtitle">AI insights on patient volume, treatment performance</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span class="pill-filter-btn">⚙️ Filter</span>
                    <span class="pill-filter-btn">Last Month ▾</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        fig_stacked = create_pill_stacked_analytics_chart()
        st.plotly_chart(fig_stacked, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_demographics:
        st.markdown("""
        <div class="ref-dashboard-card" style="position: relative;">
            <div class="ref-card-header">
                <div>
                    <h3 class="ref-card-title">Patients Gender</h3>
                    <div class="ref-card-subtitle">Cohort Demographics Breakdown</div>
                </div>
                <span style="cursor: pointer; color: #64748B;">📅</span>
            </div>
            <div style="position: absolute; top: 88px; left: 24px; z-index: 5;">
                <span style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 9999px; padding: 4px 12px; font-size: 0.74rem; font-weight: 600; color: #475569; box-shadow: 0 2px 6px rgba(0,0,0,0.05); cursor: pointer;">
                    Learn More →
                </span>
            </div>
        """, unsafe_allow_html=True)
        fig_circular = create_circular_cohort_chart()
        st.plotly_chart(fig_circular, use_container_width=True)
        st.markdown("""
            <div style="display: flex; justify-content: space-around; text-align: center; font-size: 0.8rem; margin-top: -12px; border-top: 1px solid #F1F5F9; padding-top: 10px;">
                <div><strong style="color: #7C3AED; font-size: 1rem;">73%</strong><br><span style="color: #64748B; font-size: 0.76rem;">Male</span></div>
                <div><strong style="color: #6D28D9; font-size: 1rem;">53%</strong><br><span style="color: #64748B; font-size: 0.76rem;">Female</span></div>
                <div><strong style="color: #475569; font-size: 1rem;">27%</strong><br><span style="color: #64748B; font-size: 0.76rem;">Other</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3. Diagnostic ROC & Benchmark Section
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h3 class="ref-card-title">Quantum vs Classical Model Discrimination</h3>
                <div class="ref-card-subtitle">Held-out test cohort ROC curves and AUROC ranking</div>
            </div>
            <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
                <span class="pill-filter-btn">Explore Circuit & Heatmap →</span>
            </a>
        </div>
    """, unsafe_allow_html=True)
    c_roc, c_bar = st.columns([1.2, 0.8])
    with c_roc:
        if preds_df is not None:
            fig_roc = create_interactive_roc_curves(preds_df)
            st.plotly_chart(fig_roc, use_container_width=True)
    with c_bar:
        if metrics_list:
            fig_bar = create_auroc_bar_chart(metrics_list)
            st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 4. Bottom Row: Medical Department Statistics Table matching Image 1
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h3 class="ref-card-title">Medical Department Statistics</h3>
                <div class="ref-card-subtitle">Patient volume, treatment progress, status, and critical cases.</div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <div style="display: flex; align-items: center; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 9999px; padding: 6px 14px; font-size: 0.82rem;">
                    <span style="color: #94A3B8; margin-right: 6px;">🔍</span>
                    <input type="text" placeholder="Search Data" style="border: none; background: transparent; outline: none; width: 120px; font-size: 0.8rem;">
                </div>
                <span class="pill-filter-btn">⚙️</span>
                <span class="pill-filter-btn">Export Data ▾</span>
            </div>
        </div>
        <table class="ref-patient-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Department</th>
                    <th>Length Stay</th>
                    <th>Cabin No</th>
                    <th>Admission Date</th>
                    <th>Status</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr class="ref-patient-row">
                    <td>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">
                            <div>
                                <strong style="color: #1E293B;">Sarah Mitchell</strong><br>
                                <span style="font-size: 0.75rem; color: #64748B;">Persistent cough</span>
                            </div>
                        </div>
                    </td>
                    <td>Cardiology</td>
                    <td>3 Weeks</td>
                    <td>CF-315</td>
                    <td>22/03/2026</td>
                    <td><span class="status-pill-released">Released</span></td>
                    <td style="color: #94A3B8; font-weight: bold; cursor: pointer;">⋮</td>
                </tr>
                <tr class="ref-patient-row">
                    <td>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">
                            <div>
                                <strong style="color: #1E293B;">Patient #212 (Elena Rostova)</strong><br>
                                <span style="font-size: 0.75rem; color: #64748B;">Tumour 3.5cm / Grade 3</span>
                            </div>
                        </div>
                    </td>
                    <td>Oncology / Axillary</td>
                    <td>2 Weeks</td>
                    <td>ON-108</td>
                    <td>14/03/2026</td>
                    <td><span class="status-pill-positive">N+ Metastasis</span></td>
                    <td style="color: #94A3B8; font-weight: bold; cursor: pointer;">⋮</td>
                </tr>
                <tr class="ref-patient-row">
                    <td>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">
                            <div>
                                <strong style="color: #1E293B;">Patient #389 (David Chen)</strong><br>
                                <span style="font-size: 0.75rem; color: #64748B;">Tumour 1.8cm / Grade 2</span>
                            </div>
                        </div>
                    </td>
                    <td>Surgical Staging</td>
                    <td>1 Week</td>
                    <td>ST-204</td>
                    <td>19/03/2026</td>
                    <td><span class="status-pill-negative">N0 Negative</span></td>
                    <td style="color: #94A3B8; font-weight: bold; cursor: pointer;">⋮</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
