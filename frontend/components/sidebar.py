"""
QuantumCure AI - Reference UI Sidebar Navigation Component
Faithfully reproduces the modern pill-navigation, branding, and 'Expert Insights' box from Image 1.
"""

import streamlit as st


def render_sidebar(active_tab="Dashboard"):
    """Renders the sleek, ultra-clean clinical sidebar from Reference Image 1."""
    with st.sidebar:
        # Brand Header with sleek expand arrow matching Image 1
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.75rem; padding: 4px 6px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: linear-gradient(135deg, #A855F7 0%, #6D28D9 100%); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 18px; box-shadow: 0 4px 12px rgba(109, 40, 217, 0.3);">
                    ⚡
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.12rem; font-weight: 800; color: #1E293B; letter-spacing: -0.02em;">Clinical AI</h2>
                    <span style="font-size: 0.72rem; color: #8B5CF6; font-weight: 700; letter-spacing: 0.04em;">QuantumCure v2.0</span>
                </div>
            </div>
            <div style="width: 28px; height: 28px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #64748B; font-size: 13px; cursor: pointer;">
                ›
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Nav items list matching Reference Image 1
        nav_items = [
            ("Dashboard", "/", "⊞"),
            ("Patient Cases", "/Patient_Prediction_Lab", "👥"),
            ("Medication Check", "/Dataset_and_Methods", "💼"),
            ("AI Assistant", "/Quantum_Insights", "✨"),
            ("Reports", "/Research_Handbook", "📋"),
            ("Case History", "/Dataset_and_Methods", "⌛"),
            ("Diagnosis", "/3D_Anatomy_Explorer", "⚙️"),
            ("Export", "/Reports_and_Analytics", "📥")
        ]

        nav_html = '<div style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 1.5rem;">'
        for title, link, icon in nav_items:
            is_active = (title.lower() == active_tab.lower())
            if is_active:
                item_style = "background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%); color: #FFFFFF; font-weight: 600; box-shadow: 0 4px 14px rgba(109, 40, 217, 0.28);"
            else:
                item_style = "background: transparent; color: #475569; font-weight: 500;"

            nav_html += f'<a href="{link}" target="_self" style="text-decoration: none;"><div style="{item_style} border-radius: 12px; padding: 9px 14px; font-size: 0.86rem; display: flex; align-items: center; gap: 12px; transition: all 0.15s ease;"><span style="font-size: 15px;">{icon}</span> {title}</div></a>'
        nav_html += '</div>'
        st.markdown(nav_html, unsafe_allow_html=True)

        # Expert Insights Glowing Box from Image 1
        st.markdown("""
        <div class="expert-insights-card">
            <div class="expert-insights-bulb">
                💡
            </div>
            <h4 style="margin: 0 0 6px 0; color: #1E293B; font-size: 0.95rem; font-weight: 700;">Expert Insights</h4>
            <p style="font-size: 0.78rem; color: #64748B; margin-bottom: 12px; line-height: 1.4;">
                Actionable analysis from shaping researchers the future of quantum oncology AI.
            </p>
            <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
                <div class="btn-unlock-insights">
                    Unlock Insights →
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
