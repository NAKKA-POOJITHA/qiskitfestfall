"""
QuantumCure AI - Ultra-Modern Light Medical Dashboard CSS
Faithfully reproduces the layout, typography, pill badges, and 3D metric cards from the reference UI.
"""

LIGHT_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #F3F5F9;
    --bg-card: #FFFFFF;
    --primary-purple: #7F56D9;
    --primary-purple-gradient: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
    --accent-orange: #FF7A59;
    --accent-teal: #14B8A6;
    --accent-blue: #3B82F6;
    --accent-pink: #EC4899;
    --text-primary: #1E293B;
    --text-secondary: #64748B;
    --text-muted: #94A3B8;
    --border-color: #EEF2F6;
    --card-shadow: 0 4px 20px rgba(148, 163, 184, 0.08), 0 1px 3px rgba(148, 163, 184, 0.05);
    --pill-shadow: 0 2px 8px rgba(109, 40, 217, 0.25);
}

/* Global App Container */
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
}

/* Hide default streamlit decorations and default sidebar nav */
#MainMenu, footer {visibility: hidden;}
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Header container: keep collapsedControl accessible so sidebar can never be locked away */
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
    border: 1px solid #E2E8F0 !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.1) !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: transform 0.15s ease, background-color 0.15s ease !important;
}

[data-testid="collapsedControl"]:hover {
    background: #F8FAFC !important;
    transform: scale(1.08) !important;
}

.main .block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1440px !important;
}

/* Sidebar Styling matching Reference UI */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #EEF2F6 !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.03) !important;
}

section[data-testid="stSidebar"] div.block-container {
    padding-top: 1.25rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}

/* Top Header Bar */
.top-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
}

.search-pill-container {
    display: flex;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 9999px;
    padding: 8px 18px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    width: 320px;
}

.user-profile-pill {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 9999px;
    padding: 6px 14px 6px 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

.action-icon-pill {
    width: 38px;
    height: 38px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

/* Page Title Row */
.page-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.btn-summary-ai {
    background: var(--primary-purple-gradient) !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    box-shadow: var(--pill-shadow) !important;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

/* Reference UI 4 Metric Cards */
.ref-kpi-card {
    position: relative;
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 22px;
    padding: 1.5rem 1.4rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ref-kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(148, 163, 184, 0.12);
}

.kpi-floating-badge {
    position: absolute;
    top: 14px;
    right: 14px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.kpi-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.kpi-3d-icon-box {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    margin-bottom: 1rem;
}

.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.1;
    margin-bottom: 0.35rem;
}

.kpi-subtitle {
    font-size: 0.8rem;
    font-weight: 600;
    color: #10B981; /* Green delta badge */
    display: flex;
    align-items: center;
    gap: 4px;
}

.kpi-subtitle span {
    color: var(--text-secondary);
    font-weight: 500;
}

/* Reference UI Main Card (Analytics / Statistics) */
.ref-dashboard-card {
    background: #FFFFFF;
    border: 1px solid var(--border-color);
    border-radius: 22px;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    margin-bottom: 1.5rem;
}

.ref-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
}

.ref-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.ref-card-subtitle {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-top: 3px;
}

.pill-filter-btn {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 9999px;
    padding: 6px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-primary);
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* Patient Cases Table in Reference UI */
.ref-patient-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
}

.ref-patient-table th {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: capitalize;
    padding: 8px 14px;
    border-bottom: 1px solid #F1F5F9;
}

.ref-patient-row {
    background: #FFFFFF;
    border-radius: 12px;
    transition: background 0.15s ease;
}

.ref-patient-row:hover {
    background: #F8FAFC;
}

.ref-patient-row td {
    padding: 12px 14px;
    font-size: 0.85rem;
    color: var(--text-primary);
    border-top: 1px solid #F8FAFC;
    border-bottom: 1px solid #F8FAFC;
}

.status-pill-released {
    background: #E0F2FE;
    color: #0284C7;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
}

.status-pill-positive {
    background: #FEE2E2;
    color: #DC2626;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
}

.status-pill-negative {
    background: #DCFCE7;
    color: #16A34A;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
}

/* Expert Insights Sidebar Box */
.expert-insights-card {
    background: linear-gradient(135deg, #F5F3FF 0%, #FDF4FF 100%);
    border: 1px solid #E9D5FF;
    border-radius: 20px;
    padding: 1.25rem;
    margin-top: 2rem;
    box-shadow: 0 4px 14px rgba(168, 85, 247, 0.08);
}

.expert-insights-bulb {
    width: 36px;
    height: 36px;
    background: #FFFFFF;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 6px rgba(168, 85, 247, 0.15);
}

.btn-unlock-insights {
    background: var(--primary-purple-gradient) !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    padding: 8px 18px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    border: none !important;
    width: 100%;
    text-align: center;
    box-shadow: var(--pill-shadow) !important;
}

/* Quantum Park Circuit & Gate Styling (Images 2 & 3) */
.quantum-gate-btn {
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 6px 12px !important;
    border: none !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.gate-green { background: #22C55E !important; color: white !important; }
.gate-purple { background: #A855F7 !important; color: white !important; }
.gate-coral { background: #F97316 !important; color: white !important; }
.gate-cyan { background: #06B6D4 !important; color: white !important; }

/* Streamlit Native Element Tweaks */
.stButton > button {
    border-radius: 9999px !important;
    font-weight: 600 !important;
}

.stTextInput > div > div > input {
    border-radius: 9999px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
}
</style>
"""


def apply_light_theme(st):
    """Applies strict light theme CSS rules into Streamlit application."""
    st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)
