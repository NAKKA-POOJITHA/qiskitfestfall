"""
QuantumCure AI - Page 4: Quantum Park & Quantum Insights
Faithfully reproduces the Quantum Park circuit composer, gate palette, 3D Bloch Sphere,
State Probabilities histogram, OpenQASM 2.0 codegen, and Quantum Kernel Heatmap from Images 2 & 3.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import json
import streamlit as st
import numpy as np

from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar
from frontend.components.charts import (
    create_quantum_kernel_heatmap,
    create_bloch_sphere_3d,
    create_quantum_probabilities_chart,
    create_state_vector_amplitudes_chart
)

st.set_page_config(
    page_title="Quantum Park — QuantumCure AI",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="AI Assistant")

# Top Action Bar matching Reference Image 2
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; background: #FFFFFF; border: 1px solid #EEF2F6; border-radius: 18px; padding: 12px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="background: #2563EB; color: white; border-radius: 10px; padding: 8px 16px; font-weight: 700; font-size: 0.88rem; display: flex; align-items: center; gap: 8px;">
            <span>⚛️</span> Qiskit Codegen
        </span>
    </div>
    <div style="text-align: center;">
        <h2 style="margin: 0; font-size: 1.4rem; font-weight: 800; color: #1E293B;">Quantum Park</h2>
        <span style="font-size: 0.78rem; color: #64748B;">Interactive Circuit Simulator & Kernel Engine</span>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <a href="/Research_Handbook" target="_self" style="text-decoration: none;">
            <span style="background: #2563EB; color: white; border-radius: 10px; padding: 8px 16px; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;">
                <span>📖</span> Quantum Handbook
            </span>
        </a>
        <span style="background: #2563EB; color: white; border-radius: 10px; padding: 8px 16px; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 6px; cursor: pointer;">
            <span>❓</span> Contact Developer
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Quantum Circuit Builder & Bloch Sphere Grid
col_circuit, col_bloch = st.columns([1.75, 1.25])

with col_circuit:
    st.markdown("""
    <div class="ref-dashboard-card" style="padding: 1.25rem;">
        <!-- Gate Palette from Image 2 & 3 -->
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 1rem; padding-bottom: 12px; border-bottom: 1px solid #F1F5F9;">
            <span class="quantum-gate-btn gate-green">X</span>
            <span class="quantum-gate-btn gate-green">Y</span>
            <span class="quantum-gate-btn gate-green">Z</span>
            <span class="quantum-gate-btn gate-green">H</span>
            <span class="quantum-gate-btn gate-green">S</span>
            <span class="quantum-gate-btn gate-green">T</span>
            <span class="quantum-gate-btn gate-purple">CX</span>
            <span class="quantum-gate-btn gate-purple">XC</span>
            <span class="quantum-gate-btn gate-purple">MCX</span>
            <span class="quantum-gate-btn" style="background: #FEE2E2; color: #DC2626;">🗑️</span>
        </div>
        <!-- Grid Controls -->
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1.25rem;">
            <span style="background: #F1F5F9; border-radius: 8px; padding: 4px 12px; font-size: 0.82rem; font-weight: 600; color: #334155;">- Wires +</span>
            <span style="background: #F1F5F9; border-radius: 8px; padding: 4px 12px; font-size: 0.82rem; font-weight: 600; color: #334155;">- Columns +</span>
            <span style="background: #2563EB; color: white; border-radius: 8px; padding: 4px 14px; font-size: 0.82rem; font-weight: 600; cursor: pointer;">Clear Grid</span>
            <span style="background: #2563EB; color: white; border-radius: 8px; padding: 4px 10px; font-size: 0.82rem; font-weight: 600;">📐</span>
        </div>
        <!-- Wire Grid Visual from Image 2 -->
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 1.25rem;">
                <span style="font-weight: 700; color: #334155; width: 24px; font-family: monospace;">q0</span>
                <span class="quantum-gate-btn gate-green" style="width: 44px; height: 44px;">H</span>
                <span class="quantum-gate-btn gate-purple" style="width: 44px; height: 44px;">MCX</span>
                <span style="width: 44px; height: 44px; background: #C4B5FD; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6D28D9; font-weight: bold;">●</span>
                <span style="width: 44px; height: 44px; background: #C4B5FD; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6D28D9; font-weight: bold;">●</span>
                <span style="width: 44px; height: 44px; background: #E2E8F0; border-radius: 8px;"></span>
            </div>
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 1.25rem;">
                <span style="font-weight: 700; color: #334155; width: 24px; font-family: monospace;">q1</span>
                <span class="quantum-gate-btn gate-green" style="width: 44px; height: 44px;">H</span>
                <span style="width: 44px; height: 44px; background: #C4B5FD; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6D28D9; font-weight: bold;">●</span>
                <span class="quantum-gate-btn gate-purple" style="width: 44px; height: 44px;">MCX</span>
                <span class="quantum-gate-btn gate-purple" style="width: 44px; height: 44px;">CX</span>
                <span class="quantum-gate-btn gate-purple" style="width: 44px; height: 44px;">XC</span>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <span style="font-weight: 700; color: #334155; width: 24px; font-family: monospace;">q2</span>
                <span style="width: 44px; height: 44px; background: #E2E8F0; border-radius: 8px;"></span>
                <span style="width: 44px; height: 44px; background: #C4B5FD; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6D28D9; font-weight: bold;">●</span>
                <span style="width: 44px; height: 44px; background: #C4B5FD; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6D28D9; font-weight: bold;">●</span>
                <span style="width: 44px; height: 44px; background: #E2E8F0; border-radius: 8px;"></span>
                <span style="width: 44px; height: 44px; background: #C4B5FD; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6D28D9; font-weight: bold;">●</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_bloch:
    st.markdown("""
    <div class="ref-dashboard-card" style="padding: 1.25rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
            <h4 style="margin: 0; color: #1E293B; font-size: 1.05rem;">Bloch Sphere Visualizer</h4>
            <span style="background: #0F172A; color: white; border-radius: 9999px; padding: 4px 12px; font-size: 0.75rem; font-weight: 600;">Qubit q0</span>
        </div>
        <p style="font-size: 0.78rem; color: #64748B; margin-top: 2px;">Real-time pure state projection |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩</p>
    """, unsafe_allow_html=True)
    
    col_t, col_p = st.columns(2)
    with col_t:
        theta = st.slider("Polar Angle θ (rad):", 0.0, float(np.pi), float(np.pi/4), 0.1)
    with col_p:
        phi = st.slider("Azimuth φ (rad):", 0.0, float(2*np.pi), float(np.pi/3), 0.1)

    fig_bloch = create_bloch_sphere_3d(theta=theta, phi=phi)
    st.plotly_chart(fig_bloch, use_container_width=True)
    st.markdown("""
        <div style="text-align: center; margin-top: -10px;">
            <span style="background: #EFF6FF; color: #2563EB; border-radius: 8px; padding: 4px 12px; font-size: 0.78rem; font-weight: 600; cursor: pointer;">
                🔍 Reset Zoom
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Bottom Row: State Probabilities and State Vector (from Image 2 & 3)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
col_probs, col_amps = st.columns(2)

with col_probs:
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h4 class="ref-card-title">State Probabilities</h4>
                <div class="ref-card-subtitle">Measurement statistics over computational basis states</div>
            </div>
            <span class="pill-filter-btn">Shot Count: 1024</span>
        </div>
    """, unsafe_allow_html=True)
    fig_probs = create_quantum_probabilities_chart()
    st.plotly_chart(fig_probs, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_amps:
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h4 class="ref-card-title">State Vector Amplitudes</h4>
                <div class="ref-card-subtitle">Complex quantum state amplitude & phase mapping</div>
            </div>
            <span class="pill-filter-btn">Spectrum: -π ... π</span>
        </div>
    """, unsafe_allow_html=True)
    fig_amps = create_state_vector_amplitudes_chart()
    st.plotly_chart(fig_amps, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# OpenQASM 2.0 & Qiskit Code Export from Image 3
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="ref-dashboard-card">
    <div class="ref-card-header">
        <div>
            <h4 class="ref-card-title">Qiskit & OpenQASM 2.0 Codegen</h4>
            <div class="ref-card-subtitle">Synthesized quantum instructions ready for IBM Quantum deployment</div>
        </div>
        <span class="pill-filter-btn">OpenQASM 2.0</span>
    </div>
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #1E293B;">
        <span style="color: #64748B;">// QuantumCure AI - BCNB 5-Qubit ZZFeatureMap</span><br>
        <strong style="color: #2563EB;">OPENQASM</strong> 2.0;<br>
        <strong style="color: #2563EB;">include</strong> "qelib1.inc";<br>
        <strong style="color: #7C3AED;">qreg</strong> q[5];<br>
        <strong style="color: #7C3AED;">creg</strong> c[5];<br>
        h q[0]; h q[1]; h q[2]; h q[3]; h q[4];<br>
        rz(2.41) q[0]; rz(1.85) q[1]; rz(3.14) q[2];<br>
        cx q[0], q[1]; rz(0.92) q[1]; cx q[0], q[1];<br>
        cx q[1], q[2]; rz(1.48) q[2]; cx q[1], q[2];<br>
        cx q[2], q[3]; rz(2.11) q[3]; cx q[2], q[3];<br>
        cx q[3], q[4]; rz(0.75) q[4]; cx q[3], q[4];<br>
        barrier q;<br>
        measure q -> c;
    </div>
</div>
""", unsafe_allow_html=True)

# Quantum Kernel Matrix Heatmap (Verified Patient Cohort)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
q_kernel_file = Path("results/quantum_kernel_train.npy")
if q_kernel_file.exists():
    K_quantum = np.load(q_kernel_file)
    st.markdown("""
    <div class="ref-dashboard-card">
        <div class="ref-card-header">
            <div>
                <h4 class="ref-card-title">Verified Quantum Fidelity Kernel Matrix</h4>
                <div class="ref-card-subtitle">Pairwise quantum transition fidelities evaluated on 100 patient feature vectors</div>
            </div>
            <span class="pill-filter-btn">100 x 100 Gram Matrix</span>
        </div>
    """, unsafe_allow_html=True)
    fig_heat = create_quantum_kernel_heatmap(K_quantum, max_samples=45)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
