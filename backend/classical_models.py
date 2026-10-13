"""
QuantumCure AI - Classical Machine Learning Models
Implements Classical RBF-SVM and XGBoost classifiers with fair cross-validation,
class imbalance handling, and artifact export.
"""

import os
import time
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import xgboost as xgb


def train_classical_svm(X_train, y_train, cv_folds=5, random_state=42):
    """
    Trains Classical RBF-SVM with hyperparameter grid search and class weighting.
    Uses probability=True for calibrated probabilities (Platt scaling).
    """
    t0 = time.time()
    param_grid = {
        "C": [0.5, 1.0, 2.0, 5.0],
        "gamma": ["scale", "auto", 0.1, 0.5]
    }
    
    base_svc = SVC(
        kernel="rbf",
        class_weight="balanced",
        probability=True,
        random_state=random_state
    )
    
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    grid = GridSearchCV(
        base_svc,
        param_grid,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1
    )
    grid.fit(X_train, y_train)
    
    train_time = time.time() - t0
    best_model = grid.best_estimator_
    
    return {
        "model": best_model,
        "best_params": grid.best_params_,
        "cv_best_score": float(grid.best_score_),
        "train_time_sec": round(train_time, 4)
    }


def train_xgboost(X_train, y_train, cv_folds=5, random_state=42):
    """
    Trains XGBoost classifier with imbalance compensation and hyperparameter tuning.
    """
    t0 = time.time()
    neg_count = int((y_train == 0).sum())
    pos_count = int((y_train == 1).sum())
    scale_pos_weight = max(1.0, float(neg_count) / max(1.0, float(pos_count)))
    
    param_grid = {
        "n_estimators": [50, 100],
        "max_depth": [3, 4],
        "learning_rate": [0.05, 0.1]
    }
    
    base_xgb = xgb.XGBClassifier(
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=random_state,
        use_label_encoder=False
    )
    
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    grid = GridSearchCV(
        base_xgb,
        param_grid,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1
    )
    grid.fit(X_train, y_train)
    
    train_time = time.time() - t0
    best_model = grid.best_estimator_
    
    return {
        "model": best_model,
        "best_params": grid.best_params_,
        "cv_best_score": float(grid.best_score_),
        "train_time_sec": round(train_time, 4),
        "feature_importances": [float(x) for x in best_model.feature_importances_]
    }


def save_classical_artifacts(svm_results, xgb_results, models_dir="models"):
    """Saves classical model artifacts to disk."""
    m_path = Path(models_dir)
    m_path.mkdir(parents=True, exist_ok=True)
    
    # Save SVM
    svm_file = m_path / "classical_svm.joblib"
    joblib.dump(svm_results["model"], svm_file)
    
    # Save XGBoost
    xgb_file = m_path / "xgboost_model.json"
    xgb_results["model"].save_model(str(xgb_file))
    
    # Also save joblib for python pickle convenience
    joblib.dump(xgb_results["model"], m_path / "xgboost_model.joblib")
    
    return {
        "svm_path": str(svm_file).replace("\\", "/"),
        "xgb_path": str(xgb_file).replace("\\", "/")
    }
