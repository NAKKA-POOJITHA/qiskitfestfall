"""
QuantumCure AI - Page 1: Research Dashboard
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
from frontend.dashboard_view import render_research_dashboard

st.set_page_config(
    page_title="Research Dashboard — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_research_dashboard()
