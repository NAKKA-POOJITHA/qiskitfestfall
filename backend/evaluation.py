"""
QuantumCure AI - Evaluation and Fair Comparison Module
Calculates standard oncology binary classification metrics,
generates comparison tables, and creates light-themed scientific visualizations.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    f1_score,
    recall_score,
    precision_score,
    confusion_matrix,
    roc_curve
)

# Design System Colors for strictly light-themed charts
COLOR_QUANTUM = "#7965E8"     # Purple
COLOR_CLASSICAL = "#18A999"   # Teal
COLOR_XGBOOST = "#F08A78"     # Coral
COLOR_BG = "#FFFFFF"
COLOR_GRID = "#E5E7EB"
COLOR_TEXT = "#25324A"
COLOR_TEXT_MUTED = "#64748B"


def compute_binary_metrics(y_true, y_pred, y_score=None, model_name="Model", train_time=0.0):
    """
    Computes AUROC, Accuracy, F1-score, Sensitivity, Specificity, Precision,
    Confusion Matrix and Runtime.
    """
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    sens = recall_score(y_true, y_pred, zero_division=0) # Sensitivity = Recall = TP / (TP + FN)
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0      # Specificity = TN / (TN + FP)
    prec = precision_score(y_true, y_pred, zero_division=0)

    # Check AUROC
    auroc = None
    if y_score is not None and len(np.unique(y_true)) > 1:
        try:
            auroc = float(roc_auc_score(y_true, y_score))
        except Exception:
            auroc = None

    return {
        "model_name": model_name,
        "auroc": round(auroc, 4) if auroc is not None else None,
        "accuracy": round(float(acc), 4),
        "f1_score": round(float(f1), 4),
        "sensitivity": round(float(sens), 4),
        "specificity": round(float(spec), 4),
        "precision": round(float(prec), 4),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp)
        },
        "train_time_sec": round(float(train_time), 4)
    }


def evaluate_all_models(
    y_test,
    predictions_dict,
    scores_dict,
    runtimes_dict,
    patient_ids_test,
    output_dir="results"
):
    """
    Evaluates Quantum-kernel SVM, Classical RBF-SVM, and XGBoost
    on identical held-out test cohort.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    metrics_list = []
    models_to_eval = [
        ("Quantum-kernel SVM", COLOR_QUANTUM),
        ("Classical RBF-SVM", COLOR_CLASSICAL),
        ("XGBoost", COLOR_XGBOOST)
    ]

    for model_name, color in models_to_eval:
        if model_name in predictions_dict:
            y_pred = predictions_dict[model_name]
            y_score = scores_dict.get(model_name)
            t_time = runtimes_dict.get(model_name, 0.0)
            m = compute_binary_metrics(y_test, y_pred, y_score, model_name, t_time)
            metrics_list.append(m)

    # Save metrics JSON
    metrics_json_file = out_path / "metrics.json"
    with open(metrics_json_file, "w", encoding="utf-8") as f:
        json.dump(metrics_list, f, indent=2)

    # Save metrics CSV
    metrics_df = pd.DataFrame([{
        "Model": m["model_name"],
        "AUROC": m["auroc"],
        "Accuracy": m["accuracy"],
        "F1-Score": m["f1_score"],
        "Sensitivity": m["sensitivity"],
        "Specificity": m["specificity"],
        "Precision": m["precision"],
        "Runtime (s)": m["train_time_sec"]
    } for m in metrics_list])
    metrics_csv_file = out_path / "metrics.csv"
    metrics_df.to_csv(metrics_csv_file, index=False)

    # Save patient-level predictions CSV
    preds_df = pd.DataFrame({
        "Patient ID": patient_ids_test,
        "Ground Truth Target": y_test,
        "Ground Truth Class": ["N+" if y == 1 else "N0" for y in y_test]
    })
    for m_name, _ in models_to_eval:
        if m_name in predictions_dict:
            clean_name = m_name.replace("-", "_").replace(" ", "_")
            preds_df[f"{clean_name}_Pred"] = predictions_dict[m_name]
            preds_df[f"{clean_name}_Class"] = ["N+" if p == 1 else "N0" for p in predictions_dict[m_name]]
            if m_name in scores_dict:
                preds_df[f"{clean_name}_Score"] = np.round(scores_dict[m_name], 4)

    preds_csv_file = out_path / "predictions.csv"
    preds_df.to_csv(preds_csv_file, index=False)

    # Generate strictly light-themed ROC Curves PNG
    _generate_roc_curves_plot(y_test, scores_dict, models_to_eval, out_path / "roc_curves.png")

    # Generate Confusion Matrices PNG
    _generate_confusion_matrix_plot(metrics_list, out_path / "confusion_matrices.png")

    # Generate "DID QUANTUM HELP?" automated scientific summary
    quantum_summary = _generate_did_quantum_help_summary(metrics_list)
    with open(out_path / "quantum_comparison_summary.txt", "w", encoding="utf-8") as f:
        f.write(quantum_summary)

    print("Model evaluation finished.")
    print(f"Metrics saved to {metrics_json_file} and {metrics_csv_file}")
    print(f"Predictions saved to {preds_csv_file}")
    return metrics_list


def _generate_roc_curves_plot(y_test, scores_dict, models_to_eval, save_path):
    """Draws scientific ROC curves on clean white background."""
    plt.figure(figsize=(7, 6), facecolor="#FFFFFF")
    ax = plt.subplot(111)
    ax.set_facecolor("#FAFAFA")

    for model_name, color in models_to_eval:
        if model_name in scores_dict and scores_dict[model_name] is not None:
            fpr, tpr, _ = roc_curve(y_test, scores_dict[model_name])
            auc_val = roc_auc_score(y_test, scores_dict[model_name])
            ax.plot(
                fpr,
                tpr,
                color=color,
                lw=2.5,
                label=f"{model_name} (AUROC = {auc_val:.3f})"
            )

    ax.plot([0, 1], [0, 1], color="#94A3B8", lw=1.5, linestyle="--", label="Chance (AUROC = 0.500)")

    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.05])
    ax.set_xlabel("1 - Specificity (False Positive Rate)", fontsize=11, color=COLOR_TEXT, fontweight="medium")
    ax.set_ylabel("Sensitivity (True Positive Rate)", fontsize=11, color=COLOR_TEXT, fontweight="medium")
    ax.set_title("Receiver Operating Characteristic (ROC) — Held-out Test Cohort", fontsize=12, color=COLOR_TEXT, fontweight="bold", pad=12)
    ax.legend(loc="lower right", frameon=True, facecolor="#FFFFFF", edgecolor=COLOR_GRID, fontsize=10)
    ax.grid(True, color=COLOR_GRID, linestyle="-", linewidth=0.7, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color(COLOR_GRID)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, facecolor="#FFFFFF")
    plt.close()


def _generate_confusion_matrix_plot(metrics_list, save_path):
    """Draws clean side-by-side confusion matrix tiles."""
    n_models = len(metrics_list)
    fig, axes = plt.subplots(1, n_models, figsize=(4.5 * n_models, 4.2), facecolor="#FFFFFF")
    if n_models == 1:
        axes = [axes]

    colors = [COLOR_QUANTUM, COLOR_CLASSICAL, COLOR_XGBOOST]

    for idx, (m, ax) in enumerate(zip(metrics_list, axes)):
        cm_data = m["confusion_matrix"]
        cm_array = np.array([[cm_data["tn"], cm_data["fp"]], [cm_data["fn"], cm_data["tp"]]])

        ax.set_facecolor("#FFFFFF")
        im = ax.imshow(cm_array, interpolation="nearest", cmap="Purples" if idx == 0 else ("GnBu" if idx == 1 else "OrRd"), alpha=0.85)

        for i in range(2):
            for j in range(2):
                val = cm_array[i, j]
                ax.text(j, i, f"{val:,}", ha="center", va="center", color="#1E293B", fontsize=14, fontweight="bold")

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Pred N0", "Pred N+"], fontsize=10, color=COLOR_TEXT)
        ax.set_yticklabels(["Actual N0", "Actual N+"], fontsize=10, color=COLOR_TEXT)
        ax.set_title(f"{m['model_name']}\nAcc: {m['accuracy']*100:.1f}% | F1: {m['f1_score']:.3f}", fontsize=11, fontweight="bold", color=COLOR_TEXT)

        for spine in ax.spines.values():
            spine.set_color(COLOR_GRID)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200, facecolor="#FFFFFF")
    plt.close()


def _generate_did_quantum_help_summary(metrics_list):
    """Generates an honest, automated scientific comparison between Quantum and Classical models."""
    q_metric = next((m for m in metrics_list if "Quantum" in m["model_name"]), None)
    c_metric = next((m for m in metrics_list if "Classical" in m["model_name"]), None)
    x_metric = next((m for m in metrics_list if "XGBoost" in m["model_name"]), None)

    if not q_metric or not c_metric:
        return "Insufficient models evaluated to compare Quantum vs Classical SVM."

    q_auc = q_metric.get("auroc") or 0.0
    c_auc = c_metric.get("auroc") or 0.0
    auc_diff = q_auc - c_auc

    q_acc = q_metric.get("accuracy") or 0.0
    c_acc = c_metric.get("accuracy") or 0.0
    acc_diff = q_acc - c_acc

    lines = [
        "==================================================",
        "DID QUANTUM KERNEL LEARNING HELP?",
        "==================================================",
        f"Quantum-kernel SVM AUROC: {q_auc:.4f} | Accuracy: {q_acc*100:.2f}%",
        f"Classical RBF-SVM AUROC:   {c_auc:.4f} | Accuracy: {c_acc*100:.2f}%",
        f"Measured AUROC Difference: {auc_diff:+.4f}",
        f"Measured Accuracy Difference: {acc_diff*100:+.2f}%",
        "--------------------------------------------------"
    ]

    if abs(auc_diff) < 0.02:
        lines.append(
            "SCIENTIFIC ASSESSMENT: Parity / Comparable Performance.\n"
            "The quantum kernel achieved virtually equivalent predictive discrimination to the classical RBF kernel. "
            "In this intermediate-dimensional clinical setting (5 features), the non-linear Hilbert space projection "
            "did not provide a distinct quantum advantage over classical Gaussian radial basis similarity."
        )
    elif auc_diff > 0.02:
        lines.append(
            f"SCIENTIFIC ASSESSMENT: Modest Quantum Gain (+{auc_diff:.4f} AUROC).\n"
            "The quantum feature map (ZZFeatureMap with linear entanglement) provided measurable discrimination gains "
            "over the classical RBF baseline on this cohort. However, this is an empirical observation on a single held-out test partition; "
            "multi-center external validation is necessary before inferring generalizable quantum advantage."
        )
    else:
        lines.append(
            f"SCIENTIFIC ASSESSMENT: Classical RBF-SVM Outperformed Quantum Kernel ({auc_diff:.4f} AUROC).\n"
            "The classical RBF kernel demonstrated superior predictive discrimination compared to the ZZ quantum feature map. "
            "This empirical outcome is consistent with NISQ literature: classical kernels with continuous smoothness parameters (gamma) "
            "often capture tabular non-linearities more effectively than fixed 2-repetition ZZ quantum phase interactions without circuit parameter optimization."
        )

    return "\n".join(lines)
