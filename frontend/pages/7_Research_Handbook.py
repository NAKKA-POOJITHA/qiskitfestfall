"""
QuantumCure AI - Page 7: Research Handbook
Full implementation of Master Prompt Part 13:
- 18 comprehensive chapters covering oncology, quantum computing, feature maps, and metrics
- Full-text interactive chapter search and chapter selector
- Technical glossary with rigorous clinical and quantum definitions
- Equations, markdown formatting, and citations
- Downloadable research handbook export
- Strict No-Emoji policy
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Research Handbook — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Research Handbook")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Research Handbook
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Comprehensive 18-chapter reference curriculum on quantum kernel learning, precision oncology, and statistical evaluation.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# 18 Chapters Database
HANDBOOK_CHAPTERS = [
    {
        "id": 1,
        "title": "Chapter 1: Project Overview & Clinical Mission",
        "category": "Foundations",
        "content": """
### QuantumCure AI — Mission & Scope
**QuantumCure AI** is an applied medical AI research platform designed to investigate whether quantum kernel learning (specifically, Qiskit-based `ZZFeatureMap` Quantum Kernel Support Vector Machines) provides an empirical advantage over state-of-the-art classical models for predicting **axillary lymph node metastasis in breast cancer patients**.

#### Core Scientific Objective
Benchmark three learning architectures on the exact same held-out patient cohort:
1. **Classical Radial Basis Function Support Vector Machine (RBF-SVM)**
2. **Extreme Gradient Boosting (XGBoost Decision Forest)**
3. **Quantum-kernel Support Vector Machine (Qiskit ZZFeatureMap)**

All models evaluate identical clinical biomarkers derived from the **BCNB** breast cancer dataset, predicting binary axillary lymph node metastasis (**N0** vs **N+**).
"""
    },
    {
        "id": 2,
        "title": "Chapter 2: Breast Cancer Pathophysiology",
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
        "title": "Chapter 3: Axillary Lymph Node Metastasis & Staging",
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
Knowing whether axillary metastasis is present (N0 vs N+) prior to surgery informs decisions regarding **Sentinel Lymph Node Biopsy (SLNB)** versus primary systemic therapy (neoadjuvant chemotherapy), potentially sparing node-negative patients unnecessary invasive axillary clearance with attendant chronic lymphedema risks.
"""
    },
    {
        "id": 4,
        "title": "Chapter 4: Principles of Quantum Computing",
        "category": "Quantum Computing",
        "content": """
### Principles of Quantum Computation
Classical computers operate on discrete binary bits (0 or 1). Quantum computation relies on quantum mechanical phenomena:

1. **Superposition:** A quantum register can exist in linear combinations of basis states simultaneously:
   `|ψ⟩ = α|0⟩ + β|1⟩, where |α|² + |β|² = 1`
2. **Entanglement:** Quantum states of multiple particles cannot be factored into independent product states; measurement on one qubit instantaneously correlates with another.
3. **Interference:** Probability amplitudes can constructively amplify correct computational pathways while destructively canceling incorrect ones.
"""
    },
    {
        "id": 5,
        "title": "Chapter 5: Qubits and Quantum Gates",
        "category": "Quantum Computing",
        "content": """
### Quantum Logic Gates
Unitary matrices acting on single- and multi-qubit registers:
- **Hadamard (H):** Creates equal superposition: `H|0⟩ = (|0⟩ + |1⟩)/√2`.
- **Pauli-X (NOT):** Bit-flip operation: `X|0⟩ = |1⟩, X|1⟩ = |0⟩`.
- **Pauli-Z (Phase Flip):** `Z|0⟩ = |0⟩, Z|1⟩ = -|1⟩`.
- **Controlled-NOT (CX):** Two-qubit entangling gate: flips target qubit if and only if control qubit is in state |1⟩.
- **Rotations R_Y(θ), R_Z(θ):** Continuous single-qubit rotations along the Bloch sphere axes.
"""
    },
    {
        "id": 6,
        "title": "Chapter 6: Quantum State Representation and the Bloch Sphere",
        "category": "Quantum Computing",
        "content": """
### The Bloch Sphere Geometry
Any pure single-qubit state can be represented as a point on the surface of a unit sphere in 3D Euclidean space:
`|ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩`
where:
- `θ ∈ [0, π]` is the polar angle (colatitude)
- `φ ∈ [0, 2π]` is the azimuthal angle (longitude)

State `|0⟩` corresponds to the North Pole `(θ=0)`, and `|1⟩` corresponds to the South Pole `(θ=π)`.
"""
    },
    {
        "id": 7,
        "title": "Chapter 7: Quantum Feature Maps and Hilbert Spaces",
        "category": "Quantum Machine Learning",
        "content": """
### Quantum Data Encoding
To classify classical clinical data with a quantum computer, classical vectors `x ∈ R^d` must be mapped into quantum state vectors `|Φ(x)⟩` in a Hilbert space `H` of dimension `2^n`:
`x → |Φ(x)⟩ = U_Φ(x) |0^⊗n⟩`

#### The ZZFeatureMap Formalism
In Qiskit 2.1.2, the second-order Pauli expansion `ZZFeatureMap` employs single-qubit rotations and pairwise entangling phases:
`U_Φ(x) = exp( i ∑_j x_j Z_j + i ∑_{j<k} (π - x_j)(π - x_k) Z_j Z_k ) · H^{⊗n}`
This creates non-linear correlations between biomarkers in a 32-dimensional complex space (for n=5 qubits).
"""
    },
    {
        "id": 8,
        "title": "Chapter 8: Quantum Kernel Estimation and Fidelity",
        "category": "Quantum Machine Learning",
        "content": """
### The Fidelity Quantum Kernel
The inner product between two quantum state vectors defines the kernel function:
`K(x_i, x_j) = |⟨Φ(x_i)|Φ(x_j)⟩|²`

#### Mathematical Properties
1. **Self-Fidelity Unit Diagonal:** `K(x_i, x_i) = |⟨Φ(x_i)|Φ(x_i)⟩|² = 1.0`
2. **Symmetry (Hermiticity):** `K(x_i, x_j) = K(x_j, x_i)`
3. **Bounded Range:** `0 ≤ K(x_i, x_j) ≤ 1.0`
4. **Positive Semi-Definite:** Ensures the kernel matrix is a valid Mercer kernel for convex quadratic programming optimization in SVMs.
"""
    },
    {
        "id": 9,
        "title": "Chapter 9: Quantum Support Vector Machines (QSVM)",
        "category": "Quantum Machine Learning",
        "content": """
### Quantum Kernel SVM Formulation
The Quantum SVM replaces the classical kernel function with the precomputed quantum fidelity matrix:
`max_α ∑_{i=1}^N α_i - 0.5 ∑_{i,j=1}^N α_i α_j y_i y_j K_Q(x_i, x_j)`
subject to:
`0 ≤ α_i ≤ C` and `∑_{i=1}^N α_i y_i = 0`

The decision function for a new patient `x*` is evaluated as:
`f(x*) = sign( ∑_{i ∈ SV} α_i y_i K_Q(x_i, x*) + b )`
where `K_Q(x_i, x*) = |⟨Φ(x_i)|Φ(x*)⟩|²` is computed via Qiskit transition simulation.
"""
    },
    {
        "id": 10,
        "title": "Chapter 10: Classical Support Vector Machines (RBF-SVM)",
        "category": "Classical Machine Learning",
        "content": """
### Classical Radial Basis Function (RBF) Kernel
The RBF Gaussian kernel is the state-of-the-art classical baseline for continuous tabular data:
`K_RBF(x_i, x_j) = exp( -γ ||x_i - x_j||² )`

#### Hyperparameters
- **C:** Regularization parameter controlling the trade-off between maximizing margin width and penalizing slack errors (set to C=2.0 in our benchmark).
- **γ (gamma):** Kernel bandwidth parameter defining the sphere of influence of individual support vectors (tuned to γ=0.5).
"""
    },
    {
        "id": 11,
        "title": "Chapter 11: Gradient Boosted Trees (XGBoost)",
        "category": "Classical Machine Learning",
        "content": """
### Extreme Gradient Boosting (XGBoost)
XGBoost builds an ensemble of shallow regression trees greedily minimizing a regularized objective:
`Obj(t) = ∑_{i=1}^N L(y_i, ŷ_i^{(t-1)} + f_t(x_i)) + Ω(f_t)`
where `Ω(f_t) = γ T + 0.5 λ ∑_{j=1}^T w_j²`.

#### Why XGBoost Excels on Tabular Clinical Data
- Naturally models orthogonal decision boundaries without requiring smooth distance metrics.
- Immune to feature scale disparities.
- Handles non-linear feature interactions and missing values robustly.
"""
    },
    {
        "id": 12,
        "title": "Chapter 12: BCNB Dataset Audit and Provenance",
        "category": "Data Engineering",
        "content": """
### BCNB Breast Cancer Clinical Dataset Audit
- **Source:** The Cancer Imaging Archive (TCIA) / Nature Scientific Data (CC BY 4.0 license).
- **Cohort Size:** 1,058 consecutive breast cancer patients with definitive histological ALN staging.
- **Class Distribution:**
  - `N0` (Negative): 655 patients (61.91%)
  - `N+(1-2)` (1 to 2 metastases): 210 patients (19.85%)
  - `N+(>2)` (>2 metastases): 193 patients (18.24%)
- **Binary Target:** N0 = 0 (655 patients), N+ = 1 (403 patients).
"""
    },
    {
        "id": 13,
        "title": "Chapter 13: Data Preprocessing and Leakage Prevention",
        "category": "Data Engineering",
        "content": """
### Zero-Leakage Data Processing Protocol
1. **Target Leakage Exclusion:** `Number of lymph node metastases` and surgical procedure (`Surgical`) were strictly removed from candidate feature sets.
2. **Patient-Level Stratified Partition:** 80% training (846 patients) and 20% held-out test (212 patients) using fixed random seed (Seed = 42).
3. **Training-Only Scaling:** Scikit-learn `MinMaxScaler([0, π])` was fitted strictly on the 846 training cases and applied transform-only to test cases.
4. **Missing Value Imputation:** Missing histological grades (12.48%) were imputed with the training median.
"""
    },
    {
        "id": 14,
        "title": "Chapter 14: Model Evaluation Metrics & Class Imbalance",
        "category": "Evaluation Science",
        "content": """
### Statistical Metrics in Clinical Oncology
- **AUROC (Area Under ROC):** Measures discrimination threshold-independently. Insensitive to class prevalence.
- **PR-AUC (Precision-Recall Area):** Highly informative under class imbalance (positive prevalence 38.2%). Chance baseline equals prevalence.
- **Sensitivity (Recall):** `TP / (TP + FN)`. Fraction of true metastases detected.
- **Specificity:** `TN / (TN + FP)`. Fraction of node-negative patients correctly classified.
- **F1-Score:** Harmonic mean of precision and recall.
"""
    },
    {
        "id": 15,
        "title": "Chapter 15: Model Interpretability & Explainability",
        "category": "Evaluation Science",
        "content": """
### Model Interpretability Methods
- **XGBoost Gain & Cover:** Ranks features by average reduction in loss when used in tree splits.
- **SVM Support Vector Analysis:** Margin geometry and distance `f(x) = ∑ α_i y_i K(x_i, x) + b`.
- **Quantum Fidelity Analysis:** Inspects sample similarity in Hilbert space.
- **Causality Caveat:** Model feature importance quantifies associative predictive utility; it does NOT establish biological etiology or mechanistic causation.
"""
    },
    {
        "id": 16,
        "title": "Chapter 16: Computational Complexity and Hardware Realities",
        "category": "Quantum Computing",
        "content": """
### Computational Cost: Classical vs Quantum
- **Classical RBF:** Vectorized Euclidean distance matrix construction scales as `O(N² · d)`. Takes 0.04s.
- **Quantum Statevector Simulation:** Simulating 5 qubits on classical CPU scales as `O(N · M · 2^n · L)` where n=5, L=depth=22. Takes 4.12s.
- **Hardware Realities:** State-of-the-art NISQ physical processors suffer from two-qubit gate infidelities (~0.5–1.0%) and decoherence (T1/T2 times). Real quantum advantage requires fault-tolerant logical qubits with quantum error correction (QEC).
"""
    },
    {
        "id": 17,
        "title": "Chapter 17: Clinical Ethics and Regulatory Boundaries",
        "category": "Bioethics & Governance",
        "content": """
### Clinical Ethics & Responsible Medical AI
1. **Research Prototype Designation:** QuantumCure AI is strictly an investigational research prototype. It has not undergone FDA 510(k), CE mark, or prospectively validated clinical trials.
2. **Clinical Decision Making:** Models must never be used autonomously to guide surgical intervention or systemic therapy.
3. **Data Privacy:** All patient IDs are anonymized; zero PHI/PII is persisted.
"""
    },
    {
        "id": 18,
        "title": "Chapter 18: Multi-Cancer Expansion Roadmap",
        "category": "Future Directions",
        "content": """
### Extensible Multi-Cancer Research Roadmap
- **Breast Cancer (BCNB):** Fully implemented, verified, and audited.
- **Lung Cancer (TCGA-LUAD):** Planned future task investigating EGFR / KRAS mutation status from genomic RNA-seq.
- **Colorectal Cancer (TCGA-COAD):** Planned task for Microsatellite Instability (MSI) status.
Each task requires its own independent dataset, feature dictionary, preprocessing pipeline, and verified model artifacts.
"""
    }
]

# Technical Glossary
GLOSSARY = {
    "ALN (Axillary Lymph Node)": "Regional lymph nodes located in the axilla that represent the primary lymphatic drainage basin for early breast carcinomas.",
    "AUROC": "Area Under the Receiver Operating Characteristic curve; quantifies binary classification discrimination across all decision thresholds.",
    "BCNB": "Breast Cancer Nodal / Biopsy dataset curated on TCIA comprising 1,058 biopsy records with pathological axillary node staging.",
    "Bloch Sphere": "Geometric representation of a 2-level quantum system (qubit) as a point on the surface of a unit 3D sphere.",
    "Fidelity Inner Product": "The squared modulus of the transition amplitude between two quantum states |⟨Φ(x)|Φ(y)⟩|², bounded in [0, 1].",
    "IDC (Invasive Ductal Carcinoma)": "The most common form of invasive breast cancer (~85% of cases), originating in milk duct epithelium and infiltrating stroma.",
    "N0 Status": "Pathological stage indicating zero metastatic involvement detected in regional axillary lymph nodes.",
    "N+ Status": "Pathological stage indicating the presence of metastatic tumor deposits within one or more regional axillary lymph nodes.",
    "Platt Scaling": "Logistic sigmoid transformation fitted on SVM decision scores to generate well-calibrated posterior probabilities.",
    "PR-AUC": "Area Under the Precision-Recall Curve; robust metric for evaluating classifiers on class-imbalanced datasets.",
    "Qubit": "Quantum bit; the fundamental unit of quantum information existing as a linear superposition of orthogonal basis states |0⟩ and |1⟩.",
    "RBF (Radial Basis Function)": "Real-valued Gaussian kernel function exp(-γ||x - y||²) widely utilized in classical Support Vector Machines.",
    "SLNB (Sentinel Lymph Node Biopsy)": "Minimally invasive surgical procedure to identify and resect the primary drainage lymph node(s) for pathological staging.",
    "Target Leakage": "Unintended inclusion of information in predictor features that would not be available at decision time (e.g., post-operative node counts).",
    "XGBoost": "Extreme Gradient Boosting; an efficient, scalable implementation of gradient boosted decision trees optimized for tabular datasets.",
    "ZZFeatureMap": "Second-order Pauli expansion quantum feature map implementing single-qubit rotations and pairwise ZZ phase couplings."
}

# Search Bar
search_query = st.text_input("Search handbook chapters or glossary:", placeholder="e.g., ZZFeatureMap, leakage, fidelity, AUROC...")

# Glossary Expander
with st.expander("Technical Glossary (Click to expand)", expanded=False):
    st.markdown("<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 12px;'>", unsafe_allow_html=True)
    for term, definition in sorted(GLOSSARY.items()):
        if not search_query or search_query.lower() in term.lower() or search_query.lower() in definition.lower():
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px;">
                <strong style="color: #7965E8; font-size: 0.88rem;">{term}</strong>
                <p style="margin: 4px 0 0 0; font-size: 0.78rem; color: #25324A; line-height: 1.5;">{definition}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Filter chapters based on search query
filtered_chapters = [
    ch for ch in HANDBOOK_CHAPTERS
    if not search_query or (search_query.lower() in ch["title"].lower() or search_query.lower() in ch["content"].lower() or search_query.lower() in ch["category"].lower())
]

if not filtered_chapters:
    st.info(f"No chapters match '{search_query}'. Try terms like 'quantum', 'biomarker', 'leakage', or 'ROC'.")
else:
    ch_options = [f"#{ch['id']} — {ch['title']} ({ch['category']})" for ch in filtered_chapters]
    selected_idx = st.selectbox("Select Chapter to Read:", range(len(ch_options)), format_func=lambda i: ch_options[i])
    selected_chapter = filtered_chapters[selected_idx]

    st.markdown(f"""
    <div class="ref-dashboard-card" style="margin-top: 15px;">
        <span class="status-pill-released" style="background:#F0EDFF; color:#7965E8; margin-bottom: 8px; display: inline-block;">
            {selected_chapter['category']}
        </span>
    """, unsafe_allow_html=True)
    st.markdown(selected_chapter["content"])
    st.markdown("</div>", unsafe_allow_html=True)

# Export Full Handbook
full_handbook_md = "# QuantumCure AI — Complete Research Handbook\n\n"
for ch in HANDBOOK_CHAPTERS:
    full_handbook_md += f"## {ch['title']}\n**Category:** {ch['category']}\n\n{ch['content']}\n\n---\n\n"

st.markdown("---")
st.download_button(
    label="Download Complete Research Handbook (Markdown)",
    data=full_handbook_md.encode("utf-8"),
    file_name="QuantumCure_Research_Handbook.md",
    mime="text/markdown"
)
