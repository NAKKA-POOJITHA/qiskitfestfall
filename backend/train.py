"""
QuantumCure AI - Master Training Pipeline
Orchestrates data audit, patient-level stratified splitting, preprocessing,
classical model training, genuine Qiskit quantum kernel evaluation,
fair evaluation on identical held-out test cohort, and artifact serialization.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

from backend.data_audit import audit_raw_dataset
from backend.data_preprocessing import run_data_preprocessing, CORE_FEATURES
from backend.classical_models import train_classical_svm, train_xgboost, save_classical_artifacts
from backend.quantum_kernel import train_quantum_model
from backend.evaluation import evaluate_all_models


def run_training_pipeline(
    raw_file="dataset/raw/patient-clinical-data.xlsx",
    output_dir="results",
    models_dir="models",
    quantum_n_train=100,
    random_state=42
):
    """
    Executes the complete end-to-end training and evaluation pipeline.
    """
    print("=" * 65)
    print("QuantumCure AI — Clinical Quantum Machine Learning Pipeline")
    print("=" * 65)
    t0_pipeline = time.time()

    # Step 1: Data Audit
    print("\n[Step 1/8] Auditing raw dataset...")
    audit_res = audit_raw_dataset(raw_dir="dataset/raw", output_dir=output_dir)
    if audit_res.get("status") != "VERIFIED_READY":
        print("ERROR: Dataset audit failed or target/features missing.")
        for err in audit_res.get("missing_prerequisites", []):
            print(" -", err)
        return False

    # Step 2: Data Preprocessing & Patient-level Split
    print("\n[Step 2/8] Preprocessing dataset & generating patient-level split...")
    prep_res = run_data_preprocessing(
        raw_file=raw_file,
        output_dir="dataset/processed",
        models_dir=models_dir,
        test_size=0.2,
        random_state=random_state
    )

    X_train_full = prep_res["X_train"]
    y_train_full = prep_res["y_train"]
    X_test = prep_res["X_test"]
    y_test = prep_res["y_test"]
    train_df = prep_res["train_df"]
    test_df = prep_res["test_df"]

    patient_ids_full_train = train_df["Patient ID"].values
    patient_ids_test = test_df["Patient ID"].values

    # Step 3: Subsample Training Cohort for Fair Quantum & Classical Benchmark
    # To guarantee fair comparison, all models are trained on identical training patients.
    n_train_total = len(X_train_full)
    if quantum_n_train < n_train_total:
        print(f"\n[Step 3/8] Selecting deterministic stratified training subset of {quantum_n_train} patients (out of {n_train_total})...")
        sss = StratifiedShuffleSplit(n_splits=1, train_size=quantum_n_train, random_state=random_state)
        sub_indices, _ = next(sss.split(X_train_full, y_train_full))
        sub_indices = np.sort(sub_indices)
        X_train_bench = X_train_full[sub_indices]
        y_train_bench = y_train_full[sub_indices]
        patient_ids_bench = patient_ids_full_train[sub_indices]
    else:
        print(f"\n[Step 3/8] Using complete training cohort ({n_train_total} patients)...")
        X_train_bench = X_train_full
        y_train_bench = y_train_full
        patient_ids_bench = patient_ids_full_train

    print(f"Benchmark training cohort: {len(X_train_bench)} patients (N0: {(y_train_bench == 0).sum()}, N+: {(y_train_bench == 1).sum()})")
    print(f"Held-out test cohort: {len(X_test)} patients (N0: {(y_test == 0).sum()}, N+: {(y_test == 1).sum()})")

    # Step 4: Train Classical RBF-SVM
    print("\n[Step 4/8] Training Classical RBF-SVM baseline...")
    svm_results = train_classical_svm(X_train_bench, y_train_bench, cv_folds=5, random_state=random_state)
    c_svm = svm_results["model"]
    print(f"Classical RBF-SVM trained. Best params: {svm_results['best_params']} (Time: {svm_results['train_time_sec']}s)")

    # Step 5: Train XGBoost
    print("\n[Step 5/8] Training XGBoost baseline...")
    xgb_results = train_xgboost(X_train_bench, y_train_bench, cv_folds=5, random_state=random_state)
    xgb_model = xgb_results["model"]
    print(f"XGBoost trained. Best params: {xgb_results['best_params']} (Time: {xgb_results['train_time_sec']}s)")

    # Save Classical Artifacts
    save_classical_artifacts(svm_results, xgb_results, models_dir=models_dir)

    # Step 6: Compute Real Qiskit Quantum Kernel & Train Quantum SVM
    print("\n[Step 6/8] Computing Qiskit ZZFeatureMap Quantum Kernel...")
    quantum_success = False
    quantum_error_msg = None
    q_svm_results = None
    try:
        q_svm_results = train_quantum_model(
            X_train_sub=X_train_bench,
            y_train_sub=y_train_bench,
            X_test=X_test,
            patient_ids_train=patient_ids_bench,
            patient_ids_test=patient_ids_test,
            cache_dir=output_dir,
            models_dir=models_dir,
            use_cache=False,  # Recompute freshly during training
            C=svm_results["best_params"].get("C", 1.0)
        )
        quantum_success = True
        print(f"Quantum Kernel evaluated and verified. Training Time: {q_svm_results['train_time_sec']}s")
    except Exception as e:
        quantum_error_msg = str(e)
        print(f"WARNING: Quantum kernel computation encountered error: {e}")
        print("Preserving classical model results...")

    # Step 7: Multi-Model Evaluation on Held-Out Test Cohort
    print("\n[Step 7/8] Generating predictions on held-out test patients...")
    predictions_dict = {}
    scores_dict = {}
    runtimes_dict = {}

    # Classical SVM test predictions
    predictions_dict["Classical RBF-SVM"] = c_svm.predict(X_test)
    scores_dict["Classical RBF-SVM"] = c_svm.predict_proba(X_test)[:, 1]
    runtimes_dict["Classical RBF-SVM"] = svm_results["train_time_sec"]

    # XGBoost test predictions
    predictions_dict["XGBoost"] = xgb_model.predict(X_test)
    scores_dict["XGBoost"] = xgb_model.predict_proba(X_test)[:, 1]
    runtimes_dict["XGBoost"] = xgb_results["train_time_sec"]

    # Quantum SVM test predictions
    if quantum_success and q_svm_results is not None:
        K_test = q_svm_results["K_test"]
        q_svm = q_svm_results["model"]
        predictions_dict["Quantum-kernel SVM"] = q_svm.predict(K_test)
        scores_dict["Quantum-kernel SVM"] = q_svm.predict_proba(K_test)[:, 1]
        runtimes_dict["Quantum-kernel SVM"] = q_svm_results["train_time_sec"]

    # Execute comprehensive evaluation
    metrics_list = evaluate_all_models(
        y_test=y_test,
        predictions_dict=predictions_dict,
        scores_dict=scores_dict,
        runtimes_dict=runtimes_dict,
        patient_ids_test=patient_ids_test,
        output_dir=output_dir
    )

    # Step 8: Save Experiment Configuration & Training Summary
    print("\n[Step 8/8] Writing experiment configuration and summary...")
    config_data = {
        "dataset_name": "BCNB",
        "cancer_type": "Breast cancer",
        "prediction_target": "Axillary lymph-node metastasis (ALN status)",
        "quantum_n_train": len(X_train_bench),
        "total_train_available": len(X_train_full),
        "test_n_samples": len(X_test),
        "feature_names": CORE_FEATURES,
        "feature_dimension": len(CORE_FEATURES),
        "random_state": random_state,
        "quantum_success": quantum_success,
        "quantum_error": quantum_error_msg,
        "classical_svm_params": svm_results["best_params"],
        "xgboost_params": xgb_results["best_params"],
        "total_runtime_seconds": round(time.time() - t0_pipeline, 2)
    }
    with open(Path(output_dir) / "experiment_config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    _write_training_summary(config_data, metrics_list, Path(output_dir) / "training_summary.md")

    print("\n" + "=" * 65)
    print("TRAINING PIPELINE FINISHED SUCCESSFULLY")
    print(f"Total Elapsed Time: {config_data['total_runtime_seconds']}s")
    print(f"Results directory: {output_dir}")
    print(f"Models directory:  {models_dir}")
    print("=" * 65)
    return True


def _write_training_summary(config, metrics_list, out_file):
    md = f"""# QuantumCure AI — Training Pipeline Summary

**Experiment Date & Status:** COMPLETED  
**Target:** Axillary lymph-node metastasis (Class 0: N0, Class 1: N+)  
**Training Patients:** {config['quantum_n_train']} (Stratified subset for fair quantum comparison)  
**Held-out Test Patients:** {config['test_n_samples']}  
**Features:** {', '.join(config['feature_names'])}  
**Total Pipeline Runtime:** {config['total_runtime_seconds']} seconds  

---

## Model Benchmark Results (Held-out Test Cohort)
| Model | AUROC | Accuracy | F1-Score | Sensitivity | Specificity | Precision | Train Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for m in metrics_list:
        md += f"| **{m['model_name']}** | {m.get('auroc', 'N/A')} | {m['accuracy']*100:.2f}% | {m['f1_score']:.4f} | {m['sensitivity']:.4f} | {m['specificity']:.4f} | {m['precision']:.4f} | {m['train_time_sec']}s |\n"

    md += f"""
---

## Technical Artifacts Saved:
- `models/preprocessing_pipeline.joblib`
- `models/classical_svm.joblib`
- `models/xgboost_model.json`
- `models/quantum_svm.joblib`
- `models/quantum_training_features.npy`
- `results/quantum_kernel_train.npy`
- `results/quantum_kernel_test.npy`
- `results/metrics.csv`
- `results/predictions.csv`
- `results/roc_curves.png`
- `results/confusion_matrices.png`
"""
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QuantumCure AI Training Pipeline")
    parser.add_argument("--quantum_samples", type=int, default=100, help="Training samples for quantum experiment (default: 100)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    run_training_pipeline(quantum_n_train=args.quantum_samples, random_state=args.seed)
