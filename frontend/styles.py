"""
QuantumCure AI - Global Design System & Light Medical Research Theme
Enforces Master Prompt Part 2:
- Strict Light Theme
- Exact Palette:
  Main Background: #F8FAFC
  Card Background: #FFFFFF
  Quantum Model Accent: #7965E8
  Classical RBF-SVM Accent: #18A999
  XGBoost Accent: #F08A78
  Primary Text: #25324A
  Secondary Text: #64748B
  Border: #E5E7EB
  Soft Purple Background: #F0EDFF
  Soft Teal Background: #E7F8F5
  Soft Coral Background: #FFF0EC
- Strict NO-EMOJI Rule (clean SVG / Lucide vector styling and clear typography)
- Prominent Research Prototype Disclaimer
"""

LIGHT_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #F8FAFC;
    --bg-card: #FFFFFF;
    --quantum-accent: #7965E8;
    --quantum-gradient: linear-gradient(135deg, #7965E8 0%, #5B48CC 100%);
    --rbf-accent: #18A999;
    --rbf-gradient: linear-gradient(135deg, #18A999 0%, #0F8275 100%);
    --xgb-accent: #F08A78;
    --xgb-gradient: linear-gradient(135deg, #F08A78 0%, #D86B58 100%);
    --text-primary: #25324A;
    --text-secondary: #64748B;
    --text-muted: #94A3B8;
    --border-color: #E5E7EB;
    --soft-purple: #F0EDFF;
    --soft-teal: #E7F8F5;
    --soft-coral: #FFF0EC;
    --card-shadow: 0 4px 20px rgba(37, 50, 74, 0.05), 0 1px 3px rgba(37, 50, 74, 0.03);
    --pill-shadow: 0 2px 8px rgba(121, 101, 232, 0.22);
}

/* Global App Container */
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide default streamlit decorations and default sidebar nav */
#MainMenu, footer {visibility: hidden;}
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Header container: keep collapsedControl permanently accessible */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
    min-height: 0px !important;
    padding: 0 !important;
    pointer-events: none !important;
    border-bottom: none !important;
}

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    pointer-events: auto !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important;
    background: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    box-shadow: 0 4px 14px rgba(37, 50, 74, 0.08) !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: transform 0.15s ease, background-color 0.15s ease !important;
}

[data-testid="collapsedControl"]:hover {
    background: var(--bg-main) !important;
    transform: scale(1.06) !important;
}

.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1440px !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid var(--border-color) !important;
    box-shadow: 2px 0 16px rgba(37, 50, 74, 0.03) !important;
}

section[data-testid="stSidebar"] div.block-container {
    padding-top: 1.25rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}

/* Prominent Medical Research Disclaimer Banner */
.disclaimer-banner {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 4px solid var(--quantum-accent);
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.82rem;
    color: var(--text-primary);
    font-weight: 500;
}

.disclaimer-text {
    font-weight: 700;
    color: #1E293B;
    letter-spacing: -0.01em;
}

.disclaimer-tag {
    background: #EEF2F6;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
}

/* Top Header Bar */
.top-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 0.5rem;
}

.search-pill-container {
    display: flex;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 9999px;
    padding: 8px 18px;
    box-shadow: 0 2px 6px rgba(37, 50, 74, 0.02);
    width: 320px;
    font-size: 0.86rem;
    color: var(--text-secondary);
}

.user-profile-pill {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 9999px;
    padding: 6px 14px 6px 6px;
    box-shadow: 0 2px 6px rgba(37, 50, 74, 0.02);
}

.action-icon-pill {
    width: 38px;
    height: 38px;
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(37, 50, 74, 0.02);
    color: var(--text-secondary);
    transition: background 0.15s ease;
}

.action-icon-pill:hover {
    background: var(--bg-main);
    color: var(--text-primary);
}

/* Action Primary Buttons */
.btn-summary-ai {
    background: var(--quantum-gradient) !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    padding: 9px 22px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
    box-shadow: var(--pill-shadow) !important;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    text-decoration: none;
}

/* 4 KPI Metric Cards */
.ref-kpi-card {
    position: relative;
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 1.4rem 1.3rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ref-kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(37, 50, 74, 0.08);
}

.kpi-floating-badge {
    position: absolute;
    top: 14px;
    right: 14px;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(37, 50, 74, 0.06);
}

.kpi-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.85rem;
}

.kpi-icon-box {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.85rem;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.kpi-subtitle {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--rbf-accent);
    display: flex;
    align-items: center;
    gap: 4px;
}

.kpi-subtitle span {
    color: var(--text-secondary);
    font-weight: 500;
}

/* Research Cards */
.ref-dashboard-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: var(--card-shadow);
    margin-bottom: 1.25rem;
}

.ref-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.15rem;
}

.ref-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.ref-card-subtitle {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 2px;
}

.pill-filter-btn {
    background: #F8FAFC;
    border: 1px solid var(--border-color);
    border-radius: 9999px;
    padding: 5px 13px;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-primary);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
}

/* Model-Specific Side-by-Side Cards */
.model-card-quantum {
    background: #FFFFFF;
    border: 1.5px solid var(--quantum-accent);
    border-radius: 18px;
    padding: 1.25rem;
    box-shadow: 0 4px 18px rgba(121, 101, 232, 0.08);
}

.model-card-rbf {
    background: #FFFFFF;
    border: 1.5px solid var(--rbf-accent);
    border-radius: 18px;
    padding: 1.25rem;
    box-shadow: 0 4px 18px rgba(24, 169, 153, 0.08);
}

.model-card-xgb {
    background: #FFFFFF;
    border: 1.5px solid var(--xgb-accent);
    border-radius: 18px;
    padding: 1.25rem;
    box-shadow: 0 4px 18px rgba(240, 138, 120, 0.08);
}

.model-badge-quantum {
    background: var(--soft-purple);
    color: var(--quantum-accent);
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 0.74rem;
    font-weight: 700;
    display: inline-block;
}

.model-badge-rbf {
    background: var(--soft-teal);
    color: var(--rbf-accent);
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 0.74rem;
    font-weight: 700;
    display: inline-block;
}

.model-badge-xgb {
    background: var(--soft-coral);
    color: var(--xgb-accent);
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 0.74rem;
    font-weight: 700;
    display: inline-block;
}

/* Agreement Indicators */
.agreement-card-unanimous {
    background: var(--soft-teal);
    border: 1px solid #A7F3D0;
    border-radius: 12px;
    padding: 12px 16px;
    color: #065F46;
    font-size: 0.88rem;
    margin-bottom: 1.25rem;
}

.agreement-card-split {
    background: #FEF3C7;
    border: 1px solid #FDE68A;
    border-radius: 12px;
    padding: 12px 16px;
    color: #92400E;
    font-size: 0.88rem;
    margin-bottom: 1.25rem;
}

.agreement-card-divergent {
    background: var(--soft-coral);
    border: 1px solid #FECDD3;
    border-radius: 12px;
    padding: 12px 16px;
    color: #9F1239;
    font-size: 0.88rem;
    margin-bottom: 1.25rem;
}

/* Circuit Gate Buttons in Quantum Park */
.quantum-gate-btn {
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    padding: 5px 12px !important;
    border: 1px solid transparent !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.gate-green { background: #10B981 !important; color: white !important; }
.gate-purple { background: var(--quantum-accent) !important; color: white !important; }
.gate-coral { background: var(--xgb-accent) !important; color: white !important; }
.gate-teal { background: var(--rbf-accent) !important; color: white !important; }

/* Streamlit Native Tweaks */
.stButton > button {
    border-radius: 9999px !important;
    font-weight: 600 !important;
}

.stTextInput > div > div > input, .stSelectbox > div > div > div {
    border-radius: 9999px !important;
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
}
</style>
"""

DISCLAIMER_HTML = """
<div class="disclaimer-banner">
    <div style="display: flex; align-items: center; gap: 10px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7965E8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span class="disclaimer-text">Research prototype, not clinical advice. Not validated for clinical use.</span>
    </div>
    <span class="disclaimer-tag">Academic Research</span>
</div>
"""


def apply_light_theme(st):
    """Applies strict light theme CSS rules into Streamlit application."""
    st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)


def render_disclaimer_banner(st):
    """Renders the mandatory prominent clinical disclaimer on every page."""
    st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)
