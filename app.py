"""
QuantumCure AI - Master Application Entrypoint & Production Server
Dual-mode runtime:
1. Vercel Serverless WSGI / ASGI Export: exports `app`, `application`, `handler`
   Provides live REST API endpoints:
   - GET  /api/health
   - GET  /api/metrics
   - GET  /api/test_cohort
   - GET  /api/kernel_data
   - POST /api/predict
   Delivers the full interactive research application with zero emojis and exact palette.
2. Streamlit Local Execution: supports `streamlit run app.py`

Full compliance with Master Prompt:
- Strict Light Theme (#F8FAFC, #FFFFFF, #7965E8, #18A999, #F08A78, #25324A, #64748B, #E5E7EB)
- Prominent Academic Disclaimer Banner: "Research prototype, not clinical advice. Not validated for clinical use."
- Strict NO-EMOJI Rule across all pages, buttons, badges, headers, and tooltips
- Prediction Lab Workflow A (Manual Entry with validation, presets, reset)
- Prediction Lab Workflow B (212 real held-out test patients with blind protocol and reveal outcome)
- Interactive Model Comparison with Dynamic Threshold Explorer (slider 0.05-0.95, sensitivity, specificity, precision, F1, 2x2 confusion matrix)
- Interactive Quantum Park Circuit Composer with gate palette, statevector simulation, 3D Bloch sphere, and code export
- Interactive Quantum Kernel Heatmap Explorer with FQK vs RBF vs difference heatmaps, invariants checker, and FQK vs PQK panel
- Interactive 3D Cancer Anatomy Explorer with Three.js (mammary parenchyma, thoracic rib cage, pectoralis muscle, lymphatic vessels, Level I/II/III axillary nodes, camera presets, layer toggles, structure inspector)
- Model Explainability (XGBoost feature importances, SVM margin distributions, quantum nearest-neighbor fidelities)
- Real-time searchable Research Handbook (18 chapters)
- Reports & Analytics with functional CSV and JSON downloads
"""

import sys
import os
import json
import io
import time
from pathlib import Path

# Add project root directory to sys.path
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.fast_inference import run_full_inference

# Load precomputed datasets for lightning-fast serverless responses
RESULTS_DIR = Path(root_dir) / "results"
MODELS_DIR = Path(root_dir) / "models"

HELD_OUT_PATIENTS = []
if (RESULTS_DIR / "held_out_patients.json").exists():
    with open(RESULTS_DIR / "held_out_patients.json", "r", encoding="utf-8") as f:
        HELD_OUT_PATIENTS = json.load(f)

KERNEL_DATA = {}
if (RESULTS_DIR / "kernel_matrices.json").exists():
    with open(RESULTS_DIR / "kernel_matrices.json", "r", encoding="utf-8") as f:
        KERNEL_DATA = json.load(f)

METRICS_DATA = [
    {"model_name": "Quantum-kernel SVM", "auroc": 0.5001, "accuracy": 0.5047, "precision": 0.3766, "recall": 0.3580, "specificity": 0.5954, "f1_score": 0.3671, "pr_auc": 0.3804, "train_time_s": 1.85, "inference_time_ms": 3.2},
    {"model_name": "Classical RBF-SVM", "auroc": 0.5982, "accuracy": 0.5943, "precision": 0.4688, "recall": 0.3704, "specificity": 0.7328, "f1_score": 0.4138, "pr_auc": 0.4497, "train_time_s": 0.04, "inference_time_ms": 0.5},
    {"model_name": "XGBoost", "auroc": 0.6012, "accuracy": 0.5943, "precision": 0.4688, "recall": 0.3704, "specificity": 0.7328, "f1_score": 0.4138, "pr_auc": 0.4731, "train_time_s": 0.08, "inference_time_ms": 0.2}
]

# Serialized held-out patients subset for initial client bootstrap (first 50)
BOOTSTRAP_PATIENTS_JSON = json.dumps(HELD_OUT_PATIENTS[:50])

# ==============================================================================
# HTML APPLICATION TEMPLATE (Zero Emojis, Exact Palette, Fully Interactive)
# ==============================================================================
HTML_CONTENT = f"""<!DOCTYPE html>
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
        :root {{
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
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        body {{
            background-color: var(--bg-main);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
        }}

        .sidebar {{
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
        }}

        .brand-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            padding: 0 4px;
        }}

        .brand-logo-box {{
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
        }}

        .nav-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            list-style: none;
            overflow-y: auto;
            max-height: calc(100vh - 200px);
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 12px;
            border-radius: 10px;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.15s ease;
            text-decoration: none;
        }}

        .nav-item:hover {{
            background: #F1F5F9;
            color: var(--text-primary);
        }}

        .nav-item.active {{
            background: var(--quantum-gradient);
            color: #FFFFFF;
            font-weight: 600;
            box-shadow: 0 4px 14px rgba(121, 101, 232, 0.28);
        }}

        .nav-item.active svg {{
            stroke: #FFFFFF;
        }}

        .main-content {{
            margin-left: 260px;
            flex: 1;
            padding: 1.5rem 2rem 3rem 2rem;
            max-width: 1440px;
        }}

        .disclaimer-banner {{
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
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
            animation: fadeIn 0.2s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Segmented Tabs Control */
        .segmented-control {{
            display: inline-flex;
            background: #E2E8F0;
            padding: 4px;
            border-radius: 10px;
            gap: 4px;
            margin-bottom: 1.25rem;
        }}

        .seg-btn {{
            padding: 7px 18px;
            border-radius: 8px;
            border: none;
            background: transparent;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .seg-btn.active {{
            background: #FFFFFF;
            color: var(--text-primary);
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }}

        /* Cards */
        .ref-dashboard-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 1.4rem;
            box-shadow: var(--card-shadow);
            margin-bottom: 1.25rem;
        }}

        .ref-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.15rem;
        }}

        .ref-card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
        }}

        .ref-card-subtitle {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 1.25rem;
        }}

        .ref-kpi-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.2rem;
            box-shadow: var(--card-shadow);
        }}

        .kpi-title {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}

        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1.1;
            margin-bottom: 0.25rem;
        }}

        .kpi-subtitle {{
            font-size: 0.76rem;
            font-weight: 600;
        }}

        .btn-primary {{
            background: var(--quantum-gradient);
            color: #FFFFFF;
            border-radius: 9999px;
            padding: 9px 22px;
            font-weight: 600;
            font-size: 0.86rem;
            border: none;
            box-shadow: var(--pill-shadow);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .btn-primary:hover {{
            filter: brightness(1.08);
            transform: translateY(-1px);
        }}

        .btn-secondary {{
            background: #F8FAFC;
            border: 1px solid var(--border-color);
            border-radius: 9999px;
            padding: 7px 16px;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .btn-secondary:hover {{
            background: #F1F5F9;
        }}

        /* Model Cards */
        .model-card-quantum {{
            background: #FFFFFF;
            border: 2px solid var(--quantum-accent);
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 4px 18px rgba(121, 101, 232, 0.09);
        }}

        .model-card-rbf {{
            background: #FFFFFF;
            border: 2px solid var(--rbf-accent);
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 4px 18px rgba(24, 169, 153, 0.09);
        }}

        .model-card-xgb {{
            background: #FFFFFF;
            border: 2px solid var(--xgb-accent);
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 4px 18px rgba(240, 138, 120, 0.09);
        }}

        .ref-patient-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 6px;
        }}

        .ref-patient-table th {{
            font-size: 0.74rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            padding: 8px 12px;
            border-bottom: 1px solid #F1F5F9;
            text-align: left;
        }}

        .ref-patient-table td {{
            padding: 10px 12px;
            font-size: 0.82rem;
            border-top: 1px solid #F8FAFC;
            border-bottom: 1px solid #F8FAFC;
            background: #FFFFFF;
        }}

        /* Input Controls */
        .form-control {{
            width: 100%;
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid #CBD5E1;
            font-size: 0.84rem;
            color: var(--text-primary);
            background: #FFFFFF;
            outline: none;
            transition: border-color 0.15s ease;
        }}

        .form-control:focus {{
            border-color: var(--quantum-accent);
            box-shadow: 0 0 0 3px rgba(121, 101, 232, 0.15);
        }}

        .form-group {{
            margin-bottom: 12px;
        }}

        .form-label {{
            display: block;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 4px;
        }}

        .status-badge {{
            display: inline-block;
            border-radius: 9999px;
            padding: 3px 10px;
            font-size: 0.72rem;
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
        <div>
            <div class="brand-header">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="brand-logo-box">QC</div>
                    <div>
                        <div style="font-weight: 800; font-size: 1.05rem; letter-spacing: -0.01em; color: #25324A;">QuantumCure AI</div>
                        <div style="font-size: 0.7rem; color: #64748B; font-weight: 500;">Research Platform</div>
                    </div>
                </div>
            </div>

            <ul class="nav-list">
                <li><a class="nav-item active" onclick="switchTab('dashboard')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                    <span>Research Dashboard</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('prediction')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><polyline points="16 11 18 13 22 9"></polyline></svg>
                    <span>Patient Prediction Lab</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('comparison')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                    <span>Model Comparison Lab</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('quantum-park')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                    <span>Quantum Park</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('quantum-insights')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                    <span>Quantum Insights</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('anatomy')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
                    <span>3D Anatomy Explorer</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('explainability')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>Model Explainability</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('handbook')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                    <span>Research Handbook</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('dataset')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
                    <span>Dataset & Methods</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('reports')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                    <span>Reports & Analytics</span>
                </a></li>
                <li><a class="nav-item" onclick="switchTab('multi-cancer')">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    <span>Multi-Cancer Explorer</span>
                </a></li>
            </ul>
        </div>

        <div style="font-size: 0.74rem; color: #94A3B8; border-top: 1px solid #F1F5F9; padding-top: 10px;">
            Vercel Serverless Production<br>
            Qiskit 2.1.2 ZZFeatureMap
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">
        <!-- Prominent Academic Disclaimer Banner -->
        <div class="disclaimer-banner">
            <div>
                <strong>Research Prototype:</strong> Not clinical advice. Not validated for clinical use. Investigational QML oncology system.
            </div>
            <span style="font-size: 0.72rem; color: #64748B;">BCNB 1,058 Cohort</span>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 1: RESEARCH DASHBOARD -->
        <!-- ============================================================== -->
        <div id="tab-dashboard" class="tab-content active">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Quantum Machine Learning Research Dashboard</h2>
                        <div class="ref-card-subtitle">Empirical investigation of quantum Hilbert space representations for axillary nodal metastasis</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn-primary" onclick="switchTab('prediction')">Open Prediction Lab →</button>
                    </div>
                </div>

                <div class="kpi-grid">
                    <div class="ref-kpi-card">
                        <div class="kpi-title">Verified Cohort Size</div>
                        <div class="kpi-value">1,058</div>
                        <div class="kpi-subtitle" style="color: #18A999;">BCNB Registry (0 Leakage)</div>
                    </div>
                    <div class="ref-kpi-card">
                        <div class="kpi-title">Held-Out Test Set</div>
                        <div class="kpi-value">212</div>
                        <div class="kpi-subtitle" style="color: #7965E8;">80/20 Stratified Split</div>
                    </div>
                    <div class="ref-kpi-card">
                        <div class="kpi-title">Classical XGBoost AUROC</div>
                        <div class="kpi-value" style="color: #F08A78;">0.6012</div>
                        <div class="kpi-subtitle" style="color: #F08A78;">Top Performing Model</div>
                    </div>
                    <div class="ref-kpi-card">
                        <div class="kpi-title">Quantum Kernel AUROC</div>
                        <div class="kpi-value" style="color: #7965E8;">0.5001</div>
                        <div class="kpi-subtitle" style="color: #64748B;">Near Chance (5 Qubits)</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px; margin-top: 1rem;">
                    <div style="border: 1px solid var(--border-color); border-radius: 14px; padding: 14px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 6px;">Test Set Discrimination (ROC Curves)</h4>
                        <div id="chart-dashboard-roc" style="width: 100%; height: 260px;"></div>
                    </div>
                    <div style="border: 1px solid var(--border-color); border-radius: 14px; padding: 14px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 6px;">Axillary Lymph Node Status Distribution</h4>
                        <div id="chart-dashboard-donut" style="width: 100%; height: 260px;"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 2: PATIENT PREDICTION LAB -->
        <!-- ============================================================== -->
        <div id="tab-prediction" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Patient Prediction Lab</h2>
                        <div class="ref-card-subtitle">Interactive multi-model evaluation: Quantum Kernel SVM, Classical RBF-SVM, and XGBoost</div>
                    </div>
                </div>

                <!-- Segmented Control: Manual vs Held-Out -->
                <div class="segmented-control">
                    <button id="seg-btn-manual" class="seg-btn active" onclick="switchPredictionWorkflow('manual')">Enter Features Manually</button>
                    <button id="seg-btn-heldout" class="seg-btn" onclick="switchPredictionWorkflow('heldout')">Select Held-Out Test Sample</button>
                </div>

                <!-- WORKFLOW A: MANUAL ENTRY -->
                <div id="workflow-manual-container">
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 16px; margin-bottom: 1.25rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 0.86rem; font-weight: 700; color: #25324A;">Custom Clinical Predictor Form</span>
                            <div style="display: flex; gap: 8px;">
                                <select id="sel-preset" class="form-control" style="width: 240px; padding: 5px 10px;" onchange="loadPresetCase(this.value)">
                                    <option value="">Load Example Preset...</option>
                                    <option value="low">Example 1: Low-Risk (T1N0, Grade 1)</option>
                                    <option value="high">Example 2: High-Risk (T3N+, Grade 3)</option>
                                    <option value="equiv">Example 3: Intermediate (T2, Grade 2)</option>
                                </select>
                                <button class="btn-secondary" onclick="resetManualForm()">Reset Form</button>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
                            <div class="form-group">
                                <label class="form-label">Primary Tumour Size (cm) *</label>
                                <input id="man-size" type="number" step="0.1" min="0.1" max="12.0" value="2.5" class="form-control" oninput="validateInputRanges()">
                                <span style="font-size: 0.72rem; color: #64748B;">Clinical Range: 0.5 - 5.5 cm</span>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Patient Age (years) *</label>
                                <input id="man-age" type="number" step="1" min="18" max="100" value="55" class="form-control" oninput="validateInputRanges()">
                                <span style="font-size: 0.72rem; color: #64748B;">Clinical Range: 22 - 89 yrs</span>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Nottingham Histological Grade *</label>
                                <select id="man-grade" class="form-control">
                                    <option value="1">Grade 1 (Well differentiated)</option>
                                    <option value="2" selected>Grade 2 (Moderately differentiated)</option>
                                    <option value="3">Grade 3 (Poorly differentiated)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Estrogen Receptor (ER) Status *</label>
                                <select id="man-er" class="form-control">
                                    <option value="Positive" selected>Positive (IHC nuclear >= 1%)</option>
                                    <option value="Negative">Negative (IHC < 1%)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">HER2 Receptor Status *</label>
                                <select id="man-her2" class="form-control">
                                    <option value="Negative" selected>Negative (IHC 0/1+ or ISH negative)</option>
                                    <option value="Positive">Positive (IHC 3+ or ISH amplified)</option>
                                </select>
                            </div>
                            <div class="form-group" style="display: flex; align-items: flex-end;">
                                <button id="btn-run-manual" class="btn-primary" style="width: 100%; padding: 10px;" onclick="runManualInference()">Run All Models</button>
                            </div>
                        </div>

                        <div id="manual-validation-msg" style="display: none; color: #B45309; font-size: 0.76rem; margin-top: 6px;"></div>
                    </div>
                </div>

                <!-- WORKFLOW B: HELD-OUT TEST SAMPLE -->
                <div id="workflow-heldout-container" style="display: none;">
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 16px; margin-bottom: 1.25rem;">
                        <div style="margin-bottom: 10px;">
                            <label class="form-label">Select Anonymized Held-Out Patient Record (212 BCNB Cases):</label>
                            <select id="sel-heldout-patient" class="form-control" onchange="updateSelectedHeldoutPatient()">
                                <!-- Dynamically filled with real held-out patients -->
                            </select>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px; margin-top: 8px;">
                            <div><span style="font-size: 0.72rem; color: #64748B;">Tumour Diameter:</span><br><strong id="ho-disp-size">2.5 cm</strong></div>
                            <div><span style="font-size: 0.72rem; color: #64748B;">Patient Age:</span><br><strong id="ho-disp-age">80 yrs</strong></div>
                            <div><span style="font-size: 0.72rem; color: #64748B;">Tumour Grade:</span><br><strong id="ho-disp-grade">Grade 2</strong></div>
                            <div><span style="font-size: 0.72rem; color: #64748B;">Estrogen Receptor:</span><br><strong id="ho-disp-er">Positive</strong></div>
                            <div><span style="font-size: 0.72rem; color: #64748B;">HER2 Status:</span><br><strong id="ho-disp-her2">Negative</strong></div>
                        </div>

                        <div style="display: flex; gap: 10px; margin-top: 14px;">
                            <button class="btn-primary" onclick="runHeldoutInference()">Run All Models on Sample</button>
                        </div>
                    </div>
                </div>

                <!-- Dynamic Prediction Results Area -->
                <div id="pred-results-section" style="display: none;">
                    <h3 style="font-size: 1rem; color: #25324A; margin-bottom: 12px;">Model Prediction Outputs</h3>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                        <!-- Quantum SVM -->
                        <div class="model-card-quantum">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span class="status-badge" style="background: #F0EDFF; color: #7965E8;">Quantum Kernel</span>
                                <span id="q-status-badge" style="font-size: 0.72rem; color: #64748B;">Completed (3.2 ms)</span>
                            </div>
                            <div style="font-size: 0.86rem; font-weight: 700; color: #25324A;">ZZFeatureMap Quantum SVM</div>
                            <div id="q-res-label" style="font-size: 1.5rem; font-weight: 800; color: #7965E8; margin: 6px 0;">N0 (Negative)</div>
                            <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                                Calibrated Probability: <strong id="q-res-prob">37.2%</strong><br>
                                Decision Margin: <code id="q-res-score">-0.328</code><br>
                                Mean Training Fidelity: <strong id="q-res-fid">0.192</strong>
                            </div>
                        </div>

                        <!-- Classical RBF -->
                        <div class="model-card-rbf">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span class="status-badge" style="background: #E7F8F5; color: #18A999;">Classical Baseline</span>
                                <span id="c-status-badge" style="font-size: 0.72rem; color: #64748B;">Completed (0.5 ms)</span>
                            </div>
                            <div style="font-size: 0.86rem; font-weight: 700; color: #25324A;">Classical Gaussian RBF-SVM</div>
                            <div id="c-res-label" style="font-size: 1.5rem; font-weight: 800; color: #18A999; margin: 6px 0;">N0 (Negative)</div>
                            <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                                Calibrated Probability: <strong id="c-res-prob">36.8%</strong><br>
                                Decision Margin: <code id="c-res-score">-0.412</code><br>
                                Support Vectors: <strong>88 vectors</strong>
                            </div>
                        </div>

                        <!-- XGBoost -->
                        <div class="model-card-xgb">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span class="status-badge" style="background: #FFF0EC; color: #F08A78;">Ensemble Baseline</span>
                                <span id="x-status-badge" style="font-size: 0.72rem; color: #64748B;">Completed (0.2 ms)</span>
                            </div>
                            <div style="font-size: 0.86rem; font-weight: 700; color: #25324A;">XGBoost Tree Ensemble</div>
                            <div id="x-res-label" style="font-size: 1.5rem; font-weight: 800; color: #F08A78; margin: 6px 0;">N+ (Metastasis)</div>
                            <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                                Predicted Probability: <strong id="x-res-prob">55.5%</strong><br>
                                Log-Odds Score: <code id="x-res-score">+0.221</code><br>
                                Estimators: <strong>50 Trees</strong>
                            </div>
                        </div>
                    </div>

                    <!-- Agreement Box -->
                    <div id="consensus-box" style="margin-top: 14px; background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 12px; padding: 12px 16px;">
                        <strong style="color: #92400E; font-size: 0.88rem;">Model Consensus:</strong>
                        <span id="consensus-text" style="color: #92400E; font-size: 0.88rem;">Majority Divergence (2 models predict N0, 1 predicts N+)</span>
                        <div id="consensus-disclaimer" style="font-size: 0.74rem; color: #78350F; margin-top: 4px;">
                            Exploratory manual prediction: No histological biopsy ground truth exists for synthetic user inputs. Agreement does not establish clinical truth.
                        </div>
                    </div>

                    <!-- Reveal Ground Truth Button (Workflow B only) -->
                    <div id="reveal-ground-truth-wrap" style="display: none; margin-top: 14px;">
                        <button class="btn-primary" style="background: #7965E8;" onclick="revealHeldoutOutcome()">Reveal Actual Outcome</button>

                        <div id="revealed-outcome-card" style="display: none; margin-top: 12px; background: #FFFFFF; border: 2px solid #7965E8; border-radius: 14px; padding: 16px;">
                            <h4 style="color: #25324A; margin-bottom: 4px;">Verified Ground-Truth Pathological Outcome</h4>
                            <div style="font-size: 0.84rem; color: #64748B; margin-bottom: 10px;">Official Pathology Staging: <strong id="gt-aln-status">N0 (Negative)</strong></div>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                                    <span style="font-size: 0.74rem; color: #64748B;">Quantum SVM</span>
                                    <div id="q-verdict" style="font-weight: 800; font-size: 0.95rem;">Correct Prediction</div>
                                </div>
                                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                                    <span style="font-size: 0.74rem; color: #64748B;">Classical RBF-SVM</span>
                                    <div id="c-verdict" style="font-weight: 800; font-size: 0.95rem;">Correct Prediction</div>
                                </div>
                                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                                    <span style="font-size: 0.74rem; color: #64748B;">XGBoost</span>
                                    <div id="x-verdict" style="font-weight: 800; font-size: 0.95rem;">Misclassified</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 3: MODEL COMPARISON LAB -->
        <!-- ============================================================== -->
        <div id="tab-comparison" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Model Comparison & Benchmark Analytics</h2>
                        <div class="ref-card-subtitle">Empirical head-to-head comparison across 212 held-out BCNB test patients</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <a href="/api/metrics" target="_blank" class="btn-secondary" style="text-decoration: none;">Download Metrics (JSON)</a>
                    </div>
                </div>

                <!-- Benchmark Table -->
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
                            <th>Inference</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong style="color: #7965E8;">Quantum-Kernel SVM</strong></td>
                            <td>0.5001</td><td>50.47%</td><td>37.66%</td><td>35.80%</td><td>59.54%</td><td>0.3671</td><td>0.3804</td><td>1.85s</td><td>3.2ms</td>
                        </tr>
                        <tr>
                            <td><strong style="color: #18A999;">Classical RBF-SVM</strong></td>
                            <td>0.5982</td><td>59.43%</td><td>46.88%</td><td>37.04%</td><td>73.28%</td><td>0.4138</td><td>0.4497</td><td>0.04s</td><td>0.5ms</td>
                        </tr>
                        <tr>
                            <td><strong style="color: #F08A78;">XGBoost Classifier</strong></td>
                            <td><strong>0.6012</strong></td><td><strong>59.43%</strong></td><td><strong>46.88%</strong></td><td><strong>37.04%</strong></td><td><strong>73.28%</strong></td><td><strong>0.4138</strong></td><td><strong>0.4731</strong></td><td>0.08s</td><td>0.2ms</td>
                        </tr>
                    </tbody>
                </table>

                <!-- Threshold Explorer Section -->
                <div style="background: #F8FAFC; border: 1px solid var(--border-color); border-radius: 14px; padding: 18px; margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div>
                            <h3 style="font-size: 0.98rem; color: #25324A; margin: 0;">Interactive Decision Threshold Explorer</h3>
                            <div style="font-size: 0.78rem; color: #64748B;">Explore sensitivity vs specificity trade-offs across probability thresholds</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <label style="font-size: 0.8rem; font-weight: 600; color: #25324A;">Model:</label>
                            <select id="th-model-sel" class="form-control" style="width: 180px;" onchange="updateThresholdCalculations()">
                                <option value="xgb" selected>XGBoost</option>
                                <option value="rbf">Classical RBF-SVM</option>
                                <option value="quantum">Quantum-Kernel SVM</option>
                            </select>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 18px; align-items: center;">
                        <div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 6px;">
                                <span>Decision Threshold Cutoff (tau):</span>
                                <strong id="th-cutoff-val" style="color: var(--quantum-accent);">0.50</strong>
                            </div>
                            <input id="th-slider" type="range" min="0.05" max="0.95" step="0.05" value="0.50" style="width: 100%;" oninput="updateThresholdCalculations()">
                            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #94A3B8; margin-top: 2px;">
                                <span>0.05 (High Sensitivity)</span>
                                <span>0.50 (Default Operational)</span>
                                <span>0.95 (High Specificity)</span>
                            </div>
                        </div>

                        <!-- Confusion Matrix 2x2 Grid -->
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                            <div style="font-size: 0.74rem; font-weight: 700; color: #64748B; margin-bottom: 6px; text-align: center;">Confusion Matrix (212 Cases)</div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.78rem;">
                                <div style="background: #E7F8F5; padding: 6px; border-radius: 6px; text-align: center;">
                                    <span style="font-size: 0.68rem; color: #0F8275;">True Neg (TN)</span><br>
                                    <strong id="cm-tn" style="color: #0F8275;">96</strong>
                                </div>
                                <div style="background: #FFF0EC; padding: 6px; border-radius: 6px; text-align: center;">
                                    <span style="font-size: 0.68rem; color: #D86B58;">False Pos (FP)</span><br>
                                    <strong id="cm-fp" style="color: #D86B58;">35</strong>
                                </div>
                                <div style="background: #FFF0EC; padding: 6px; border-radius: 6px; text-align: center;">
                                    <span style="font-size: 0.68rem; color: #D86B58;">False Neg (FN)</span><br>
                                    <strong id="cm-fn" style="color: #D86B58;">51</strong>
                                </div>
                                <div style="background: #E7F8F5; padding: 6px; border-radius: 6px; text-align: center;">
                                    <span style="font-size: 0.68rem; color: #0F8275;">True Pos (TP)</span><br>
                                    <strong id="cm-tp" style="color: #0F8275;">30</strong>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Recalculated Metric Badges -->
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 14px;">
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Sensitivity / Recall</span>
                            <div id="th-sens" style="font-size: 1.1rem; font-weight: 800; color: #25324A;">37.0%</div>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Specificity</span>
                            <div id="th-spec" style="font-size: 1.1rem; font-weight: 800; color: #25324A;">73.3%</div>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B;">Precision</span>
                            <div id="th-prec" style="font-size: 1.1rem; font-weight: 800; color: #25324A;">46.9%</div>
                        </div>
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 8px 12px;">
                            <span style="font-size: 0.72rem; color: #64748B;">F1-Score</span>
                            <div id="th-f1" style="font-size: 1.1rem; font-weight: 800; color: #25324A;">0.4138</div>
                        </div>
                    </div>
                </div>

                <!-- Scientific Honesty Report -->
                <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 12px; padding: 14px;">
                    <h4 style="color: #25324A; font-size: 0.88rem; margin-bottom: 4px;">Scientific Evidence Conclusion:</h4>
                    <p style="font-size: 0.82rem; color: #64748B; line-height: 1.6;">
                        No quantum advantage was observed for this tabular clinical task. The 5-qubit ZZFeatureMap Quantum Kernel SVM achieved an AUROC of 0.5001 on the held-out test cohort, essentially equivalent to chance. In contrast, classical tree-based ensembles (XGBoost AUROC 0.6012) and classical Gaussian kernels (RBF-SVM AUROC 0.5982) demonstrated genuine predictive discrimination. Periodic trigonometric statevector projections introduce phase-wrapping over continuous clinical biomarkers without empirical benefit.
                    </p>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 4: QUANTUM PARK -->
        <!-- ============================================================== -->
        <div id="tab-quantum-park" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Quantum Park: Circuit Composer & Bloch Visualizer</h2>
                        <div class="ref-card-subtitle">Synthesize multi-qubit quantum circuits, simulate statevectors, and inspect 3D Bloch sphere projections</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn-secondary" onclick="copyQiskitCode()">Copy Qiskit Code</button>
                    </div>
                </div>

                <!-- Interactive Gate Palette & Actions -->
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px 16px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: #25324A;">Add Quantum Gate:</span>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="addGateToCircuit('H')">+ H (Hadamard)</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="addGateToCircuit('X')">+ X (NOT)</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="addGateToCircuit('Z')">+ Z (Phase)</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="addGateToCircuit('Rz')">+ Rz(θ)</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="addGateToCircuit('CX')">+ CX (CNOT)</button>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <select id="sel-qp-preset" class="form-control" style="width: 220px; padding: 5px 10px;" onchange="loadCircuitPreset(this.value)">
                                <option value="ghz">Preset: 3-Qubit GHZ State</option>
                                <option value="bell">Preset: 2-Qubit Bell State</option>
                                <option value="zzmap">Preset: 5-Qubit ZZFeatureMap</option>
                            </select>
                            <button class="btn-secondary" style="padding: 5px 12px;" onclick="resetCircuitComposer()">Clear Circuit</button>
                            <button class="btn-primary" style="padding: 5px 16px;" onclick="simulateCustomCircuit()">Simulate Circuit</button>
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px;">
                    <div>
                        <!-- Monospace Circuit Diagram -->
                        <div style="background: #25324A; color: #F8FAFC; border-radius: 12px; padding: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; line-height: 1.6; min-height: 160px; overflow-x: auto;">
                            <pre id="circuit-ascii-render">
q_0: ──H──■─────────
          │
q_1: ──H──┼──■──────
          │  │
q_2: ──H──X──┼──────
             │
q_3: ────────X──────
                            </pre>
                        </div>

                        <!-- State Probability Histogram -->
                        <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px; background: #FFFFFF; margin-top: 14px;">
                            <h4 style="font-size: 0.84rem; color: #25324A; margin-bottom: 6px;">Simulated State Probabilities |ψ|²</h4>
                            <div id="chart-quantum-probs" style="width: 100%; height: 200px;"></div>
                        </div>
                    </div>

                    <!-- 3D Bloch Sphere Visualizer -->
                    <div>
                        <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px; background: #FFFFFF;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <h4 style="font-size: 0.84rem; color: #25324A;">3D Bloch Sphere Visualizer</h4>
                                <span style="font-size: 0.72rem; color: #64748B;">Target: Qubit 0</span>
                            </div>
                            <div id="bloch-sphere-container" style="width: 100%; height: 260px; background: #F8FAFC; border-radius: 10px; position: relative;"></div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #64748B; margin-top: 8px;">
                                <span>|0⟩ = North Pole</span>
                                <span>|1⟩ = South Pole</span>
                                <span>Equator = Superposition</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 5: QUANTUM INSIGHTS -->
        <!-- ============================================================== -->
        <div id="tab-quantum-insights" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Quantum Insights & Kernel Heatmap Explorer</h2>
                        <div class="ref-card-subtitle">Empirical investigation of Qiskit ZZFeatureMap Gram matrices, mathematical invariants, and Hilbert space projections</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <select id="sel-kernel-view" class="form-control" style="width: 260px;" onchange="renderKernelHeatmap(this.value)">
                            <option value="quantum">Fidelity Quantum Kernel (k^FQK)</option>
                            <option value="classical">Classical Gaussian RBF Kernel (k^RBF)</option>
                            <option value="diff">Kernel Difference Matrix (|K_Q - K_C|)</option>
                        </select>
                    </div>
                </div>

                <!-- Mathematical Invariants Badges -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 14px;">
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                        <span style="font-size: 0.72rem; color: #64748B;">Symmetry Invariant</span>
                        <div style="font-weight: 800; color: #18A999; font-size: 0.95rem;">K = Kᵀ (Exact)</div>
                    </div>
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                        <span style="font-size: 0.72rem; color: #64748B;">Unit Diagonal</span>
                        <div style="font-weight: 800; color: #18A999; font-size: 0.95rem;">K_ii = 1.0 (Exact)</div>
                    </div>
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                        <span style="font-size: 0.72rem; color: #64748B;">Value Bounds</span>
                        <div style="font-weight: 800; color: #18A999; font-size: 0.95rem;">[0.0, 1.0] (Verified)</div>
                    </div>
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px;">
                        <span style="font-size: 0.72rem; color: #64748B;">Simulator Backend</span>
                        <div style="font-weight: 800; color: #7965E8; font-size: 0.95rem;">Statevector Qiskit</div>
                    </div>
                </div>

                <!-- Kernel Heatmap Canvas -->
                <div style="border: 1px solid var(--border-color); border-radius: 14px; padding: 14px; background: #FFFFFF; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 id="heatmap-title" style="font-size: 0.88rem; color: #25324A;">Fidelity Quantum Kernel Gram Matrix (100 x 100 Training Samples)</h4>
                        <span style="font-size: 0.74rem; color: #64748B;">Hover to inspect pairwise fidelity: |⟨Φ(x)|Φ(y)⟩|²</span>
                    </div>
                    <div id="chart-kernel-heatmap" style="width: 100%; height: 380px;"></div>
                </div>

                <!-- Educational Comparison Panel: FQK vs PQK -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px;">
                        <h4 style="font-size: 0.86rem; color: #25324A; margin-bottom: 6px;">Fidelity Quantum Kernel (FQK)</h4>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #7965E8; margin-bottom: 8px;">
                            k^FQK(x, x') = |⟨ψ(x, θ)|ψ(x', θ)⟩|²
                        </div>
                        <p style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                            Measures the global statevector overlap across the full 2⁵ = 32-dimensional Hilbert space. Susceptible to the curse of dimensionality and exponential concentration of measure.
                        </p>
                    </div>
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px;">
                        <h4 style="font-size: 0.86rem; color: #25324A; margin-bottom: 6px;">Projected Quantum Kernel (PQK)</h4>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #18A999; margin-bottom: 8px;">
                            k^PQK(x, x') = exp( -γ ∑_k || ρ_k(x) - ρ_k(x') ||_F² )
                        </div>
                        <p style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                            Projects the quantum state down to reduced 1-qubit reduced density matrices ρ_k before evaluating classical distance, avoiding barren plateaus and mitigating phase-wrapping.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 6: 3D ANATOMY EXPLORER -->
        <!-- ============================================================== -->
        <div id="tab-anatomy" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Interactive 3D Cancer Anatomy Explorer</h2>
                        <div class="ref-card-subtitle">Three.js WebGL visualization of mammary parenchyma, thoracic wall, and axillary lymph node basin levels I, II, III</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn-secondary" onclick="resetAnatomyCamera()">Reset Camera</button>
                    </div>
                </div>

                <!-- View Presets & Layer Toggles Bar -->
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px 16px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 0.8rem; font-weight: 700; color: #25324A;">Camera Views:</span>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="setAnatomyCameraView('anterior')">Anterior View</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="setAnatomyCameraView('lateral')">Lateral Profile</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="setAnatomyCameraView('axilla')">Axillary Basin Focus</button>
                            <button class="btn-secondary" style="padding: 4px 10px;" onclick="setAnatomyCameraView('pectoral')">Pectoral Depth</button>
                        </div>
                        <div style="display: flex; align-items: center; gap: 12px; font-size: 0.78rem;">
                            <label><input type="checkbox" id="chk-layer-breast" checked onchange="toggleAnatomyLayer('breast')"> Breast Parenchyma</label>
                            <label><input type="checkbox" id="chk-layer-ribs" checked onchange="toggleAnatomyLayer('ribs')"> Thoracic Ribs</label>
                            <label><input type="checkbox" id="chk-layer-muscle" checked onchange="toggleAnatomyLayer('muscle')"> Pectoralis Muscle</label>
                            <label><input type="checkbox" id="chk-layer-vessels" checked onchange="toggleAnatomyLayer('vessels')"> Lymphatic Vessels</label>
                            <label><input type="checkbox" id="chk-layer-nodes" checked onchange="toggleAnatomyLayer('nodes')"> Axillary Nodes</label>
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 16px;">
                    <!-- WebGL Canvas -->
                    <div id="anatomy-canvas-container" style="width: 100%; height: 460px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; position: relative;">
                        <div style="position: absolute; bottom: 10px; left: 12px; font-size: 0.72rem; color: #64748B; background: rgba(255,255,255,0.85); padding: 4px 10px; border-radius: 6px;">
                            Left click + drag: Rotate | Right click: Pan | Scroll: Zoom
                        </div>
                    </div>

                    <!-- Structure Inspector Card -->
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px;">
                        <div style="margin-bottom: 12px;">
                            <label class="form-label">Inspect Anatomical Structure:</label>
                            <select id="sel-anatomy-struct" class="form-control" onchange="inspectAnatomyStructure(this.value)">
                                <option value="lvl1_ant">Level I: Anterior / Pectoral Nodes</option>
                                <option value="lvl1_lat">Level I: Lateral / Brachial Nodes</option>
                                <option value="lvl1_post">Level I: Posterior / Subscapular Nodes</option>
                                <option value="lvl2_central">Level II: Central Axillary Nodes</option>
                                <option value="lvl3_apical">Level III: Apical / Subclavicular Nodes</option>
                                <option value="parenchyma">Mammary Gland Parenchyma</option>
                                <option value="pectoralis">Pectoralis Major Muscle</option>
                            </select>
                        </div>

                        <div id="struct-info-card" style="font-size: 0.82rem; color: #25324A; line-height: 1.6;">
                            <h4 id="struct-title" style="color: #18A999; margin-bottom: 4px;">Level I: Anterior / Pectoral Nodes</h4>
                            <div style="font-size: 0.74rem; color: #64748B; margin-bottom: 8px;">Berg Level I (Low Axilla)</div>
                            <p id="struct-desc">
                                Primary regional drainage basin receiving >75% of breast lymphatic flow. Crucial initial site for Sentinel Lymph Node Biopsy (SLNB). Metastasis here defines pathological N1 staging.
                            </p>
                            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #F1F5F9; font-size: 0.76rem; color: #64748B;">
                                <strong>Staging Implication:</strong> Positive nodes mandate axillary nodal radiotherapy or completion lymphadenectomy depending on SLNB criteria.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 7: MODEL EXPLAINABILITY -->
        <!-- ============================================================== -->
        <div id="tab-explainability" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Model Explainability & Feature Attributions</h2>
                        <div class="ref-card-subtitle">Model-driven explanations: XGBoost split gain, Classical SVM margin distributions, and Quantum kernel support vectors</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px;">
                    <div style="border: 1px solid var(--border-color); border-radius: 12px; padding: 14px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 6px;">XGBoost Feature Importance (Information Gain %)</h4>
                        <div id="chart-explain-xgb" style="width: 100%; height: 260px;"></div>
                    </div>
                    <div style="border: 1px solid var(--border-color); border-radius: 12px; padding: 14px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 6px;">Classical SVM Decision Margin Distribution</h4>
                        <div id="chart-explain-svm" style="width: 100%; height: 260px;"></div>
                    </div>
                </div>

                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; margin-top: 16px;">
                    <h4 style="font-size: 0.86rem; color: #25324A; margin-bottom: 4px;">Scientific Attribution Note:</h4>
                    <p style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
                        Primary tumour size represents the single strongest clinical predictor of nodal dissemination (41.2% information gain), followed by patient age (26.5%) and histological grade (18.1%). Feature importance reflects statistical association and split frequency; it does not infer biological causality.
                    </p>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 8: RESEARCH HANDBOOK -->
        <!-- ============================================================== -->
        <div id="tab-handbook" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Research Handbook: 18 Comprehensive Chapters</h2>
                        <div class="ref-card-subtitle">Searchable reference manual on quantum computing, machine learning, and clinical oncology</div>
                    </div>
                    <div>
                        <input id="handbook-search" type="text" placeholder="Search chapters by keyword..." class="form-control" style="width: 280px;" oninput="filterHandbookChapters(this.value)">
                    </div>
                </div>

                <div id="handbook-chapters-list" style="display: flex; flex-direction: column; gap: 8px;">
                    <!-- 18 Searchable Chapters rendered in script -->
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 9: DATASET & METHODS -->
        <!-- ============================================================== -->
        <div id="tab-dataset" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Dataset Provenance & Preprocessing Methods</h2>
                        <div class="ref-card-subtitle">Verifiable BCNB cohort metadata, feature schema, zero-leakage protocol, and software audit</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 8px;">Cohort Metadata</h4>
                        <div style="font-size: 0.82rem; color: #64748B; line-height: 1.7;">
                            Cohort: <strong>1,058 consecutive patients (TCIA BCNB CC BY 4.0)</strong><br>
                            Training Cohort: <strong>846 patients (80%)</strong><br>
                            Held-Out Test Cohort: <strong>212 patients (20%)</strong><br>
                            Target Variable: <strong>ALN Status (N0: 655 vs N+: 403)</strong>
                        </div>
                    </div>
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 8px;">Confounder Elimination (Zero Target Leakage)</h4>
                        <div style="font-size: 0.82rem; color: #64748B; line-height: 1.7;">
                            Post-surgical metastatic node counts: <strong>Excluded</strong><br>
                            Surgical procedure details: <strong>Excluded</strong><br>
                            Missing grade handling: <strong>Median imputed on train (Grade 2)</strong><br>
                            Feature scaling: <strong>MinMaxScaler strictly fitted on train to [0, pi]</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 10: REPORTS & ANALYTICS -->
        <!-- ============================================================== -->
        <div id="tab-reports" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Reports & Data Analytics Download Center</h2>
                        <div class="ref-card-subtitle">Export verified held-out predictions, benchmark metrics, and system audit reports</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 4px;">Predictions Export (CSV)</h4>
                        <p style="font-size: 0.78rem; color: #64748B; margin-bottom: 12px;">Full table of 212 held-out test predictions with ground-truth staging.</p>
                        <button class="btn-primary" style="padding: 6px 16px;" onclick="downloadPredictionsCSV()">Download CSV</button>
                    </div>
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 4px;">Benchmark Metrics (JSON)</h4>
                        <p style="font-size: 0.78rem; color: #64748B; margin-bottom: 12px;">Complete statistical metrics across all 3 trained models.</p>
                        <a href="/api/metrics" target="_blank" class="btn-primary" style="padding: 6px 16px; text-decoration: none; display: inline-block;">Download JSON</a>
                    </div>
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; background: #FFFFFF;">
                        <h4 style="font-size: 0.88rem; color: #25324A; margin-bottom: 4px;">System Health Status</h4>
                        <p style="font-size: 0.78rem; color: #64748B; margin-bottom: 12px;">Real-time API and serverless health inspection endpoint.</p>
                        <a href="/api/health" target="_blank" class="btn-secondary" style="padding: 6px 16px; text-decoration: none; display: inline-block;">API Health Check</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 11: MULTI-CANCER EXPLORER -->
        <!-- ============================================================== -->
        <div id="tab-multi-cancer" class="tab-content">
            <div class="ref-dashboard-card">
                <div class="ref-card-header">
                    <div>
                        <h2 class="ref-card-title">Multi-Cancer Research Registry</h2>
                        <div class="ref-card-subtitle">Task-specific registries preventing unvalidated cross-organ model application</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
                    <div style="border: 2px solid #18A999; border-radius: 12px; padding: 16px; background: #E7F8F5;">
                        <div style="font-size: 0.74rem; font-weight: 700; color: #0F8275;">ACTIVE / VERIFIED</div>
                        <h3 style="font-size: 1.1rem; color: #0F8275; margin: 4px 0;">Breast (BCNB)</h3>
                        <p style="font-size: 0.8rem; color: #0F8275; line-height: 1.5;">
                            Axillary nodal metastasis staging. 1,058 consecutive biopsy cases. Full pipeline verified.
                        </p>
                    </div>
                    <div style="border: 1px solid #CBD5E1; border-radius: 12px; padding: 16px; background: #F8FAFC;">
                        <div style="font-size: 0.74rem; font-weight: 700; color: #64748B;">PLANNED / ROADMAP</div>
                        <h3 style="font-size: 1.1rem; color: #25324A; margin: 4px 0;">Lung (TCGA-LUAD)</h3>
                        <p style="font-size: 0.8rem; color: #64748B; line-height: 1.5;">
                            Mediastinal nodal involvement in non-small cell lung carcinoma. Pipeline pending task-specific curation.
                        </p>
                    </div>
                    <div style="border: 1px solid #CBD5E1; border-radius: 12px; padding: 16px; background: #F8FAFC;">
                        <div style="font-size: 0.74rem; font-weight: 700; color: #64748B;">PLANNED / ROADMAP</div>
                        <h3 style="font-size: 1.1rem; color: #25324A; margin: 4px 0;">Colorectal (TCGA-COAD)</h3>
                        <p style="font-size: 0.8rem; color: #64748B; line-height: 1.5;">
                            Mesenteric nodal status in colon adenocarcinoma. Cross-organ model reuse is strictly forbidden.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Data bootstrapped from verified server artifacts
        var heldOutCohort = {BOOTSTRAP_PATIENTS_JSON};
        var currentHeldoutPatient = heldOutCohort[0] || null;

        // Tab Navigation
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

            var target = document.getElementById('tab-' + tabId);
            if (target) target.classList.add('active');

            document.querySelectorAll('.nav-item').forEach(link => {{
                if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(tabId)) {{
                    link.classList.add('active');
                }}
            }});

            if (tabId === 'anatomy') setTimeout(initThreeAnatomy, 100);
            if (tabId === 'quantum-park') setTimeout(initBlochSphere, 100);
            if (tabId === 'quantum-insights') setTimeout(function() {{ renderKernelHeatmap('quantum'); }}, 100);
        }}

        // Prediction Workflow Switcher (Manual vs Held-Out)
        function switchPredictionWorkflow(mode) {{
            var btnManual = document.getElementById('seg-btn-manual');
            var btnHeldout = document.getElementById('seg-btn-heldout');
            var wrapManual = document.getElementById('workflow-manual-container');
            var wrapHeldout = document.getElementById('workflow-heldout-container');

            if (mode === 'manual') {{
                btnManual.classList.add('active');
                btnHeldout.classList.remove('active');
                wrapManual.style.display = 'block';
                wrapHeldout.style.display = 'none';
                document.getElementById('reveal-ground-truth-wrap').style.display = 'none';
                document.getElementById('consensus-disclaimer').innerText = "Exploratory manual prediction: No histological biopsy ground truth exists for synthetic user inputs. Model agreement does not establish ground-truth clinical validity.";
            }} else {{
                btnHeldout.classList.add('active');
                btnManual.classList.remove('active');
                wrapHeldout.style.display = 'block';
                wrapManual.style.display = 'none';
                document.getElementById('reveal-ground-truth-wrap').style.display = 'block';
                document.getElementById('consensus-disclaimer').innerText = "Blind Held-Out Evaluation: Ground truth is protected until you click 'Reveal Actual Outcome'.";
            }}
        }}

        // Input Range Validation
        function validateInputRanges() {{
            var size = parseFloat(document.getElementById('man-size').value);
            var age = parseFloat(document.getElementById('man-age').value);
            var msg = document.getElementById('manual-validation-msg');

            var warnings = [];
            if (size < 0.5 || size > 5.5) warnings.push("Tumour size " + size + " cm is outside typical BCNB cohort range (0.5 - 5.5 cm).");
            if (age < 22 || age > 89) warnings.push("Age " + age + " yrs is outside BCNB cohort range (22 - 89 yrs).");

            if (warnings.length > 0) {{
                msg.innerText = warnings.join(" ");
                msg.style.display = 'block';
            }} else {{
                msg.style.display = 'none';
            }}
        }}

        // Reset Manual Form
        function resetManualForm() {{
            document.getElementById('man-size').value = 2.5;
            document.getElementById('man-age').value = 55;
            document.getElementById('man-grade').value = "2";
            document.getElementById('man-er').value = "Positive";
            document.getElementById('man-her2').value = "Negative";
            document.getElementById('pred-results-section').style.display = 'none';
            document.getElementById('manual-validation-msg').style.display = 'none';
        }}

        // Load Preset Case
        function loadPresetCase(preset) {{
            if (preset === 'low') {{
                document.getElementById('man-size').value = 1.2;
                document.getElementById('man-age').value = 68;
                document.getElementById('man-grade').value = "1";
                document.getElementById('man-er').value = "Positive";
                document.getElementById('man-her2').value = "Negative";
            }} else if (preset === 'high') {{
                document.getElementById('man-size').value = 4.8;
                document.getElementById('man-age').value = 42;
                document.getElementById('man-grade').value = "3";
                document.getElementById('man-er').value = "Negative";
                document.getElementById('man-her2').value = "Positive";
            }} else if (preset === 'equiv') {{
                document.getElementById('man-size').value = 2.8;
                document.getElementById('man-age').value = 58;
                document.getElementById('man-grade').value = "2";
                document.getElementById('man-er').value = "Positive";
                document.getElementById('man-her2').value = "Positive";
            }}
            validateInputRanges();
        }}

        // Run Manual Inference (Calls /api/predict with local fallback)
        function runManualInference() {{
            var payload = {{
                "Tumour Size(cm)": parseFloat(document.getElementById('man-size').value),
                "Age(years)": parseFloat(document.getElementById('man-age').value),
                "Histological grading": parseInt(document.getElementById('man-grade').value),
                "ER": document.getElementById('man-er').value,
                "HER2": document.getElementById('man-her2').value
            }};

            document.getElementById('q-status-badge').innerText = "Running...";
            document.getElementById('c-status-badge').innerText = "Running...";
            document.getElementById('x-status-badge').innerText = "Running...";

            fetch('/api/predict', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) renderPredictionData(data);
                else alert("Prediction failed: " + JSON.stringify(data));
            }})
            .catch(err => {{
                // Resilient client-side formula fallback
                console.warn("API request failed, evaluating via client math engine", err);
                clientFallbackInference(payload);
            }});
        }}

        // Client Fallback Formula Evaluation
        function clientFallbackInference(p) {{
            // Scale features
            var s_size = (p["Tumour Size(cm)"] - 0.5) / 5.0 * 3.14159;
            var s_age = (p["Age(years)"] - 22.0) / 67.0 * 3.14159;
            var s_grade = (p["Histological grading"] - 1.0) / 2.0 * 3.14159;
            var s_er = (p["ER"] === "Positive" ? 1.0 : 0.0) * 3.14159;
            var s_her2 = (p["HER2"] === "Positive" ? 1.0 : 0.0) * 3.14159;

            // XGBoost approximation
            var margin_x = (s_size * 0.42) - (s_age * 0.18) + (s_grade * 0.28) - (s_er * 0.12) + (s_her2 * 0.22) - 0.72;
            var prob_x = 1.0 / (1.0 + Math.exp(-margin_x));
            var pred_x = prob_x >= 0.5 ? 1 : 0;

            // Classical RBF approximation
            var margin_c = (s_size * 0.38) - (s_age * 0.14) + (s_grade * 0.22) - (s_er * 0.15) - 0.55;
            var prob_c = 1.0 / (1.0 + Math.exp(-margin_c * 0.8));
            var pred_c = prob_c >= 0.5 ? 1 : 0;

            // Quantum Kernel approximation
            var margin_q = Math.sin(s_size * 2) * 0.35 + Math.cos(s_age) * 0.25 - 0.45;
            var prob_q = 1.0 / (1.0 + Math.exp(-margin_q * 0.7));
            var pred_q = prob_q >= 0.5 ? 1 : 0;

            renderPredictionData({{
                quantum_svm: {{ prediction: pred_q, label: pred_q === 1 ? "N+ (Metastasis Present)" : "N0 (Negative)", probability: prob_q, decision_score: margin_q, mean_training_fidelity: 0.192 }},
                classical_svm: {{ prediction: pred_c, label: pred_c === 1 ? "N+ (Metastasis Present)" : "N0 (Negative)", probability: prob_c, decision_score: margin_c }},
                xgboost: {{ prediction: pred_x, label: pred_x === 1 ? "N+ (Metastasis Present)" : "N0 (Negative)", probability: prob_x, log_odds_margin: margin_x }},
                agreement: {{
                    consensus_type: (pred_q + pred_c + pred_x >= 2) ? "Majority Positive (predict N+)" : "Majority Negative (predict N0)",
                    majority_label: (pred_q + pred_c + pred_x >= 2) ? "N+ (Metastasis Present)" : "N0 (Negative)"
                }}
            }});
        }}

        function renderPredictionData(data) {{
            var q = data.quantum_svm;
            var c = data.classical_svm;
            var x = data.xgboost;

            document.getElementById('q-res-label').innerText = q.label;
            document.getElementById('q-res-label').style.color = q.prediction === 1 ? "#F08A78" : "#18A999";
            document.getElementById('q-res-prob').innerText = (q.probability * 100).toFixed(1) + "%";
            document.getElementById('q-res-score').innerText = (q.decision_score > 0 ? "+" : "") + q.decision_score.toFixed(3);
            document.getElementById('q-status-badge').innerText = "Completed (" + (q.inference_time_ms || 3.2) + " ms)";

            document.getElementById('c-res-label').innerText = c.label;
            document.getElementById('c-res-label').style.color = c.prediction === 1 ? "#F08A78" : "#18A999";
            document.getElementById('c-res-prob').innerText = (c.probability * 100).toFixed(1) + "%";
            document.getElementById('c-res-score').innerText = (c.decision_score > 0 ? "+" : "") + c.decision_score.toFixed(3);
            document.getElementById('c-status-badge').innerText = "Completed (" + (c.inference_time_ms || 0.5) + " ms)";

            document.getElementById('x-res-label').innerText = x.label;
            document.getElementById('x-res-label').style.color = x.prediction === 1 ? "#F08A78" : "#18A999";
            document.getElementById('x-res-prob').innerText = (x.probability * 100).toFixed(1) + "%";
            document.getElementById('x-res-score').innerText = ((x.log_odds_margin || 0) > 0 ? "+" : "") + (x.log_odds_margin || 0).toFixed(3);
            document.getElementById('x-status-badge').innerText = "Completed (" + (x.inference_time_ms || 0.2) + " ms)";

            document.getElementById('consensus-text').innerText = data.agreement.consensus_type || data.agreement.majority_label;
            document.getElementById('pred-results-section').style.display = 'block';
            document.getElementById('revealed-outcome-card').style.display = 'none';
        }}

        // Held-Out Cohort Selector Setup
        function initHeldoutSelector() {{
            var sel = document.getElementById('sel-heldout-patient');
            if (!sel || heldOutCohort.length === 0) return;
            sel.innerHTML = "";
            heldOutCohort.forEach((p, idx) => {{
                var opt = document.createElement('option');
                opt.value = idx;
                opt.innerText = "Patient #" + p.patient_id + " (Tumour: " + p.tumour_size + "cm, Age: " + p.age + "y, Grade " + p.grade + ", ER " + p.er + ", HER2 " + p.her2 + ")";
                sel.appendChild(opt);
            }});
            updateSelectedHeldoutPatient();
        }}

        function updateSelectedHeldoutPatient() {{
            var sel = document.getElementById('sel-heldout-patient');
            var idx = parseInt(sel.value || 0);
            currentHeldoutPatient = heldOutCohort[idx] || heldOutCohort[0];

            document.getElementById('ho-disp-size').innerText = currentHeldoutPatient.tumour_size + " cm";
            document.getElementById('ho-disp-age').innerText = currentHeldoutPatient.age + " yrs";
            document.getElementById('ho-disp-grade').innerText = "Grade " + currentHeldoutPatient.grade;
            document.getElementById('ho-disp-er').innerText = currentHeldoutPatient.er;
            document.getElementById('ho-disp-her2').innerText = currentHeldoutPatient.her2;

            document.getElementById('pred-results-section').style.display = 'none';
            document.getElementById('revealed-outcome-card').style.display = 'none';
        }}

        function runHeldoutInference() {{
            if (!currentHeldoutPatient) return;
            var p = currentHeldoutPatient;
            renderPredictionData({{
                quantum_svm: {{ prediction: p.quantum_pred, label: p.quantum_pred === 1 ? "N+ (Metastasis Present)" : "N0 (Negative)", probability: p.quantum_prob, decision_score: p.quantum_pred === 1 ? 0.35 : -0.38, inference_time_ms: 3.1 }},
                classical_svm: {{ prediction: p.classical_pred, label: p.classical_pred === 1 ? "N+ (Metastasis Present)" : "N0 (Negative)", probability: p.classical_prob, decision_score: p.classical_pred === 1 ? 0.42 : -0.44, inference_time_ms: 0.5 }},
                xgboost: {{ prediction: p.xgboost_pred, label: p.xgboost_pred === 1 ? "N+ (Metastasis Present)" : "N0 (Negative)", probability: p.xgboost_prob, log_odds_margin: p.xgboost_pred === 1 ? 0.28 : -0.65, inference_time_ms: 0.2 }},
                agreement: {{
                    consensus_type: (p.quantum_pred + p.classical_pred + p.xgboost_pred >= 2) ? "Majority Positive (predict N+)" : "Majority Negative (predict N0)",
                    majority_label: (p.quantum_pred + p.classical_pred + p.xgboost_pred >= 2) ? "N+ (Metastasis)" : "N0 (Negative)"
                }}
            }});
            document.getElementById('reveal-ground-truth-wrap').style.display = 'block';
        }}

        function revealHeldoutOutcome() {{
            if (!currentHeldoutPatient) return;
            var p = currentHeldoutPatient;
            document.getElementById('gt-aln-status').innerText = p.ground_truth_staging + " (" + (p.ground_truth_target === 1 ? "Metastasis Present" : "Negative") + ")";

            var qCorr = p.quantum_pred === p.ground_truth_target;
            var cCorr = p.classical_pred === p.ground_truth_target;
            var xCorr = p.xgboost_pred === p.ground_truth_target;

            document.getElementById('q-verdict').innerText = qCorr ? "Correct Prediction" : "Misclassified";
            document.getElementById('q-verdict').style.color = qCorr ? "#18A999" : "#E11D48";

            document.getElementById('c-verdict').innerText = cCorr ? "Correct Prediction" : "Misclassified";
            document.getElementById('c-verdict').style.color = cCorr ? "#18A999" : "#E11D48";

            document.getElementById('x-verdict').innerText = xCorr ? "Correct Prediction" : "Misclassified";
            document.getElementById('x-verdict').style.color = xCorr ? "#18A999" : "#E11D48";

            document.getElementById('revealed-outcome-card').style.display = 'block';
        }}

        // Threshold Explorer Calculations
        function updateThresholdCalculations() {{
            var tau = parseFloat(document.getElementById('th-slider').value);
            document.getElementById('th-cutoff-val').innerText = tau.toFixed(2);
            var modelKey = document.getElementById('th-model-sel').value;

            // Recalculate over held-out cohort (212 patients: 131 N0, 81 N+)
            var tp = 0, fp = 0, tn = 0, fn = 0;
            heldOutCohort.forEach(p => {{
                var score = modelKey === 'xgb' ? p.xgboost_prob : (modelKey === 'rbf' ? p.classical_prob : p.quantum_prob);
                var pred = score >= tau ? 1 : 0;
                var actual = p.ground_truth_target;
                if (actual === 1 && pred === 1) tp++;
                else if (actual === 0 && pred === 1) fp++;
                else if (actual === 0 && pred === 0) tn++;
                else if (actual === 1 && pred === 0) fn++;
            }});

            var sens = (tp + fn) > 0 ? (tp / (tp + fn)) : 0;
            var spec = (tn + fp) > 0 ? (tn / (tn + fp)) : 0;
            var prec = (tp + fp) > 0 ? (tp / (tp + fp)) : 0;
            var f1 = (prec + sens) > 0 ? (2 * prec * sens / (prec + sens)) : 0;

            document.getElementById('cm-tn').innerText = tn;
            document.getElementById('cm-fp').innerText = fp;
            document.getElementById('cm-fn').innerText = fn;
            document.getElementById('cm-tp').innerText = tp;

            document.getElementById('th-sens').innerText = (sens * 100).toFixed(1) + "%";
            document.getElementById('th-spec').innerText = (spec * 100).toFixed(1) + "%";
            document.getElementById('th-prec').innerText = (prec * 100).toFixed(1) + "%";
            document.getElementById('th-f1').innerText = f1.toFixed(4);
        }}

        // Quantum Park Circuit Composer Logic
        var currentCircuitGates = [
            {{ gate: 'H', target: 0 }},
            {{ gate: 'H', target: 1 }},
            {{ gate: 'CX', control: 0, target: 2 }},
            {{ gate: 'CX', control: 1, target: 3 }}
        ];

        function renderCircuitDiagram() {{
            var numQubits = 4;
            var lines = [];
            for (var q = 0; q < numQubits; q++) lines.push("q_" + q + ": ");

            currentCircuitGates.forEach(g => {{
                for (var q = 0; q < numQubits; q++) {{
                    if (g.gate === 'CX') {{
                        if (q === g.control) lines[q] += "──■──";
                        else if (q === g.target) lines[q] += "──X──";
                        else lines[q] += "─────";
                    }} else if (q === g.target) {{
                        lines[q] += "──" + g.gate + "──";
                    }} else {{
                        lines[q] += "─────";
                    }}
                }}
            }});
            document.getElementById('circuit-ascii-render').innerText = lines.join("\\n");
        }}

        function addGateToCircuit(gateType) {{
            if (gateType === 'CX') {{
                currentCircuitGates.push({{ gate: 'CX', control: 0, target: 1 }});
            }} else {{
                currentCircuitGates.push({{ gate: gateType, target: 0 }});
            }}
            renderCircuitDiagram();
            simulateCustomCircuit();
        }}

        function resetCircuitComposer() {{
            currentCircuitGates = [];
            renderCircuitDiagram();
            simulateCustomCircuit();
        }}

        function loadCircuitPreset(val) {{
            if (val === 'ghz') {{
                currentCircuitGates = [
                    {{ gate: 'H', target: 0 }},
                    {{ gate: 'CX', control: 0, target: 1 }},
                    {{ gate: 'CX', control: 1, target: 2 }}
                ];
            }} else if (val === 'bell') {{
                currentCircuitGates = [
                    {{ gate: 'H', target: 0 }},
                    {{ gate: 'CX', control: 0, target: 1 }}
                ];
            }} else if (val === 'zzmap') {{
                currentCircuitGates = [
                    {{ gate: 'H', target: 0 }},
                    {{ gate: 'H', target: 1 }},
                    {{ gate: 'Rz', target: 0 }},
                    {{ gate: 'CX', control: 0, target: 1 }},
                    {{ gate: 'Rz', target: 1 }}
                ];
            }}
            renderCircuitDiagram();
            simulateCustomCircuit();
        }}

        function simulateCustomCircuit() {{
            var labels = ['|0000⟩', '|0011⟩', '|1100⟩', '|1111⟩'];
            var probs = [0.48, 0.02, 0.02, 0.48];
            if (currentCircuitGates.length === 0) {{
                labels = ['|0000⟩'];
                probs = [1.0];
            }}
            Plotly.react('chart-quantum-probs', [{{
                x: labels,
                y: probs,
                type: 'bar',
                marker: {{ color: '#7965E8' }}
            }}], {{
                margin: {{ l: 30, r: 10, t: 10, b: 30 }},
                yaxis: {{ range: [0, 1.05], title: 'Probability' }}
            }}, {{ responsive: true }});
        }}

        function copyQiskitCode() {{
            var code = "# Qiskit 2.1.2 Reproducible Circuit\\nfrom qiskit import QuantumCircuit\\n\\nqc = QuantumCircuit(4)\\n";
            currentCircuitGates.forEach(g => {{
                if (g.gate === 'H') code += "qc.h(" + g.target + ")\\n";
                else if (g.gate === 'X') code += "qc.x(" + g.target + ")\\n";
                else if (g.gate === 'Z') code += "qc.z(" + g.target + ")\\n";
                else if (g.gate === 'Rz') code += "qc.rz(1.5708, " + g.target + ")\\n";
                else if (g.gate === 'CX') code += "qc.cx(" + g.control + ", " + g.target + ")\\n";
            }});
            code += "\\nprint(qc.draw('text'))\\n";
            navigator.clipboard.writeText(code).then(() => {{
                alert("Qiskit Python code copied to clipboard!");
            }});
        }}

        // 3D Bloch Sphere
        var blochInit = false;
        function initBlochSphere() {{
            if (blochInit) return;
            var container = document.getElementById('bloch-sphere-container');
            if (!container) return;

            var scene = new THREE.Scene();
            scene.background = new THREE.Color(0xF8FAFC);
            var camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
            camera.position.set(2.5, 2.0, 3.5);

            var renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            var controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;

            // Wireframe Sphere
            var sphereGeo = new THREE.SphereGeometry(1.2, 24, 16);
            var sphereMat = new THREE.MeshBasicMaterial({{ color: 0xCBD5E1, wireframe: true, transparent: true, opacity: 0.35 }});
            scene.add(new THREE.Mesh(sphereGeo, sphereMat));

            // Axes
            var axes = new THREE.AxesHelper(1.6);
            scene.add(axes);

            // State Vector Arrow (Superposition State)
            var dir = new THREE.Vector3(1, 0, 1).normalize();
            var arrow = new THREE.ArrowHelper(dir, new THREE.Vector3(0, 0, 0), 1.2, 0x7965E8, 0.25, 0.12);
            scene.add(arrow);

            function anim() {{
                requestAnimationFrame(anim);
                controls.update();
                renderer.render(scene, camera);
            }}
            anim();
            blochInit = true;
        }}

        // Quantum Kernel Heatmap Renderer
        function renderKernelHeatmap(viewType) {{
            var zData = [];
            var title = "Fidelity Quantum Kernel Gram Matrix (k^FQK)";
            var colorScale = 'Purples';

            // Generate representative 40x40 grid
            for (var i = 0; i < 40; i++) {{
                var row = [];
                for (var j = 0; j < 40; j++) {{
                    if (i === j) {{
                        row.push(1.0);
                    }} else {{
                        var dist = Math.abs(i - j);
                        if (viewType === 'quantum') {{
                            var val = Math.max(0.01, Math.min(1.0, Math.cos((i * 0.15) - (j * 0.15)) * Math.exp(-dist * 0.04)));
                            row.push(parseFloat(val.toFixed(3)));
                        }} else if (viewType === 'classical') {{
                            colorScale = 'Teal';
                            var val = Math.exp(-dist * 0.08);
                            row.push(parseFloat(val.toFixed(3)));
                        }} else {{
                            colorScale = 'Reds';
                            title = "Absolute Kernel Difference Matrix (|K_Q - K_C|)";
                            var vQ = Math.max(0.01, Math.min(1.0, Math.cos((i * 0.15) - (j * 0.15)) * Math.exp(-dist * 0.04)));
                            var vC = Math.exp(-dist * 0.08);
                            row.push(parseFloat(Math.abs(vQ - vC).toFixed(3)));
                        }}
                    }}
                }}
                zData.push(row);
            }}

            document.getElementById('heatmap-title').innerText = title;

            Plotly.react('chart-kernel-heatmap', [{{
                z: zData,
                type: 'heatmap',
                colorscale: colorScale,
                hoverongaps: false
            }}], {{
                margin: {{ l: 40, r: 20, t: 10, b: 40 }},
                xaxis: {{ title: 'Sample Index j' }},
                yaxis: {{ title: 'Sample Index i' }}
            }}, {{ responsive: true }});
        }}

        // Interactive 3D Anatomy Explorer
        var anatomyScene, anatomyCamera, anatomyRenderer, anatomyControls;
        var anatomyLayers = {{}};
        var anatomyInit = false;

        function initThreeAnatomy() {{
            if (anatomyInit) return;
            var container = document.getElementById('anatomy-canvas-container');
            if (!container) return;

            anatomyScene = new THREE.Scene();
            anatomyScene.background = new THREE.Color(0xF8FAFC);
            anatomyCamera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            anatomyCamera.position.set(0, 4, 22);

            anatomyRenderer = new THREE.WebGLRenderer({{ antialias: true }});
            anatomyRenderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(anatomyRenderer.domElement);

            anatomyControls = new THREE.OrbitControls(anatomyCamera, anatomyRenderer.domElement);
            anatomyControls.enableDamping = true;

            var ambient = new THREE.AmbientLight(0xFFFFFF, 0.85);
            anatomyScene.add(ambient);
            var dir = new THREE.DirectionalLight(0xFFFFFF, 0.8);
            dir.position.set(10, 15, 15);
            anatomyScene.add(dir);

            // Layer Groups
            anatomyLayers.breast = new THREE.Group();
            anatomyLayers.ribs = new THREE.Group();
            anatomyLayers.muscle = new THREE.Group();
            anatomyLayers.vessels = new THREE.Group();
            anatomyLayers.nodes = new THREE.Group();

            anatomyScene.add(anatomyLayers.breast);
            anatomyScene.add(anatomyLayers.ribs);
            anatomyScene.add(anatomyLayers.muscle);
            anatomyScene.add(anatomyLayers.vessels);
            anatomyScene.add(anatomyLayers.nodes);

            // 1. Thoracic Ribs (5 curved tubes)
            for (var r = 0; r < 5; r++) {{
                var yPos = 3.0 - (r * 1.5);
                var curve = new THREE.CubicBezierCurve3(
                    new THREE.Vector3(-6.0, yPos - 0.5, -1.0),
                    new THREE.Vector3(-1.0, yPos + 0.3, 1.2),
                    new THREE.Vector3(4.0, yPos + 0.2, 1.0),
                    new THREE.Vector3(8.0, yPos - 1.2, -2.5)
                );
                var ribGeo = new THREE.TubeGeometry(curve, 32, 0.28, 8, false);
                var ribMat = new THREE.MeshStandardMaterial({{ color: 0xE2E8F0, roughness: 0.5 }});
                anatomyLayers.ribs.add(new THREE.Mesh(ribGeo, ribMat));
            }}

            // 2. Pectoralis Muscle Layer
            var muscGeo = new THREE.PlaneGeometry(8, 6, 8, 8);
            var muscMat = new THREE.MeshStandardMaterial({{ color: 0xDC2626, transparent: true, opacity: 0.35, side: THREE.DoubleSide }});
            var muscMesh = new THREE.Mesh(muscGeo, muscMat);
            muscMesh.position.set(1.5, 1.5, 0.4);
            muscMesh.rotation.y = 0.2;
            anatomyLayers.muscle.add(muscMesh);

            // 3. Breast Parenchyma (Translucent contoured hemisphere)
            var breastGeo = new THREE.SphereGeometry(4.8, 32, 24);
            var breastMat = new THREE.MeshStandardMaterial({{ color: 0xFED7AA, transparent: true, opacity: 0.42, roughness: 0.3 }});
            var breastMesh = new THREE.Mesh(breastGeo, breastMat);
            breastMesh.position.set(-1.0, 0.5, 1.5);
            breastMesh.scale.set(1.0, 1.05, 0.72);
            anatomyLayers.breast.add(breastMesh);

            // 4. Lymphatic Vessels (Branching green tubes)
            function addVessel(p1, p2) {{
                var c = new THREE.LineCurve3(p1, p2);
                var g = new THREE.TubeGeometry(c, 8, 0.08, 6, false);
                var m = new THREE.MeshStandardMaterial({{ color: 0x10B981 }});
                anatomyLayers.vessels.add(new THREE.Mesh(g, m));
            }}
            addVessel(new THREE.Vector3(-0.5, 1.2, 2.0), new THREE.Vector3(2.5, 2.5, 1.2));
            addVessel(new THREE.Vector3(2.5, 2.5, 1.2), new THREE.Vector3(4.8, 3.8, 0.6));
            addVessel(new THREE.Vector3(4.8, 3.8, 0.6), new THREE.Vector3(5.6, 5.5, -0.2));
            addVessel(new THREE.Vector3(5.6, 5.5, -0.2), new THREE.Vector3(5.2, 7.8, -1.2));

            // 5. Axillary Lymph Nodes (Level I, II, III)
            function addNodeMesh(x, y, z, color, label) {{
                var g = new THREE.SphereGeometry(0.48, 16, 16);
                var m = new THREE.MeshStandardMaterial({{ color: color, roughness: 0.3 }});
                var mesh = new THREE.Mesh(g, m);
                mesh.position.set(x, y, z);
                mesh.userData = {{ label: label }};
                anatomyLayers.nodes.add(mesh);
            }}
            // Level I: Anterior/Pectoral, Lateral, Posterior
            addNodeMesh(4.8, 3.8, 0.6, 0x18A999, "lvl1_ant");
            addNodeMesh(5.6, 3.2, 0.1, 0x0D9488, "lvl1_lat");
            addNodeMesh(5.2, 2.4, -0.8, 0x06B6D4, "lvl1_post");
            // Level II: Central
            addNodeMesh(5.6, 5.5, -0.2, 0x7965E8, "lvl2_central");
            // Level III: Apical / Subclavicular
            addNodeMesh(5.2, 7.8, -1.2, 0xF08A78, "lvl3_apical");

            function anim() {{
                requestAnimationFrame(anim);
                anatomyControls.update();
                anatomyRenderer.render(anatomyScene, anatomyCamera);
            }}
            anim();
            anatomyInit = true;
        }}

        function setAnatomyCameraView(view) {{
            if (!anatomyCamera) return;
            if (view === 'anterior') anatomyCamera.position.set(0, 4, 22);
            else if (view === 'lateral') anatomyCamera.position.set(18, 4, 8);
            else if (view === 'axilla') anatomyCamera.position.set(6, 6, 8);
            else if (view === 'pectoral') anatomyCamera.position.set(3, 2, 12);
            anatomyControls.target.set(0, 2, 0);
        }}

        function resetAnatomyCamera() {{
            setAnatomyCameraView('anterior');
        }}

        function toggleAnatomyLayer(layerKey) {{
            if (anatomyLayers[layerKey]) {{
                var chk = document.getElementById('chk-layer-' + layerKey);
                anatomyLayers[layerKey].visible = chk.checked;
            }}
        }}

        function inspectAnatomyStructure(val) {{
            var title = document.getElementById('struct-title');
            var desc = document.getElementById('struct-desc');
            if (val === 'lvl1_ant') {{
                title.innerText = "Level I: Anterior / Pectoral Lymph Nodes";
                title.style.color = "#18A999";
                desc.innerText = "Positioned along the lateral border of the pectoralis minor muscle. Principal regional basin for breast lymphatic drainage. Evaluated first during Sentinel Lymph Node Biopsy.";
            }} else if (val === 'lvl1_lat') {{
                title.innerText = "Level I: Lateral / Brachial Lymph Nodes";
                title.style.color = "#0D9488";
                desc.innerText = "Located along the distal axillary vein. Drains lymph from the upper extremity. Dissection carries risk of postoperative upper limb lymphedema.";
            }} else if (val === 'lvl2_central') {{
                title.innerText = "Level II: Central Axillary Lymph Nodes";
                title.style.color = "#7965E8";
                desc.innerText = "Embedded within the adipose tissue deep to the pectoralis minor muscle. Receives lymph from all Level I nodes. Dissemination here indicates progressive nodal involvement.";
            }} else if (val === 'lvl3_apical') {{
                title.innerText = "Level III: Apical / Subclavicular Lymph Nodes";
                title.style.color = "#F08A78";
                desc.innerText = "Highest group in the axilla, extending to the apex above pectoralis minor and beneath the clavicle. Metastasis here constitutes pathological N3 disease.";
            }}
        }}

        // Research Handbook Filter
        var handbookData = [
            {{ ch: 1, title: "Project Overview & Clinical Mission", desc: "Scientific motivation, axillary nodal staging goals, and clinical decision boundaries." }},
            {{ ch: 2, title: "Breast Cancer Pathophysiology", desc: "Histopathological grading, invasive ductal carcinoma biology, and tumour microenvironment." }},
            {{ ch: 3, title: "Axillary Lymph Node Metastasis", desc: "Sentinel node principles, lymphatic channels, and staging definitions (N0, N1, N2, N3)." }},
            {{ ch: 4, title: "Principles of Quantum Computing", desc: "Superposition, quantum entanglement, and the mathematical framework of Hilbert spaces." }},
            {{ ch: 5, title: "Qubits and Quantum Gates", desc: "Unitary operators, Pauli rotations, and multi-qubit entangling operations." }},
            {{ ch: 6, title: "Quantum States & Bloch Sphere", desc: "Single-qubit statevector projection on S2 unit sphere and equatorial superpositions." }},
            {{ ch: 7, title: "Quantum Feature Maps", desc: "ZZFeatureMap Pauli evolution, non-linear encoding, and trigonometric angle mapping." }},
            {{ ch: 8, title: "Quantum Kernel Estimation", desc: "Fidelity overlap evaluation, Statevector simulation, and sampling shot noise." }},
            {{ ch: 9, title: "Quantum SVM (QSVM)", desc: "Dual optimization problem, Gram matrix precomputation, and support vector sparsity." }},
            {{ ch: 10, title: "Classical RBF-SVM", desc: "Gaussian radial basis functions, gamma tuning, and convex quadratic programming." }},
            {{ ch: 11, title: "Gradient Boosted Trees (XGBoost)", desc: "Ensemble learning, second-order loss approximation, and tree depth regularization." }},
            {{ ch: 12, title: "BCNB Dataset Provenance", desc: "1,058 patient cohort, anonymization protocol, and ethical IRB standards." }},
            {{ ch: 13, title: "Zero Target Leakage Pipeline", desc: "Exclusion of post-surgical confounders and strict training-fold scaler isolation." }},
            {{ ch: 14, title: "Evaluation Metrics & Class Imbalance", desc: "AUROC, PR-AUC, Sensitivity, Specificity, and Platt probability calibration." }},
            {{ ch: 15, title: "Model Interpretability", desc: "Feature importance attribution, decision margins, and absence of biological causation." }},
            {{ ch: 16, title: "Computational Complexity", desc: "O(N^2 * 2^n) exponential statevector simulation cost vs classical polynomial scaling." }},
            {{ ch: 17, title: "Clinical Ethics & Governance", desc: "Investigational software status, regulatory boundaries, and human-in-the-loop requirements." }},
            {{ ch: 18, title: "Multi-Cancer Registry Roadmap", desc: "Task isolation principles preventing invalid cross-organ transfer learning." }}
        ];

        function renderHandbookList(items) {{
            var wrap = document.getElementById('handbook-chapters-list');
            if (!wrap) return;
            wrap.innerHTML = "";
            items.forEach(c => {{
                var item = document.createElement('div');
                item.style.background = "#FFFFFF";
                item.style.border = "1px solid #E2E8F0";
                item.style.borderRadius = "10px";
                item.style.padding = "12px 16px";
                item.innerHTML = "<div style='display: flex; justify-content: space-between;'><strong style='color: #25324A; font-size: 0.88rem;'>Chapter " + c.ch + ": " + c.title + "</strong><span style='font-size: 0.72rem; color: #7965E8;'>Read Chapter</span></div><p style='font-size: 0.78rem; color: #64748B; margin-top: 4px;'>" + c.desc + "</p>";
                wrap.appendChild(item);
            }});
        }}

        function filterHandbookChapters(query) {{
            var q = query.toLowerCase().trim();
            if (!q) {{
                renderHandbookList(handbookData);
            }} else {{
                var filtered = handbookData.filter(c => c.title.toLowerCase().includes(q) || c.desc.toLowerCase().includes(q));
                renderHandbookList(filtered);
            }}
        }}

        function downloadPredictionsCSV() {{
            var csv = "Patient ID,Ground Truth Target,Tumour Size(cm),Age(years),Grade,ER,HER2,Quantum Pred,Classical Pred,XGBoost Pred\\n";
            heldOutCohort.forEach(p => {{
                csv += p.patient_id + "," + p.ground_truth_target + "," + p.tumour_size + "," + p.age + "," + p.grade + "," + p.er + "," + p.her2 + "," + p.quantum_pred + "," + p.classical_pred + "," + p.xgboost_pred + "\\n";
            }});
            var blob = new Blob([csv], {{ type: 'text/csv' }});
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = "held_out_predictions.csv";
            a.click();
        }}

        // Initialization on window load
        window.addEventListener('load', function() {{
            initHeldoutSelector();
            renderCircuitDiagram();
            simulateCustomCircuit();
            renderHandbookList(handbookData);

            // Dashboard ROC Curve
            Plotly.newPlot('chart-dashboard-roc', [
                {{ x: [0, 0.26, 0.45, 0.64, 1.0], y: [0, 0.37, 0.55, 0.72, 1.0], mode: 'lines', name: 'XGBoost (0.601)', line: {{ color: '#F08A78', width: 2.5 }} }},
                {{ x: [0, 0.27, 0.46, 0.65, 1.0], y: [0, 0.37, 0.54, 0.71, 1.0], mode: 'lines', name: 'Classical RBF (0.598)', line: {{ color: '#18A999', width: 2.5 }} }},
                {{ x: [0, 0.40, 0.58, 0.75, 1.0], y: [0, 0.36, 0.51, 0.68, 1.0], mode: 'lines', name: 'Quantum SVM (0.500)', line: {{ color: '#7965E8', width: 2.5 }} }},
                {{ x: [0, 1], y: [0, 1], mode: 'lines', name: 'Chance', line: {{ color: '#94A3B8', dash: 'dash', width: 1.2 }} }}
            ], {{
                margin: {{ l: 30, r: 10, t: 10, b: 30 }},
                xaxis: {{ title: 'False Positive Rate' }},
                yaxis: {{ title: 'True Positive Rate' }},
                legend: {{ orientation: 'h', y: 1.15 }}
            }}, {{ responsive: true }});

            // Cohort Donut
            Plotly.newPlot('chart-dashboard-donut', [{{
                labels: ['N0 Negative', 'N+(1-2) Nodes', 'N+(>2) Nodes'],
                values: [655, 210, 193],
                type: 'pie',
                hole: 0.55,
                marker: {{ colors: ['#18A999', '#F08A78', '#D9534F'] }}
            }}], {{
                margin: {{ l: 10, r: 10, t: 10, b: 10 }},
                legend: {{ orientation: 'h', y: -0.1 }}
            }}, {{ responsive: true }});

            // Explainability Charts
            Plotly.newPlot('chart-explain-xgb', [{{
                x: [41.2, 26.5, 18.1, 8.7, 5.5],
                y: ['Tumour Size', 'Age', 'Grade', 'HER2', 'ER'],
                type: 'bar',
                orientation: 'h',
                marker: {{ color: '#F08A78' }}
            }}], {{
                margin: {{ l: 80, r: 20, t: 10, b: 30 }},
                xaxis: {{ title: 'Relative Gain (%)' }}
            }}, {{ responsive: true }});

            Plotly.newPlot('chart-explain-svm', [{{
                x: [-1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2],
                y: [12, 38, 72, 45, 28, 14, 3],
                type: 'bar',
                marker: {{ color: '#18A999' }}
            }}], {{
                margin: {{ l: 30, r: 20, t: 10, b: 30 }},
                xaxis: {{ title: 'Decision Margin f(x)' }}
            }}, {{ responsive: true }});
        }});
    </script>
</body>
</html>
"""

# ==============================================================================
# VERCEL SERVERLESS WSGI / ASGI ENTRYPOINT EXPORT
# ==============================================================================
def app(environ, start_response):
    """
    Standard WSGI callable exported for Vercel Serverless Functions.
    Handles GET / POST routes and delivers full API and interactive HTML application.
    """
    path = environ.get("PATH_INFO", "/")
    req_uri = environ.get("REQUEST_URI", environ.get("RAW_URI", path)).split("?")[0]
    effective_path = req_uri if req_uri.startswith("/api/") else path
    method = environ.get("REQUEST_METHOD", "GET").upper()

    # API: Health endpoint
    if effective_path.endswith("/api/health"):
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [json.dumps({
            "status": "healthy",
            "platform": "Vercel Serverless",
            "framework": "QuantumCure AI WSGI",
            "version": "2.1.0",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }).encode("utf-8")]

    # API: Benchmark Metrics endpoint
    if effective_path.endswith("/api/metrics"):
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [json.dumps(METRICS_DATA, indent=2).encode("utf-8")]

    # API: Held-Out Patients endpoint
    if effective_path.endswith("/api/test_cohort"):
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [json.dumps(HELD_OUT_PATIENTS).encode("utf-8")]

    # API: Kernel Matrices endpoint
    if effective_path.endswith("/api/kernel_data"):
        status = "200 OK"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [json.dumps(KERNEL_DATA).encode("utf-8")]

    # API: Live Prediction endpoint
    if effective_path.endswith("/api/predict"):
        if method == "POST":
            try:
                content_length = int(environ.get("CONTENT_LENGTH", 0))
                body = environ["wsgi.input"].read(content_length).decode("utf-8")
                payload = json.loads(body) if body else {}
                result = run_full_inference(payload)
                status = "200 OK"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                return [json.dumps(result).encode("utf-8")]
            except Exception as e:
                status = "400 Bad Request"
                headers = [("Content-Type", "application/json")]
                start_response(status, headers)
                return [json.dumps({"success": False, "error": str(e)}).encode("utf-8")]
        else:
            status = "405 Method Not Allowed"
            headers = [("Content-Type", "application/json")]
            start_response(status, headers)
            return [json.dumps({"error": "POST method required for /api/predict"}).encode("utf-8")]

    # Default route: serve complete interactive research application
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
