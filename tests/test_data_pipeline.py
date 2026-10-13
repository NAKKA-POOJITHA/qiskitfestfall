"""
Unit and Integration Tests for QuantumCure AI Data Pipeline
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from backend.data_preprocessing import (
    parse_ki67_value,
    PreprocessingPipeline,
    CORE_FEATURES,
    run_data_preprocessing
)
from backend.data_audit import audit_raw_dataset


def test_ki67_parsing():
    """Tests robust parsing of heterogeneous Ki67 strings."""
    assert parse_ki67_value("0.3") == 0.3
    assert parse_ki67_value("0.15") == 0.15
    assert parse_ki67_value("30-40%") == 0.35
    assert parse_ki67_value("＜5%") == 0.025
    assert parse_ki67_value("＞90%") == 0.95
    assert np.isnan(parse_ki67_value(None))


def test_data_audit():
    """Tests data audit report generation and validation."""
    res = audit_raw_dataset()
    assert res["status"] == "VERIFIED_READY"
    assert res["records_count"] == 1058
    assert res["target_identified"] is True
    assert res["duplicates"]["row_duplicates"] == 0
    assert "Number of lymph node metastases" in res["excluded_columns"]


def test_leakage_prevention_and_splitting():
    """Tests strict leakage prevention and patient-level split independence."""
    prep = run_data_preprocessing()
    train_df = prep["train_df"]
    test_df = prep["test_df"]

    # Verify patient independence (no overlap)
    train_pids = set(train_df["Patient ID"])
    test_pids = set(test_df["Patient ID"])
    overlap = train_pids.intersection(test_pids)
    assert len(overlap) == 0, f"Target leakage! Overlapping patient IDs: {overlap}"

    # Verify excluded columns are not in core features
    assert "Number of lymph node metastases" not in CORE_FEATURES
    assert "Patient ID" not in CORE_FEATURES
    assert "ALN status" not in CORE_FEATURES


def test_pipeline_transformation_bounds():
    """Tests that preprocessing pipeline scales features into [0, pi] without NaNs."""
    prep = run_data_preprocessing()
    X_train = prep["X_train"]
    X_test = prep["X_test"]

    assert X_train.shape[1] == 5
    assert X_test.shape[1] == 5
    assert np.isfinite(X_train).all()
    assert np.isfinite(X_test).all()
    assert X_train.min() >= -1e-6
    assert X_train.max() <= np.pi + 1e-5
