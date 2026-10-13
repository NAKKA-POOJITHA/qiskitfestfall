# QuantumCure AI — Training Pipeline Summary

**Experiment Date & Status:** COMPLETED  
**Target:** Axillary lymph-node metastasis (Class 0: N0, Class 1: N+)  
**Training Patients:** 100 (Stratified subset for fair quantum comparison)  
**Held-out Test Patients:** 212  
**Features:** Tumour Size(cm), Age(years), Histological grading, ER_encoded, HER2_encoded  
**Total Pipeline Runtime:** 19.54 seconds  

---

## Model Benchmark Results (Held-out Test Cohort)
| Model | AUROC | Accuracy | F1-Score | Sensitivity | Specificity | Precision | Train Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Quantum-kernel SVM** | 0.5001 | 50.47% | 0.3312 | 0.3210 | 0.6183 | 0.3421 | 1.5475s |
| **Classical RBF-SVM** | 0.5982 | 59.43% | 0.5000 | 0.5309 | 0.6336 | 0.4725 | 13.3594s |
| **XGBoost** | 0.6012 | 59.43% | 0.5169 | 0.5679 | 0.6107 | 0.4742 | 2.0361s |

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
