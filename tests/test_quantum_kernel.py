"""
Unit Tests for QuantumCure AI Quantum Kernel Engine
"""

import pytest
import numpy as np
from backend.quantum_kernel import QuantumKernelEngine


def test_quantum_kernel_invariants():
    """Tests dimensions, unit diagonal, symmetry, and fidelity bounds of QuantumKernelEngine."""
    engine = QuantumKernelEngine(feature_dimension=5, reps=2, entanglement="linear")

    # Generate synthetic feature vectors within [0, pi]
    np.random.seed(42)
    X_sample = np.random.uniform(0.0, np.pi, size=(10, 5))

    # Evaluate square training kernel
    K = engine.evaluate_kernel_matrix(X_sample)

    # 1. Dimensions check
    assert K.shape == (10, 10)

    # 2. Finite values check
    assert np.isfinite(K).all()

    # 3. Unit diagonal check
    diag = np.diag(K)
    assert np.allclose(diag, 1.0, atol=1e-5), f"Diagonal not unit: {diag}"

    # 4. Strict symmetry check
    assert np.allclose(K, K.T, atol=1e-5), "Kernel matrix is not symmetric"

    # 5. Transition fidelity bounds [0, 1]
    assert np.all(K >= -1e-6)
    assert np.all(K <= 1.0 + 1e-6)

    # 6. Verify method passes without exception
    checks = engine.verify_kernel_matrix(K, "TestSynthetic")
    assert checks["is_symmetric"] is True
    assert checks["is_unit_diagonal"] is True


def test_quantum_test_kernel_dimensions():
    """Tests rectangular test-to-training kernel evaluation."""
    engine = QuantumKernelEngine(feature_dimension=5, reps=2, entanglement="linear")
    X_train = np.random.uniform(0.0, np.pi, size=(8, 5))
    X_test = np.random.uniform(0.0, np.pi, size=(5, 5))

    K_test = engine.evaluate_kernel_matrix(X_test, X_train)
    assert K_test.shape == (5, 8)
    assert np.isfinite(K_test).all()
    assert np.all(K_test >= -1e-6)
    assert np.all(K_test <= 1.0 + 1e-6)
