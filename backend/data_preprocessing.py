"""
QuantumCure AI - Data Preprocessing Pipeline
Handles data cleaning, target validation, clinical feature transformation,
leakage prevention, patient-level train/test splitting, and artifact serialization.
"""

import os
import json
import joblib
import openpyxl
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.impute import SimpleImputer


CORE_FEATURES = [
    "Tumour Size(cm)",
    "Age(years)",
    "Histological grading",
    "ER_encoded",
    "HER2_encoded"
]

FEATURE_DICTIONARY = {
    "Tumour Size(cm)": {
        "description": "Maximum clinical/pathological diameter of primary tumor in centimeters.",
        "type": "Continuous numerical",
        "units": "cm",
        "clinical_significance": "Single strongest clinical predictor of axillary nodal involvement in invasive breast carcinoma. Larger tumor volume correlates with increased vascular and lymphatic invasion probability."
    },
    "Age(years)": {
        "description": "Patient age in completed years at the time of primary diagnosis.",
        "type": "Continuous numerical",
        "units": "years",
        "clinical_significance": "Younger age is an established clinical risk factor for more aggressive breast cancer phenotypes and higher rate of nodal metastasis."
    },
    "Histological grading": {
        "description": "Nottingham Histological Grade (Elston-Ellis modification of Scarff-Bloom-Richardson system), Grade 1 to 3.",
        "type": "Ordinal numerical",
        "units": "Grade 1 (Well differentiated), Grade 2 (Moderately differentiated), Grade 3 (Poorly differentiated)",
        "clinical_significance": "High tumor grade reflects rapid cellular proliferation, marked nuclear pleomorphism, and loss of glandular architecture, predisposing to lymph node metastasis."
    },
    "ER_encoded": {
        "description": "Estrogen Receptor nuclear immunohistochemistry status (1 = Positive, 0 = Negative).",
        "type": "Binary categorical",
        "units": "0 or 1",
        "clinical_significance": "Estrogen receptor expression governs tumor hormone sensitivity, differentiation status, and systemic therapeutic responsiveness."
    },
    "HER2_encoded": {
        "description": "Human Epidermal Growth Factor Receptor 2 amplification / overexpression status (1 = Positive, 0 = Negative).",
        "type": "Binary categorical",
        "units": "0 or 1",
        "clinical_significance": "HER2 amplification drives accelerated oncogenic proliferation, invasiveness, and historical predisposition to axillary dissemination."
    }
}


def parse_ki67_value(val):
    """Parses heterogeneous clinical Ki67 representations into a decimal fraction [0, 1]."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip().replace("＜", "<").replace("＞", ">").replace("%", "")
    if "-" in s:
        parts = s.split("-")
        try:
            return (float(parts[0]) + float(parts[1])) / 2.0 / 100.0
        except Exception:
            pass
    if s.startswith("<"):
        try:
            return float(s[1:]) / 100.0 / 2.0
        except Exception:
            pass
    if s.startswith(">"):
        try:
            return (float(s[1:]) + 100.0) / 2.0 / 100.0
        except Exception:
            pass
    try:
        f = float(s)
        if f > 1.0:
            f = f / 100.0
        return f
    except Exception:
        return np.nan


class PreprocessingPipeline:
    """
    Fitted clinical preprocessing pipeline for QuantumCure AI.
    Fits imputers and scalers strictly on training data to prevent leakage.
    """
    def __init__(self, feature_names=None):
        self.feature_names = feature_names or CORE_FEATURES
        self.grade_imputer = SimpleImputer(strategy="median")
        self.scaler = MinMaxScaler(feature_range=(0.0, np.pi))  # Scale to [0, pi] optimal for ZZFeatureMap

    def fit(self, df_train):
        """Fits transformers on raw training dataframe."""
        # Fit grade imputer
        grade_vals = df_train[["Histological grading"]].values
        self.grade_imputer.fit(grade_vals)

        # Extract features
        X_train_raw = self._extract_raw_features(df_train)
        self.scaler.fit(X_train_raw)
        return self

    def transform(self, df):
        """Transforms dataframe into scaled feature matrix."""
        X_raw = self._extract_raw_features(df)
        X_scaled = self.scaler.transform(X_raw)
        return X_scaled

    def _extract_raw_features(self, df):
        """Extracts and validates raw numeric and encoded columns."""
        df_copy = df.copy()

        # Grade imputation
        if "Histological grading" in df_copy.columns:
            df_copy["grade_imputed"] = self.grade_imputer.transform(df_copy[["Histological grading"]].values).ravel()
        else:
            df_copy["grade_imputed"] = 2.0  # default median grade

        # ER encoding
        if "ER" in df_copy.columns:
            df_copy["ER_encoded"] = df_copy["ER"].apply(lambda v: 1.0 if str(v).strip().lower() == "positive" else 0.0)
        elif "ER_encoded" not in df_copy.columns:
            df_copy["ER_encoded"] = 0.0

        # HER2 encoding
        if "HER2" in df_copy.columns:
            df_copy["HER2_encoded"] = df_copy["HER2"].apply(lambda v: 1.0 if str(v).strip().lower() == "positive" else 0.0)
        elif "HER2_encoded" not in df_copy.columns:
            df_copy["HER2_encoded"] = 0.0

        # Construct array in exact CORE_FEATURES order
        cols = [
            df_copy["Tumour Size(cm)"].values.astype(float),
            df_copy["Age(years)"].values.astype(float),
            df_copy["grade_imputed"].values.astype(float),
            df_copy["ER_encoded"].values.astype(float),
            df_copy["HER2_encoded"].values.astype(float)
        ]
        return np.column_stack(cols)


def run_data_preprocessing(
    raw_file="dataset/raw/patient-clinical-data.xlsx",
    output_dir="dataset/processed",
    models_dir="models",
    test_size=0.2,
    random_state=42
):
    """
    Executes end-to-end dataset preprocessing, validation, splitting,
    and artifact export.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    models_path = Path(models_dir)
    models_path.mkdir(parents=True, exist_ok=True)

    # 1. Load raw file
    raw_path = Path(raw_file)
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {raw_file}")

    df_raw = pd.read_excel(raw_path)
    total_raw_rows = len(df_raw)

    # 2. Validate target
    if "ALN status" not in df_raw.columns:
        raise ValueError("Target column 'ALN status' not found in raw dataset.")

    # Exclude any invalid rows (if any)
    valid_mask = df_raw["ALN status"].isin(["N0", "N+(1-2)", "N+(>2)"])
    excluded_rows = int((~valid_mask).sum())
    df_clean = df_raw[valid_mask].copy()

    # Map target: N0 -> 0, N+ -> 1
    df_clean["target"] = df_clean["ALN status"].apply(lambda v: 0 if v == "N0" else 1)

    # 3. Patient ID audit & split
    # Verify each patient is unique
    if df_clean["Patient ID"].duplicated().any():
        raise ValueError("Duplicate Patient IDs found in clean dataset.")

    # Stratified train/test split by patient
    train_df, test_df = train_test_split(
        df_clean,
        test_size=test_size,
        random_state=random_state,
        stratify=df_clean["target"]
    )

    # 4. Fit preprocessing pipeline on training data ONLY
    pipeline = PreprocessingPipeline(feature_names=CORE_FEATURES)
    pipeline.fit(train_df)

    # Transform features
    X_train = pipeline.transform(train_df)
    X_test = pipeline.transform(test_df)
    y_train = train_df["target"].values
    y_test = test_df["target"].values

    # 5. Save processed data CSVs (including metadata and features)
    def make_processed_df(original_sub_df, X_sub):
        res = original_sub_df[["Patient ID", "ALN status", "target"]].copy()
        for idx, feat in enumerate(CORE_FEATURES):
            res[f"feat_{feat}"] = X_sub[:, idx]
        # Include original clinical values for demonstration and lab
        res["orig_Age"] = original_sub_df["Age(years)"].values
        res["orig_Tumour_Size"] = original_sub_df["Tumour Size(cm)"].values
        res["orig_Histological_grade"] = original_sub_df["Histological grading"].values
        res["orig_ER"] = original_sub_df["ER"].values
        res["orig_HER2"] = original_sub_df["HER2"].values
        return res

    proc_train_df = make_processed_df(train_df, X_train)
    proc_test_df = make_processed_df(test_df, X_test)

    train_csv = out_path / "bcnb_train.csv"
    test_csv = out_path / "bcnb_test.csv"
    proc_train_df.to_csv(train_csv, index=False)
    proc_test_df.to_csv(test_csv, index=False)

    # 6. Save fitted pipeline
    pipeline_file = models_path / "preprocessing_pipeline.joblib"
    joblib.dump(pipeline, pipeline_file)

    # 7. Save feature dictionary
    feat_dict_file = out_path / "feature_dictionary.json"
    with open(feat_dict_file, "w", encoding="utf-8") as f:
        json.dump(FEATURE_DICTIONARY, f, indent=2)

    # 8. Create Preprocessing Report
    rep_file = out_path / "preprocessing_report.md"
    train_n0 = int((y_train == 0).sum())
    train_n1 = int((y_train == 1).sum())
    test_n0 = int((y_test == 0).sum())
    test_n1 = int((y_test == 1).sum())

    report_content = f"""# QuantumCure AI — Dataset Preprocessing Report

**Dataset:** BCNB (Breast Cancer Nodal / Biopsy Clinical Dataset)  
**Task:** Binary Classification — Axillary Lymph Node Metastasis (`ALN status`)  
**Target Definition:** Class 0 = `N0` (No metastasis), Class 1 = `N+` (Metastasis present)  
**Split Method:** Patient-level stratified split (`test_size={test_size}`, `random_state={random_state}`)  
**Fitted Pipeline:** Saved to `{pipeline_file}`  

---

## 1. Data Partition Summary
| Metric | Full Cohort | Training Set | Held-out Test Set |
| :--- | :--- | :--- | :--- |
| **Total Patients** | {len(df_clean)} | {len(train_df)} ({round(len(train_df)/len(df_clean)*100, 1)}%) | {len(test_df)} ({round(len(test_df)/len(df_clean)*100, 1)}%) |
| **Class 0 (N0)** | {train_n0 + test_n0} ({round((train_n0 + test_n0)/len(df_clean)*100, 1)}%) | {train_n0} ({round(train_n0/len(train_df)*100, 1)}%) | {test_n0} ({round(test_n0/len(test_df)*100, 1)}%) |
| **Class 1 (N+)** | {train_n1 + test_n1} ({round((train_n1 + test_n1)/len(df_clean)*100, 1)}%) | {train_n1} ({round(train_n1/len(train_df)*100, 1)}%) | {test_n1} ({round(test_n1/len(test_df)*100, 1)}%) |
| **Excluded Invalid Rows** | {excluded_rows} | 0 | 0 |

---

## 2. Selected Predictor Features ({len(CORE_FEATURES)} Features)
The following 5 legitimate pre-operative features were selected to balance oncological predictive fidelity with the Hilbert-space dimensionality constraints of quantum feature mapping ($2^5 = 32$ quantum basis states):

1. **`Tumour Size(cm)`**: Maximum primary tumor diameter.
2. **`Age(years)`**: Patient age at diagnosis.
3. **`Histological grading`**: Modified Bloom-Richardson grading (1, 2, or 3). Median imputed strictly using training fold median (`{pipeline.grade_imputer.statistics_[0]}`).
4. **`ER_encoded`**: Estrogen receptor status (1 = Positive, 0 = Negative).
5. **`HER2_encoded`**: HER2 overexpression status (1 = Positive, 0 = Negative).

---

## 3. Leakage Prevention Protocol
- **Target Proxy Exclusion:** `Number of lymph node metastases` is completely excluded from feature generation.
- **Surgical Staging Exclusion:** `Surgical` method is excluded to avoid procedural confounding.
- **Transformation Isolation:** All imputation statistics and scaling extrema ($[0, \\pi]$) were computed exclusively on the 846 training patients and applied downstream to the 212 held-out test patients.
- **Patient Independence:** Each record represents an independent patient; no patient appears across both partitions.

---

## 4. Quantum Hilbert Space Encoding
Features are scaled to $[0, \\pi]$ using `MinMaxScaler` fitted on training data:
- Prevents $2\\pi$ phase periodicity wrap-around in the `ZZFeatureMap`.
- Provides numerical compatibility for classical RBF-SVM, XGBoost, and Quantum Kernels.
"""

    with open(rep_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print("Preprocessing completed successfully.")
    print(f"Train samples: {len(train_df)}, Test samples: {len(test_df)}")
    print(f"Artifacts saved to {out_path} and {models_path}")

    return {
        "train_df": train_df,
        "test_df": test_df,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "pipeline": pipeline
    }


if __name__ == "__main__":
    run_data_preprocessing()
