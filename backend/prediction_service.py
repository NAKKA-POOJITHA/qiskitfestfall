"""
QuantumCure AI - Prediction Service
Provides inference functions for individual patient records using
pre-trained models, the fitted preprocessing pipeline, and quantum fidelity projections.
"""

import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import xgboost as xgb
from backend.quantum_kernel import QuantumKernelEngine


class PredictionService:
    """
    Inference service managing trained models, preprocessing, and quantum similarity computation.
    """
    def __init__(self, models_dir="models", dataset_dir="dataset/processed"):
        self.models_path = Path(models_dir)
        self.dataset_path = Path(dataset_dir)
        self.pipeline = None
        self.classical_svm = None
        self.xgboost_model = None
        self.quantum_svm = None
        self.quantum_train_features = None
        self.quantum_engine = None
        self._is_loaded = False

    def load_artifacts(self):
        """Loads all persisted model artifacts and feature arrays."""
        pipeline_file = self.models_path / "preprocessing_pipeline.joblib"
        c_svm_file = self.models_path / "classical_svm.joblib"
        xgb_file = self.models_path / "xgboost_model.joblib"
        q_svm_file = self.models_path / "quantum_svm.joblib"
        q_feats_file = self.models_path / "quantum_training_features.npy"

        missing = []
        for name, f in [("Pipeline", pipeline_file), ("Classical SVM", c_svm_file),
                        ("XGBoost", xgb_file), ("Quantum SVM", q_svm_file),
                        ("Quantum Features", q_feats_file)]:
            if not f.exists():
                missing.append(f"{name} ({f.name})")

        if missing:
            raise FileNotFoundError(f"Missing required model artifacts: {', '.join(missing)}. Run training first.")

        self.pipeline = joblib.load(pipeline_file)
        self.classical_svm = joblib.load(c_svm_file)
        self.xgboost_model = joblib.load(xgb_file)
        self.quantum_svm = joblib.load(q_svm_file)
        self.quantum_train_features = np.load(q_feats_file)

        # Initialize Quantum Engine for inference with matching parameters
        n_features = self.quantum_train_features.shape[1]
        self.quantum_engine = QuantumKernelEngine(feature_dimension=n_features, reps=2, entanglement="linear")

        self._is_loaded = True
        return True

    def predict_patient(self, input_dict):
        """
        Runs multi-model inference for a patient.
        input_dict keys:
          - 'Tumour Size(cm)' (float)
          - 'Age(years)' (float)
          - 'Histological grading' (float 1, 2, or 3)
          - 'ER' ('Positive' or 'Negative')
          - 'HER2' ('Positive' or 'Negative')
        """
        if not self._is_loaded:
            self.load_artifacts()

        # Validate inputs
        val_errors = self._validate_inputs(input_dict)
        if val_errors:
            return {"success": False, "errors": val_errors}

        # Build single-row DataFrame
        df_row = pd.DataFrame([{
            "Tumour Size(cm)": float(input_dict["Tumour Size(cm)"]),
            "Age(years)": float(input_dict["Age(years)"]),
            "Histological grading": float(input_dict.get("Histological grading", 2.0)),
            "ER": str(input_dict.get("ER", "Negative")).strip().capitalize(),
            "HER2": str(input_dict.get("HER2", "Negative")).strip().capitalize()
        }])

        # Transform features using fitted pipeline
        X_scaled = self.pipeline.transform(df_row)  # shape (1, 5)

        # 1. Classical RBF-SVM prediction
        c_pred = int(self.classical_svm.predict(X_scaled)[0])
        c_score = float(self.classical_svm.predict_proba(X_scaled)[0, 1])
        c_decision = float(self.classical_svm.decision_function(X_scaled)[0])

        # 2. XGBoost prediction
        x_pred = int(self.xgboost_model.predict(X_scaled)[0])
        x_score = float(self.xgboost_model.predict_proba(X_scaled)[0, 1])

        # 3. Quantum-kernel SVM prediction
        # Compute quantum fidelity vector against saved training statevectors
        k_vec = self.quantum_engine.evaluate_kernel_matrix(X_scaled, self.quantum_train_features) # shape (1, N_train)
        q_pred = int(self.quantum_svm.predict(k_vec)[0])
        q_score = float(self.quantum_svm.predict_proba(k_vec)[0, 1])
        q_decision = float(self.quantum_svm.decision_function(k_vec)[0])

        # Agreement analysis
        preds = [q_pred, c_pred, x_pred]
        all_agree = (len(set(preds)) == 1)
        majority_vote = 1 if sum(preds) >= 2 else 0

        # Mean quantum similarity with training support
        mean_quantum_fidelity = float(np.mean(k_vec))
        max_quantum_fidelity = float(np.max(k_vec))

        return {
            "success": True,
            "inputs_received": input_dict,
            "scaled_features": [round(float(v), 4) for v in X_scaled[0]],
            "quantum_svm": {
                "prediction": q_pred,
                "label": "N+ (Metastasis Present)" if q_pred == 1 else "N0 (No Metastasis)",
                "probability": round(q_score, 4),
                "decision_score": round(q_decision, 4),
                "mean_training_fidelity": round(mean_quantum_fidelity, 4),
                "max_training_fidelity": round(max_quantum_fidelity, 4)
            },
            "classical_svm": {
                "prediction": c_pred,
                "label": "N+ (Metastasis Present)" if c_pred == 1 else "N0 (No Metastasis)",
                "probability": round(c_score, 4),
                "decision_score": round(c_decision, 4)
            },
            "xgboost": {
                "prediction": x_pred,
                "label": "N+ (Metastasis Present)" if x_pred == 1 else "N0 (No Metastasis)",
                "probability": round(x_score, 4)
            },
            "agreement": {
                "unanimous": all_agree,
                "majority_prediction": majority_vote,
                "majority_label": "N+ (Metastasis Present)" if majority_vote == 1 else "N0 (No Metastasis)",
                "models_positive": sum(preds),
                "models_negative": 3 - sum(preds)
            }
        }

    def _validate_inputs(self, input_dict):
        errors = []
        try:
            ts = float(input_dict.get("Tumour Size(cm)", -1))
            if ts <= 0 or ts > 20:
                errors.append("Tumour Size must be between 0.1 cm and 20.0 cm.")
        except (ValueError, TypeError):
            errors.append("Tumour Size must be a valid numeric value.")

        try:
            age = float(input_dict.get("Age(years)", -1))
            if age < 18 or age > 120:
                errors.append("Age must be between 18 and 120 years.")
        except (ValueError, TypeError):
            errors.append("Age must be a valid numeric value.")

        grade = input_dict.get("Histological grading")
        if grade is not None:
            try:
                g = float(grade)
                if g not in [1.0, 2.0, 3.0]:
                    errors.append("Histological grading must be 1, 2, or 3.")
            except (ValueError, TypeError):
                errors.append("Histological grading must be 1, 2, or 3.")

        er = str(input_dict.get("ER", "")).strip().capitalize()
        if er not in ["Positive", "Negative"]:
            errors.append("ER status must be either 'Positive' or 'Negative'.")

        her2 = str(input_dict.get("HER2", "")).strip().capitalize()
        if her2 not in ["Positive", "Negative"]:
            errors.append("HER2 status must be either 'Positive' or 'Negative'.")

        return errors

    def load_test_patients(self):
        """Loads genuine held-out test patients for the interactive demo."""
        test_file = self.dataset_path / "bcnb_test.csv"
        if not test_file.exists():
            return []
        df_test = pd.read_csv(test_file)
        return df_test
