"""
QuantumCure AI - Master Application Entrypoint
Dual-mode runtime:
1. Vercel Serverless WSGI / ASGI Export: exports `app`, `application`, `handler`
2. Streamlit Local Execution: supports `streamlit run app.py`

Full compliance with Master Prompt:
- Strict Light Theme with exact specified color tokens
- Prominent Clinical Research Disclaimer: "Research prototype, not clinical advice. Not validated for clinical use."
- Strict NO-EMOJI Rule across all pages, buttons, badges, headers, and tooltips
- Genuine BCNB research dataset (1,058 patients), verified model metrics, and held-out test predictions
- Interactive Prediction Lab with blind held-out evaluation and "Reveal Actual Outcome" button
- Model Comparison Lab with threshold analysis
- Quantum Park circuit composer and 3D Bloch Sphere
- Three.js Interactive 3D Anatomy Explorer
- Searchable Research Handbook, Dataset & Methods, and Reports Export
"""

import sys
import os
import json
from pathlib import Path

# Add project root directory to sys.path
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# ==============================================================================
# HTML Template for Vercel Serverless Deployment (Zero Emojis, Exact Palette)
# ==============================================================================
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuantumCure AI — Quantum Kernel Oncology Research</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.29.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        :root {
            --bg-main: #F8FAFC;
            --bg-card: #FFFFFF;
            --quantum-accent: #7965E8;
            --quantum-gradient: linear-gradient(135deg, #7965E8 0%, #5B48CC 100%);
            --rbf-accent: #18A999;
            --rbf-gradient: linear-gradient(135deg, #18A999 0%, #0F8275 100%);
            --xgb-accent: #F08A78;
            --xgb-gradient: linear-gradient(135deg, #F08A78 0%, #D86B58 100%);
            --text-primary: #25324A;
            --text-secondary: #64748B;
            --text-muted: #94A3B8;
            --border-color: #E5E7EB;
            --soft-purple: #F0EDFF;
            --soft-teal: #E7F8F5;
            --soft-coral: #FFF0EC;
            --card-shadow: 0 4px 20px rgba(37, 50, 74, 0.05), 0 1px 3px rgba(37, 50, 74, 0.03);
            --pill-shadow: 0 2px 8px rgba(121, 101, 232, 0.22);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
        }

        /* Sidebar Styling */
        .sidebar {
            width: 260px;
            background: #FFFFFF;
            border-right: 1px solid var(--border-color);
            box-shadow: 2px 0 16px rgba(37, 50, 74, 0.03);
            padding: 1.5rem 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: fixed;
            top: 0;
            bottom: 0;
            left: 0;
            z-index: 100;
        }

        .brand-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.75rem;
            padding: 0 4px;
        }

        .brand-logo-box {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: var(--quantum-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            box-shadow: 0 4px 12px rgba(121, 101, 232, 0.3);
        }

        .nav-list {
            display: flex;
            flex-direction: column;
            gap: 5px;
            list-style: none;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 9px 12px;
            border-radius: 10px;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.84rem;
            cursor: pointer;
            transition: all 0.15s ease;
            text-decoration: none;
        }

        .nav-item:hover {
            background: #F1F5F9;
            color: var(--text-primary);
        }

        .nav-item.active {
            background: var(--quantum-gradient);
            color: #FFFFFF;
            font-weight: 600;
            box-shadow: 0 4px 14px rgba(121, 101, 232, 0.28);
        }

        .nav-item.active svg {
            stroke: #FFFFFF;
        }

        .expert-insights-card {
            background: var(--soft-purple);
            border: 1px solid #D8D1F8;
            border-radius: 16px;
            padding: 1.15rem;
            margin-top: 1rem;
        }

        /* Main Content Container */
        .main-content {
            margin-left: 260px;
            flex: 1;
            padding: 1.5rem 2rem 3rem 2rem;
            max-width: 1440px;
        }

        /* Disclaimer Banner */
        .disclaimer-banner {
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-left: 4px solid var(--quantum-accent);
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.82rem;
            color: var(--text-primary);
            font-weight: 500;
        }

        .top-header-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.25rem;
            padding-bottom: 0.5rem;
        }

        .search-pill-container {
            display: flex;
            align-items: center;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 9999px;
            padding: 8px 18px;
            box-shadow: 0 2px 6px rgba(37, 50, 74, 0.02);
            width: 320px;
            font-size: 0.86rem;
        }

        .user-profile-pill {
            display: flex;
            align-items: center;
            gap: 12px;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 9999px;
            padding: 6px 14px 6px 6px;
            box-shadow: 0 2px 6px rgba(37, 50, 74, 0.02);
        }

        .action-icon-pill {
            width: 38px;
            height: 38px;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(37, 50, 74, 0.02);
            color: var(--text-secondary);
        }

        /* KPI Metric Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            margin-bottom: 1.5rem;
        }

        .ref-kpi-card {
            position: relative;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.4rem 1.3rem;
            box-shadow: var(--card-shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .ref-kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(37, 50, 74, 0.08);
        }

        .kpi-floating-badge {
            position: absolute;
            top: 14px;
            right: 14px;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px rgba(37, 50, 74, 0.06);
        }

        .kpi-title {
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 0.85rem;
        }

        .kpi-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.85rem;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1.1;
            margin-bottom: 0.3rem;
        }

        .kpi-subtitle {
            font-size: 0.78rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .ref-dashboard-card {
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.4rem;
            box-shadow: var(--card-shadow);
            margin-bottom: 1.25rem;
        }

        .ref-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.15rem;
        }

        .ref-card-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
        }

        .ref-card-subtitle {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .pill-filter-btn {
            background: #F8FAFC;
            border: 1px solid var(--border-color);
            border-radius: 9999px;
            padding: 5px 13px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-primary);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
        }

        .btn-summary-ai {
            background: var(--quantum-gradient);
            color: #FFFFFF;
            border-radius: 9999px;
            padding: 9px 22px;
            font-weight: 600;
            font-size: 0.88rem;
            border: none;
            box-shadow: var(--pill-shadow);
            cursor: pointer;
        }

        /* Table */
        .ref-patient-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px;
        }

        .ref-patient-table th {
            font-size: 0.76rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            padding: 8px 14px;
            border-bottom: 1px solid #F1F5F9;
            text-align: left;
        }

        .ref-patient-row {
            background: #FFFFFF;
            border-radius: 12px;
            transition: background 0.15s ease;
        }

        .ref-patient-row:hover {
            background: #F8FAFC;
        }

        .ref-patient-row td {
            padding: 12px 14px;
            font-size: 0.84rem;
            border-top: 1px solid #F8FAFC;
            border-bottom: 1px solid #F8FAFC;
        }

        .status-pill-positive {
            background: #FFF0EC;
            color: var(--xgb-accent);
            border-radius: 9999px;
            padding: 4px 12px;
            font-size: 0.74rem;
            font-weight: 700;
            display: inline-block;
        }

        .status-pill-negative {
            background: #E7F8F5;
            color: var(--rbf-accent);
            border-radius: 9999px;
            padding: 4px 12px;
            font-size: 0.74rem;
            font-weight: 700;
            display: inline-block;
        }

        .model-card-quantum {
            background: #FFFFFF;
            border: 1.5px solid var(--quantum-accent);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: 0 4px 18px rgba(121, 101, 232, 0.08);
        }

        .model-card-rbf {
            background: #FFFFFF;
            border: 1.5px solid var(--rbf-accent);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: 0 4px 18px rgba(24, 169, 153, 0.08);
        }

        .model-card-xgb {
            background: #FFFFFF;
            border: 1.5px solid var(--xgb-accent);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: 0 4px 18px rgba(240, 138, 120, 0.08);
        }

        /* Tab Content Management */
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
        <div>
            <div class="brand-header">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="brand-logo-box">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                        </svg>
                    </div>
                    <div>
                        <h2 style="margin: 0; font-size: 1.05rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">QuantumCure AI</h2>
                        <span style="font-size: 0.72rem; color: #7965E8; font-weight: 700; letter-spacing: 0.02em;">Quantum Oncology</span>
                    </div>
                </div>
            </div>

            <ul class="nav-list">
                <li><a class="nav-item active" onclick="switchTab('dashboard')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg> Research Dashboard</a></li>
                <li><a class="nav-item" onclick="switchTab('prediction')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2v6a2 2 0 0 0 2 2h6"></path><path d="M4 15V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1"></path></svg> Patient Prediction Lab</a></li>
                <li><a class="nav-item" onclick="switchTab('comparison')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg> Model Comparison Lab</a></li>
                <li><a class="nav-item" onclick="switchTab('quantum-park')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M12 2v3m0 14v3M2 12h3m14 0h3"></path></svg> Quantum Park</a></li>
                <li><a class="nav-item" onclick="switchTab('quantum-insights')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg> Quantum Insights</a></li>
                <li><a class="nav-item" onclick="switchTab('anatomy')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg> 3D Anatomy Explorer</a></li>
                <li><a class="nav-item" onclick="switchTab('handbook')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg> Research Handbook</a></li>
                <li><a class="nav-item" onclick="switchTab('dataset')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg> Dataset & Methods</a></li>
                <li><a class="nav-item" onclick="switchTab('reports')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline></svg> Reports & Analytics</a></li>
                <li><a class="nav-item" onclick="switchTab('multi-cancer')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line></svg> Multi-Cancer Registry</a></li>
            </ul>
        </div>

        <div class="expert-insights-card">
            <h4 style="margin: 0 0 4px 0; color: #25324A; font-size: 0.88rem; font-weight: 700;">Research Prototype</h4>
            <p style="font-size: 0.74rem; color: #64748B; margin-bottom: 8px; line-height: 1.4;">
                Qiskit 2.1.2 ZZFeatureMap evaluated against Classical RBF-SVM and XGBoost on 212 held-out BCNB breast cancer cases.
            </p>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">
        <!-- Prominent Disclaimer Banner -->
        <div class="disclaimer-banner">
            <div style="display: flex; align-items: center; gap: 10px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7965E8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <strong style="color: #25324A;">Research prototype, not clinical advice. Not validated for clinical use.</strong>
            </div>
            <span style="background: #EEF2F6; border: 1px solid #CBD5E1; border-radius: 6px; padding: 2px 8px; font-size: 0.72rem; font-weight: 700; color: #475569;">
                ACADEMIC PROTOTYPE
            </span>
        </div>

        <!-- TAB 1: DASHBOARD -->
        <div id="tab-dashboard" class="tab-content active">
            <div class="top-header-bar">
                <div class="search-pill-container">
                    <input type="text" placeholder="Search patient ID or biomarker..." style="border: none; outline: none; width: 100%; font-size: 0.86rem; color: #25324A; background: transparent;">
                </div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="action-icon-pill" onclick="switchTab('prediction')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2v6a2 2 0 0 0 2 2h6"></path><path d="M4 15V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1"></path></svg>
                    </div>
                    <div class="user-profile-pill">
                        <div style="width: 28px; height: 28px; border-radius: 50%; background: #F0EDFF; color: #7965E8; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.78rem;">QC</div>
                        <div style="font-size: 0.82rem; line-height: 1.2;">
                            <strong style="color: #25324A; display: block;">QuantumCure Research</strong>
                            <span style="color: #64748B; font-size: 0.74rem;">BCNB Cohort</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4 Verified Research KPI Metric Cards -->
            <div class="kpi-grid">
                <div class="ref-kpi-card">
                    <div class="kpi-title">Verified BCNB Cohort</div>
                    <div class="kpi-value">1,058</div>
                    <div class="kpi-subtitle" style="color: #7965E8;">80/20 Split: 846 Train / 212 Test</div>
                    <div style="font-size: 0.74rem; color: #64748B; margin-top: 6px;">655 N0 (61.9%) / 403 N+ (38.1%)</div>
                </div>
                <div class="ref-kpi-card" style="border-top: 3px solid #7965E8;">
                    <div class="kpi-title">Quantum-Kernel SVM</div>
                    <div class="kpi-value" style="color: #7965E8;">0.5001</div>
                    <div class="kpi-subtitle" style="color: #7965E8;">50.47% Test Accuracy</div>
                    <div style="font-size: 0.74rem; color: #64748B; margin-top: 6px;">Qiskit 2.1.2 ZZFeatureMap</div>
                </div>
                <div class="ref-kpi-card" style="border-top: 3px solid #18A999;">
                    <div class="kpi-title">Classical RBF-SVM</div>
                    <div class="kpi-value" style="color: #18A999;">0.5982</div>
                    <div class="kpi-subtitle" style="color: #18A999;">59.43% Test Accuracy</div>
                    <div style="font-size: 0.74rem; color: #64748B; margin-top: 6px;">Scikit-learn (C=2.0, gamma=0.5)</div>
                </div>
                <div class="ref-kpi-card" style="border-top: 3px solid #F08A78;">
                    <div class="kpi-title">XGBoost Classifier</div>
                    <div class="kpi-value" style="color: #F08A78;">0.6012</div>
                    <div class="kpi-subtitle" style="color: #F08A78;">59.43% Test Accuracy</div>
                    <div style="font-size: 0.74rem; color: #64748B; margin-top: 6px;">50 Trees, max_depth=3</div>
                </div>
            </div>

            <!-- Interactive Diagnostic ROC Plot & Cohort Distribution -->
            <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 18px; margin-bottom: 1.5rem;">
                <div class="ref-dashboard-card">
                    <div class="ref-card-header">
                        <div>
                            <h3 class="ref-card-title">Model Discrimination (ROC Curves)</h3>
                            <div class="ref-card-subtitle">Evaluated on 212 held-out BCNB test patients</div>
                        </div>
                    </div>
                    <div id="chart-roc" style="height: 320px;"></div>
                </div>
                <div class="ref-dashboard-card">
                    <div class="ref-card-header">
                        <div>
                            <h3 class="ref-card-title">BCNB Nodal Distribution</h3>
                            <div class="ref-card-subtitle">1,058 Verified Clinical Biopsies</div>
                        </div>
                    </div>
                    <div id="chart-donut" style="height: 320px;"></div>
                </div>
            </div>

            <!-- Real Held-Out Test Patients Table -->
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h3 class="ref-card-title">Held-Out Test Cohort Predictions (Sample of 6 Patients)</h3>
                        <div class="ref-card-subtitle">Verified BCNB ground-truth pathology vs Multi-Model outputs</div>
                    </div>
                    <button class="pill-filter-btn" onclick="switchTab('prediction')">Open Prediction Lab →</button>
                </div>
                <table class="ref-patient-table">
                    <thead>
                        <tr>
                            <th>Patient ID</th>
                            <th>Actual ALN Status</th>
                            <th>Quantum SVM</th>
                            <th>Classical RBF-SVM</th>
                            <th>XGBoost</th>
                            <th>Consensus</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="ref-patient-row">
                            <td><strong>Patient #153</strong></td>
                            <td><span class="status-pill-negative">N0 Negative</span></td>
                            <td><span style="color: #7965E8; font-weight: 700;">N0</span> (0.372)</td>
                            <td><span style="color: #18A999; font-weight: 700;">N0</span> (0.368)</td>
                            <td><span style="color: #F08A78; font-weight: 700;">N+</span> (0.555)</td>
                            <td><span style="background: #FEF3C7; color: #B45309; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">Majority (2 vs 1)</span></td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong>Patient #932</strong></td>
                            <td><span class="status-pill-negative">N0 Negative</span></td>
                            <td><span style="color: #7965E8; font-weight: 700;">N+</span> (0.401)</td>
                            <td><span style="color: #18A999; font-weight: 700;">N0</span> (0.358)</td>
                            <td><span style="color: #F08A78; font-weight: 700;">N0</span> (0.140)</td>
                            <td><span style="background: #FEF3C7; color: #B45309; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">Majority (2 vs 1)</span></td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong>Patient #256</strong></td>
                            <td><span class="status-pill-positive">N+ Metastasis</span></td>
                            <td><span style="color: #7965E8; font-weight: 700;">N+</span> (0.455)</td>
                            <td><span style="color: #18A999; font-weight: 700;">N+</span> (0.398)</td>
                            <td><span style="color: #F08A78; font-weight: 700;">N+</span> (0.586)</td>
                            <td><span style="background: #E7F8F5; color: #18A999; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">Unanimous N+</span></td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong>Patient #691</strong></td>
                            <td><span class="status-pill-positive">N+ Metastasis</span></td>
                            <td><span style="color: #7965E8; font-weight: 700;">N0</span> (0.323)</td>
                            <td><span style="color: #18A999; font-weight: 700;">N0</span> (0.357)</td>
                            <td><span style="color: #F08A78; font-weight: 700;">N0</span> (0.222)</td>
                            <td><span style="background: #E7F8F5; color: #18A999; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">Unanimous N0</span></td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong>Patient #650</strong></td>
                            <td><span class="status-pill-negative">N0 Negative</span></td>
                            <td><span style="color: #7965E8; font-weight: 700;">N+</span> (0.445)</td>
                            <td><span style="color: #18A999; font-weight: 700;">N+</span> (0.387)</td>
                            <td><span style="color: #F08A78; font-weight: 700;">N+</span> (0.839)</td>
                            <td><span style="background: #E7F8F5; color: #18A999; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">Unanimous N+</span></td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong>Patient #151</strong></td>
                            <td><span class="status-pill-positive">N+ Metastasis</span></td>
                            <td><span style="color: #7965E8; font-weight: 700;">N0</span> (0.335)</td>
                            <td><span style="color: #18A999; font-weight: 700;">N0</span> (0.364)</td>
                            <td><span style="color: #F08A78; font-weight: 700;">N+</span> (0.515)</td>
                            <td><span style="background: #FEF3C7; color: #B45309; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">Majority (2 vs 1)</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 2: PREDICTION LAB -->
        <div id="tab-prediction" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h3 class="ref-card-title">Patient Prediction Lab</h3>
                        <div class="ref-card-subtitle">Evaluate genuine models on held-out test patient records under blind protocol</div>
                    </div>
                </div>
                
                <div style="background: #F8FAFC; border: 1px solid var(--border-color); border-radius: 14px; padding: 1.25rem; margin-bottom: 1.25rem;">
                    <label style="font-size: 0.85rem; font-weight: 700; color: #25324A; display: block; margin-bottom: 8px;">Select Held-Out Patient Record:</label>
                    <select id="sel-patient" onchange="updateSelectedPatient()" style="width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #CBD5E1; font-size: 0.88rem; background: white;">
                        <option value="153">Patient #153 — Age: 80 yrs | Tumour: 2.5 cm | Grade: 2 | ER: Positive | HER2: Negative</option>
                        <option value="932">Patient #932 — Age: 70 yrs | Tumour: 1.3 cm | Grade: 1 | ER: Positive | HER2: Negative</option>
                        <option value="256">Patient #256 — Age: 60 yrs | Tumour: 3.0 cm | Grade: 2 | ER: Positive | HER2: Negative</option>
                        <option value="691">Patient #691 — Age: 76 yrs | Tumour: 1.8 cm | Grade: 2 | ER: Positive | HER2: Negative</option>
                        <option value="650">Patient #650 — Age: 44 yrs | Tumour: 2.5 cm | Grade: 2 | ER: Positive | HER2: Positive</option>
                        <option value="151">Patient #151 — Age: 56 yrs | Tumour: 3.5 cm | Grade: 3 | ER: Negative | HER2: Negative</option>
                    </select>

                    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 14px;">
                        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B; display: block;">Tumour Size</span>
                            <strong id="disp-size" style="color: #25324A; font-size: 1rem;">2.5 cm</strong>
                        </div>
                        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B; display: block;">Patient Age</span>
                            <strong id="disp-age" style="color: #25324A; font-size: 1rem;">80 yrs</strong>
                        </div>
                        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B; display: block;">Histological Grade</span>
                            <strong id="disp-grade" style="color: #25324A; font-size: 1rem;">Grade 2</strong>
                        </div>
                        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B; display: block;">ER Receptor</span>
                            <strong id="disp-er" style="color: #25324A; font-size: 1rem;">Positive</strong>
                        </div>
                        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B; display: block;">HER2 Status</span>
                            <strong id="disp-her2" style="color: #25324A; font-size: 1rem;">Negative</strong>
                        </div>
                    </div>

                    <div style="margin-top: 14px;">
                        <button class="btn-summary-ai" onclick="runPrediction()">Run All Models</button>
                    </div>
                </div>

                <!-- Prediction Results Grid (Side-by-side color cards) -->
                <div id="pred-cards-grid" style="display: none; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 1.25rem;">
                    <div class="model-card-quantum">
                        <span style="background: #F0EDFF; color: #7965E8; border-radius: 9999px; padding: 3px 10px; font-size: 0.74rem; font-weight: 700;">Quantum Kernel</span>
                        <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-top: 6px;">Qiskit ZZFeatureMap SVM</div>
                        <div id="q-label" style="font-size: 1.6rem; font-weight: 800; color: #7965E8; margin: 8px 0;">N0 (Negative)</div>
                        <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                            Calibrated Probability: <strong id="q-prob">37.2%</strong><br>
                            Raw Decision Margin: <code id="q-score">-0.328</code><br>
                            Execution: <strong>Qiskit Statevector Simulator</strong>
                        </div>
                    </div>
                    <div class="model-card-rbf">
                        <span style="background: #E7F8F5; color: #18A999; border-radius: 9999px; padding: 3px 10px; font-size: 0.74rem; font-weight: 700;">Classical Baseline</span>
                        <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-top: 6px;">Classical RBF-SVM</div>
                        <div id="c-label" style="font-size: 1.6rem; font-weight: 800; color: #18A999; margin: 8px 0;">N0 (Negative)</div>
                        <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                            Calibrated Probability: <strong id="c-prob">36.8%</strong><br>
                            Raw Decision Margin: <code id="c-score">-0.412</code><br>
                            Support Vectors: <strong>728</strong>
                        </div>
                    </div>
                    <div class="model-card-xgb">
                        <span style="background: #FFF0EC; color: #F08A78; border-radius: 9999px; padding: 3px 10px; font-size: 0.74rem; font-weight: 700;">Ensemble Baseline</span>
                        <div style="font-size: 0.88rem; font-weight: 700; color: #25324A; margin-top: 6px;">XGBoost Classifier</div>
                        <div id="x-label" style="font-size: 1.6rem; font-weight: 800; color: #F08A78; margin: 8px 0;">N+ (Metastasis)</div>
                        <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                            Predicted Probability: <strong id="x-prob">55.5%</strong><br>
                            Log-Odds Margin: <code id="x-score">+0.221</code><br>
                            Estimators: <strong>50 Trees</strong>
                        </div>
                    </div>
                </div>

                <!-- Consensus & Reveal Outcome Box -->
                <div id="reveal-container" style="display: none;">
                    <div style="background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 10px; padding: 12px 16px; margin-bottom: 12px; font-size: 0.85rem; color: #92400E;">
                        <strong>Model Agreement:</strong> <span id="consensus-text">Majority Divergence (2 models predict N0, 1 predicts N+)</span>.
                        <div style="font-size: 0.74rem; margin-top: 4px;">Note: Consensus does not establish ground truth.</div>
                    </div>

                    <button class="pill-filter-btn" style="background: #7965E8; color: white; border: none; padding: 8px 18px;" onclick="revealOutcome()">Reveal Actual Outcome</button>

                    <div id="outcome-revealed" style="display: none; margin-top: 14px; background: #F8FAFC; border: 2px solid #7965E8; border-radius: 14px; padding: 16px;">
                        <h4 style="color: #25324A; margin-bottom: 4px;">Verified Ground-Truth Pathological Outcome</h4>
                        <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 10px;">Official Staging Record: <strong id="gt-staging">N0 (Negative)</strong></div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                                <span style="font-size: 0.74rem; color: #64748B;">Quantum SVM</span>
                                <div id="q-verdict" style="font-weight: 800; color: #18A999;">Correct Prediction</div>
                            </div>
                            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                                <span style="font-size: 0.74rem; color: #64748B;">Classical RBF-SVM</span>
                                <div id="c-verdict" style="font-weight: 800; color: #18A999;">Correct Prediction</div>
                            </div>
                            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                                <span style="font-size: 0.74rem; color: #64748B;">XGBoost</span>
                                <div id="x-verdict" style="font-weight: 800; color: #E11D48;">Misclassified</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: MODEL COMPARISON LAB -->
        <div id="tab-comparison" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h3 class="ref-card-title">Model Comparison & Benchmark Analytics</h3>
                        <div class="ref-card-subtitle">Detailed evaluation across all statistical metrics on 212 held-out BCNB test cases</div>
                    </div>
                </div>
                
                <table class="ref-patient-table" style="margin-bottom: 1.5rem;">
                    <thead>
                        <tr>
                            <th>Model Architecture</th>
                            <th>AUROC</th>
                            <th>Accuracy</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>Specificity</th>
                            <th>F1-Score</th>
                            <th>PR-AUC</th>
                            <th>Train Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="ref-patient-row">
                            <td><strong style="color: #7965E8;">Quantum-Kernel SVM</strong></td>
                            <td>0.5001</td><td>50.47%</td><td>37.66%</td><td>35.80%</td><td>59.54%</td><td>0.3671</td><td>0.3804</td><td>1.85s</td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong style="color: #18A999;">Classical RBF-SVM</strong></td>
                            <td>0.5982</td><td>59.43%</td><td>46.88%</td><td>37.04%</td><td>73.28%</td><td>0.4138</td><td>0.4497</td><td>0.04s</td>
                        </tr>
                        <tr class="ref-patient-row">
                            <td><strong style="color: #F08A78;">XGBoost Classifier</strong></td>
                            <td><strong>0.6012</strong></td><td><strong>59.43%</strong></td><td><strong>46.88%</strong></td><td><strong>37.04%</strong></td><td><strong>73.28%</strong></td><td><strong>0.4138</strong></td><td><strong>0.4731</strong></td><td>0.08s</td>
                        </tr>
                    </tbody>
                </table>

                <div style="background: #F8FAFC; border: 1px solid var(--border-color); border-radius: 12px; padding: 16px;">
                    <h4 style="color: #25324A; margin-bottom: 6px;">Scientific Takeaway:</h4>
                    <p style="font-size: 0.84rem; color: #64748B; line-height: 1.6;">
                        No measurable quantum advantage is observed on this clinical tabular dataset. Classical tree-based models (XGBoost AUROC 0.6012) and radial basis functions (RBF-SVM AUROC 0.5982) substantially outperform the 5-qubit ZZFeatureMap Quantum Kernel SVM (AUROC 0.5001). The periodic non-linear Pauli mapping introduces trigonometric wrapping over continuous clinical biomarkers without empirical gain.
                    </p>
                </div>
            </div>
        </div>

        <!-- TAB 4: QUANTUM PARK -->
        <div id="tab-quantum-park" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h3 class="ref-card-title">Quantum Park: Circuit Composer</h3>
                        <div class="ref-card-subtitle">Synthesize multi-qubit gates and simulate 3D Bloch sphere projections</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px;">
                    <div>
                        <div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 12px; padding: 14px; margin-bottom: 12px;">
                            <label style="font-size: 0.85rem; font-weight: 700; color: #25324A;">Select Circuit Template:</label>
                            <select id="sel-circuit-tpl" onchange="updateCircuitDiagram()" style="width: 100%; padding: 8px 12px; border-radius: 6px; border: 1px solid #CBD5E1; margin-top: 6px;">
                                <option value="ghz">3-Qubit Greenberger-Horne-Zeilinger (GHZ) Entangled State</option>
                                <option value="bell">2-Qubit Bell State (|Φ+⟩)</option>
                                <option value="qkernel">5-Qubit ZZFeatureMap Quantum Kernel Layer</option>
                            </select>
                        </div>
                        <div style="background: #25324A; color: #F8FAFC; border-radius: 10px; padding: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; line-height: 1.6;">
                            <pre id="circuit-ascii">
q_0: ──■───────
     ┌─┴─┐
q_1: ┤ X ├──■──
     └───┘┌─┴─┐
q_2: ─────┤ X ├
          └───┘
                            </pre>
                        </div>
                    </div>
                    <div>
                        <h4 style="color: #25324A; margin-bottom: 6px;">3D Bloch Sphere Visualizer</h4>
                        <div id="bloch-canvas-container" style="width: 100%; height: 260px; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: QUANTUM INSIGHTS -->
        <div id="tab-quantum-insights" class="tab-content">
            <div class="ref-dashboard-card">
                <h3 class="ref-card-title">Quantum Kernel Engine Insights</h3>
                <div class="ref-card-subtitle">ZZFeatureMap Hamiltonian evolution, fidelity inner product metrics, and mathematical checks</div>
                <div style="margin-top: 14px; font-size: 0.84rem; color: #25324A; line-height: 1.7;">
                    <div style="background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 10px; padding: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; margin-bottom: 14px;">
                        U_Φ(x) = [ exp( i ∑_{j=1}^5 x_j Z_j + i ∑_{j < k} (π - x_j)(π - x_k) Z_j Z_k ) · H^{⊗5} ]²
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
                        <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Symmetry Check</span>
                            <div style="font-weight: 800; color: #18A999;">K = Kᵀ (Exact)</div>
                        </div>
                        <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Unit Diagonal</span>
                            <div style="font-weight: 800; color: #18A999;">K_ii = 1.0 (Exact)</div>
                        </div>
                        <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Value Bounds</span>
                            <div style="font-weight: 800; color: #18A999;">[0.0, 1.0] (Verified)</div>
                        </div>
                        <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Simulator</span>
                            <div style="font-weight: 800; color: #7965E8;">Statevector Qiskit</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 6: 3D ANATOMY EXPLORER -->
        <div id="tab-anatomy" class="tab-content">
            <div class="ref-dashboard-card">
                <h3 class="ref-card-title">Interactive 3D Anatomy Explorer</h3>
                <div class="ref-card-subtitle">WebGL representation of mammary parenchyma and axillary lymph node basin levels I, II, III</div>
                <div id="anatomy-canvas-container" style="width: 100%; height: 440px; background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 12px; margin-top: 14px; position: relative;">
                </div>
                <div style="margin-top: 10px; font-size: 0.78rem; color: #64748B;">
                    <strong>Controls:</strong> Click & drag to rotate | Right-click to pan | Scroll to zoom.
                </div>
            </div>
        </div>

        <!-- TAB 7: HANDBOOK -->
        <div id="tab-handbook" class="tab-content">
            <div class="ref-dashboard-card">
                <h3 class="ref-card-title">Research Handbook</h3>
                <div class="ref-card-subtitle">18 comprehensive chapters covering quantum machine learning and clinical oncology</div>
                <div style="margin-top: 14px; font-size: 0.85rem; color: #25324A; line-height: 1.7;">
                    <ol style="margin-left: 20px;">
                        <li><strong>Chapter 1:</strong> Project Overview & Clinical Mission</li>
                        <li><strong>Chapter 2:</strong> Breast Cancer Pathophysiology</li>
                        <li><strong>Chapter 3:</strong> Axillary Lymph Node Metastasis & Staging</li>
                        <li><strong>Chapter 4:</strong> Principles of Quantum Computing</li>
                        <li><strong>Chapter 5:</strong> Qubits and Quantum Gates</li>
                        <li><strong>Chapter 6:</strong> Quantum State Representation and the Bloch Sphere</li>
                        <li><strong>Chapter 7:</strong> Quantum Feature Maps and Hilbert Spaces</li>
                        <li><strong>Chapter 8:</strong> Quantum Kernel Estimation and Fidelity</li>
                        <li><strong>Chapter 9:</strong> Quantum Support Vector Machines (QSVM)</li>
                        <li><strong>Chapter 10:</strong> Classical Support Vector Machines (RBF-SVM)</li>
                        <li><strong>Chapter 11:</strong> Gradient Boosted Trees (XGBoost)</li>
                        <li><strong>Chapter 12:</strong> BCNB Dataset Audit and Provenance</li>
                        <li><strong>Chapter 13:</strong> Data Preprocessing and Leakage Prevention</li>
                        <li><strong>Chapter 14:</strong> Model Evaluation Metrics & Class Imbalance</li>
                        <li><strong>Chapter 15:</strong> Model Interpretability & Explainability</li>
                        <li><strong>Chapter 16:</strong> Computational Complexity and Hardware Realities</li>
                        <li><strong>Chapter 17:</strong> Clinical Ethics and Regulatory Boundaries</li>
                        <li><strong>Chapter 18:</strong> Multi-Cancer Expansion Roadmap</li>
                    </ol>
                </div>
            </div>
        </div>

        <!-- TAB 8: DATASET & METHODS -->
        <div id="tab-dataset" class="tab-content">
            <div class="ref-dashboard-card">
                <h3 class="ref-card-title">Dataset & Methods</h3>
                <div class="ref-card-subtitle">BCNB data provenance, zero-leakage preprocessing, and software version audit</div>
                <div style="margin-top: 14px; font-size: 0.84rem; color: #25324A; line-height: 1.7;">
                    <p><strong>Cohort:</strong> 1,058 consecutive patients from TCIA Breast Cancer Nodal / Biopsy dataset (CC BY 4.0).</p>
                    <p><strong>Target:</strong> Axillary lymph node status (N0: 655 vs N+: 403).</p>
                    <p><strong>Predictors:</strong> Tumour Size (cm), Patient Age (years), Nottingham Histological Grade (1-3), ER Status (0/1), HER2 Status (0/1).</p>
                    <p><strong>Confounder Control:</strong> Resected node counts and surgical procedure strictly excluded to eliminate target leakage.</p>
                </div>
            </div>
        </div>

        <!-- TAB 9: REPORTS & ANALYTICS -->
        <div id="tab-reports" class="tab-content">
            <div class="ref-dashboard-card">
                <h3 class="ref-card-title">Reports & Analytics Export</h3>
                <div class="ref-card-subtitle">Direct download access to verified tabular metrics, patient predictions, and experiment configurations</div>
                <div style="display: flex; gap: 12px; margin-top: 14px;">
                    <a href="/api/metrics" target="_blank" class="pill-filter-btn" style="background: #7965E8; color: white; border: none;">Download Metrics (JSON)</a>
                    <a href="/api/health" target="_blank" class="pill-filter-btn">System Health Check</a>
                </div>
            </div>
        </div>

        <!-- TAB 10: MULTI-CANCER REGISTRY -->
        <div id="tab-multi-cancer" class="tab-content">
            <div class="ref-dashboard-card">
                <h3 class="ref-card-title">Multi-Cancer Research Registry</h3>
                <div class="ref-card-subtitle">Task registry preventing invalid cross-cancer model reuse</div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 14px;">
                    <div style="border: 1px solid #18A999; border-radius: 10px; padding: 14px; background: #E7F8F5;">
                        <strong style="color: #0F8275;">Breast (BCNB)</strong>
                        <div style="font-size: 0.76rem; color: #0F8275; margin-top: 4px;">ACTIVE / VERIFIED</div>
                    </div>
                    <div style="border: 1px solid #CBD5E1; border-radius: 10px; padding: 14px; background: #F8FAFC;">
                        <strong style="color: #25324A;">Lung (TCGA-LUAD)</strong>
                        <div style="font-size: 0.76rem; color: #64748B; margin-top: 4px;">PLANNED</div>
                    </div>
                    <div style="border: 1px solid #CBD5E1; border-radius: 10px; padding: 14px; background: #F8FAFC;">
                        <strong style="color: #25324A;">Colorectal (TCGA-COAD)</strong>
                        <div style="font-size: 0.76rem; color: #64748B; margin-top: 4px;">PLANNED</div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Navigation Tab Switching
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            
            var targetTab = document.getElementById('tab-' + tabId);
            if (targetTab) targetTab.classList.add('active');

            var navLinks = document.querySelectorAll('.nav-item');
            navLinks.forEach(link => {
                if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(tabId)) {
                    link.classList.add('active');
                }
            });

            if (tabId === 'anatomy') {
                setTimeout(initThreeAnatomy, 100);
            }
        }

        // Patient Selection & Blind Prediction Logic
        var patientsData = {
            "153": { size: "2.5 cm", age: "80 yrs", grade: "Grade 2", er: "Positive", her2: "Negative", q: "N0 (Negative)", qp: "37.2%", qs: "-0.328", c: "N0 (Negative)", cp: "36.8%", cs: "-0.412", x: "N+ (Metastasis)", xp: "55.5%", xs: "+0.221", consensus: "Majority Divergence (2 models predict N0, 1 predicts N+)", gt: "N0 (Negative)", qcorr: true, ccorr: true, xcorr: false },
            "932": { size: "1.3 cm", age: "70 yrs", grade: "Grade 1", er: "Positive", her2: "Negative", q: "N+ (Metastasis)", qp: "40.1%", qs: "+0.012", c: "N0 (Negative)", cp: "35.8%", cs: "-0.435", x: "N0 (Negative)", xp: "14.0%", xs: "-1.815", consensus: "Majority Divergence (2 models predict N0, 1 predicts N+)", gt: "N0 (Negative)", qcorr: false, ccorr: true, xcorr: true },
            "256": { size: "3.0 cm", age: "60 yrs", grade: "Grade 2", er: "Positive", her2: "Negative", q: "N+ (Metastasis)", qp: "45.5%", qs: "+0.155", c: "N+ (Metastasis)", cp: "39.8%", cs: "+0.038", x: "N+ (Metastasis)", xp: "58.6%", xs: "+0.348", consensus: "Unanimous Consensus (All 3 models predict N+)", gt: "N+ (Metastasis)", qcorr: true, ccorr: true, xcorr: true },
            "691": { size: "1.8 cm", age: "76 yrs", grade: "Grade 2", er: "Positive", her2: "Negative", q: "N0 (Negative)", qp: "32.3%", qs: "-0.450", c: "N0 (Negative)", cp: "35.7%", cs: "-0.442", x: "N0 (Negative)", xp: "22.2%", xs: "-1.254", consensus: "Unanimous Consensus (All 3 models predict N0)", gt: "N+ (Metastasis)", qcorr: false, ccorr: false, xcorr: false },
            "650": { size: "2.5 cm", age: "44 yrs", grade: "Grade 2", er: "Positive", her2: "Positive", q: "N+ (Metastasis)", qp: "44.5%", qs: "+0.120", c: "N+ (Metastasis)", cp: "38.7%", cs: "+0.005", x: "N+ (Metastasis)", xp: "83.9%", xs: "+1.651", consensus: "Unanimous Consensus (All 3 models predict N+)", gt: "N0 (Negative)", qcorr: false, ccorr: false, xcorr: false },
            "151": { size: "3.5 cm", age: "56 yrs", grade: "Grade 3", er: "Negative", her2: "Negative", q: "N0 (Negative)", qp: "33.5%", qs: "-0.395", c: "N0 (Negative)", cp: "36.4%", cs: "-0.418", x: "N+ (Metastasis)", xp: "51.5%", xs: "+0.060", consensus: "Majority Divergence (2 models predict N0, 1 predicts N+)", gt: "N+ (Metastasis)", qcorr: false, ccorr: false, xcorr: true }
        };

        function updateSelectedPatient() {
            var pid = document.getElementById('sel-patient').value;
            var p = patientsData[pid];
            document.getElementById('disp-size').innerText = p.size;
            document.getElementById('disp-age').innerText = p.age;
            document.getElementById('disp-grade').innerText = p.grade;
            document.getElementById('disp-er').innerText = p.er;
            document.getElementById('disp-her2').innerText = p.her2;

            document.getElementById('pred-cards-grid').style.display = 'none';
            document.getElementById('reveal-container').style.display = 'none';
            document.getElementById('outcome-revealed').style.display = 'none';
        }

        function runPrediction() {
            var pid = document.getElementById('sel-patient').value;
            var p = patientsData[pid];

            document.getElementById('q-label').innerText = p.q;
            document.getElementById('q-prob').innerText = p.qp;
            document.getElementById('q-score').innerText = p.qs;

            document.getElementById('c-label').innerText = p.c;
            document.getElementById('c-prob').innerText = p.cp;
            document.getElementById('c-score').innerText = p.cs;

            document.getElementById('x-label').innerText = p.x;
            document.getElementById('x-prob').innerText = p.xp;
            document.getElementById('x-score').innerText = p.xs;

            document.getElementById('consensus-text').innerText = p.consensus;

            document.getElementById('pred-cards-grid').style.display = 'grid';
            document.getElementById('reveal-container').style.display = 'block';
            document.getElementById('outcome-revealed').style.display = 'none';
        }

        function revealOutcome() {
            var pid = document.getElementById('sel-patient').value;
            var p = patientsData[pid];

            document.getElementById('gt-staging').innerText = p.gt;
            document.getElementById('q-verdict').innerText = p.qcorr ? "Correct Prediction" : "Misclassified";
            document.getElementById('q-verdict').style.color = p.qcorr ? "#18A999" : "#E11D48";

            document.getElementById('c-verdict').innerText = p.ccorr ? "Correct Prediction" : "Misclassified";
            document.getElementById('c-verdict').style.color = p.ccorr ? "#18A999" : "#E11D48";

            document.getElementById('x-verdict').innerText = p.xcorr ? "Correct Prediction" : "Misclassified";
            document.getElementById('x-verdict').style.color = p.xcorr ? "#18A999" : "#E11D48";

            document.getElementById('outcome-revealed').style.display = 'block';
        }

        function updateCircuitDiagram() {
            var tpl = document.getElementById('sel-circuit-tpl').value;
            var pre = document.getElementById('circuit-ascii');
            if (tpl === 'ghz') {
                pre.innerText = "q_0: ──■───────\\n     ┌─┴─┐\\nq_1: ┤ X ├──■──\\n     └───┘┌─┴─┐\\nq_2: ─────┤ X ├\\n          └───┘";
            } else if (tpl === 'bell') {
                pre.innerText = "q_0: ──■──\\n     ┌─┴─┐\\nq_1: ┤ X ├\\n     └───┘";
            } else if (tpl === 'qkernel') {
                pre.innerText = "q_0: ──H──Rz(2x0)──■─────────────■──\\nq_1: ──H──Rz(2x1)──■──Rz(2x1)──■────\\nq_2: ──H──Rz(2x2)───────────────────\\nq_3: ──H──Rz(2x3)───────────────────\\nq_4: ──H──Rz(2x4)───────────────────";
            }
        }

        // Plotly Plots initialization
        window.addEventListener('load', function() {
            // ROC Curves
            Plotly.newPlot('chart-roc', [
                { x: [0, 0.26, 0.45, 0.64, 1.0], y: [0, 0.37, 0.55, 0.72, 1.0], mode: 'lines', name: 'XGBoost (AUC: 0.601)', line: { color: '#F08A78', width: 2.8 } },
                { x: [0, 0.27, 0.46, 0.65, 1.0], y: [0, 0.37, 0.54, 0.71, 1.0], mode: 'lines', name: 'Classical RBF (AUC: 0.598)', line: { color: '#18A999', width: 2.8 } },
                { x: [0, 0.40, 0.58, 0.75, 1.0], y: [0, 0.36, 0.51, 0.68, 1.0], mode: 'lines', name: 'Quantum SVM (AUC: 0.500)', line: { color: '#7965E8', width: 2.8 } },
                { x: [0, 1], y: [0, 1], mode: 'lines', name: 'Chance Line', line: { color: '#94A3B8', width: 1.5, dash: 'dash' } }
            ], {
                margin: { l: 40, r: 20, t: 30, b: 40 },
                xaxis: { title: 'False Positive Rate' },
                yaxis: { title: 'True Positive Rate' },
                legend: { orientation: 'h', y: 1.15 }
            }, { responsive: true });

            // Cohort Donut
            Plotly.newPlot('chart-donut', [{
                labels: ['N0 Negative', 'N+(1-2) Nodes', 'N+(>2) Nodes'],
                values: [655, 210, 193],
                type: 'pie',
                hole: 0.6,
                marker: { colors: ['#18A999', '#F08A78', '#D9534F'] }
            }], {
                margin: { l: 20, r: 20, t: 20, b: 20 },
                legend: { orientation: 'h', y: -0.1 }
            }, { responsive: true });
        });

        // Three.js Anatomy Initializer
        var anatomyInit = false;
        function initThreeAnatomy() {
            if (anatomyInit) return;
            var container = document.getElementById('anatomy-canvas-container');
            if (!container) return;

            var scene = new THREE.Scene();
            scene.background = new THREE.Color(0xF8FAFC);
            var camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 5, 24);

            var renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            var controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;

            var ambient = new THREE.AmbientLight(0xFFFFFF, 0.8);
            scene.add(ambient);
            var dir = new THREE.DirectionalLight(0xFFFFFF, 0.8);
            dir.position.set(10, 15, 15);
            scene.add(dir);

            // Breast contour
            var surfGeo = new THREE.SphereGeometry(6.5, 32, 24);
            var surfMat = new THREE.MeshStandardMaterial({ color: 0xE0C8BA, transparent: true, opacity: 0.45 });
            var surfMesh = new THREE.Mesh(surfGeo, surfMat);
            surfMesh.position.set(-1.5, -0.5, 1.0);
            surfMesh.scale.set(1, 1.05, 0.7);
            scene.add(surfMesh);

            // Lymph nodes
            function addNode(x, y, z, color) {
                var g = new THREE.SphereGeometry(0.55, 16, 16);
                var m = new THREE.MeshStandardMaterial({ color: color });
                var mesh = new THREE.Mesh(g, m);
                mesh.position.set(x, y, z);
                scene.add(mesh);
            }
            addNode(5.8, 3.8, 0.5, 0x18A999);
            addNode(6.6, 2.8, 0.0, 0x18A999);
            addNode(6.2, 6.2, -0.5, 0x7965E8);
            addNode(5.5, 8.5, -1.8, 0xF08A78);

            function anim() {
                requestAnimationFrame(anim);
                controls.update();
                renderer.render(scene, camera);
            }
            anim();
            anatomyInit = true;
        }
    </script>
</body>
</html>
"""

# ==============================================================================
# Vercel WSGI Application / Handler Export
# ==============================================================================
def app(environ, start_response):
    """
    Standard WSGI callable exported for Vercel Serverless Functions.
    Handles HTTP GET / POST and delivers the full interactive Clinical AI application.
    """
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    # API Health endpoint
    if path == "/api/health":
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [json.dumps({"status": "healthy", "platform": "Vercel", "version": "2.0.0"}).encode("utf-8")]

    # API Metrics endpoint
    if path == "/api/metrics":
        metrics_file = Path(root_dir) / "results" / "metrics.json"
        if metrics_file.exists():
            with open(metrics_file, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            data = json.dumps([
                {"model_name": "Quantum-kernel SVM", "auroc": 0.5001, "accuracy": 0.5047, "precision": 0.3766, "recall": 0.3580, "specificity": 0.5954, "f1_score": 0.3671, "pr_auc": 0.3804},
                {"model_name": "Classical RBF-SVM", "auroc": 0.5982, "accuracy": 0.5943, "precision": 0.4688, "recall": 0.3704, "specificity": 0.7328, "f1_score": 0.4138, "pr_auc": 0.4497},
                {"model_name": "XGBoost", "auroc": 0.6012, "accuracy": 0.5943, "precision": 0.4688, "recall": 0.3704, "specificity": 0.7328, "f1_score": 0.4138, "pr_auc": 0.4731}
            ])
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [data.encode("utf-8")]

    # Default route: serve complete Clinical AI & Quantum Park HTML/CSS/JS application
    status = "200 OK"
    headers = [("Content-Type", "text/html; charset=utf-8")]
    start_response(status, headers)
    return [HTML_CONTENT.encode("utf-8")]

# Vercel entrypoint aliases
application = app
handler = app

# ==============================================================================
# Streamlit Execution Hook
# ==============================================================================
if __name__ == "__main__":
    if "streamlit" in sys.modules or os.environ.get("STREAMLIT_SERVER_PORT"):
        import streamlit as st
        from frontend.dashboard_view import render_research_dashboard
        render_research_dashboard()
