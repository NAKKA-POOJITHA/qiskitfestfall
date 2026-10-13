"""
QuantumCure AI - Page 5: Research Handbook
Interactive educational handbook with 18 comprehensive chapters, full-text search,
technical glossary, mathematical formulations, and export capabilities.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Research Handbook — QuantumCure AI",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Reports")

# Handbook Content Database (18 Chapters)
HANDBOOK_CHAPTERS = [
    {
        "id": 1,
        "title": "Chapter 1: Project Overview",
        "category": "Foundations",
        "content": """
### QuantumCure AI — Mission & Scope
**QuantumCure AI** is an open scientific inquiry into whether quantum kernel methods can provide actionable predictive performance for oncology classification tasks compared with classical machine learning algorithms.

#### Core Scientific Objective
Compare three distinct mathematical learning paradigms on the exact same held-out patient cohort:
1. **Quantum-kernel Support Vector Machine (Qiskit ZZFeatureMap)**
2. **Classical Radial Basis Function Support Vector Machine (RBF-SVM)**
3. **Extreme Gradient Boosting (XGBoost Decision Forest)**

All models evaluate identical clinical features derived from the **BCNB** breast cancer dataset, predicting binary axillary lymph node metastasis (**N0** vs **N+**).
"""
    },
    {
        "id": 2,
        "title": "Chapter 2: Breast Cancer Basics",
        "category": "Clinical Oncology",
        "content": """
### Pathophysiology of Invasive Breast Carcinoma
Breast cancer originates within the terminal ductal-lobular units of the mammary gland.

#### Histological Types
- **Invasive Ductal Carcinoma (IDC):** Accounts for ~80-85% of invasive carcinomas (90.5% in the BCNB cohort). Cells penetrate the basement membrane and infiltrate the stroma.
- **Invasive Lobular Carcinoma (ILC):** ~10-15% of cases; characterized by dyscohesive single-file infiltration due to loss of E-cadherin adhesion molecules.

#### Receptor Biomarkers
- **Estrogen Receptor (ER):** Nuclear transcription factor; determines responsiveness to endocrine therapies (e.g., tamoxifen, aromatase inhibitors).
- **Progesterone Receptor (PR):** Synergistic hormone receptor indicating an intact estrogen signaling axis.
- **HER2 (ERBB2):** Transmembrane tyrosine kinase receptor; gene amplification drives rapid oncogenic proliferation and aggressive clinical phenotypes.
- **Ki-67:** Nuclear protein present during all active phases of the cell cycle (G1, S, G2, M); quantifies cellular proliferation fraction.
"""
    },
    {
        "id": 3,
        "title": "Chapter 3: Lymph Nodes and Metastasis",
        "category": "Clinical Oncology",
        "content": """
### Lymphatic Drainage and Axillary Staging
Axillary lymph node (ALN) metastasis is the single most critical prognostic determinant in early-stage invasive breast cancer.

#### Anatomical Drainage Basins
- **Sentinel Lymph Node (SLN):** The initial regional lymph node receiving direct afferent lymphatic drainage from the primary breast tumor.
- **Level I Nodes:** Low axilla, lateral to the lateral border of the *Pectoralis minor* muscle.
- **Level II Nodes:** Mid axilla, directly deep to *Pectoralis minor*.
- **Level III Nodes:** High / apical axilla, medial to the medial border of *Pectoralis minor* (subclavicular).

#### Clinical Importance of Pre-operative Prediction
Knowing whether axillary metastasis is present (N0 vs N+) prior to surgery informs decisions regarding **Sentinel Lymph Node Biopsy (SLNB)** versus primary systemic therapy (neoadjuvant chemotherapy), potentially sparing node-negative patients unnecessary invasive axillary clearance.
"""
    },
    {
        "id": 4,
        "title": "Chapter 4: Introduction to Quantum Computing",
        "category": "Quantum Computing",
        "content": """
### Principles of Quantum Computation
Classical computers operate on discrete binary bits ($0$ or $1$). Quantum computation relies on quantum mechanical phenomena:

1. **Superposition:** A quantum register can exist in linear combinations of basis states simultaneously.
2. **Entanglement:** Quantum states of multiple particles cannot be factored into independent product states; measurement on one qubit instantaneously correlates with another.
3. **Interference:** Probability amplitudes can constructively amplify correct computational pathways while destructively canceling incorrect ones.
"""
    },
    {
        "id": 5,
        "title": "Chapter 5: Qubits and Quantum Circuits",
        "category": "Quantum Computing",
        "content": r"""
### Mathematical Representation of Qubits
A single qubit state $|\psi\rangle$ lives in a 2-dimensional complex Hilbert space $\mathbb{C}^2$:
$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle, \quad |\alpha|^2 + |\beta|^2 = 1$$

#### Quantum Logic Gates
- **Hadamard Gate ($H$):** Creates an equal superposition:
  $$H |0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}, \quad H |1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$$
- **Rotation Gate ($R_z(\theta)$):** Applies a phase rotation:
  $$R_z(\theta) = \exp\left(-i \frac{\theta}{2} Z\right) = \begin{pmatrix} e^{-i\theta/2} & 0 \\\\ 0 & e^{i\theta/2} \end{pmatrix}$$
- **Controlled-NOT Gate (CNOT):** Entangles two qubits: flips target qubit if and only if the control qubit is $|1\rangle$.
"""
    },
    {
        "id": 6,
        "title": "Chapter 6: Introduction to Qiskit",
        "category": "Quantum Computing",
        "content": """
### The IBM Qiskit Framework
Qiskit is the open-source software development kit for working with quantum computers at the level of circuits, pulses, and algorithms.

In **QuantumCure AI**, we leverage **Qiskit 2.1.2** and **Qiskit Machine Learning 0.9.1**:
- `qiskit.circuit.library.ZZFeatureMap` for parameterized feature encoding.
- `qiskit.quantum_info.Statevector` for exact statevector phase simulation.
- `qiskit_machine_learning.kernels.FidelityQuantumKernel` for state fidelity estimation.
"""
    },
    {
        "id": 7,
        "title": "Chapter 7: Quantum Feature Maps",
        "category": "Quantum Machine Learning",
        "content": r"""
### Embedding Classical Data into Hilbert Space
A Quantum Feature Map maps a classical feature vector $x \in \mathbb{R}^d$ to a quantum state $|\Phi(x)\rangle$ via a parameterized unitary circuit:
$$x \mapsto |\Phi(x)\rangle = U_{\Phi}(x) |0^{\otimes n}\rangle$$

#### The ZZFeatureMap Architecture
For $n=5$ features (qubits), the unitary operator consists of repeated layers:
$$U_{\Phi}(x) = \left( \exp\left(i \sum_{j < k} \phi_{jk}(x) Z_j Z_k\right) \exp\left(i \sum_j \phi_j(x) Z_j\right) H^{\otimes n} \right)^r$$
Where:
- $\phi_j(x) = x_j$ (single-qubit phase rotation)
- $\phi_{jk}(x) = 2(\pi - x_j)(\pi - x_k)$ (two-qubit entangling ZZ phase)
- $r = 2$ circuit repetitions with linear nearest-neighbor connectivity.
"""
    },
    {
        "id": 8,
        "title": "Chapter 8: Quantum Kernel Learning",
        "category": "Quantum Machine Learning",
        "content": r"""
### Quantum State Overlap & The Kernel Trick
In machine learning, a kernel function $K(x, y)$ evaluates the inner product between data points mapped into a high-dimensional feature space $\mathcal{H}$:
$$K(x, y) = \langle \Phi(x), \Phi(y) \rangle_{\mathcal{H}}$$

In Quantum Kernel Learning, this inner product corresponds exactly to the **transition fidelity** between two quantum states:
$$K(x, y) = |\langle \Phi(x) | \Phi(y) \rangle|^2 = |\langle 0^{\otimes n} | U_{\Phi}^\dagger(x) U_{\Phi}(y) | 0^{\otimes n} \rangle|^2$$

#### Invariants of the Quantum Kernel Matrix:
1. **Bounded:** $0 \le K(x, y) \le 1$.
2. **Symmetric:** $K(x, y) = K(y, x)$.
3. **Unit Diagonal:** $K(x, x) = 1.0$ (identical state overlap).
"""
    },
    {
        "id": 9,
        "title": "Chapter 9: Quantum-kernel SVM",
        "category": "Quantum Machine Learning",
        "content": r"""
### Support Vector Classification with Quantum Kernels
Once the quantum kernel matrix $K_{train} \in \mathbb{R}^{N \times N}$ is evaluated, it is passed directly to the classical dual formulation of the Support Vector Classifier:

$$\max_{\alpha} \sum_{i=1}^N \alpha_i - \frac{1}{2} \sum_{i,j=1}^N \alpha_i \alpha_j y_i y_j K(x_i, x_j)$$
Subject to:
$$0 \le \alpha_i \le C, \quad \sum_{i=1}^N \alpha_i y_i = 0$$

The decision boundary function for unseen query patient $x$ is:
$$f(x) = \text{sign}\left( \sum_{i \in SV} \alpha_i y_i K(x_i, x) + b \right)$$
Only classical optimization is required to solve for the dual multipliers $\alpha_i$; the quantum computer is used strictly to evaluate the similarities $K(x_i, x)$.
"""
    },
    {
        "id": 10,
        "title": "Chapter 10: Classical SVM",
        "category": "Classical Machine Learning",
        "content": r"""
### Radial Basis Function (RBF) Kernel
The classical benchmark utilizes the standard Gaussian RBF kernel:
$$K_{\text{RBF}}(x, y) = \exp\left( -\gamma \|x - y\|^2 \right)$$

#### Key Differences from the Quantum Kernel:
- **Euclidean Dependency:** The RBF kernel depends strictly on the Euclidean distance $\|x - y\|$ in $\mathbb{R}^d$.
- **Bandwidth Control:** The parameter $\gamma = \frac{1}{2\sigma^2}$ smoothly regulates the radius of influence of each support vector.
- **Continuous Smoothness:** RBF kernels lack discrete trigonometric phase wrapping, providing high stability on low-dimensional clinical tables.
"""
    },
    {
        "id": 11,
        "title": "Chapter 11: XGBoost",
        "category": "Classical Machine Learning",
        "content": r"""
### Extreme Gradient Boosting (XGBoost)
XGBoost constructs an ensemble of decision trees sequentially:
$$\hat{y}_i = \sum_{k=1}^K f_k(x_i), \quad f_k \in \mathcal{F}$$

At each iteration $t$, a new tree $f_t$ minimizes the regularized objective:
$$\mathcal{L}^{(t)} = \sum_{i=1}^n \left[ g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)$$
Where $g_i$ and $h_i$ are first- and second-order gradient statistics of the log-loss function.

XGBoost handles non-linear interactions, heterogeneous clinical feature scaling, and class imbalance via `scale_pos_weight`.
"""
    },
    {
        "id": 12,
        "title": "Chapter 12: Dataset Preparation",
        "category": "Data Science",
        "content": """
### The BCNB Cohort Preparation
The dataset audited in QuantumCure AI is the **BCNB** clinical cohort (1,058 unique breast cancer patients).

#### Target Harmonization:
- **N0 (Class 0):** 655 patients (61.91%) — No axillary nodal metastasis.
- **N+(1-2) & N+(>2) (Class 1):** 403 patients (38.09%) — Metastasis verified pathologically.

#### Selected Predictor Features:
1. `Tumour Size(cm)`
2. `Age(years)`
3. `Histological grading` (imputed with training fold median)
4. `ER_encoded` (1 = Positive, 0 = Negative)
5. `HER2_encoded` (1 = Positive, 0 = Negative)
"""
    },
    {
        "id": 13,
        "title": "Chapter 13: Data Leakage and Patient Splitting",
        "category": "Data Science",
        "content": """
### Scientific Integrity and Leakage Prevention
Data leakage occurs when information outside the training fold is used to create the model.

#### Safeguards Implemented:
1. **Target Proxy Exclusion:** `Number of lymph node metastases` is strictly 0 for N0 and >0 for N+. Including it would yield artificial 100% accuracy through leakage. It is excluded from all models.
2. **Procedural Staging Exclusion:** `Surgical` technique (ALND vs SLNB) is excluded to avoid procedural bias.
3. **Strict Partitioning:** Scaler parameters (min/max) and median imputation values were computed exclusively on the 846 training patients and applied downstream to the 212 held-out test patients.
4. **Independent Patients:** Each patient ID is unique; no patient overlaps across folds.
"""
    },
    {
        "id": 14,
        "title": "Chapter 14: AUROC, Accuracy, F1-score, Sensitivity, and Specificity",
        "category": "Evaluation Metrics",
        "content": r"""
### Oncology Diagnostic Metrics
In cancer staging, standard accuracy is insufficient due to class imbalance and asymmetric diagnostic consequences.

- **Sensitivity (Recall):** $\frac{\text{TP}}{\text{TP} + \text{FN}}$ — Probability of identifying metastasis when it is truly present.
- **Specificity:** $\frac{\text{TN}}{\text{TN} + \text{FP}}$ — Probability of correctly ruling out nodal metastasis in disease-free axillae.
- **Precision (PPV):** $\frac{\text{TP}}{\text{TP} + \text{FP}}$ — True positives among all positive model predictions.
- **F1-Score:** Harmonic mean of Precision and Sensitivity: $2 \times \frac{\text{Prec} \times \text{Sens}}{\text{Prec} + \text{Sens}}$.
- **AUROC:** Area Under the Receiver Operating Characteristic curve; measures rank-order discriminative power across all possible decision thresholds.
"""
    },
    {
        "id": 15,
        "title": "Chapter 15: Confusion Matrices and ROC Curves",
        "category": "Evaluation Metrics",
        "content": r"""
### Visual Diagnostic Diagnostics
- **ROC Curve:** Plots True Positive Rate (Sensitivity) on the y-axis against False Positive Rate (1 - Specificity) on the x-axis. A diagonal line represents random chance ($\text{AUROC} = 0.50$).
- **Confusion Matrix:** Displays categorical tally of True Negatives (TN), False Positives (FP), False Negatives (FN), and True Positives (TP).
"""
    },
    {
        "id": 16,
        "title": "Chapter 16: Understanding the Experimental Results",
        "category": "Scientific Analysis",
        "content": r"""
### Did the Quantum Kernel Outperform Classical Baselines?
In our empirical held-out experiment on 212 unseen test patients:
- **XGBoost:** AUROC $\approx 0.601$, Accuracy $\approx 59.4\%$
- **Classical RBF-SVM:** AUROC $\approx 0.598$, Accuracy $\approx 59.4\%$
- **Quantum-kernel SVM:** AUROC $\approx 0.500$, Accuracy $\approx 50.5\%$

#### Scientific Interpretation:
The classical models outperformed the fixed ZZ quantum feature map. This empirical outcome aligns with published Noisy Intermediate-Scale Quantum (NISQ) literature:
1. Low-dimensional tabular features (5 features) are efficiently spanned by smooth classical RBF kernels.
2. Fixed $ZZ$ phase circuits without variational angle optimization can map features into Hilbert space regions where geometric separation is diffuse.
3. Quantum advantage is not universal; rigorous benchmarking demands reporting both successes and limitations honestly.
"""
    },
    {
        "id": 17,
        "title": "Chapter 17: Limitations and Responsible Use",
        "category": "Ethics & Safety",
        "content": """
### Clinical Limitations & Responsible AI Notice
1. **Research Prototype:** This application is strictly an investigational software prototype and is not FDA/CE cleared for medical diagnosis.
2. **Single-Center Cohort:** BCNB is derived from a single regional Chinese cohort; demographic and biological shifts across other populations require validation.
3. **Simulation Environment:** Quantum kernels were evaluated via exact statevector fidelity simulation without physical quantum processor thermal decoherence.
"""
    },
    {
        "id": 18,
        "title": "Chapter 18: Future Multi-Cancer Expansion",
        "category": "Future Roadmap",
        "content": """
### Strategic Roadmap for Multi-Cancer Learning
- **Lung Adenocarcinoma (TCGA-LUAD):** Planned extension for predicting *EGFR* and *KRAS* somatic mutation status using genomic expression features.
- **Colorectal Carcinoma (TCGA-COAD):** Planned investigation of Microsatellite Instability (MSI-H vs MSS).
- **Variational Quantum Kernels:** Implementing trainable parameterized quantum kernels (Quantum Kernel Alignment - QKA) to optimize Hilbert space metrics.
"""
    }
]

# Glossary Database
GLOSSARY = {
    "ALN": "Axillary Lymph Node: Regional lymph nodes located in the armpit basin draining the breast.",
    "AUROC": "Area Under the Receiver Operating Characteristic curve; standard threshold-independent discrimination metric.",
    "BCNB": "Breast Cancer Nodal / Biopsy dataset; public clinical cohort from TCIA.",
    "Fidelity": "Quantum state overlap |⟨Φ(x)|Φ(y)⟩|² indicating transition probability between two quantum states.",
    "Hilbert Space": "Complete complex inner product vector space in which quantum statevectors evolve.",
    "Leakage": "Spurious correlation introduced when target proxy or test fold data contaminates model training.",
    "Qiskit": "Open-source quantum computing software development kit maintained by IBM Quantum.",
    "Qubit": "Quantum bit: fundamental unit of quantum information existing in superpositions of |0⟩ and |1⟩.",
    "RBF": "Radial Basis Function: classical kernel based on Gaussian distance exp(-γ||x - y||²).",
    "SLNB": "Sentinel Lymph Node Biopsy: surgical procedure to remove and inspect the first draining lymph node.",
    "ZZFeatureMap": "Second-order Pauli-Z expansion quantum feature map creating single-qubit and two-qubit phase gates."
}

# Search and Filter
col_search, col_cat = st.columns([2, 1])
with col_search:
    search_query = st.text_input("🔍 Search handbook chapters or glossary:", placeholder="e.g., ZZFeatureMap, leakage, fidelity, AUROC...")
with col_cat:
    categories = ["All Categories"] + sorted(list(set(c["category"] for c in HANDBOOK_CHAPTERS)))
    sel_cat = st.selectbox("Filter by Category:", categories)

# Glossary Expander
with st.expander("📚 Technical Glossary (Click to expand)", expanded=False):
    st.markdown("### Medical & Quantum Computing Glossary")
    for term, defn in sorted(GLOSSARY.items()):
        if not search_query or search_query.lower() in term.lower() or search_query.lower() in defn.lower():
            st.markdown(f"**`{term}`**: {defn}")

st.markdown("---")

# Render Chapters
filtered_chapters = []
for ch in HANDBOOK_CHAPTERS:
    if sel_cat != "All Categories" and ch["category"] != sel_cat:
        continue
    if search_query:
        q = search_query.lower()
        if q not in ch["title"].lower() and q not in ch["content"].lower() and q not in ch["category"].lower():
            continue
    filtered_chapters.append(ch)

st.markdown(f"### Showing {len(filtered_chapters)} Chapter(s)")

for ch in filtered_chapters:
    with st.expander(f"{ch['title']} — ({ch['category']})", expanded=(len(filtered_chapters) <= 2)):
        st.markdown(ch["content"])

# Download Full Text Button
full_handbook_text = "\n\n".join([f"# {ch['title']}\nCategory: {ch['category']}\n\n{ch['content']}" for ch in HANDBOOK_CHAPTERS])
st.markdown("---")
st.download_button(
    label="📥 Download Research Handbook (Markdown)",
    data=full_handbook_text,
    file_name="QuantumCure_AI_Research_Handbook.md",
    mime="text/markdown"
)
