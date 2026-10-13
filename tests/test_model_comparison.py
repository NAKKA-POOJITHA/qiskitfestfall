"""
QuantumCure AI - Unit Tests for Model Comparison and Benchmark Artifacts
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

root_dir = Path(__file__).resolve().parent.parent


def test_metrics_json_integrity():
    """Verify that results/metrics.json exists and contains complete benchmark data."""
    metrics_file = root_dir / "results" / "metrics.json"
    assert metrics_file.exists(), "results/metrics.json does not exist"

    with open(metrics_file, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    assert isinstance(metrics, list), "metrics.json must be a list of model summaries"
    assert len(metrics) == 3, f"Expected 3 models in metrics, found {len(metrics)}"

    required_keys = ["model_name", "auroc", "accuracy", "precision", "recall", "specificity", "f1_score", "pr_auc"]
    for m in metrics:
        for k in required_keys:
            assert k in m, f"Key '{k}' missing in model summary for {m.get('model_name')}"
            assert isinstance(m[k], (float, int, str)), f"Invalid type for key '{k}'"
            if isinstance(m[k], (float, int)) and k in ["auroc", "accuracy", "precision", "recall", "specificity", "pr_auc"]:
                assert 0.0 <= m[k] <= 1.0, f"Metric '{k}' out of range: {m[k]}"


def test_predictions_csv_integrity():
    """Verify that results/predictions.csv contains all 212 held-out patients with valid scores."""
    preds_file = root_dir / "results" / "predictions.csv"
    assert preds_file.exists(), "results/predictions.csv does not exist"

    df = pd.read_csv(preds_file)
    assert len(df) == 212, f"Expected exactly 212 test records, found {len(df)}"

    required_cols = [
        "Patient ID", "Ground Truth Target", "Ground Truth Class",
        "Quantum_kernel_SVM_Pred", "Quantum_kernel_SVM_Score",
        "Classical_RBF_SVM_Pred", "Classical_RBF_SVM_Score",
        "XGBoost_Pred", "XGBoost_Score"
    ]
    for col in required_cols:
        assert col in df.columns, f"Column '{col}' missing from predictions.csv"

    # Verify score ranges
    for prefix in ["Quantum_kernel_SVM", "Classical_RBF_SVM", "XGBoost"]:
        scores = df[f"{prefix}_Score"].values
        assert np.all(scores >= 0.0) and np.all(scores <= 1.0), f"Scores out of bounds for {prefix}"
