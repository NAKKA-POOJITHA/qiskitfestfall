import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import json
import joblib
import numpy as np
import pandas as pd

models_dir = Path("models")
results_dir = Path("results")
dataset_dir = Path("dataset/processed")

# 1. Preprocessing Scaler & Imputer
pipe = joblib.load(models_dir / "preprocessing_pipeline.joblib")
scaler_params = {
    "feature_names": ["Tumour Size(cm)", "Age(years)", "Histological grading", "ER_encoded", "HER2_encoded"],
    "data_min": pipe.scaler.data_min_.tolist(),
    "data_max": pipe.scaler.data_max_.tolist(),
    "scale": pipe.scaler.scale_.tolist(),
    "min": pipe.scaler.min_.tolist(),
    "grade_imputer_default": float(pipe.grade_imputer.statistics_[0])
}
with open(models_dir / "scaler_params.json", "w") as f:
    json.dump(scaler_params, f, indent=2)
print("Saved models/scaler_params.json")

# 2. Classical RBF-SVM Parameters
c_svm = joblib.load(models_dir / "classical_svm.joblib")
c_params = {
    "gamma": float(c_svm._gamma),
    "intercept": float(c_svm.intercept_[0]),
    "dual_coef": c_svm.dual_coef_[0].tolist(),
    "support_vectors": c_svm.support_vectors_.tolist(),
    "probA": float(c_svm.probA_[0]),
    "probB": float(c_svm.probB_[0])
}
with open(models_dir / "classical_svm_params.json", "w") as f:
    json.dump(c_params, f, indent=2)
print("Saved models/classical_svm_params.json")

# 3. Quantum Kernel SVM Parameters
q_svm = joblib.load(models_dir / "quantum_svm.joblib")
train_svs = np.load(models_dir / "quantum_training_statevectors.npy")
# Store real and imag parts for training statevectors (100, 32)
train_svs_serialized = [
    [{"r": round(float(c.real), 6), "i": round(float(c.imag), 6)} for c in sv]
    for sv in train_svs
]

q_params = {
    "intercept": float(q_svm.intercept_[0]),
    "dual_coef": q_svm.dual_coef_[0].tolist(),
    "support_indices": [int(idx) for idx in q_svm.support_],
    "probA": float(q_svm.probA_[0]),
    "probB": float(q_svm.probB_[0]),
    "num_training_samples": len(train_svs),
    "train_statevectors": train_svs_serialized
}
with open(models_dir / "quantum_svm_params.json", "w") as f:
    json.dump(q_params, f)
print("Saved models/quantum_svm_params.json")

# 4. Held-Out Test Patients (212 real records)
test_df = pd.read_csv(dataset_dir / "bcnb_test.csv")
pred_df = pd.read_csv(results_dir / "predictions.csv")

merged_df = test_df.merge(pred_df, on="Patient ID")
held_out_list = []
for _, row in merged_df.iterrows():
    grade_val = 2 if pd.isna(row["orig_Histological_grade"]) else int(row["orig_Histological_grade"])
    held_out_list.append({
        "patient_id": str(int(row["Patient ID"])),
        "tumour_size": round(float(row["orig_Tumour_Size"]), 2),
        "age": int(row["orig_Age"]),
        "grade": grade_val,
        "er": str(row["orig_ER"]),
        "her2": str(row["orig_HER2"]),
        "ground_truth_target": int(row["target"]),
        "ground_truth_label": "N+ (Metastasis Present)" if row["target"] == 1 else "N0 (Negative)",
        "ground_truth_staging": str(row["ALN status"]),
        "quantum_pred": int(row["Quantum_kernel_SVM_Pred"]),
        "quantum_prob": round(float(row["Quantum_kernel_SVM_Score"]), 4),
        "classical_pred": int(row["Classical_RBF_SVM_Pred"]),
        "classical_prob": round(float(row["Classical_RBF_SVM_Score"]), 4),
        "xgboost_pred": int(row["XGBoost_Pred"]),
        "xgboost_prob": round(float(row["XGBoost_Score"]), 4)
    })

with open(results_dir / "held_out_patients.json", "w") as f:
    json.dump(held_out_list, f, indent=2)
print(f"Saved results/held_out_patients.json ({len(held_out_list)} patients)")

# 5. Kernel Matrices (100x100) for Heatmap
qk = np.load(results_dir / "quantum_kernel_train.npy")
ck = np.load(results_dir / "classical_rbf_kernel_train.npy")

kernel_data = {
    "dimensions": [int(qk.shape[0]), int(qk.shape[1])],
    "quantum_kernel": [[round(float(v), 4) for v in row] for row in qk],
    "classical_kernel": [[round(float(v), 4) for v in row] for row in ck],
    "difference_kernel": [[round(float(abs(qk[i, j] - ck[i, j])), 4) for j in range(qk.shape[1])] for i in range(qk.shape[0])]
}
with open(results_dir / "kernel_matrices.json", "w") as f:
    json.dump(kernel_data, f)
print("Saved results/kernel_matrices.json")

print("All artifact exports complete!")
