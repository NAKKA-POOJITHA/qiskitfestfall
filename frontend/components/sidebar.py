"""
QuantumCure AI - Sidebar Navigation Component
Adheres to strict No-Emoji policy (Master Prompt Part 2).
Uses clean SVG vector icons and medical research navigation labels.
"""

import streamlit as st


def render_sidebar(active_tab="Dashboard"):
    """Renders the sleek, ultra-clean clinical sidebar without any emojis."""
    with st.sidebar:
        # Brand Header with SVG icon
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; padding: 2px 4px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: linear-gradient(135deg, #7965E8 0%, #5B48CC 100%); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; box-shadow: 0 4px 12px rgba(121, 101, 232, 0.3);">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                    </svg>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.05rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">QuantumCure AI</h2>
                    <span style="font-size: 0.72rem; color: #7965E8; font-weight: 700; letter-spacing: 0.02em;">Quantum Kernel Oncology</span>
                </div>
            </div>
            <div style="width: 26px; height: 26px; background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #64748B; font-size: 13px;">
                ›
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Scientific Navigation Links matching all Master Prompt labs (clean SVGs, zero emojis)
        nav_items = [
            ("Dashboard", "/", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>"""),
            ("Prediction Lab", "/Patient_Prediction_Lab", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2v6a2 2 0 0 0 2 2h6"></path><path d="M4 15V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1"></path><polyline points="3 15 6 18 11 13"></polyline></svg>"""),
            ("Model Comparison", "/Model_Comparison_Lab", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>"""),
            ("Quantum Park", "/Quantum_Park", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M12 2v3m0 14v3M2 12h3m14 0h3"></path><path d="m4.93 4.93 2.12 2.12m9.9 9.9 2.12 2.12M4.93 19.07l2.12-2.12m9.9-9.9 2.12-2.12"></path></svg>"""),
            ("Quantum Insights", "/Quantum_Insights", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>"""),
            ("3D Anatomy Explorer", "/3D_Anatomy_Explorer", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>"""),
            ("Research Handbook", "/Research_Handbook", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>"""),
            ("Dataset & Methods", "/Dataset_and_Methods", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>"""),
            ("Reports & Analytics", "/Reports_and_Analytics", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>"""),
            ("Multi-Cancer Registry", "/Multi_Cancer_Explorer", """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>""")
        ]

        nav_html = '<div style="display: flex; flex-direction: column; gap: 5px; margin-bottom: 1.5rem;">'
        for title, link, svg_icon in nav_items:
            is_active = (title.lower() == active_tab.lower())
            if is_active:
                item_style = "background: linear-gradient(135deg, #7965E8 0%, #5B48CC 100%); color: #FFFFFF; font-weight: 600; box-shadow: 0 4px 14px rgba(121, 101, 232, 0.28);"
            else:
                item_style = "background: transparent; color: #475569; font-weight: 500;"

            nav_html += f'<a href="{link}" target="_self" style="text-decoration: none;"><div style="{item_style} border-radius: 10px; padding: 8px 12px; font-size: 0.84rem; display: flex; align-items: center; gap: 10px; transition: all 0.15s ease;"><span>{svg_icon}</span> {title}</div></a>'
        nav_html += '</div>'
        st.markdown(nav_html, unsafe_allow_html=True)

        # Expert Insights Box without emoji
        st.markdown("""
        <div style="background: #F0EDFF; border: 1px solid #D8D1F8; border-radius: 16px; padding: 1.15rem; margin-top: 1rem;">
            <div style="width: 32px; height: 32px; background: #FFFFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #7965E8; margin-bottom: 0.6rem; box-shadow: 0 2px 6px rgba(121, 101, 232, 0.15);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
            </div>
            <h4 style="margin: 0 0 4px 0; color: #25324A; font-size: 0.9rem; font-weight: 700;">Research Note</h4>
            <p style="font-size: 0.76rem; color: #64748B; margin-bottom: 10px; line-height: 1.4;">
                ZZFeatureMap kernel evaluated against Classical RBF-SVM on 212 held-out BCNB breast cancer patients.
            </p>
            <a href="/Quantum_Insights" target="_self" style="text-decoration: none;">
                <div style="background: linear-gradient(135deg, #7965E8 0%, #5B48CC 100%); color: #FFFFFF; border-radius: 9999px; padding: 7px 14px; font-size: 0.78rem; font-weight: 600; text-align: center; box-shadow: 0 2px 8px rgba(121, 101, 232, 0.25);">
                    Kernel Heatmaps →
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
