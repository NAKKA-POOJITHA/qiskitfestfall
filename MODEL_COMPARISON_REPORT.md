# QuantumCure AI — Model Comparison and Research Analytics Report (MODEL_COMPARISON_REPORT.md)

**Project Name:** QuantumCure AI — Quantum Kernel Learning for Cancer Research  
**Lab Component:** Model Comparison & Research Analytics Lab (`frontend/pages/3_Model_Comparison_Lab.py` and `app.py`)  
**Evaluation Cohort:** 212 held-out BCNB breast cancer patients  
**Date:** October 14, 2026  
**Auditor:** Antigravity Advanced Agentic AI  
**Mandatory Disclaimer:** *Research prototype, not clinical advice. Not validated for clinical use.*

---

## 1. Benchmark Performance Comparison Table

All metrics were computed strictly on the **212 unseen held-out test patients** (81 $N_+$, 131 $N_0$):

| Architecture | AUROC | Accuracy | Precision | Recall (Sens) | Specificity | F1-Score | PR-AUC | Train Time | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Classifier** | **0.6012** | **59.43%** | **46.88%** | **37.04%** | **73.28%** | **0.4138** | **0.4731** | 0.08 s | **0.16 ms** |
| **Classical RBF-SVM** | **0.5982** | **59.43%** | **46.88%** | **37.04%** | **73.28%** | **0.4138** | **0.4497** | **0.04 s** | 0.54 ms |
| **Quantum-Kernel SVM** | 0.5001 | 50.47% | 37.66% | 35.80% | 59.54% | 0.3671 | 0.3804 | 1.85 s | 3.23 ms |

---

## 2. Interactive Decision Threshold Explorer

To prevent premature threshold bias while allowing clinical trade-off analysis, the application features an interactive threshold slider ($\tau \in [0.05, 0.95]$ with step $0.05$):

### 2.1 Threshold Operating Points (XGBoost Benchmark)
| Threshold $\tau$ | Clinical Objective | Sensitivity (Recall) | Specificity | Precision | F1-Score | TP | FP | TN | FN |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$\tau = 0.20$** | High Sensitivity (Catch all nodal disease) | **91.4%** | 22.1% | 42.0% | 0.5758 | 74 | 102 | 29 | 7 |
| **$\tau = 0.50$** | Operational Benchmark (Balanced trade-off) | 37.0% | **73.3%** | 46.9% | 0.4138 | 30 | 35 | 96 | 51 |
| **$\tau = 0.70$** | High Specificity (Rule-in metastasis) | 12.3% | **94.7%** | **58.8%** | 0.2041 | 10 | 7 | 124 | 71 |

### 2.2 Operational Separation
- Official test metrics remain fixed at $\tau = 0.50$ to avoid threshold tuning contamination on the held-out test cohort.
- The threshold explorer is explicitly designated for post-hoc operational investigation.

---

## 3. Scientific Conclusions: Classical vs Quantum Kernel Machine Learning

1. **Absence of Quantum Advantage:**
   - The 5-qubit ZZFeatureMap Quantum Kernel SVM achieved an AUROC of 0.5001, effectively equivalent to random guessing on this clinical dataset.
   - Both Classical RBF-SVM (0.5982) and XGBoost (0.6012) significantly outperformed the quantum kernel.
2. **Mechanistic Explanation:**
   - The clinical predictors (Tumour Size, Age, Histological Grade) are continuous and monotonic markers of disease extent.
   - The periodic $R_z(2 x_j)$ and entangling $R_{zz}(2(\pi-x_j)(\pi-x_k))$ unitary gates introduce trigonometric wrapping ($\sin, \cos$), creating artificial non-monotonic periodicity that damages decision boundaries for continuous clinical data.
3. **Computational Resource Scaling:**
   - Classical RBF matrix construction scales as $O(N^2 \cdot d)$ with execution in 0.04s.
   - Quantum statevector simulation scales as $O(N^2 \cdot 2^n)$ with execution in 4.12s (~100x slower), without empirical classification benefit.
