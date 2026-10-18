"""
Organizational Intelligence Module: Leading R&D Organizations, Inventors, and Collaboration Networks.
"""

import streamlit as st
import pandas as pd
from utils.visualizations import plot_top_organizations, plot_collaboration_network
from config import ORGANIZATION_TYPES

def render_org_intelligence(patents_df: pd.DataFrame, pubs_df: pd.DataFrame):
    """Render institutional intelligence, inventor leaderboards, and network graphs."""
    st.markdown("## 🏛️ Institutional Intelligence & R&D Ecosystem")
    st.markdown(
        "Analyze the leading organizations driving Indian critical mineral innovation. "
        "Benchmark national laboratories, premier academic institutions, public sector enterprises, and private industry leaders."
    )

    tab_overview, tab_network, tab_profile = st.tabs([
        "📊 Sector Leaderboards",
        "🕸️ Collaboration & Ecosystem Graph",
        "🏢 Institutional Deep-Dive"
    ])

    with tab_overview:
        col_top, col_filter = st.columns([3, 1])
        with col_filter:
            st.markdown("#### Filter Assignee Sector")
            selected_sectors = st.multiselect(
                "Filter Sectors:",
                ORGANIZATION_TYPES,
                default=ORGANIZATION_TYPES
            )
            top_n = st.slider("Number of Top Orgs:", min_value=5, max_value=20, value=10)
        
        with col_top:
            filtered_patents = patents_df[patents_df["assignee_type"].isin(selected_sectors)]
            st.plotly_chart(plot_top_organizations(filtered_patents, top_n=top_n), use_container_width=True)

        st.markdown("---")
        st.markdown("### 🏆 National R&D Sector Champions")
        
        # Sector champions summary
        sec_cols = st.columns(4)
        champions = [
            ("CSIR / National Labs", "CSIR-NML & CSIR-IMMT", "Hydrometallurgy, extraction, and mineral beneficiation"),
            ("Premier Academia", "IIT Madras & IISc Bangalore", "Next-gen cathodes, recycling, and battery chemistry"),
            ("PSUs & State Enterprises", "IREL (India) & NALCO", "Monazite rare earth refining and bauxite co-recovery"),
            ("Indian Private Industry", "Tata Chemicals & Lohum Cleantech", "Cathode active precursor synthesis and closed-loop recycling")
        ]
        for col, (sector_title, champ_name, champ_desc) in zip(sec_cols, champions):
            with col:
                st.markdown(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; height: 140px;">
                        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">{sector_title}</div>
                        <div style="font-size: 15px; font-weight: 800; color: #1E3A8A; margin: 4px 0;">{champ_name}</div>
                        <div style="font-size: 11px; color: #475569; line-height: 1.3;">{champ_desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab_network:
        st.markdown("### 🌐 National Critical Minerals Technological Overlap Network")
        st.markdown(
            "This graph reveals institutions with shared technology domains and complementary capabilities. "
            "Hover over nodes to explore institutional connectivity."
        )
        st.plotly_chart(plot_collaboration_network(patents_df), use_container_width=True)
        st.info("💡 **Policy Insight:** Connecting CSIR extraction laboratories directly with private cathode and magnet manufacturers offers the highest potential for indigenous commercialization.")

    with tab_profile:
        st.markdown("### 🔍 Institutional Portfolio Deep-Dive")
        unique_orgs = sorted(patents_df["assignee"].unique())
        selected_org = st.selectbox("Select Organization to Inspect:", unique_orgs, index=0)
        
        org_patents = patents_df[patents_df["assignee"] == selected_org]
        org_pubs = pubs_df[pubs_df["institution"].str.contains(selected_org[:10], case=False, na=False)]
        
        p_count = len(org_patents)
        granted_count = len(org_patents[org_patents["status"] == "Granted"])
        avg_trl = round(org_patents["trl"].mean(), 1) if p_count > 0 else 0
        state = org_patents["assignee_state"].iloc[0] if p_count > 0 else "N/A"
        sec = org_patents["assignee_type"].iloc[0] if p_count > 0 else "N/A"
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total Patents", f"{p_count}")
        col_m2.metric("Granted Patents", f"{granted_count}")
        col_m3.metric("Average TRL", f"{avg_trl} / 9")
        col_m4.metric("Location & Sector", f"{state} ({sec.split(' ')[0]})")
        
        st.markdown("#### 🔬 Core Minerals & Value Chain Focus")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Patents by Mineral:**")
            st.write(org_patents["critical_mineral"].value_counts().to_frame("Patents"))
        with c2:
            st.markdown("**Patents by Value Chain Stage:**")
            st.write(org_patents["value_chain_stage"].value_counts().to_frame("Patents"))
            
        st.markdown("#### 📄 Key Patent Filings:")
        for _, p in org_patents.iterrows():
            st.markdown(f"- **{p['patent_id']}** ({p['filing_year']}): *{p['title']}* — **{p['status']}** (TRL {p['trl']})")
            
        if not org_pubs.empty:
            st.markdown("#### 📚 Correlated R&D Publications:")
            for _, pb in org_pubs.iterrows():
                st.markdown(f"- **[{pb['year']}]** *{pb['title']}* — *{pb['journal']}* (Citations: {pb['citations']})")
