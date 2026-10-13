"""
QuantumCure AI - Page 3: 3D Anatomy Explorer
Interactive 3D educational model of breast anatomy, lymphatic drainage channels,
and axillary lymph node levels (Levels I, II, III) rendered via Plotly 3D graphics.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import numpy as np
import plotly.graph_objects as go

from frontend.styles import apply_light_theme
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="3D Anatomy Explorer — QuantumCure AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="Diagnosis")

st.markdown("""
<div style="margin-bottom: 1.25rem;">
    <div style="display: flex; align-items: baseline; gap: 10px;">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #25324A;">3D Anatomy Explorer</h1>
        <span class="badge-classical" style="font-size: 0.8rem;">Educational Schematic</span>
    </div>
    <p style="margin-top: 4px; font-size: 0.95rem; color: #64748B;">
        Interactive 3D educational model of the mammary parenchyma and axillary lymphatic basin.
    </p>
    <div class="clinical-disclaimer">
        <strong>Educational Disclaimer:</strong> This schematic 3D visualization demonstrates regional anatomical structures for educational understanding. 
        The machine learning models in QuantumCure AI predict binary presence of metastasis (N0 vs N+); they do NOT localize specific nodes, measure anatomical distance, or reconstruct patient-specific computed tomography / MRI scans.
    </div>
</div>
""", unsafe_allow_html=True)

# Layout: Controls on left, 3D Plot on right
col_ctrl, col_plot = st.columns([1, 2.5])

with col_ctrl:
    st.markdown("""
    <div class="qc-card">
        <h4 style="margin: 0 0 10px 0; color: #25324A;">Anatomy Display Controls</h4>
    """, unsafe_allow_html=True)

    show_breast = st.checkbox("Breast Parenchyma & Contour", value=True)
    show_tumor = st.checkbox("Primary Tumour Illustration", value=True)
    show_channels = st.checkbox("Lymphatic Drainage Channels", value=True)
    show_nodes = st.checkbox("Axillary Lymph Node Basin (Levels I-III)", value=True)
    show_landmarks = st.checkbox("Chest Wall & Clavicular Landmark", value=True)

    st.markdown("---")
    st.markdown("<h5 style='margin: 0 0 8px 0; color: #25324A;'>Simulated Tumour Parameters</h5>", unsafe_allow_html=True)
    tumor_size = st.slider("Tumour Diameter (cm):", min_value=0.5, max_value=5.0, value=2.5, step=0.5)
    quadrant = st.selectbox(
        "Primary Quadrant:",
        ["Upper Outer Quadrant (UOQ - ~50% incidence)", "Upper Inner Quadrant (UIQ)", "Lower Outer Quadrant (LOQ)", "Lower Inner Quadrant (LIQ)"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="qc-card" style="font-size: 0.82rem; color: #64748B;">
        <strong style="color: #25324A;">Axillary Basin Staging:</strong><br>
        • <strong>Level I:</strong> Inferior / lateral to Pectoralis Minor.<br>
        • <strong>Level II:</strong> Directly posterior to Pectoralis Minor.<br>
        • <strong>Level III:</strong> Superior / medial to Pectoralis Minor (Subclavicular).
    </div>
    """, unsafe_allow_html=True)

with col_plot:
    # Build 3D Schematic Scene
    fig = go.Figure()

    # 1. Breast Semi-transparent Parenchyma Contour
    if show_breast:
        u = np.linspace(0, np.pi, 25)
        v = np.linspace(0, np.pi, 25)
        # Hemisphere centered near (0, 0, 0)
        x_breast = 6.0 * np.outer(np.sin(u), np.sin(v))
        y_breast = 4.5 * np.outer(np.cos(u), np.ones_like(v))
        z_breast = 6.0 * np.outer(np.sin(u), np.cos(v))
        # Keep positive z for forward projection
        z_breast = np.clip(z_breast, 0, 6.0)

        fig.add_trace(go.Surface(
            x=x_breast, y=y_breast, z=z_breast,
            colorscale=[[0, "#FCE7F3"], [1, "#FED7AA"]],
            opacity=0.32,
            showscale=False,
            name="Breast Contour",
            hoverinfo="name"
        ))

    # 2. Chest Wall Landmark
    if show_landmarks:
        wall_x = np.linspace(-4, 10, 10)
        wall_y = np.linspace(-6, 8, 10)
        wx, wy = np.meshgrid(wall_x, wall_y)
        wz = np.zeros_like(wx) - 0.2

        fig.add_trace(go.Surface(
            x=wx, y=wy, z=wz,
            colorscale=[[0, "#E2E8F0"], [1, "#CBD5E1"]],
            opacity=0.4,
            showscale=False,
            name="Pectoral Chest Wall",
            hoverinfo="name"
        ))

        # Clavicular line
        fig.add_trace(go.Scatter3d(
            x=[2, 8, 10], y=[6, 7.5, 8], z=[1, 1.5, 1],
            mode="lines+text",
            line=dict(color="#94A3B8", width=4, dash="dot"),
            text=["", "Clavicle Landmark", ""],
            name="Clavicle Reference",
            hoverinfo="name"
        ))

    # Determine Tumor Coordinates based on quadrant
    q_coords = {
        "Upper Outer": (2.5, 2.0, 3.0),
        "Upper Inner": (-2.0, 2.0, 2.8),
        "Lower Outer": (2.2, -2.0, 2.6),
        "Lower Inner": (-2.0, -2.0, 2.4)
    }
    prefix = quadrant.split(" (")[0]
    tx, ty, tz = q_coords.get(prefix, (2.5, 2.0, 3.0))

    # 3. Primary Tumor Illustration
    if show_tumor:
        radius = tumor_size * 0.4
        tu = np.linspace(0, 2 * np.pi, 16)
        tv = np.linspace(0, np.pi, 16)
        tum_x = tx + radius * np.outer(np.cos(tu), np.sin(tv))
        tum_y = ty + radius * np.outer(np.sin(tu), np.sin(tv))
        tum_z = tz + radius * np.outer(np.ones_like(tu), np.cos(tv))

        fig.add_trace(go.Surface(
            x=tum_x, y=tum_y, z=tum_z,
            colorscale=[[0, "#F08A78"], [1, "#E11D48"]],
            opacity=0.9,
            showscale=False,
            name=f"Primary Tumour ({tumor_size} cm)",
            hoverinfo="name"
        ))

    # 4. Axillary Lymph Nodes (Levels I, II, III)
    if show_nodes:
        # Level I Nodes (Low Axilla) - Teal
        l1_x = [6.0, 6.5, 7.0, 6.2, 7.3, 6.8]
        l1_y = [4.0, 4.5, 3.8, 5.2, 4.8, 5.6]
        l1_z = [1.2, 1.6, 0.8, 1.5, 1.0, 1.8]

        fig.add_trace(go.Scatter3d(
            x=l1_x, y=l1_y, z=l1_z,
            mode="markers+text",
            marker=dict(size=8, color="#18A999", symbol="circle", opacity=0.95),
            text=["SLN", "L1", "L1", "L1", "L1", "L1"],
            textposition="top center",
            textfont=dict(size=10, color="#10786C"),
            name="Level I (Low Axilla / SLN)",
            hoverinfo="name+text"
        ))

        # Level II Nodes (Mid Axilla) - Purple
        l2_x = [7.5, 7.8, 8.2, 8.0]
        l2_y = [5.8, 6.3, 6.0, 6.7]
        l2_z = [1.5, 2.0, 1.2, 1.7]

        fig.add_trace(go.Scatter3d(
            x=l2_x, y=l2_y, z=l2_z,
            mode="markers+text",
            marker=dict(size=8, color="#7965E8", symbol="diamond", opacity=0.95),
            text=["L2", "L2", "L2", "L2"],
            textposition="top center",
            textfont=dict(size=10, color="#563ED6"),
            name="Level II (Interpectoral)",
            hoverinfo="name+text"
        ))

        # Level III Nodes (High / Apical) - Coral
        l3_x = [8.5, 8.8, 9.2]
        l3_y = [7.0, 7.4, 7.8]
        l3_z = [1.8, 2.2, 2.0]

        fig.add_trace(go.Scatter3d(
            x=l3_x, y=l3_y, z=l3_z,
            mode="markers+text",
            marker=dict(size=9, color="#F08A78", symbol="square", opacity=0.95),
            text=["L3 (Apical)", "L3", "L3"],
            textposition="top center",
            textfont=dict(size=10, color="#C2410C"),
            name="Level III (Subclavicular)",
            hoverinfo="name+text"
        ))

    # 5. Lymphatic Drainage Pathways
    if show_channels and show_tumor:
        # Channels from tumor to Sentinel Lymph Node (Level I)
        drain_x = [tx, tx + 1.5, 4.5, 6.0]
        drain_y = [ty, ty + 1.0, 3.2, 4.0]
        drain_z = [tz, tz * 0.7, 1.8, 1.2]

        fig.add_trace(go.Scatter3d(
            x=drain_x, y=drain_y, z=drain_z,
            mode="lines",
            line=dict(color="#0284C7", width=5, dash="solid"),
            name="Primary Lymphatic Drainage Track",
            hoverinfo="name"
        ))

        # Inter-nodal trunk Level I -> II -> III
        trunk_x = [6.0, 7.0, 7.8, 8.8]
        trunk_y = [4.0, 5.0, 6.3, 7.4]
        trunk_z = [1.2, 1.5, 2.0, 2.2]

        fig.add_trace(go.Scatter3d(
            x=trunk_x, y=trunk_y, z=trunk_z,
            mode="lines",
            line=dict(color="#38BDF8", width=3, dash="dot"),
            name="Inter-nodal Lymphatic Trunk",
            hoverinfo="name"
        ))

    # Scene styling - Strict clean white background
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        scene=dict(
            bgcolor="#FAFAFA",
            xaxis=dict(showbackground=False, showgrid=True, gridcolor="#E5E7EB", title="Lateral Axis (cm)"),
            yaxis=dict(showbackground=False, showgrid=True, gridcolor="#E5E7EB", title="Superior Axis (cm)"),
            zaxis=dict(showbackground=False, showgrid=True, gridcolor="#E5E7EB", title="Anterior Axis (cm)"),
            camera=dict(eye=dict(x=1.6, y=-1.5, z=1.2))
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600,
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#E5E7EB",
            borderwidth=1,
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02
        )
    )

    st.plotly_chart(fig, use_container_width=True)
