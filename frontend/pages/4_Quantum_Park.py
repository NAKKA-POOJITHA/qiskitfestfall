"""
QuantumCure AI - Page 4: Quantum Park (Interactive Circuit Explorer)
Full implementation of Master Prompt Part 9:
- Add and remove qubits (1 to 5 qubits)
- Add and remove gates: H, X, Y, Z, S, T, CX, RZ, RY
- Target and control qubit selection
- Clear & Reset circuit actions
- Genuine Qiskit circuit execution & ASCII diagram
- Circuit depth and gate count statistics
- Exact statevector amplitudes and computational basis state probabilities
- Interactive 3D Bloch Sphere visualization
- Source code export: Valid Qiskit 2.x Python script and OpenQASM 2.0
- Strict No-Emoji policy
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import numpy as np

from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar
from frontend.components.charts import (
    create_bloch_sphere_3d,
    create_quantum_probabilities_chart,
    create_state_vector_amplitudes_chart
)

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

st.set_page_config(
    page_title="Quantum Park — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Quantum Park")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            Quantum Park: Circuit Explorer
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Interactive quantum circuit composer, statevector simulator, 3D Bloch sphere, and Qiskit 2.x codegen.
        </p>
    </div>
    <div style="display: flex; gap: 10px;">
        <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
            <button class="btn-summary-ai">
                <span>Kernel Heatmaps & Insights →</span>
            </button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Circuit State Initialization in Streamlit Session
if "circuit_qubits" not in st.session_state:
    st.session_state["circuit_qubits"] = 3

if "circuit_gates" not in st.session_state:
    # Default initial Bell/GHZ state sequence
    st.session_state["circuit_gates"] = [
        {"gate": "H", "target": 0, "control": None},
        {"gate": "CX", "target": 1, "control": 0},
        {"gate": "CX", "target": 2, "control": 1}
    ]

# ==============================================================================
# SECTION A: CIRCUIT COMPOSER & GATE CONTROLS
# ==============================================================================
col_composer, col_bloch = st.columns([1.6, 1.2])

with col_composer:
    st.markdown("""
    <div class="ref-dashboard-card" style="margin-bottom: 1rem;">
        <div class="ref-card-header">
            <div>
                <h3 class="ref-card-title">Circuit Palette & Wire Configuration</h3>
                <div class="ref-card-subtitle">Synthesize multi-qubit unitary operations with verified Qiskit simulation</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_q_ctrl, col_act_ctrl = st.columns([1, 1.5])
    with col_q_ctrl:
        num_qubits = st.slider("Active Qubits:", min_value=1, max_value=5, value=st.session_state["circuit_qubits"], step=1)
        st.session_state["circuit_qubits"] = num_qubits

    with col_act_ctrl:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("Reset to Default (GHZ)", use_container_width=True):
                st.session_state["circuit_gates"] = [
                    {"gate": "H", "target": 0, "control": None},
                    {"gate": "CX", "target": 1, "control": 0},
                    {"gate": "CX", "target": 2, "control": 1}
                ]
                st.session_state["circuit_qubits"] = 3
                st.rerun()
        with col_c2:
            if st.button("Clear All Gates", use_container_width=True):
                st.session_state["circuit_gates"] = []
                st.rerun()

    st.markdown("<div style='border-top: 1px solid #E5E7EB; margin: 12px 0;'></div>", unsafe_allow_html=True)

    # Gate insertion form
    st.markdown("<strong style='font-size: 0.88rem; color: #25324A;'>Insert New Quantum Gate:</strong>", unsafe_allow_html=True)
    g_col1, g_col2, g_col3, g_col4 = st.columns([1.2, 1, 1, 1])

    with g_col1:
        gate_type = st.selectbox("Gate Type:", ["H", "X", "Y", "Z", "S", "T", "CX", "RY", "RZ"])
    with g_col2:
        target_q = st.selectbox("Target Qubit:", list(range(num_qubits)), format_func=lambda q: f"q[{q}]")
    with g_col3:
        if gate_type == "CX":
            available_controls = [q for q in range(num_qubits) if q != target_q]
            ctrl_q = st.selectbox("Control Qubit:", available_controls, format_func=lambda q: f"q[{q}]") if available_controls else None
        else:
            ctrl_q = None
            st.selectbox("Control Qubit:", ["N/A"], disabled=True)
    with g_col4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Append Gate", type="primary", use_container_width=True):
            if gate_type == "CX" and ctrl_q is None:
                st.error("CX gate requires at least 2 qubits.")
            else:
                st.session_state["circuit_gates"].append({
                    "gate": gate_type,
                    "target": target_q,
                    "control": ctrl_q
                })
                st.rerun()

    # Active Gate sequence list with delete
    if st.session_state["circuit_gates"]:
        st.markdown("<div style='margin-top: 10px;'><strong style='font-size: 0.82rem; color: #64748B;'>Active Gate Sequence:</strong></div>", unsafe_allow_html=True)
        gate_pills = ""
        for idx, g in enumerate(st.session_state["circuit_gates"]):
            if g["gate"] == "CX":
                pill_label = f"#{idx+1}: CX(q[{g['control']}]→q[{g['target']}])"
            else:
                pill_label = f"#{idx+1}: {g['gate']}(q[{g['target']}])"
            gate_pills += f'<span class="quantum-gate-btn gate-purple" style="margin: 3px; font-size: 0.78rem;">{pill_label}</span>'
        st.markdown(f'<div style="margin-bottom: 8px;">{gate_pills}</div>', unsafe_allow_html=True)

        if st.button("Delete Last Gate", key="btn_del_gate"):
            st.session_state["circuit_gates"].pop()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Build Qiskit Circuit & Run Simulation
qc = QuantumCircuit(num_qubits) if QISKIT_AVAILABLE else None
sim_error = None
state_probs = {}
state_amps = {}
depth_val = 0
gate_counts_dict = {}

if QISKIT_AVAILABLE and qc is not None:
    try:
        for g in st.session_state["circuit_gates"]:
            g_name = g["gate"]
            t = g["target"]
            c = g.get("control")

            if t >= num_qubits or (c is not None and c >= num_qubits):
                continue  # skip gates exceeding current qubit count

            if g_name == "H":
                qc.h(t)
            elif g_name == "X":
                qc.x(t)
            elif g_name == "Y":
                qc.y(t)
            elif g_name == "Z":
                qc.z(t)
            elif g_name == "S":
                qc.s(t)
            elif g_name == "T":
                qc.t(t)
            elif g_name == "CX" and c is not None:
                qc.cx(c, t)
            elif g_name == "RY":
                qc.ry(np.pi/4, t)
            elif g_name == "RZ":
                qc.rz(np.pi/4, t)

        # Simulation
        sv = Statevector.from_instruction(qc)
        probs_vec = sv.probabilities()
        depth_val = qc.depth()
        gate_counts_dict = dict(qc.count_ops())

        # Form probability and amplitude dicts
        n_states = min(len(probs_vec), 16)
        for i in range(n_states):
            binary_repr = format(i, f"0{num_qubits}b")
            state_key = f"|{binary_repr}⟩"
            state_probs[state_key] = float(probs_vec[i])
            state_amps[state_key] = float(np.abs(sv.data[i]))

    except Exception as e:
        sim_error = str(e)

with col_bloch:
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h4 class="ref-card-title">3D Bloch Sphere Visualizer</h4>
                <div class="ref-card-subtitle">Pure single-qubit state projection |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩</div>
            </div>
            <span class="status-pill-released" style="background:#F0EDFF; color:#7965E8;">Single Qubit Mode</span>
        </div>
    """, unsafe_allow_html=True)

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        bloch_theta = st.slider("Polar Angle θ (rad):", 0.0, float(np.pi), float(np.pi/3), 0.1)
    with c_b2:
        bloch_phi = st.slider("Azimuth φ (rad):", 0.0, float(2*np.pi), float(np.pi/4), 0.1)

    fig_bloch = create_bloch_sphere_3d(theta=bloch_theta, phi=bloch_phi)
    st.plotly_chart(fig_bloch, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# SECTION B: SIMULATED MEASUREMENT OUTCOMES & STATEVECTOR AMPLITUDES
# ==============================================================================
st.markdown("### Quantum State Simulation Outcomes")
c_p1, c_p2 = st.columns(2)

with c_p1:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Computational Basis State Probabilities</h4>
        <div class="ref-card-subtitle">Exact statevector squared moduli P(x) = |⟨x|ψ⟩|²</div>
    """, unsafe_allow_html=True)
    if state_probs:
        fig_prob = create_quantum_probabilities_chart(state_probs)
        st.plotly_chart(fig_prob, use_container_width=True)
    else:
        st.info("No probability distribution computed.")
    st.markdown("</div>", unsafe_allow_html=True)

with c_p2:
    st.markdown("""
    <div class="ref-dashboard-card">
        <h4 class="ref-card-title">Statevector Probability Amplitudes</h4>
        <div class="ref-card-subtitle">Complex state magnitude |c_x| for basis vectors</div>
    """, unsafe_allow_html=True)
    if state_amps:
        fig_amps = create_state_vector_amplitudes_chart(state_amps)
        st.plotly_chart(fig_amps, use_container_width=True)
    else:
        st.info("No statevector calculated.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# SECTION C: QISKIT CIRCUIT DRAWING & CODEGEN EXPORT
# ==============================================================================
st.markdown("""
<div class="ref-dashboard-card">
    <div class="ref-card-header">
        <div>
            <h3 class="ref-card-title">Qiskit Circuit Representation & Valid Codegen</h3>
            <div class="ref-card-subtitle">Execution Backend: Statevector Simulator (Ideal, noise-free unitary evolution)</div>
        </div>
        <div>
            <span class="status-pill-released" style="background:#E7F8F5; color:#18A999;">Depth: {depth_val}</span>
            <span class="status-pill-released" style="background:#F0EDFF; color:#7965E8;">Gates: {len(st.session_state['circuit_gates'])}</span>
        </div>
    </div>
""".format(depth_val=depth_val), unsafe_allow_html=True)

if QISKIT_AVAILABLE and qc is not None:
    # Text circuit representation
    circuit_text = str(qc.draw(output="text"))
    st.markdown("<strong style='font-size: 0.82rem; color: #64748B;'>ASCII Circuit Diagram:</strong>", unsafe_allow_html=True)
    st.code(circuit_text, language="text")

    # Qiskit Python Code Generation
    qiskit_python_code = f"""# QuantumCure AI — Qiskit 2.x Circuit Export
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Instantiate Quantum Circuit with {num_qubits} qubits
qc = QuantumCircuit({num_qubits})
"""
    for g in st.session_state["circuit_gates"]:
        gn = g["gate"]
        t = g["target"]
        c = g.get("control")
        if t < num_qubits and (c is None or c < num_qubits):
            if gn == "H":
                qiskit_python_code += f"qc.h({t})\n"
            elif gn == "X":
                qiskit_python_code += f"qc.x({t})\n"
            elif gn == "Y":
                qiskit_python_code += f"qc.y({t})\n"
            elif gn == "Z":
                qiskit_python_code += f"qc.z({t})\n"
            elif gn == "S":
                qiskit_python_code += f"qc.s({t})\n"
            elif gn == "T":
                qiskit_python_code += f"qc.t({t})\n"
            elif gn == "CX" and c is not None:
                qiskit_python_code += f"qc.cx({c}, {t})\n"
            elif gn == "RY":
                qiskit_python_code += f"qc.ry(np.pi/4, {t})\n"
            elif gn == "RZ":
                qiskit_python_code += f"qc.rz(np.pi/4, {t})\n"

    qiskit_python_code += """
# Compute Statevector
sv = Statevector.from_instruction(qc)
print("Statevector:", sv)
print("Probabilities:", sv.probabilities_dict())
"""

    # OpenQASM 2.0 Code Generation
    try:
        from qiskit.qasm2 import dumps as qasm2_dumps
        qasm_code = qasm2_dumps(qc)
    except Exception:
        qasm_code = f"// OpenQASM 2.0 representation\nOPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[{num_qubits}];\n"

    tab_code1, tab_code2 = st.tabs(["Qiskit Python Code", "OpenQASM 2.0"])
    with tab_code1:
        st.code(qiskit_python_code, language="python")
        st.download_button(
            "Download Qiskit Script (.py)",
            data=qiskit_python_code.encode("utf-8"),
            file_name="quantum_circuit.py",
            mime="text/plain"
        )
    with tab_code2:
        st.code(qasm_code, language="text")
        st.download_button(
            "Download OpenQASM (.qasm)",
            data=qasm_code.encode("utf-8"),
            file_name="quantum_circuit.qasm",
            mime="text/plain"
        )
else:
    st.warning("Qiskit is not available in the current runtime environment.")

st.markdown("</div>", unsafe_allow_html=True)
