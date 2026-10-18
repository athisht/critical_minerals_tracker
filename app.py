"""
Smart Technology and Patent Tracker for Critical Minerals
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_patents_df, load_publications_df
from modules.overview import render_overview
from modules.tech_mapping import render_tech_mapping
from modules.trends import render_trends
from modules.org_intelligence import render_org_intelligence
from modules.gap_analysis import render_gap_analysis
from modules.live_search import render_live_search
from modules.policy_dossier import render_policy_dossier

# Configure page
st.set_page_config(
    page_title="Smart Technology & Patent Tracker | Critical Minerals",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown(
    """
    <style>
    /* Global Styles */
    .main {
        background-color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #0F172A;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    /* Sidebar header banner */
    .sidebar-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        padding: 16px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar-title {
        font-size: 16px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .sidebar-subtitle {
        font-size: 11px;
        opacity: 0.85;
        margin-top: 4px;
    }
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #64748B !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #1E3A8A !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Load cached datasets
    patents_df = load_patents_df()
    pubs_df = load_publications_df()

    # Sidebar
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-header">
                <div style="font-size: 24px; margin-bottom: 4px;">🇮🇳 ⛏️</div>
                <div class="sidebar-title">CRITICAL MINERALS IP TRACKER</div>
                <div class="sidebar-subtitle">Smart Patent & R&D Intelligence Platform</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        nav_selection = st.radio(
            "Navigation Modules:",
            [
                "📊 Executive Overview",
                "🗺️ Technology Mapping",
                "📈 Technology Trends & Velocity",
                "🏛️ Institutional Intelligence",
                "🎯 Technology Gaps & Gaps Matrix",
                "🔎 Unified Search & Live OpenAlex",
                "📜 Policy Dossier Generator"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("### ⚙️ Global Filter Parameters")
        
        # Year range filter
        min_year = int(patents_df["filing_year"].min())
        max_year = int(patents_df["filing_year"].max())
        year_range = st.slider("Filing Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

        # Status filter
        all_statuses = ["All Statuses"] + list(patents_df["status"].unique())
        selected_status = st.selectbox("Patent Status:", all_statuses)

        # Apply global filters to working dataframe
        working_patents = patents_df[
            (patents_df["filing_year"] >= year_range[0]) &
            (patents_df["filing_year"] <= year_range[1])
        ]
        if selected_status != "All Statuses":
            working_patents = working_patents[working_patents["status"] == selected_status]

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 11px; color: #64748B; line-height: 1.4;">
                <b>Integrated Data Sources:</b><br>
                • Indian Patent Office (InPASS / IPO)<br>
                • OpenAlex Scholarly Database (IN)<br>
                • CSIR, DAE, IIT Portfolios<br>
                • Ministry of Mines Critical Minerals List
            </div>
            """,
            unsafe_allow_html=True
        )

    # Dispatch to Selected Navigation Module
    if nav_selection == "📊 Executive Overview":
        render_overview(working_patents, pubs_df)
    elif nav_selection == "🗺️ Technology Mapping":
        render_tech_mapping(working_patents)
    elif nav_selection == "📈 Technology Trends & Velocity":
        render_trends(working_patents)
    elif nav_selection == "🏛️ Institutional Intelligence":
        render_org_intelligence(working_patents, pubs_df)
    elif nav_selection == "🎯 Technology Gaps & Gaps Matrix":
        render_gap_analysis(working_patents)
    elif nav_selection == "🔎 Unified Search & Live OpenAlex":
        render_live_search(working_patents, pubs_df)
    elif nav_selection == "📜 Policy Dossier Generator":
        render_policy_dossier(working_patents, pubs_df)

if __name__ == "__main__":
    main()
