"""
Unit Tests for Model Artifacts and Prediction Service
"""

import pytest
import numpy as np
from pathlib import Path
from backend.prediction_service import PredictionService
from backend.evaluation import compute_binary_metrics


def test_artifact_loading_and_inference():
    """Tests loading saved model artifacts and running multi-model prediction."""
    svc = PredictionService()
    loaded = svc.load_artifacts()
    assert loaded is True

    # Valid clinical input
    test_input = {
        "Tumour Size(cm)": 2.8,
        "Age(years)": 48,
        "Histological grading": 2.0,
        "ER": "Positive",
        "HER2": "Negative"
    }

    res = svc.predict_patient(test_input)
    assert res["success"] is True
    assert res["quantum_svm"]["prediction"] in [0, 1]
    assert res["classical_svm"]["prediction"] in [0, 1]
    assert res["xgboost"]["prediction"] in [0, 1]
    assert 0.0 <= res["quantum_svm"]["probability"] <= 1.0
    assert 0.0 <= res["classical_svm"]["probability"] <= 1.0
    assert 0.0 <= res["xgboost"]["probability"] <= 1.0


def test_invalid_input_rejection():
    """Tests that input validation rejects out-of-bounds or invalid values."""
    svc = PredictionService()
    svc.load_artifacts()

    # Invalid negative age and extreme tumor size
    bad_input = {
        "Tumour Size(cm)": -5.0,
        "Age(years)": -10,
        "Histological grading": 5.0,  # only 1, 2, 3 allowed
        "ER": "InvalidValue",
        "HER2": "InvalidValue"
    }

    res = svc.predict_patient(bad_input)
    assert res["success"] is False
    assert len(res["errors"]) >= 4


def test_metrics_computation():
    """Tests binary classification metric calculations."""
    y_true = np.array([0, 0, 1, 1, 1])
    y_pred = np.array([0, 1, 1, 1, 0])
    y_score = np.array([0.1, 0.7, 0.9, 0.8, 0.4])

    m = compute_binary_metrics(y_true, y_pred, y_score, model_name="TestModel")
    assert m["accuracy"] == 0.6
    assert m["confusion_matrix"]["tn"] == 1
    assert m["confusion_matrix"]["fp"] == 1
    assert m["confusion_matrix"]["fn"] == 1
    assert m["confusion_matrix"]["tp"] == 2
    assert m["auroc"] is not None
