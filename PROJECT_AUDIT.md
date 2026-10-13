# QuantumCure AI — Comprehensive Project Audit (PROJECT_AUDIT.md)

**Project Name:** QuantumCure AI — Quantum Kernel Learning for Cancer Research  
**Live Production URL:** [https://qiskitfestfall-2lqc.vercel.app/](https://qiskitfestfall-2lqc.vercel.app/)  
**GitHub Repository:** [https://github.com/NAKKA-POOJITHA/qiskitfestfall.git](https://github.com/NAKKA-POOJITHA/qiskitfestfall.git) (`main` branch)  
**Audit Date:** October 14, 2026  
**Auditor:** Antigravity Advanced Agentic AI  
**Mandatory Disclaimer:** *Research prototype, not clinical advice. Not validated for clinical use.*

---

## 1. Executive Summary

QuantumCure AI is an applied medical AI research platform designed to investigate whether quantum kernel learning (specifically, Qiskit-based `ZZFeatureMap` Quantum Kernel Support Vector Machines) provides a measurable advantage over state-of-the-art classical machine learning models (Classical RBF-SVM and XGBoost) for predicting **axillary lymph node (ALN) metastasis in breast cancer patients**.

This audit assesses the complete full-stack codebase, dataset provenance, zero-leakage preprocessing, model training artifacts, quantum simulator infrastructure, interactive visualizations, and dual-deployment runtime (Vercel Serverless and Streamlit Local).

---

## 2. Architecture & File Inventory

### 2.1 Directory Structure
```
c:\Users\DELL\OneDrive\Desktop\freewill/
├── .streamlit/
│   └── config.toml                  # Streamlit theme & port configuration
├── app.py                           # Dual-mode runtime: Vercel WSGI entrypoint + Streamlit hook
├── vercel.json                      # Vercel deployment configuration (routes, build, exclusions)
├── requirements.txt                 # Lean dependencies for Vercel Serverless (~35MB bundle)
├── requirements-full.txt            # Complete research stack (Qiskit 2.1.2, XGBoost, Scikit-learn)
├── backend/
│   ├── data_audit.py                # BCNB dataset validation engine
│   ├── data_preprocessing.py        # Stratified 80/20 train/test split, zero-leakage MinMax scaling
│   ├── classical_models.py          # Classical RBF-SVM & XGBoost training pipeline
│   ├── quantum_kernel.py            # Qiskit 2.1.2 ZZFeatureMap & Fidelity kernel calculation
│   ├── evaluation.py                # AUROC, PR-AUC, confusion matrices, runtime profiling
│   └── prediction_service.py        # Multi-model inference service & agreement calculator
├── dataset/
│   ├── raw/
│   │   └── patient-clinical-data.xlsx  # Original 1,058-patient BCNB clinical file
│   └── processed/
│       ├── bcnb_train.csv           # 846 training patients (zero test leakage)
│       ├── bcnb_test.csv            # 212 held-out evaluation patients
│       ├── feature_dictionary.json  # Feature descriptions, types, and clinical relevance
│       └── preprocessing_report.md  # Step-by-step split and transformation record
├── models/
│   ├── classical_svm.joblib         # Calibrated RBF-SVM model artifact
│   ├── xgboost_model.joblib         # Tuned XGBoost classifier artifact
│   ├── xgboost_model.json           # Native portable XGBoost JSON model
│   ├── quantum_svm.joblib           # Precomputed Quantum Kernel SVM artifact
│   ├── preprocessing_pipeline.joblib# Scikit-learn MinMaxScaler fitted strictly on train data
│   ├── quantum_training_features.npy# 100 reference train feature vectors (5-qubit scaled [0, π])
│   └── quantum_train_patient_ids.npy# Reference patient identifiers
├── results/
│   ├── data_audit.json              # Full column audit summary
│   ├── data_audit_report.md         # Narrative data integrity report
│   ├── experiment_config.json       # Exact seeds, hyperparameters, and environment specs
│   ├── metrics.json                 # Real evaluated metrics on held-out test cohort
│   ├── metrics.csv                  # Tabular metrics for export
│   ├── predictions.csv              # Exact predictions of all 212 held-out patients across 3 models
│   ├── quantum_kernel_train.npy     # 100x100 training kernel Gram matrix
│   ├── quantum_kernel_test.npy      # 212x100 test kernel transition matrix
│   ├── classical_rbf_kernel_train.npy# 100x100 classical RBF kernel matrix
│   ├── roc_curves.png               # Verified overlaid ROC curves
│   └── confusion_matrices.png       # Side-by-side confusion matrices
├── frontend/
│   ├── app.py                       # Streamlit entrypoint
│   ├── styles.py                    # Light medical research design system & CSS injection
│   ├── dashboard_view.py            # Main research dashboard view
│   ├── components/
│   │   ├── sidebar.py               # Navigation sidebar
│   │   ├── metric_cards.py          # KPI metrics display
│   │   ├── charts.py                # Plotly ROC curves, PR curves, heatmaps, Bloch sphere
│   │   └── patient_form.py          # Clinical input form
│   └── pages/
│       ├── 1_Research_Dashboard.py  # Overview KPIs, dataset distribution, ROC curves
│       ├── 2_Patient_Prediction_Lab.py # Blind held-out evaluation & manual prediction
│       ├── 3_Model_Comparison_Lab.py# Deep comparative analytics & threshold slider
│       ├── 4_Quantum_Park.py        # Interactive Qiskit circuit composer & Bloch sphere
│       ├── 5_Quantum_Insights.py    # ZZFeatureMap & kernel heatmaps
│       ├── 6_3D_Anatomy_Explorer.py # Interactive Three.js breast & axillary lymph node model
│       ├── 7_Research_Handbook.py   # 18-chapter searchable research handbook
│       ├── 8_Dataset_and_Methods.py # Data provenance, CC BY 4.0, zero-leakage protocol
│       ├── 9_Reports_and_Analytics.py # Experiment exports (CSV/JSON/print-friendly)
│       └── 10_Multi_Cancer_Explorer.py# Extensible cancer research registry (BCNB Active, LUAD Planned)
└── tests/
    ├── test_data_pipeline.py        # Tests for dataset integrity and leakage prevention
    ├── test_quantum_kernel.py       # Tests for quantum kernel dimensions and symmetry
    └── test_models_and_prediction.py# Tests for artifact loading and inference service
```

---

## 3. Feature & Page Status Audit

| Feature / Page | Functional Status | Verification Method | Known Blockers / Notes |
| :--- | :--- | :--- | :--- |
| **Dataset Validation (`backend/data_audit.py`)** | Verified Working | Automated script & pytest | Zero missing targets, 1,058 patients verified. |
| **Zero-Leakage Preprocessing (`backend/data_preprocessing.py`)** | Verified Working | Automated script & pytest | Confounder columns (`Number of lymph node metastases`, `Surgical`) excluded. |
| **Classical RBF-SVM Pipeline** | Verified Working | Trained & evaluated | AUROC: 0.5982, Acc: 59.43% on 212 held-out patients. |
| **XGBoost Pipeline** | Verified Working | Trained & evaluated | AUROC: 0.6012, Acc: 59.43% on 212 held-out patients. |
| **Qiskit ZZFeatureMap Quantum Kernel SVM** | Verified Working | Trained & evaluated | AUROC: 0.5001, Acc: 50.47% on 212 held-out patients. |
| **Patient Prediction Lab (Held-Out Blind Eval)** | Verified Working | Tested with all 212 patients | True label hidden until user clicks "Reveal Actual Outcome". |
| **Patient Prediction Lab (Manual Case)** | Verified Working | Interactive input testing | Scaler and model pipelines execute successfully. |
| **Model Agreement Indicator** | Verified Working | Code audit & test | Identifies Unanimous, Majority (2 vs 1), or Disagreement. |
| **Model Comparison Lab (ROC / PR / Confusion Matrix)** | Verified Working | Unit test & UI render | Uses real test evaluation results from `results/metrics.json`. |
| **Threshold Analysis Slider** | Verified Working | UI interaction | Explores trade-offs without retraining or data leakage. |
| **Quantum Park (Circuit Composer)** | Partially Working | UI render | Needed interactive gate manipulation and real Qiskit statevector execution. |
| **Quantum Insights (Kernel Heatmaps)** | Verified Working | Rendered from saved .npy | Visualizes genuine 100x100 and 212x100 kernel matrices. |
| **3D Anatomy Explorer (Three.js)** | Verified Working | Browser WebGL render | Supports OrbitControls, layer toggles, and structure highlighting. |
| **Research Handbook (18 Chapters)** | Verified Working | Text search & display | Searchable by keyword, with technical glossary. |
| **Dataset & Methods Page** | Verified Working | UI render | Fully documents BCNB source, license, and split protocol. |
| **Reports & Analytics (CSV/JSON Export)** | Verified Working | File download tests | Serves genuine `metrics.csv`, `metrics.json`, `predictions.csv`. |
| **Multi-Cancer Registry** | Verified Working | UI render | BCNB marked as Active; TCGA-LUAD marked as Planned. |
| **Vercel Serverless Deployment** | Verified Working | Vercel CLI & HTTP tests | WSGI callable (`app`) responds with HTTP 200 within 500MB limit. |
| **Streamlit Local Multi-Page App** | Verified Working | Local browser on port 8501 | Runs with rich interactivity and Plotly visualization. |

---

## 4. Priority Issues Identified & Resolution Plan

1. **Emoji Contamination (Priority: High):**  
   *Root Cause:* Visual decorators copied from consumer template code.  
   *Fix:* Enforce strict no-emoji policy across all files, headers, sidebars, buttons, and alert components. Use text labels or minimalist SVG icons.

2. **Design Palette Standardization (Priority: High):**  
   *Root Cause:* Slight color deviations in CSS variables (e.g., `#7F56D9` instead of `#7965E8`, `#FF7A59` instead of `#F08A78`).  
   *Fix:* Align `--quantum-accent: #7965E8`, `--rbf-accent: #18A999`, `--xgb-accent: #F08A78`, `--bg-main: #F8FAFC`, `--text-primary: #25324A`, `--text-secondary: #64748B`, `--border-color: #E5E7EB`.

3. **Mandatory Disclaimer Visibility (Priority: High):**  
   *Root Cause:* Disclaimer was placed in small footer text.  
   *Fix:* Prominently mount *"Research prototype, not clinical advice. Not validated for clinical use."* on top navigation and header banners.

4. **Quantum Park Dynamic Circuit Calculation (Priority: Medium):**  
   *Root Cause:* Wire grid used static HTML spans.  
   *Fix:* Connect an interactive circuit editor that dynamically builds a Qiskit `QuantumCircuit`, simulates statevectors, computes exact probabilities, and exports valid Qiskit 2.x and OpenQASM 2.0 code.

5. **Navigation Structure Completeness (Priority: Medium):**  
   *Root Cause:* Model Comparison and Quantum Park were partially grouped with other pages.  
   *Fix:* Dedicate standalone pages for `3_Model_Comparison_Lab.py` and `4_Quantum_Park.py` to match the 20-part Master Prompt.
