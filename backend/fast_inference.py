"""
QuantumCure AI - Fast Lightweight Inference Engine
Executes genuine mathematical inference for Classical RBF-SVM, Quantum ZZFeatureMap SVM,
and XGBoost with zero heavy dependencies (pure NumPy + JSON), ideal for Vercel Serverless.
"""

import json
import math
import time
from pathlib import Path
import numpy as np

# Load parameters once at module import
_ROOT = Path(__file__).resolve().parent.parent
_MODELS_DIR = _ROOT / "models"

with open(_MODELS_DIR / "scaler_params.json", "r", encoding="utf-8") as f:
    SCALER_PARAMS = json.load(f)

with open(_MODELS_DIR / "classical_svm_params.json", "r", encoding="utf-8") as f:
    CLASSICAL_PARAMS = json.load(f)

with open(_MODELS_DIR / "quantum_svm_params.json", "r", encoding="utf-8") as f:
    QUANTUM_PARAMS = json.load(f)

with open(_MODELS_DIR / "xgboost_model.json", "r", encoding="utf-8") as f:
    XGB_JSON = json.load(f)

XGB_TREES = XGB_JSON["learner"]["gradient_booster"]["model"]["trees"]

# Convert cached structures to fast NumPy arrays
C_SUPPORT_VECTORS = np.array(CLASSICAL_PARAMS["support_vectors"], dtype=np.float64) # (88, 5)
C_DUAL_COEF = np.array(CLASSICAL_PARAMS["dual_coef"], dtype=np.float64) # (88,)
C_GAMMA = CLASSICAL_PARAMS["gamma"]
C_INTERCEPT = CLASSICAL_PARAMS["intercept"]
C_PROB_A = CLASSICAL_PARAMS["probA"]
C_PROB_B = CLASSICAL_PARAMS["probB"]

Q_DUAL_COEF = np.array(QUANTUM_PARAMS["dual_coef"], dtype=np.float64) # (84,)
Q_SUPPORT_INDICES = QUANTUM_PARAMS["support_indices"]
Q_INTERCEPT = QUANTUM_PARAMS["intercept"]
Q_PROB_A = QUANTUM_PARAMS["probA"]
Q_PROB_B = QUANTUM_PARAMS["probB"]

# Reconstruct training statevectors (100, 32)
Q_TRAIN_SVS = np.array([
    [complex(c["r"], c["i"]) for c in sv]
    for sv in QUANTUM_PARAMS["train_statevectors"]
], dtype=np.complex128)


def scale_features(input_dict):
    """Transforms raw clinical input features to [0, pi] feature space."""
    try:
        size = float(input_dict.get("Tumour Size(cm)", 2.5))
    except (ValueError, TypeError):
        size = 2.5

    try:
        age = float(input_dict.get("Age(years)", 55.0))
    except (ValueError, TypeError):
        age = 55.0

    try:
        grade = float(input_dict.get("Histological grading", SCALER_PARAMS["grade_imputer_default"]))
        if grade not in (1.0, 2.0, 3.0):
            grade = 2.0
    except (ValueError, TypeError):
        grade = 2.0

    er_raw = str(input_dict.get("ER", "Negative")).strip().capitalize()
    er_val = 1.0 if er_raw == "Positive" or er_raw == "1" else 0.0

    her2_raw = str(input_dict.get("HER2", "Negative")).strip().capitalize()
    her2_val = 1.0 if her2_raw == "Positive" or her2_raw == "1" else 0.0

    raw_vec = np.array([size, age, grade, er_val, her2_val], dtype=np.float64)
    scale = np.array(SCALER_PARAMS["scale"], dtype=np.float64)
    min_val = np.array(SCALER_PARAMS["min"], dtype=np.float64)

    scaled = raw_vec * scale + min_val
    # Clamp to [0, pi]
    scaled = np.clip(scaled, 0.0, np.pi)
    return scaled, {
        "Tumour Size(cm)": size,
        "Age(years)": age,
        "Histological grading": int(grade),
        "ER": "Positive" if er_val == 1.0 else "Negative",
        "HER2": "Positive" if her2_val == 1.0 else "Negative"
    }


def predict_classical_rbf(scaled_features):
    """Evaluates Classical Gaussian RBF-SVM using exact support vector dual coefficients."""
    # Compute RBF Kernel distances: exp(-gamma * ||x - sv_i||^2)
    diff = C_SUPPORT_VECTORS - scaled_features # (88, 5)
    sq_dist = np.sum(diff ** 2, axis=1) # (88,)
    k_vals = np.exp(-C_GAMMA * sq_dist) # (88,)

    # Decision function f(x) = sum(alpha_i * k_i) + b
    decision_margin = float(np.sum(C_DUAL_COEF * k_vals) + C_INTERCEPT)

    # Platt calibrated probability: 1 / (1 + exp(A * f(x) + B))
    prob = 1.0 / (1.0 + math.exp(C_PROB_A * decision_margin + C_PROB_B))
    pred_class = 1 if prob >= 0.5 else 0

    return {
        "model_name": "Classical RBF-SVM",
        "prediction": pred_class,
        "label": "N+ (Metastasis Present)" if pred_class == 1 else "N0 (Negative)",
        "probability": round(prob, 4),
        "decision_score": round(decision_margin, 4),
        "support_vectors": len(C_SUPPORT_VECTORS),
        "kernel": "Gaussian Radial Basis Function (gamma = 0.5)"
    }


def _hadamard_all_5q(sv):
    """Applies Hadamard gate to all 5 qubits."""
    for q in range(5):
        stride = 1 << q
        for i in range(0, 32, 2 * stride):
            for j in range(i, i + stride):
                u = sv[j]
                v = sv[j + stride]
                sv[j] = (u + v) / 1.4142135623730951
                sv[j + stride] = (u - v) / 1.4142135623730951
    return sv


def compute_quantum_statevector(scaled_features, reps=2):
    """Simulates 5-qubit ZZFeatureMap quantum statevector."""
    sv = np.zeros(32, dtype=np.complex128)
    sv[0] = 1.0

    x = scaled_features
    for _ in range(reps):
        sv = _hadamard_all_5q(sv)
        phases = np.zeros(32, dtype=np.float64)
        for k in range(32):
            bits = [(k >> q) & 1 for q in range(5)]
            phi = 0.0
            for j in range(5):
                z_j = 1.0 if bits[j] == 0 else -1.0
                phi += -x[j] * z_j
            for j in range(4):
                z_j = 1.0 if bits[j] == 0 else -1.0
                z_next = 1.0 if bits[j + 1] == 0 else -1.0
                phi += -(np.pi - x[j]) * (np.pi - x[j + 1]) * (z_j * z_next)
            phases[k] = phi
        sv = sv * np.exp(1j * phases)
    return sv


def predict_quantum_svm(scaled_features):
    """Evaluates 5-Qubit ZZFeatureMap Quantum Kernel SVM with fidelity evaluation."""
    sv = compute_quantum_statevector(scaled_features, reps=2)

    # Compute fidelity vector K(x, x_train_i) = |<psi(x)|psi(x_train_i)>|^2
    inner_products = np.sum(sv.conj() * Q_TRAIN_SVS, axis=1) # (100,)
    fidelities = np.abs(inner_products) ** 2 # (100,)

    # Extract fidelities for the 84 support vectors
    support_fidelities = fidelities[Q_SUPPORT_INDICES] # (84,)

    # Decision function f(x) = sum(alpha_i * k_i) + b
    decision_margin = float(np.sum(Q_DUAL_COEF * support_fidelities) + Q_INTERCEPT)

    # Platt calibrated probability
    prob = 1.0 / (1.0 + math.exp(Q_PROB_A * decision_margin + Q_PROB_B))
    pred_class = 1 if prob >= 0.5 else 0

    mean_fidelity = float(np.mean(fidelities))
    max_fidelity = float(np.max(fidelities))

    return {
        "model_name": "Quantum-Kernel SVM",
        "prediction": pred_class,
        "label": "N+ (Metastasis Present)" if pred_class == 1 else "N0 (Negative)",
        "probability": round(prob, 4),
        "decision_score": round(decision_margin, 4),
        "mean_training_fidelity": round(mean_fidelity, 4),
        "max_training_fidelity": round(max_fidelity, 4),
        "support_vectors": len(Q_SUPPORT_INDICES),
        "feature_map": "5-Qubit ZZFeatureMap (reps=2, linear entanglement)"
    }


def predict_xgboost(scaled_features):
    """Evaluates 50-tree gradient boosted ensemble from saved tree structure."""
    total_margin = 0.0
    for tree in XGB_TREES:
        lefts = tree["left_children"]
        rights = tree["right_children"]
        splits = tree["split_indices"]
        conds = tree["split_conditions"]
        weights = tree["base_weights"]
        node = 0
        while lefts[node] != -1:
            feat_idx = splits[node]
            threshold = conds[node]
            if scaled_features[feat_idx] < threshold:
                node = lefts[node]
            else:
                node = rights[node]
        total_margin += weights[node]

    # Logistic sigmoid
    prob = 1.0 / (1.0 + math.exp(-total_margin))
    pred_class = 1 if prob >= 0.5 else 0

    return {
        "model_name": "XGBoost Classifier",
        "prediction": pred_class,
        "label": "N+ (Metastasis Present)" if pred_class == 1 else "N0 (Negative)",
        "probability": round(prob, 4),
        "log_odds_margin": round(total_margin, 4),
        "num_trees": len(XGB_TREES)
    }


def run_full_inference(input_dict):
    """
    Executes full multi-model prediction pipeline.
    Validates, scales, and runs Quantum SVM, Classical RBF-SVM, and XGBoost.
    Returns comprehensive metrics, timing, consensus, and interpretations.
    """
    t_start = time.perf_counter()

    # Validate inputs and scale
    scaled, clean_inputs = scale_features(input_dict)

    # 1. Classical RBF
    t0 = time.perf_counter()
    c_res = predict_classical_rbf(scaled)
    c_time_ms = round((time.perf_counter() - t0) * 1000, 2)
    c_res["inference_time_ms"] = c_time_ms
    c_res["status"] = "Completed"

    # 2. Quantum Kernel SVM
    t0 = time.perf_counter()
    q_res = predict_quantum_svm(scaled)
    q_time_ms = round((time.perf_counter() - t0) * 1000, 2)
    q_res["inference_time_ms"] = q_time_ms
    q_res["status"] = "Completed"

    # 3. XGBoost
    t0 = time.perf_counter()
    x_res = predict_xgboost(scaled)
    x_time_ms = round((time.perf_counter() - t0) * 1000, 2)
    x_res["inference_time_ms"] = x_time_ms
    x_res["status"] = "Completed"

    total_time_ms = round((time.perf_counter() - t_start) * 1000, 2)

    # Consensus analysis
    preds = [q_res["prediction"], c_res["prediction"], x_res["prediction"]]
    num_positive = sum(preds)
    num_negative = 3 - num_positive

    if num_positive == 3:
        consensus_type = "Unanimous Positive (3 of 3 models predict N+)"
        majority_vote = 1
    elif num_positive == 0:
        consensus_type = "Unanimous Negative (3 of 3 models predict N0)"
        majority_vote = 0
    elif num_positive == 2:
        consensus_type = "Majority Positive (2 models predict N+, 1 predicts N0)"
        majority_vote = 1
    else:
        consensus_type = "Majority Negative (2 models predict N0, 1 predicts N+)"
        majority_vote = 0

    return {
        "success": True,
        "inputs_received": clean_inputs,
        "scaled_coordinates": [round(float(v), 4) for v in scaled],
        "quantum_svm": q_res,
        "classical_svm": c_res,
        "xgboost": x_res,
        "agreement": {
            "consensus_type": consensus_type,
            "majority_prediction": majority_vote,
            "majority_label": "N+ (Metastasis Present)" if majority_vote == 1 else "N0 (Negative)",
            "models_positive": num_positive,
            "models_negative": num_negative,
            "disclaimer": "Note: Model agreement is not proof of ground-truth correctness."
        },
        "total_inference_time_ms": total_time_ms,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
