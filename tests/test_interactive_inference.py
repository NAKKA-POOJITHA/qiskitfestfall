"""
Tests for interactive inference engine and WSGI API endpoints.
"""

import io
import json
import pytest
from app import app
from backend.fast_inference import run_full_inference, scale_features


def test_scale_features_bounds():
    # Test valid input within range
    scaled, clean = scale_features({
        "Tumour Size(cm)": 2.5,
        "Age(years)": 55,
        "Histological grading": 2,
        "ER": "Positive",
        "HER2": "Negative"
    })
    assert len(scaled) == 5
    assert all(0.0 <= v <= 3.1416 for v in scaled)
    assert clean["Tumour Size(cm)"] == 2.5
    assert clean["ER"] == "Positive"


def test_inference_value_sensitivity():
    # Changing input feature values must genuinely alter inference predictions / probabilities
    low_risk = run_full_inference({
        "Tumour Size(cm)": 1.0,
        "Age(years)": 70,
        "Histological grading": 1,
        "ER": "Positive",
        "HER2": "Negative"
    })

    high_risk = run_full_inference({
        "Tumour Size(cm)": 5.0,
        "Age(years)": 40,
        "Histological grading": 3,
        "ER": "Negative",
        "HER2": "Positive"
    })

    assert low_risk["success"] is True
    assert high_risk["success"] is True

    # High risk case must have higher predicted probability in XGBoost and Classical RBF
    assert high_risk["xgboost"]["probability"] > low_risk["xgboost"]["probability"]
    assert high_risk["classical_svm"]["decision_score"] > low_risk["classical_svm"]["decision_score"]


def test_wsgi_health_endpoint():
    env = {
        "PATH_INFO": "/api/health",
        "REQUEST_METHOD": "GET",
        "CONTENT_LENGTH": "0",
        "wsgi.input": io.BytesIO(b"")
    }
    captured = {}
    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    body = b"".join(app(env, start_response))
    assert captured["status"] == "200 OK"
    data = json.loads(body.decode("utf-8"))
    assert data["status"] == "healthy"


def test_wsgi_metrics_endpoint():
    env = {
        "PATH_INFO": "/api/metrics",
        "REQUEST_METHOD": "GET",
        "CONTENT_LENGTH": "0",
        "wsgi.input": io.BytesIO(b"")
    }
    captured = {}
    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    body = b"".join(app(env, start_response))
    assert captured["status"] == "200 OK"
    data = json.loads(body.decode("utf-8"))
    assert len(data) == 3
    model_names = [m["model_name"] for m in data]
    assert "Quantum-kernel SVM" in model_names
    assert "Classical RBF-SVM" in model_names
    assert "XGBoost" in model_names


def test_wsgi_predict_endpoint_post():
    payload = {
        "Tumour Size(cm)": 3.2,
        "Age(years)": 60,
        "Histological grading": 2,
        "ER": "Positive",
        "HER2": "Negative"
    }
    body_bytes = json.dumps(payload).encode("utf-8")
    env = {
        "PATH_INFO": "/api/predict",
        "REQUEST_METHOD": "POST",
        "CONTENT_LENGTH": str(len(body_bytes)),
        "wsgi.input": io.BytesIO(body_bytes)
    }
    captured = {}
    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    body = b"".join(app(env, start_response))
    assert captured["status"] == "200 OK"
    data = json.loads(body.decode("utf-8"))
    assert data["success"] is True
    assert "quantum_svm" in data
    assert "classical_svm" in data
    assert "xgboost" in data
    assert "agreement" in data
