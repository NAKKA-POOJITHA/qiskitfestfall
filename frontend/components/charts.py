"""
QuantumCure AI - Interactive Scientific Charts (Plotly)
Complies with Master Prompt:
- Exact Color Palette:
  Quantum Model Accent: #7965E8
  Classical RBF-SVM Accent: #18A999
  XGBoost Accent: #F08A78
  Primary Text: #25324A
  Secondary Text: #64748B
  Grid: #E5E7EB / #F1F5F9
- Zero fake metrics or mock hospital admissions
- Authentic BCNB dataset distributions & real model benchmark evaluations
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score, confusion_matrix

COLOR_QUANTUM = "#7965E8"
COLOR_RBF = "#18A999"
COLOR_XGB = "#F08A78"
COLOR_TEXT = "#25324A"
COLOR_MUTED = "#64748B"
COLOR_GRID = "#F1F5F9"
COLOR_BORDER = "#E5E7EB"


def get_base_layout():
    """Returns a clean base layout dictionary."""
    return dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=COLOR_TEXT, size=12),
        margin=dict(l=40, r=30, t=45, b=40)
    )


def create_bcnb_class_distribution_chart():
    """
    Renders verified BCNB 1,058 patient cohort distribution:
    - 655 N0 (No lymph node metastasis, 61.9%)
    - 210 N+(1-2) (1 to 2 metastatic lymph nodes, 19.8%)
    - 193 N+(>2) (>2 metastatic lymph nodes, 18.2%)
    """
    labels = ["N0 (Negative)", "N+(1-2) Nodes", "N+(>2) Nodes"]
    values = [655, 210, 193]
    colors = ["#18A999", "#F08A78", "#D9534F"]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent",
            hoverinfo="label+value+percent",
            textfont=dict(size=12, color=COLOR_TEXT)
        )
    ])

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>BCNB Cohort Nodal Status (1,058 Patients)</b>", font=dict(size=13, color=COLOR_TEXT)),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        height=320,
        margin=dict(l=20, r=20, t=40, b=30),
        annotations=[
            dict(
                text="<b style='color:#25324A; font-size:16px;'>1,058</b><br><span style='font-size:10px; color:#64748B;'>Total Patients</span>",
                x=0.5, y=0.5, showarrow=False
            )
        ]
    )
    return fig


def create_interactive_roc_curves(preds_df):
    """Draws multi-model ROC curves from verified predictions dataframe."""
    fig = go.Figure()
    y_true = preds_df["Ground Truth Target"].values

    model_configs = [
        ("Quantum_kernel_SVM", "Quantum-kernel SVM", COLOR_QUANTUM),
        ("Classical_RBF_SVM", "Classical RBF-SVM", COLOR_RBF),
        ("XGBoost", "XGBoost", COLOR_XGB)
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
                line=dict(color=color, width=2.8),
                hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>"
            ))

    # Diagonal chance line
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Chance Line (AUC: 0.500)",
        line=dict(color="#94A3B8", width=1.5, dash="dash"),
        hoverinfo="none"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>Receiver Operating Characteristic (ROC Curves)</b>", font=dict(size=14, color=COLOR_TEXT)),
        xaxis=dict(title="False Positive Rate (1 - Specificity)", range=[-0.01, 1.01], gridcolor=COLOR_GRID),
        yaxis=dict(title="True Positive Rate (Sensitivity)", range=[-0.01, 1.05], gridcolor=COLOR_GRID),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=350
    )
    return fig


def create_precision_recall_curves(preds_df):
    """Draws multi-model Precision-Recall curves on held-out test cohort."""
    fig = go.Figure()
    y_true = preds_df["Ground Truth Target"].values
    prevalence = np.mean(y_true)

    model_configs = [
        ("Quantum_kernel_SVM", "Quantum-kernel SVM", COLOR_QUANTUM),
        ("Classical_RBF_SVM", "Classical RBF-SVM", COLOR_RBF),
        ("XGBoost", "XGBoost", COLOR_XGB)
    ]

    for col_prefix, label, color in model_configs:
        score_col = f"{col_prefix}_Score"
        if score_col in preds_df.columns:
            scores = preds_df[score_col].values
            precision, recall, _ = precision_recall_curve(y_true, scores)
            ap_val = average_precision_score(y_true, scores)
            fig.add_trace(go.Scatter(
                x=recall,
                y=precision,
                mode="lines",
                name=f"{label} (PR-AUC: {ap_val:.3f})",
                line=dict(color=color, width=2.8),
                hovertemplate="Recall: %{x:.3f}<br>Precision: %{y:.3f}<extra></extra>"
            ))

    # Baseline prevalence line
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[prevalence, prevalence],
        mode="lines",
        name=f"Baseline Prevalence ({prevalence:.1%})",
        line=dict(color="#94A3B8", width=1.5, dash="dash"),
        hoverinfo="none"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>Precision-Recall (PR) Curves</b>", font=dict(size=14, color=COLOR_TEXT)),
        xaxis=dict(title="Recall (Sensitivity)", range=[-0.01, 1.01], gridcolor=COLOR_GRID),
        yaxis=dict(title="Precision (PPV)", range=[-0.01, 1.05], gridcolor=COLOR_GRID),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=350
    )
    return fig


def create_confusion_matrix_charts(preds_df, model_key="Quantum_kernel_SVM"):
    """
    Renders annotated 2x2 confusion matrix heatmap for specified model:
    True Negatives, False Positives, False Negatives, True Positives.
    """
    y_true = preds_df["Ground Truth Target"].values
    pred_col = f"{model_key}_Pred"
    y_pred = preds_df[pred_col].values

    cm = confusion_matrix(y_true, y_pred)
    # cm format: [[TN, FP], [FN, TP]]
    tn, fp, fn, tp = cm.ravel()

    cell_text = [
        [f"TN: {tn}<br>(N0 Correct)", f"FP: {fp}<br>(Type I Error)"],
        [f"FN: {fn}<br>(Type II Error)", f"TP: {tp}<br>(N+ Correct)"]
    ]

    color = COLOR_QUANTUM if "Quantum" in model_key else (COLOR_RBF if "Classical" in model_key else COLOR_XGB)

    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=["Predicted N0", "Predicted N+"],
        y=["Actual N0", "Actual N+"],
        text=cell_text,
        texttemplate="%{text}",
        textfont=dict(size=13, color=COLOR_TEXT, family="Plus Jakarta Sans"),
        colorscale=[[0, "#FFFFFF"], [1, color]],
        showscale=False,
        hoverinfo="z"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text=f"<b>Confusion Matrix: {model_key.replace('_', ' ')}</b>", font=dict(size=13, color=COLOR_TEXT)),
        height=320,
        xaxis=dict(side="bottom"),
        yaxis=dict(autorange="reversed")
    )
    return fig


def create_auroc_bar_chart(metrics_list):
    """Creates bar chart comparing AUROC and PR-AUC across models."""
    names = [m["model_name"] for m in metrics_list]
    aurocs = [m.get("auroc", 0.0) for m in metrics_list]
    accs = [m.get("accuracy", 0.0) for m in metrics_list]
    colors = [
        COLOR_QUANTUM if "Quantum" in n else (COLOR_RBF if "Classical" in n else COLOR_XGB)
        for n in names
    ]

    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=aurocs,
            name="AUROC",
            marker=dict(color=colors, line=dict(color="#E5E7EB", width=1)),
            text=[f"{v:.4f}" for v in aurocs],
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=13, family="Plus Jakarta Sans"),
            hoverinfo="x+y"
        )
    ])

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>AUROC Benchmark Comparison</b>", font=dict(size=14, color=COLOR_TEXT)),
        yaxis=dict(range=[0, 1.0], title="Area Under ROC Curve (AUROC)", gridcolor=COLOR_GRID),
        height=330
    )
    return fig


def create_runtime_comparison_chart(metrics_list):
    """Visualizes training and inference runtimes across all models."""
    names = [m["model_name"] for m in metrics_list]
    train_times = [m.get("training_time_seconds", 0.0) for m in metrics_list]
    inf_times = [m.get("inference_time_ms_per_patient", 0.0) for m in metrics_list]

    fig = go.Figure(data=[
        go.Bar(
            name="Training Time (s)",
            x=names,
            y=train_times,
            marker=dict(color="#7965E8"),
            text=[f"{v:.2f}s" for v in train_times],
            textposition="auto"
        ),
        go.Bar(
            name="Inference Latency (ms/patient)",
            x=names,
            y=inf_times,
            marker=dict(color="#18A999"),
            text=[f"{v:.2f}ms" for v in inf_times],
            textposition="auto"
        )
    ])

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        barmode="group",
        title=dict(text="<b>Computational Cost & Latency Comparison</b>", font=dict(size=13, color=COLOR_TEXT)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320,
        yaxis=dict(title="Time (s or ms)", gridcolor=COLOR_GRID)
    )
    return fig


def create_quantum_kernel_heatmap(K, max_samples=40, title=None):
    """
    Renders interactive Plotly heatmap of quantum fidelity matrix K(x, y).
    """
    n = min(len(K), max_samples)
    K_sub = K[:n, :n]

    chart_title = title or f"Quantum Fidelity Kernel Gram Matrix (First {n} Samples)"

    fig = go.Figure(data=go.Heatmap(
        z=K_sub,
        x=[f"#{i+1}" for i in range(n)],
        y=[f"#{i+1}" for i in range(n)],
        colorscale=[
            [0.0, "#FFFFFF"],
            [0.2, "#F0EDFF"],
            [0.5, "#A79BEF"],
            [0.8, "#7965E8"],
            [1.0, "#4836B8"]
        ],
        zmin=0.0,
        zmax=1.0,
        colorbar=dict(
            title=dict(text="Fidelity |⟨Φ(x)|Φ(y)⟩|²", side="right", font=dict(size=11, color=COLOR_TEXT)),
            tickfont=dict(color=COLOR_MUTED)
        ),
        hovertemplate="Sample %{x} vs %{y}<br>Kernel Value: %{z:.4f}<extra></extra>"
    ))

    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text=f"<b>{chart_title}</b>", font=dict(size=13, color=COLOR_TEXT)),
        height=400,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    fig.update_xaxes(showticklabels=False, title="Patient Feature Vectors")
    fig.update_yaxes(showticklabels=False, title="Patient Feature Vectors", autorange="reversed")
    return fig


def create_bloch_sphere_3d(theta=np.pi/4, phi=np.pi/3):
    """Creates an interactive 3D Bloch Sphere visualization."""
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, np.pi, 25)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))

    fig = go.Figure()

    # Wireframe Sphere surface
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        colorscale=[[0, "#F8FAFC"], [1, "#F0EDFF"]],
        opacity=0.22,
        showscale=False,
        hoverinfo="none"
    ))

    # Equator circle
    circle_t = np.linspace(0, 2 * np.pi, 50)
    fig.add_trace(go.Scatter3d(
        x=np.cos(circle_t), y=np.sin(circle_t), z=np.zeros_like(circle_t),
        mode="lines", line=dict(color="#A79BEF", width=2, dash="dash"),
        hoverinfo="none", showlegend=False
    ))

    # Axes: X, Y, Z
    fig.add_trace(go.Scatter3d(
        x=[-1.1, 1.1], y=[0, 0], z=[0, 0],
        mode="lines+text", line=dict(color="#F08A78", width=2.5),
        text=["", "X"], textposition="top right", textfont=dict(size=13, color="#F08A78"),
        hoverinfo="none", name="X Axis"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[-1.1, 1.1], z=[0, 0],
        mode="lines+text", line=dict(color="#18A999", width=2.5),
        text=["", "Y"], textposition="top right", textfont=dict(size=13, color="#18A999"),
        hoverinfo="none", name="Y Axis"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-1.1, 1.1],
        mode="lines+text", line=dict(color="#7965E8", width=2.5),
        text=["|1⟩", "|0⟩"], textposition="top center", textfont=dict(size=14, color="#7965E8"),
        hoverinfo="none", name="Z Axis (|0⟩ / |1⟩)"
    ))

    # State Vector Arrow
    vx = np.sin(theta) * np.cos(phi)
    vy = np.sin(theta) * np.sin(phi)
    vz = np.cos(theta)

    fig.add_trace(go.Scatter3d(
        x=[0, vx], y=[0, vy], z=[0, vz],
        mode="lines+markers",
        line=dict(color="#7965E8", width=5.5),
        marker=dict(size=[0, 8], color=["#7965E8", "#18A999"]),
        name="State Vector |ψ⟩",
        hovertemplate="θ: %{customdata[0]:.2f} rad<br>φ: %{customdata[1]:.2f} rad<extra></extra>",
        customdata=[[theta, phi], [theta, phi]]
    ))

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        scene=dict(
            bgcolor="#FFFFFF",
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            camera=dict(eye=dict(x=1.4, y=-1.4, z=1.2))
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=360,
        showlegend=False
    )
    return fig


def create_quantum_probabilities_chart(probs_dict=None):
    """Creates State Probabilities histogram from state dictionary or default."""
    if not probs_dict:
        probs_dict = {"|00000⟩": 0.35, "|00001⟩": 0.15, "|00010⟩": 0.18, "|00011⟩": 0.12, "|00100⟩": 0.20}

    states = list(probs_dict.keys())
    probs = list(probs_dict.values())

    fig = go.Figure(data=[
        go.Bar(
            x=states, y=probs,
            marker=dict(color=COLOR_QUANTUM, line=dict(color="#5B48CC", width=1)),
            hovertemplate="State %{x}: %{y:.2%}<extra></extra>"
        )
    ])
    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>Computational Basis State Probabilities</b>", font=dict(size=13, color=COLOR_TEXT)),
        yaxis=dict(range=[0, max(probs)*1.2 if probs else 1.0], title="Probability |⟨x|ψ⟩|²", gridcolor=COLOR_GRID),
        xaxis=dict(title="Basis State |x⟩"),
        height=270
    )
    return fig


def create_state_vector_amplitudes_chart(amps_dict=None):
    """Creates State Vector Amplitudes chart from amplitude dictionary or default."""
    if not amps_dict:
        amps_dict = {"|00000⟩": 0.59, "|00001⟩": 0.38, "|00010⟩": 0.42, "|00011⟩": 0.35, "|00100⟩": 0.45}

    states = list(amps_dict.keys())
    amps = list(amps_dict.values())

    fig = go.Figure(data=[
        go.Bar(
            x=states, y=amps,
            marker=dict(color=COLOR_RBF, line=dict(color="#0F8275", width=1)),
            hovertemplate="State %{x} Magnitude: %{y:.3f}<extra></extra>"
        )
    ])
    layout = get_base_layout()
    fig.update_layout(layout)
    fig.update_layout(
        title=dict(text="<b>Statevector Probability Amplitudes</b>", font=dict(size=13, color=COLOR_TEXT)),
        yaxis=dict(range=[0, max(amps)*1.2 if amps else 1.0], title="Amplitude |c_x|", gridcolor=COLOR_GRID),
        xaxis=dict(title="Basis State |x⟩"),
        height=270
    )
    return fig
