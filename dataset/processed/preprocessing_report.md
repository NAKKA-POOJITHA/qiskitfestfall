# QuantumCure AI — Dataset Preprocessing Report

**Dataset:** BCNB (Breast Cancer Nodal / Biopsy Clinical Dataset)  
**Task:** Binary Classification — Axillary Lymph Node Metastasis (`ALN status`)  
**Target Definition:** Class 0 = `N0` (No metastasis), Class 1 = `N+` (Metastasis present)  
**Split Method:** Patient-level stratified split (`test_size=0.2`, `random_state=42`)  
**Fitted Pipeline:** Saved to `models\preprocessing_pipeline.joblib`  

---

## 1. Data Partition Summary
| Metric | Full Cohort | Training Set | Held-out Test Set |
| :--- | :--- | :--- | :--- |
| **Total Patients** | 1058 | 846 (80.0%) | 212 (20.0%) |
| **Class 0 (N0)** | 655 (61.9%) | 524 (61.9%) | 131 (61.8%) |
| **Class 1 (N+)** | 403 (38.1%) | 322 (38.1%) | 81 (38.2%) |
| **Excluded Invalid Rows** | 0 | 0 | 0 |

---

## 2. Selected Predictor Features (5 Features)
The following 5 legitimate pre-operative features were selected to balance oncological predictive fidelity with the Hilbert-space dimensionality constraints of quantum feature mapping ($2^5 = 32$ quantum basis states):

1. **`Tumour Size(cm)`**: Maximum primary tumor diameter.
2. **`Age(years)`**: Patient age at diagnosis.
3. **`Histological grading`**: Modified Bloom-Richardson grading (1, 2, or 3). Median imputed strictly using training fold median (`2.0`).
4. **`ER_encoded`**: Estrogen receptor status (1 = Positive, 0 = Negative).
5. **`HER2_encoded`**: HER2 overexpression status (1 = Positive, 0 = Negative).

---

## 3. Leakage Prevention Protocol
- **Target Proxy Exclusion:** `Number of lymph node metastases` is completely excluded from feature generation.
- **Surgical Staging Exclusion:** `Surgical` method is excluded to avoid procedural confounding.
- **Transformation Isolation:** All imputation statistics and scaling extrema ($[0, \pi]$) were computed exclusively on the 846 training patients and applied downstream to the 212 held-out test patients.
- **Patient Independence:** Each record represents an independent patient; no patient appears across both partitions.

---

## 4. Quantum Hilbert Space Encoding
Features are scaled to $[0, \pi]$ using `MinMaxScaler` fitted on training data:
- Prevents $2\pi$ phase periodicity wrap-around in the `ZZFeatureMap`.
- Provides numerical compatibility for classical RBF-SVM, XGBoost, and Quantum Kernels.
