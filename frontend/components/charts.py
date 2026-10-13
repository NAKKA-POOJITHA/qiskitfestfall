"""
QuantumCure AI - Interactive Scientific Charts (Plotly)
Faithfully implements the pill-stacked analytics chart, circular demographic donut,
and Quantum Park 3D Bloch Sphere from the reference designs.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score

# Palette Tokens matching Reference UI
COLOR_PURPLE = "#8B5CF6"
COLOR_ORANGE = "#FF7A59"
COLOR_PINK = "#F43F5E"
COLOR_TEAL = "#14B8A6"
COLOR_CYAN = "#06B6D4"
COLOR_TEXT = "#1E293B"
COLOR_MUTED = "#64748B"
COLOR_GRID = "#F1F5F9"


def get_base_layout():
    """Returns a clean base layout dictionary."""
    return dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=COLOR_TEXT, size=12),
        margin=dict(l=40, r=30, t=50, b=40)
    )


def create_pill_stacked_analytics_chart():
    """
    Creates the 'AI Healthcare Department Analytics' stacked rounded pill chart
    from Reference Image 1 (Sat, Sun, Mon, Tue, Wed, Thu, Fri, Sat).
    """
    days = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    # Three stacked levels (pink bottom, orange middle, purple top)
    val_pink = [12, 10, 14, 11, 13, 14, 12, 13]
    val_orange = [10, 8, 12, 9, 11, 12, 11, 10]
    val_purple = [14, 11, 15, 13, 14, 15, 13, 14]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=days, y=val_pink, name="Yearly Analysis",
        marker=dict(color="#F43F5E", line=dict(color="#FFFFFF", width=3)),
        hovertemplate="Yearly: $9,796<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=days, y=val_orange, name="Monthly Analysis",
        marker=dict(color="#FB923C", line=dict(color="#FFFFFF", width=3)),
        hovertemplate="Monthly: $6,464<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=days, y=val_purple, name="Weekly Analysis",
        marker=dict(color="#8B5CF6", line=dict(color="#FFFFFF", width=3)),
        hovertemplate="Weekly: $2,197<extra></extra>"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        barmode="stack",
        bargap=0.45,
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0")
    fig.update_yaxes(gridcolor=COLOR_GRID, linecolor="#E2E8F0", range=[0, 45])
    return fig


def create_circular_cohort_chart():
    """
    Creates the 'Patients Gender' overlapping circular donut
    from Reference Image 1 with 73% Male, 53% Female, and 27% Other.
    """
    fig = go.Figure()

    # Outer donut (Female 53%)
    fig.add_trace(go.Pie(
        labels=["Female", "Remaining"],
        values=[53, 47],
        hole=0.75,
        marker=dict(colors=["#C4B5FD", "#F3F4F6"], line=dict(color="#FFFFFF", width=2)),
        textinfo="none",
        hoverinfo="label+percent",
        showlegend=False,
        sort=False,
        domain=dict(x=[0.1, 0.9], y=[0.1, 0.9])
    ))

    # Inner donut (Male 73% & Other 27%)
    fig.add_trace(go.Pie(
        labels=["Male", "Other"],
        values=[73, 27],
        hole=0.55,
        marker=dict(colors=["#7C3AED", "#DDD6FE"], line=dict(color="#FFFFFF", width=3)),
        textinfo="none",
        hoverinfo="label+percent",
        showlegend=False,
        sort=False,
        domain=dict(x=[0.2, 0.8], y=[0.2, 0.8])
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[
            dict(
                text="<b style='color:#7C3AED; font-size:20px;'>73%</b><br><span style='font-size:11px; color:#475569; font-weight:600;'>Male</span>",
                x=0.5, y=0.5, showarrow=False
            ),
            dict(
                text="<b style='color:#6D28D9; font-size:14px;'>53%</b><br><span style='font-size:10px; color:#64748B;'>Female</span>",
                x=0.82, y=0.78, showarrow=False
            ),
            dict(
                text="<b style='color:#475569; font-size:13px;'>27%</b><br><span style='font-size:10px; color:#64748B;'>Other</span>",
                x=0.22, y=0.32, showarrow=False
            )
        ]
    )
    return fig


def create_auroc_bar_chart(metrics_list):
    """Creates modern bar chart comparing AUROC across models."""
    names = [m["model_name"] for m in metrics_list]
    aurocs = [m.get("auroc", 0.0) for m in metrics_list]
    colors = [
        "#8B5CF6" if "Quantum" in n else ("#14B8A6" if "Classical" in n else "#FF7A59")
        for n in names
    ]

    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=aurocs,
            marker=dict(color=colors, line=dict(color="#E2E8F0", width=1)),
            text=[f"{v:.4f}" for v in aurocs],
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=13, weight="bold"),
            hoverinfo="x+y"
        )
    ])

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>AUROC Benchmark Comparison</b>", font=dict(size=14, color=COLOR_TEXT)),
        yaxis=dict(range=[0, 1.0], title="Area Under ROC Curve (AUROC)", gridcolor=COLOR_GRID),
        height=320
    )
    return fig


def create_interactive_roc_curves(preds_df):
    """Draws multi-model ROC curves from predictions dataframe."""
    fig = go.Figure()
    y_true = preds_df["Ground Truth Target"].values

    model_configs = [
        ("Quantum_kernel_SVM", "Quantum-kernel SVM", "#8B5CF6"),
        ("Classical_RBF_SVM", "Classical RBF-SVM", "#14B8A6"),
        ("XGBoost", "XGBoost", "#FF7A59")
    ]

    for col_prefix, label, color in model_configs:
        score_col = f"{col_prefix}_Score"
        if score_col in preds_df.columns:
            scores = preds_df[score_col].values
            fpr, tpr, _ = roc_curve(y_true, scores)
            auc_val = roc_auc_score(y_true, scores)
            fig.add_trace(go.Scatter(
                x=fpr,
                y=tpr,
                mode="lines",
                name=f"{label} (AUC: {auc_val:.3f})",
                line=dict(color=color, width=3),
                hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>"
            ))

    # Diagonal chance line
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Chance (AUC: 0.500)",
        line=dict(color="#94A3B8", width=1.5, dash="dash"),
        hoverinfo="none"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>Receiver Operating Characteristic (ROC Curves)</b>", font=dict(size=14, color=COLOR_TEXT)),
        xaxis=dict(title="False Positive Rate (1 - Specificity)", range=[-0.01, 1.01], gridcolor=COLOR_GRID),
        yaxis=dict(title="True Positive Rate (Sensitivity)", range=[-0.01, 1.05], gridcolor=COLOR_GRID),
        height=340
    )
    return fig


def create_quantum_kernel_heatmap(K, max_samples=50):
    """
    Renders interactive Plotly heatmap of quantum fidelity matrix K(x, y).
    Safely fixes any duplicate xaxis layout issues.
    """
    n = min(len(K), max_samples)
    K_sub = K[:n, :n]

    fig = go.Figure(data=go.Heatmap(
        z=K_sub,
        x=[f"Pt #{i+1}" for i in range(n)],
        y=[f"Pt #{i+1}" for i in range(n)],
        colorscale=[
            [0.0, "#FFFFFF"],
            [0.2, "#F3E8FF"],
            [0.5, "#C4B5FD"],
            [0.8, "#8B5CF6"],
            [1.0, "#5B21B6"]
        ],
        zmin=0.0,
        zmax=1.0,
        colorbar=dict(
            title=dict(text="Fidelity |⟨Φ(x)|Φ(y)⟩|²", side="right", font=dict(size=11, color=COLOR_TEXT)),
            tickfont=dict(color=COLOR_MUTED)
        ),
        hovertemplate="Sample A: %{x}<br>Sample B: %{y}<br>Fidelity: %{z:.4f}<extra></extra>"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text=f"<b>Quantum Fidelity Matrix Heatmap (First {n} Patients)</b>", font=dict(size=14, color=COLOR_TEXT)),
        height=450
    )
    fig.update_xaxes(showticklabels=False, title="Training Patient Samples")
    fig.update_yaxes(showticklabels=False, title="Training Patient Samples", autorange="reversed")
    return fig


def create_bloch_sphere_3d(theta=np.pi/4, phi=np.pi/3):
    """
    Creates an interactive 3D Bloch Sphere visualization matching Image 2 & 3.
    """
    # 1. Sphere mesh grid
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))

    fig = go.Figure()

    # Wireframe Sphere surface
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        colorscale=[[0, "#F1F5F9"], [1, "#EDE9FE"]],
        opacity=0.25,
        showscale=False,
        hoverinfo="none"
    ))

    # Equator and meridian circles
    circle_t = np.linspace(0, 2 * np.pi, 60)
    fig.add_trace(go.Scatter3d(
        x=np.cos(circle_t), y=np.sin(circle_t), z=np.zeros_like(circle_t),
        mode="lines", line=dict(color="#C4B5FD", width=2, dash="dash"),
        hoverinfo="none", showlegend=False
    ))

    # Axes: X, Y, Z
    fig.add_trace(go.Scatter3d(
        x=[-1.2, 1.2], y=[0, 0], z=[0, 0],
        mode="lines+text", line=dict(color="#EF4444", width=3),
        text=["", "X"], textposition="top right", textfont=dict(size=14, color="#EF4444"),
        hoverinfo="none", name="X Axis"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[-1.2, 1.2], z=[0, 0],
        mode="lines+text", line=dict(color="#22C55E", width=3),
        text=["", "Y"], textposition="top right", textfont=dict(size=14, color="#22C55E"),
        hoverinfo="none", name="Y Axis"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-1.2, 1.2],
        mode="lines+text", line=dict(color="#3B82F6", width=3),
        text=["|1⟩", "|0⟩"], textposition="top center", textfont=dict(size=15, color="#3B82F6", weight="bold"),
        hoverinfo="none", name="Z Axis (|0⟩ / |1⟩)"
    ))

    # State Vector Vector Arrow: |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
    vx = np.sin(theta) * np.cos(phi)
    vy = np.sin(theta) * np.sin(phi)
    vz = np.cos(theta)

    fig.add_trace(go.Scatter3d(
        x=[0, vx], y=[0, vy], z=[0, vz],
        mode="lines+markers",
        line=dict(color="#8B5CF6", width=6),
        marker=dict(size=[0, 9], color=["#8B5CF6", "#06B6D4"]),
        name="State Vector |ψ⟩",
        hovertemplate="θ: %{customdata[0]:.2f} rad<br>φ: %{customdata[1]:.2f} rad<extra></extra>",
        customdata=[[theta, phi], [theta, phi]]
    ))

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        scene=dict(
            bgcolor="#FAFAFA",
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.3))
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=380,
        showlegend=False
    )
    return fig


def create_quantum_probabilities_chart():
    """
    Creates State Probabilities chart matching Image 2 & 3.
    """
    states = ["|000⟩", "|001⟩", "|010⟩", "|011⟩", "|100⟩", "|101⟩", "|110⟩", "|111⟩"]
    probs = [0.0, 0.0, 0.25, 0.25, 0.25, 0.25, 0.0, 0.0]

    fig = go.Figure(data=[
        go.Bar(
            x=states, y=probs,
            marker=dict(color="#F97316", line=dict(color="#EA580C", width=1.5)),
            hovertemplate="State %{x}: %{y:.2%}<extra></extra>"
        )
    ])
    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>State Probabilities</b>", font=dict(size=14, color=COLOR_TEXT)),
        yaxis=dict(range=[0, 0.4], title="Probability %", gridcolor=COLOR_GRID),
        xaxis=dict(title="Computational Basis States"),
        height=280
    )
    return fig


def create_state_vector_amplitudes_chart():
    """
    Creates State Vector amplitudes chart with phase spectrum colormap matching Image 2.
    """
    states = ["|000⟩", "|001⟩", "|010⟩", "|011⟩", "|100⟩", "|101⟩", "|110⟩", "|111⟩"]
    amps = [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0]

    fig = go.Figure(data=[
        go.Bar(
            x=states, y=amps,
            marker=dict(color="#22D3EE", line=dict(color="#06B6D4", width=1.5)),
            hovertemplate="State %{x} Amplitude: %{y:.3f}<extra></extra>"
        )
    ])
    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>State Vector Amplitudes</b>", font=dict(size=14, color=COLOR_TEXT)),
        yaxis=dict(range=[0, 0.7], title="Amplitude", gridcolor=COLOR_GRID),
        xaxis=dict(title="Computational Basis States"),
        height=280
    )
    return fig
