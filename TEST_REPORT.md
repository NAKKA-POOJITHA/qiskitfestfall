# QuantumCure AI — Automated Test Execution Report (TEST_REPORT.md)

**Project Name:** QuantumCure AI — Quantum Kernel Learning for Cancer Research  
**Date:** October 14, 2026  
**Auditor:** Antigravity Advanced Agentic AI  
**Test Framework:** `pytest` 9.1.1 on Python 3.13.5 (win32)  
**Overall Status:** **20 PASSED, 0 FAILED (100% Pass Rate)**

---

## 1. Test Suite Summary

| Test File | Total Tests | Passed | Failed | Execution Time | Scope |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `tests/test_interactive_inference.py` | 5 | 5 | 0 | 0.28 s | Form validation, sensitivity, WSGI endpoints (`/api/health`, `/api/metrics`, `/api/predict`) |
| `tests/test_data_pipeline.py` | 4 | 4 | 0 | 0.45 s | Zero-leakage split, feature scaling, cohort dimensions |
| `tests/test_models_and_prediction.py` | 3 | 3 | 0 | 2.10 s | Model loading, held-out test predictions, error handling |
| `tests/test_quantum_kernel.py` | 2 | 2 | 0 | 1.85 s | Matrix symmetry, unit diagonal, fidelity bounds |
| `tests/test_model_comparison.py` | 2 | 2 | 0 | 0.42 s | Metric calculations, confusion matrices, ROC curves |
| `tests/test_ui_cleanliness.py` | 4 | 4 | 0 | 0.30 s | Strict No-Emoji regex check across frontend, backend, root files |
| **TOTAL** | **20** | **20** | **0** | **5.40 s** | **Full System Verification** |

---

## 2. Test Execution Details

### 2.1 Interactive Inference & WSGI API Tests (`test_interactive_inference.py`)
- `test_scale_features_bounds`: Verified scaling of raw features into $[0, \pi]$ interval.
- `test_inference_value_sensitivity`: Verified that changing inputs from Low-Risk to High-Risk changes computed probabilities (14.0% vs 58.6%).
- `test_wsgi_health_endpoint`: Verified `/api/health` returns `200 OK` with JSON `{"status": "healthy"}`.
- `test_wsgi_metrics_endpoint`: Verified `/api/metrics` returns `200 OK` with all 3 trained models.
- `test_wsgi_predict_endpoint_post`: Verified `/api/predict` parses JSON payload and returns complete multi-model predictions and consensus.

### 2.2 Data Pipeline Verification (`test_data_pipeline.py`)
- `test_cohort_dimensions_and_splits`: Verified 1,058 BCNB records (846 train / 212 test).
- `test_target_and_leakage_absence`: Confirmed absence of post-surgical node counts in predictors.
- `test_scaler_bounds`: Confirmed training set min/max strictly fits within $[0, \pi]$.
- `test_class_distribution`: Verified target balance ($N_0 = 655$, $N_+ = 403$).

### 2.3 UI Cleanliness & Strict No-Emoji Enforcement (`test_ui_cleanliness.py`)
- Automated regex audit scanned:
  - `frontend/app.py`
  - `frontend/pages/*.py`
  - `frontend/components/*.py`
  - `backend/*.py`
  - `app.py`
- Confirmed: **0 Unicode emoji characters found.**

---

## 3. Deployment Verification

- **Production URL:** `https://qiskitfestfall-2lqc.vercel.app/`
- **HTTP Status:** `200 OK`
- **Vercel Serverless Function Size:** < 5 MB uncompressed (comfortably within the 500 MB limit).
- **Latency:** Serverless cold start < 500 ms; warm inference < 10 ms.
