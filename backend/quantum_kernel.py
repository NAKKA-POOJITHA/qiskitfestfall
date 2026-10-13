"""
QuantumCure AI - Real Qiskit Quantum Kernel Module
Computes genuine quantum kernel matrices using Qiskit ZZFeatureMap circuits,
evaluates state fidelities, trains precomputed SVM, and validates mathematical invariants.
"""

import os
import time
import json
import warnings
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.svm import SVC
from sklearn.metrics.pairwise import rbf_kernel

# Suppress deprecation warnings from Qiskit 2.x
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import qiskit
    from qiskit.circuit.library import ZZFeatureMap
    from qiskit.quantum_info import Statevector
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    HAS_QISKIT = True
except ImportError:
    HAS_QISKIT = False


class QuantumKernelEngine:
    """
    Manages Qiskit ZZFeatureMap circuit generation, fidelity evaluation,
    matrix verification, caching, and precomputed SVM training.
    """
    def __init__(self, feature_dimension=5, reps=2, entanglement="linear", random_state=42):
        if not HAS_QISKIT:
            raise RuntimeError("Qiskit and Qiskit Machine Learning are required but not installed.")
        self.feature_dimension = feature_dimension
        self.reps = reps
        self.entanglement = entanglement
        self.random_state = random_state

        # Instantiate Qiskit ZZFeatureMap
        self.feature_map = ZZFeatureMap(
            feature_dimension=feature_dimension,
            reps=reps,
            entanglement=entanglement
        )
        self.qkernel = FidelityQuantumKernel(feature_map=self.feature_map)

    def compute_statevectors(self, X):
        """
        Computes statevectors for each input vector using Qiskit quantum circuit parameter binding.
        Strictly preserves Qiskit simulation semantics.
        """
        statevectors = []
        for x in X:
            bound_circ = self.feature_map.assign_parameters(x)
            sv = Statevector.from_instruction(bound_circ)
            statevectors.append(sv.data)
        return np.array(statevectors, dtype=complex)

    def evaluate_kernel_matrix(self, X1, X2=None):
        """
        Computes the quantum fidelity matrix K(x, y) = |<Phi(x)|Phi(y)>|^2.
        For X2=None, evaluates square symmetric matrix K(X1, X1).
        Uses exact Qiskit Statevector inner product for fast, machine-precision fidelity.
        """
        sv1 = self.compute_statevectors(X1)
        if X2 is None or X2 is X1:
            # Self inner-products
            inner = sv1 @ sv1.conj().T
            K = np.abs(inner) ** 2
            # Numerical cleanup: enforce exact symmetry and 1.0 diagonal
            K = 0.5 * (K + K.T)
            np.fill_diagonal(K, 1.0)
            return K
        else:
            sv2 = self.compute_statevectors(X2)
            inner = sv1 @ sv2.conj().T
            K = np.abs(inner) ** 2
            return K

    def verify_kernel_matrix(self, K, name="Train"):
        """
        Verifies mathematical invariants of the quantum kernel:
        1. Square dimensions (if self-kernel)
        2. Finite values (no NaNs or Infs)
        3. Unit diagonal (K_ii = 1.0)
        4. Strict symmetry (K_ij = K_ji)
        5. Valid fidelity bounds (0.0 <= K_ij <= 1.0)
        """
        n_rows, n_cols = K.shape
        is_finite = bool(np.isfinite(K).all())
        if not is_finite:
            raise ValueError(f"{name} kernel contains non-finite (NaN/Inf) values.")

        min_val = float(np.min(K))
        max_val = float(np.max(K))

        checks = {
            "is_finite": is_finite,
            "min_fidelity": min_val,
            "max_fidelity": max_val,
            "valid_bounds": bool(min_val >= -1e-6 and max_val <= 1.0 + 1e-6)
        }

        if n_rows == n_cols:
            diag = np.diag(K)
            diag_diff = float(np.max(np.abs(diag - 1.0)))
            sym_diff = float(np.max(np.abs(K - K.T)))
            checks["diagonal_unit_max_error"] = diag_diff
            checks["symmetry_max_error"] = sym_diff
            checks["is_symmetric"] = bool(sym_diff < 1e-5)
            checks["is_unit_diagonal"] = bool(diag_diff < 1e-5)

            if not checks["is_symmetric"]:
                raise ValueError(f"{name} kernel violates symmetry: max error = {sym_diff}")
            if not checks["is_unit_diagonal"]:
                raise ValueError(f"{name} kernel violates unit diagonal: max error = {diag_diff}")

        return checks


def train_quantum_model(
    X_train_sub,
    y_train_sub,
    X_test,
    patient_ids_train=None,
    patient_ids_test=None,
    cache_dir="results",
    models_dir="models",
    use_cache=True,
    C=1.0
):
    """
    Executes real Quantum Kernel learning pipeline:
    1. Evaluates K_train (N_train x N_train)
    2. Validates invariants
    3. Fits SVC(kernel='precomputed', probability=True)
    4. Evaluates K_test (N_test x N_train)
    5. Saves matrices, metadata, and model artifacts
    """
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    models_path = Path(models_dir)
    models_path.mkdir(parents=True, exist_ok=True)

    n_train = len(X_train_sub)
    n_test = len(X_test)
    n_features = X_train_sub.shape[1]

    engine = QuantumKernelEngine(feature_dimension=n_features, reps=2, entanglement="linear")

    # Cache metadata check
    cache_train_file = cache_path / "quantum_kernel_train.npy"
    cache_test_file = cache_path / "quantum_kernel_test.npy"
    meta_file = cache_path / "quantum_kernel_meta.json"

    meta_match = False
    if use_cache and cache_train_file.exists() and cache_test_file.exists() and meta_file.exists():
        try:
            with open(meta_file, "r") as f:
                saved_meta = json.load(f)
            if (saved_meta.get("n_train") == n_train and
                saved_meta.get("n_test") == n_test and
                saved_meta.get("n_features") == n_features):
                meta_match = True
        except Exception:
            meta_match = False

    t0_train = time.time()
    if meta_match and use_cache:
        print(f"Loading cached quantum kernel matrices from {cache_dir}...")
        K_train = np.load(cache_train_file)
        K_test = np.load(cache_test_file)
        train_kernel_time = 0.0
    else:
        print(f"Computing genuine Qiskit quantum kernel matrix (N_train={n_train})...")
        t_start = time.time()
        K_train = engine.evaluate_kernel_matrix(X_train_sub)
        train_kernel_time = time.time() - t_start
        print(f"Quantum train kernel computed in {train_kernel_time:.2f}s")

        print(f"Computing quantum test-to-train kernel matrix (N_test={n_test} x N_train={n_train})...")
        t_start_test = time.time()
        K_test = engine.evaluate_kernel_matrix(X_test, X_train_sub)
        test_kernel_time = time.time() - t_start_test
        print(f"Quantum test kernel computed in {test_kernel_time:.2f}s")

        # Save matrices to cache
        np.save(cache_train_file, K_train)
        np.save(cache_test_file, K_test)

    # Verify invariants
    train_checks = engine.verify_kernel_matrix(K_train, "Training")
    test_checks = engine.verify_kernel_matrix(K_test, "Test")

    # Fit precomputed SVM with balanced weights and calibrated probabilities
    print("Fitting precomputed Support Vector Classifier...")
    t_fit_start = time.time()
    q_svm = SVC(
        kernel="precomputed",
        C=C,
        class_weight="balanced",
        probability=True,
        random_state=42
    )
    q_svm.fit(K_train, y_train_sub)
    fit_time = time.time() - t_fit_start
    total_time = (time.time() - t0_train)

    # Also compute Classical RBF kernel on identical training vectors for comparative heatmap
    K_rbf_train = rbf_kernel(X_train_sub, X_train_sub)
    np.save(cache_path / "classical_rbf_kernel_train.npy", K_rbf_train)

    # Save metadata
    qiskit_ver = getattr(qiskit, "__version__", "unknown")
    meta_info = {
        "feature_map": "ZZFeatureMap",
        "feature_dimension": n_features,
        "reps": 2,
        "entanglement": "linear",
        "circuit_depth": int(engine.feature_map.decompose().depth()),
        "n_train": n_train,
        "n_test": n_test,
        "train_kernel_time_sec": round(train_kernel_time, 4),
        "svm_fit_time_sec": round(fit_time, 4),
        "total_quantum_time_sec": round(total_time, 4),
        "qiskit_version": qiskit_ver,
        "train_matrix_shape": list(K_train.shape),
        "test_matrix_shape": list(K_test.shape),
        "train_checks": train_checks,
        "test_checks": test_checks
    }
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)

    # Save model and inference training vectors
    q_svm_file = models_path / "quantum_svm.joblib"
    joblib.dump(q_svm, q_svm_file)

    q_features_file = models_path / "quantum_training_features.npy"
    np.save(q_features_file, X_train_sub)

    if patient_ids_train is not None:
        np.save(models_path / "quantum_train_patient_ids.npy", np.array(patient_ids_train))

    print(f"Quantum SVM model saved to {q_svm_file}")
    print(f"Training vectors saved to {q_features_file}")

    return {
        "model": q_svm,
        "engine": engine,
        "K_train": K_train,
        "K_test": K_test,
        "metadata": meta_info,
        "train_time_sec": round(total_time, 4)
    }
