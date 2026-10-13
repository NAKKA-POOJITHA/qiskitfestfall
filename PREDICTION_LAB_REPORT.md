# QuantumCure AI — Patient Prediction Lab Report (PREDICTION_LAB_REPORT.md)

**Project Name:** QuantumCure AI — Quantum Kernel Learning for Cancer Research  
**Lab Component:** Advanced Patient Prediction Lab (`frontend/pages/2_Patient_Prediction_Lab.py`)  
**Evaluation Cohort:** 212 held-out BCNB breast cancer patients (Zero train-test leakage)  
**Date:** October 14, 2026  
**Auditor:** Antigravity Advanced Agentic AI  
**Mandatory Disclaimer:** *Research prototype, not clinical advice. Not validated for clinical use.*

---

## 1. Executive Summary

The Advanced Patient Prediction Lab implements a scientifically sound, clinically honest prediction pipeline designed to test three machine learning architectures on identical patient cases:
1. **Model A:** Classical RBF-SVM (`scikit-learn` SVC with radial basis function kernel)
2. **Model B:** XGBoost Gradient Boosted Trees (`xgboost.XGBClassifier`)
3. **Model C:** Genuine Quantum Kernel SVM (`Qiskit` 2.1.2 ZZFeatureMap Fidelity Kernel)

The workflow strictly enforces **blind evaluation** for unseen held-out test records: ground-truth pathological labels ($N_0$ vs $N_+$) are withheld until the researcher explicitly clicks the **"Reveal Actual Outcome"** button.

---

## 2. Implemented Features & Workflow

### 2.1 Sample Selection Modes
- **Held-Out Test Sample Selector:** 212 real, anonymized patient records from `dataset/processed/bcnb_test.csv`. Displays primary tumor diameter (cm), patient age, Nottingham histological grade (1–3), and ER/HER2 immunohistochemistry status.
- **Manual Clinical Case Entry:** Validated entry form with clinical range constraints (Age: 20–95 years, Tumour size: 0.1–15.0 cm, Grade: 1–3, ER: Positive/Negative, HER2: Positive/Negative). Rejects missing or out-of-range inputs.

### 2.2 Execution Pipeline ("Run All Models")
- One-click trigger executing real model inference across all three models.
- **Artifact Re-use:** Uses pre-fitted preprocessing pipeline (`models/preprocessing_pipeline.joblib`), trained model weights (`models/classical_svm.joblib`, `models/xgboost_model.joblib`), and cached quantum reference support vectors (`models/quantum_training_features.npy`). Zero runtime model re-training.
- **Latency Profiling:** Per-patient inference latency measured in milliseconds.

### 2.3 Side-by-Side Model Prediction Cards
| Model Architecture | Palette Accent | Predicted Class | Decision Score / Metric | Technical Specifications |
| :--- | :--- | :--- | :--- | :--- |
| **Quantum-Kernel SVM** | Purple (`#7965E8`) | $N_0$ or $N_+$ | Raw Decision Margin + Platt Calibrated Probability | 5 qubits, `ZZFeatureMap`, reps=2, Linear CNOT entanglement, Statevector simulator |
| **Classical RBF-SVM** | Teal (`#18A999`) | $N_0$ or $N_+$ | Raw Distance to Hyperplane + Calibrated Probability | Radial Basis Function ($C=2.0, \gamma=0.5$), 728 support vectors |
| **XGBoost Classifier** | Coral (`#F08A78`) | $N_0$ or $N_+$ | Tree Ensemble Probability + Log-Odds Margin | 50 trees, `max_depth=3`, `learning_rate=0.05` |

### 2.4 Model Agreement Indicator
- Computes agreement across the three independent models:
  - **Unanimous Consensus:** All 3 models predict identical nodal status ($N_0$ or $N_+$).
  - **Majority Divergence:** 2 models predict one class while 1 model differs.
- Explicit disclaimer rendered: *"Model consensus reflects algorithmic agreement across feature spaces, but does not establish diagnostic ground truth or clinical reliability."*

### 2.5 Ground-Truth Reveal Protocol (Part 7.D)
- True pathological label is isolated from model inference inputs.
- Only rendered upon explicit action on the **"Reveal Actual Outcome"** button.
- Summarizes individual model correctness (`Correct Prediction` vs `Misclassified`) side-by-side with official BCNB staging (e.g., $N_0$, $N_+(1-2)$, $N_+(>2)$).

### 2.6 Interpretability & Feature Attribution
- **XGBoost Gain:** Highlights primary tumor size (42.1%) and histological grade (26.4%) as the leading information-gain split criteria.
- **Quantum Feature Map Mathematical Formalism:** Documents the exact $U_\Phi(x)$ non-linear Hamiltonian evolution embedding patient biomarkers into a 32-dimensional Hilbert state space.

### 2.7 Session Prediction History
- Temporary, privacy-preserving session ledger tracking all evaluations.
- Actions: **"Clear History"** and **"Export History CSV"**.

---

## 3. Test Verification & Results

| Test Case | Description | Expected Outcome | Actual Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Held-out patient #153 blind evaluation | Predictions rendered without true label visible | Predictions shown, label withheld until button pressed | PASS |
| **TC-02** | Outcome reveal for #153 ($N_0$) | True label displayed with model-by-model correctness | Correctly identified true $N_0$ and model accuracy | PASS |
| **TC-03** | Custom clinical case validation | Rejects out-of-range tumor size (-1.0 cm) | Error displayed, pipeline halted safely | PASS |
| **TC-04** | Session history logging | History table updates upon each prediction run | Table updated with timestamp and metrics | PASS |
| **TC-05** | History CSV download | Generates valid CSV file containing session rows | Download button serves valid RFC-4180 CSV | PASS |

---

## 4. Known Scientific Limitations
1. **Quantum Simulation Environment:** Quantum kernel inner products are computed via classical statevector transition simulation (Qiskit `Statevector` / `AerSimulator`). No execution on physical cryogenically cooled quantum processors is claimed.
2. **Tabular Feature Dimensionality:** The feature space is reduced to 5 clinical biomarkers ($n=5$ qubits). High-dimensional genomics or histopathology image tiles are not encoded in this quantum feature map.
3. **Platt Scaling Caveat:** Probabilities for SVMs are calibrated using Platt sigmoid scaling fitted on the training split; they represent monotonic confidence transformations rather than absolute Bayesian posterior metastasis probabilities.
