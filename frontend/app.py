"""
QuantumCure AI - Master Streamlit Application Entrypoint
"""

import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from frontend.dashboard_view import render_research_dashboard

st.set_page_config(
    page_title="QuantumCure AI — Quantum Cancer Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

if __name__ == "__main__":
    render_research_dashboard()
