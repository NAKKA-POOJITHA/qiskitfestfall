# QuantumCure AI — Clinical Dataset Audit Report

**Dataset Audited:** BCNB (Breast Cancer Nodal / Biopsy Clinical Dataset)  
**Audit Status:** `VERIFIED_READY`  
**Source:** The Cancer Imaging Archive (TCIA) / Nature Scientific Data  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Primary File:** `dataset/raw/patient-clinical-data.xlsx`  

---

## 1. Discovered Files
| File Path | File Size (Bytes) | Status |
| :--- | :--- | :--- |
| `dataset/raw/patient-clinical-data.xlsx` | 77,507 bytes | Available |

---

## 2. Records and Data Integrity
- **Total Records:** 1058 patients
- **Exact Duplicate Rows:** 0
- **Duplicate Patient IDs:** 0
- **Data Completeness:** 100% of patients have valid target outcomes; 12.48% (132/1058) have missing histological grades.

---

## 3. Target Variable Verification
- **Target Column:** `ALN status`
- **Identified Successfully:** `True`

### Raw Class Distribution:
- **`N0`**: 655 patients (61.91%)
- **`N+(1-2)`**: 210 patients (19.85%)
- **`N+(>2)`**: 193 patients (18.24%)

### Mapped Binary Classification Target:
- **Class 0 (N0 - No Axillary Lymph Node Metastasis):** 655 patients (61.91%)
- **Class 1 (N+ - Axillary Lymph Node Metastasis Present):** 403 patients (38.09%)
- **Unknown / Invalid Labels:** 0 patients (0.0%)

> [!NOTE]
> All 1,058 records possess definitive ALN staging. N0 maps unambiguously to Class 0, and both N+(1-2) and N+(>2) map strictly to Class 1. No artificial target labels were generated.

---

## 4. Feature Audit & Leakage Prevention

### Critical Exclusions (Target Leakage):
- **`Number of lymph node metastases`**: Direct target proxy / severe post-outcome leakage. Strictly 0 for N0 and >0 for N+. *(Risk: CRITICAL - MUST EXCLUDE)*
- **`Patient ID`**: Anonymized administrative tracking identifier. Non-predictive; preserved strictly for patient-level grouping and split integrity. *(Risk: ID Leakage - MUST EXCLUDE from features)*
- **`ALN status`**: Ground-truth target variable for binary classification. *(Risk: Target Label)*
- **`Surgical`**: Surgical procedure type (ALND vs SLNB). Staging decision post-biopsy; excluded from pre-operative baseline to prevent procedural confounding. *(Risk: Procedural confounding)*

### Usable Candidate Predictor Features:
- **`Age(years)`** (int64, 0 missing, 63 unique values)
- **`Tumour Size(cm)`** (float64, 0 missing, 38 unique values)
- **`Tumour Type`** (object, 0 missing, 3 unique values)
- **`ER`** (object, 0 missing, 2 unique values)
- **`PR`** (object, 0 missing, 2 unique values)
- **`HER2`** (object, 0 missing, 2 unique values)
- **`HER2 Expression`** (object, 0 missing, 4 unique values)
- **`Histological grading`** (float64, 132 missing, 3 unique values)
- **`Ki67`** (object, 0 missing, 43 unique values)
- **`Molecular subtype`** (object, 0 missing, 4 unique values)

---

## 5. Column-Level Inspection Table
| Column Name | Data Type | Null Count | Null % | Unique Values | Sample / Frequencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Patient ID` | `int64` | 0 | 0.0% | 1058 | Continuous / High-cardinality |
| `Age(years)` | `int64` | 0 | 0.0% | 63 | Continuous / High-cardinality |
| `Tumour Size(cm)` | `float64` | 0 | 0.0% | 38 | Continuous / High-cardinality |
| `Tumour Type` | `object` | 0 | 0.0% | 3 | {'Invasive ductal carcinoma': 957, 'Other typ |
| `ER` | `object` | 0 | 0.0% | 2 | {'Positive': 831, 'Negative': 227} |
| `PR` | `object` | 0 | 0.0% | 2 | {'Positive': 790, 'Negative': 268} |
| `HER2` | `object` | 0 | 0.0% | 2 | {'Negative': 781, 'Positive': 277} |
| `HER2 Expression` | `object` | 0 | 0.0% | 4 | {'2+': 483, '1+': 242, '3+': 206, '0': 127} |
| `Histological grading` | `float64` | 132 | 12.48% | 3 | {'2.0': 518, '3.0': 370, 'nan': 132, '1.0': 3 |
| `Surgical` | `object` | 0 | 0.0% | 2 | {'Axillary lymph node dissection': 974, 'Sent |
| `Ki67` | `object` | 0 | 0.0% | 43 | Continuous / High-cardinality |
| `Molecular subtype` | `object` | 0 | 0.0% | 4 | {'Luminal B': 372, 'Luminal A': 288, 'HER2(+) |
| `Number of lymph node metastases` | `int64` | 0 | 0.0% | 10 | {'0': 655, '1': 134, '2': 76, '3': 52, '4': 3 |
| `ALN status` | `object` | 0 | 0.0% | 3 | {'N0': 655, 'N+(1-2)': 210, 'N+(>2)': 193} |

---

## 6. Known Limitations & Scientific Caveats
- Ki67 column contains heterogeneous string representations (e.g., '0.3', '30-40%', '<5%', '>90%') requiring robust numerical parsing.
- Histological grading has 132 missing values (12.48%) requiring median or mode imputation.
- Number of lymph node metastases is an exact pathological count and must never be permitted in predictor sets to avoid target leakage.
- BCNB dataset is single-center (Chinese cohort); external geographic generalizability is unverified.
- Pre-operative imaging (ultrasound/MRI/CT) and whole slide histopathology images from BCNB are not included in this clinical tabular subset.

---
*Audit conducted automatically by QuantumCure AI Audit Engine.*
