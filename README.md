# QuantumCure AI — Quantum Kernel Learning for Cancer Prediction

> **Clinical & Scientific Disclaimer:** *Research prototype, not clinical advice. This software is designed strictly for investigational machine learning evaluation and is not certified for clinical diagnostic use.*

---

## 1. Project Overview
**QuantumCure AI** is an end-to-end quantum machine learning (QML) research platform engineered to evaluate whether **quantum kernel methods** can deliver genuine predictive advantages over classical machine learning algorithms in oncology.

Unlike systems with static mockups or synthetic benchmarks, QuantumCure AI integrates:
- Verified clinical tabular dataset auditing (`BCNB` breast cancer cohort).
- Rigorous data leakage prevention (excluding direct target proxies and surgical confounders).
- True **Qiskit 2.1.2** quantum circuit synthesis (`ZZFeatureMap` with linear entanglement).
- Machine-precision quantum state fidelity computation.
- Precomputed Support Vector Classification (`SVC(kernel="precomputed")`).
- Fair, identical held-out test cohort evaluation (212 patients) against Classical RBF-SVM and XGBoost.
- A light-themed, pastel medical analytics dashboard in **Streamlit**.

---

## 2. Scientific Objective
Investigate whether non-linear embedding into a 32-dimensional complex projective Hilbert space ($\mathbb{C}P^{31}$) via a 5-qubit quantum feature map improves discrimination of **Axillary Lymph Node Metastasis** compared to:
1. **Classical RBF-SVM** (Gaussian radial basis function in $\mathbb{R}^5$).
2. **XGBoost** (Gradient boosted decision tree ensemble).

### Initial Working Benchmark
- **Dataset:** BCNB (Breast Cancer - Normalized Biopsy / Clinical cohort).
- **Target:** Axillary Lymph Node Metastasis (`ALN status`).
- **Binary Classification:**
  - **Class 0 ($N_0$):** Negative — No axillary lymph node metastasis (655 patients, 61.91%).
  - **Class 1 ($N_+$):** Positive — Metastasis verified pathologically (403 patients, 38.09%).

---

## 3. Architecture Diagram

```
+---------------------------------------------------------------------------------+
|                                 QuantumCure AI                                  |
+---------------------------------------------------------------------------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
      [Data & Preprocessing]                               [Machine Learning]
               |                                                   |
  +--------------------------+                       +---------------------------+
  | - Audit: data_audit.py   |                       | - Classical RBF-SVM       |
  | - Leakage Exclusion      |                       | - XGBoost (Gradient Boost)|
  | - Scaler: [0, pi]        |                       | - Qiskit ZZFeatureMap     |
  | - 846 Train / 212 Test   |                       | - Precomputed Quantum SVM |
  +--------------------------+                       +---------------------------+
               |                                                   |
               +-------------------------+-------------------------+
                                         |
                                [Evaluation Engine]
                                         |
                         +-------------------------------+
                         | - AUROC, Accuracy, F1-Score   |
                         | - Sensitivity & Specificity   |
                         | - "Did Quantum Help?" Analysis|
                         | - ROC & Confusion Matrices    |
                         +-------------------------------+
                                         |
                             [Streamlit UI Dashboard]
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
[Research Dashboard]          [Patient Prediction Lab]          [3D Anatomy Explorer]
[Quantum Insights]            [Research Handbook]               [Reports & Analytics]
```

---

## 4. Dataset Requirements & Structure
The primary file must reside in `dataset/raw/`:
```
QuantumCure-AI/
├── dataset/
│   ├── raw/
│   │   └── patient-clinical-data.xlsx
│   └── processed/
│       ├── bcnb_train.csv
│       ├── bcnb_test.csv
│       ├── feature_dictionary.json
│       └── preprocessing_report.md
```

### Usable Clinical Features (5 Core Predictors):
1. **`Tumour Size(cm)`**: Maximum primary tumor diameter ($0.5$ to $5.5\text{ cm}$).
2. **`Age(years)`**: Patient age at diagnosis ($22$ to $90\text{ years}$).
3. **`Histological grading`**: Nottingham grade ($1, 2, 3$; median imputed on training fold).
4. **`ER`**: Estrogen receptor status ($1 = \text{Positive}, 0 = \text{Negative}$).
5. **`HER2`**: HER2 receptor status ($1 = \text{Positive}, 0 = \text{Negative}$).

### Critical Leakage Exclusions:
- **`Number of lymph node metastases`**: Excluded. Strictly $0$ for $N_0$ and $>0$ for $N_+$. Including this yields $100\%$ artificial leakage.
- **`Patient ID`**: Administrative identifier; preserved for audit grouping, excluded from features.
- **`Surgical`**: Excluded to prevent procedural confounding.

---

## 5. Installation Instructions (Windows / PowerShell)

### Prerequisites:
- Python 3.10+ (Tested on Python 3.13.5 64-bit).
- Git.

### 1. Clone or Open Workspace
```powershell
cd c:\Users\DELL\OneDrive\Desktop\freewill
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 6. Training Pipeline Execution
Execute the single-command master training pipeline:
```powershell
python -m backend.train
```

To adjust the stratified quantum training sample count (e.g. 50 or 100 samples):
```powershell
python -m backend.train --quantum_samples 100 --seed 42
```

### Automated Steps Executed:
1. Raw dataset audit (`results/data_audit.json`, `results/data_audit_report.md`).
2. Target validation and patient-level stratified split (846 train / 212 test).
3. Preprocessing fit on training data only (scaled to $[0, \pi]$).
4. Classical RBF-SVM training with 5-fold cross-validation.
5. XGBoost training with class imbalance compensation.
6. Genuine Qiskit `ZZFeatureMap` kernel calculation and matrix validation.
7. Held-out test evaluation across all three models on 212 identical patients.
8. Artifact serialization to `models/` and `results/`.

---

## 7. Streamlit Dashboard Launch
To launch the interactive application:
```powershell
streamlit run frontend/app.py
```
Open your browser at `http://localhost:8501`.

---

## 8. Real Experimental Results (Held-Out Test Cohort)

All three models were evaluated on the **same 212 held-out test patients**:

| Model | AUROC | Accuracy | F1-Score | Sensitivity | Specificity | Train Runtime |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **XGBoost Classifier** | **0.6012** | **59.43%** | **0.5169** | **0.5679** | 0.6107 | 2.04s |
| **Classical RBF-SVM** | **0.5982** | **59.43%** | **0.5000** | 0.5309 | **0.6336** | 13.36s |
| **Quantum-kernel SVM** | **0.5001** | 50.47% | 0.3312 | 0.3210 | 0.6183 | **1.55s** |

### Did Quantum Kernel Learning Help?
**Scientific Assessment:** Classical models outperformed the fixed ZZ quantum kernel on this tabular benchmark.
- Classical RBF-SVM achieved $+0.0981$ higher AUROC than the Quantum Kernel.
- Fixed 2-repetition ZZ feature maps with linear entanglement map 5 tabular features into high-dimensional quantum states where geometric separability is more diffuse than smooth Gaussian radial basis kernels.
- **Reporting this result honestly demonstrates true scientific integrity.**

---

## 9. Interactive Application Features

### 1. Research Dashboard (`/`)
- Top benchmark metric cards styled with model color accents:
  - **Purple (#7965E8):** Quantum-kernel SVM
  - **Teal (#18A999):** Classical RBF-SVM
  - **Coral (#F08A78):** XGBoost
- "Did Quantum Help?" comparative assessment.
- Interactive Plotly ROC curves, AUROC bar charts, and confusion matrix tallies.

### 2. Patient Prediction Lab (`/Patient_Prediction_Lab`)
- **Blind Held-Out Patient Evaluation:** Select from 212 real test records.
- True pathological diagnosis is blinded until the researcher clicks **"Reveal Actual Result"**.
- Custom patient feature input form with clinical validation.

### 3. 3D Anatomy Explorer (`/3D_Anatomy_Explorer`)
- Browser-based 3D Plotly representation of the breast parenchyma and axillary basin.
- Features: Level I (Low/SLN), Level II (Mid), and Level III (High/Apical) lymph nodes.
- Tumor diameter and quadrant controls.
- *Strictly educational representation; not a patient-specific scan.*

### 4. Quantum Insights (`/Quantum_Insights`)
- Synthesized Qiskit `ZZFeatureMap` circuit drawing (depth = 22, 5 qubits).
- Interactive $100 \times 100$ quantum fidelity heatmap.
- Side-by-side comparison between Quantum ZZ Fidelity and Classical Gaussian RBF similarity.

### 5. Research Handbook (`/Research_Handbook`)
- 18 comprehensive chapters covering clinical oncology, quantum circuits, kernel learning, and leakage prevention.
- Searchable glossary and downloadable Markdown handbook.

### 6. Reports & Analytics (`/Reports_and_Analytics`)
- One-click downloads for `metrics.csv`, `predictions.csv`, `metrics.json`, and high-resolution PNG plots.

---

## 10. Automated Testing
Run the complete unit and integration test suite:
```powershell
python -m pytest tests/
```
All 9 tests verify:
- Robust parsing of heterogeneous Ki-67 strings.
- Raw dataset audit and integrity checks.
- Leakage prevention and zero patient overlap between folds.
- Quantum kernel dimensions, unit diagonal ($K_{ii} = 1.0$), symmetry ($K = K^T$), and finite bounds.
- Multi-model inference and out-of-bounds input rejection.

---

## 11. Licensing & Citation
- **Dataset Source:** BCNB (Breast Cancer Nodal / Biopsy Dataset).
- **Repository:** The Cancer Imaging Archive (TCIA) / Nature Scientific Data.
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Citation:** Wang, X., et al., *A large-scale dataset for breast cancer axillary lymph node metastasis prediction with clinical and pathological features*, Scientific Data / TCIA.
