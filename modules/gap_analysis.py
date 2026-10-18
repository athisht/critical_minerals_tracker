"""
Technology Gap Analysis Module: Matrix Heatmap, Vulnerability Index, and White Space Discovery.
"""

import streamlit as st
import pandas as pd
from utils.visualizations import plot_gap_matrix
from config import CRITICAL_MINERALS, VALUE_CHAIN_STAGES

# Predefined strategic vulnerability benchmarks for Indian critical mineral ecosystem
STRATEGIC_GAPS = [
    {
        "mineral": "Rare Earth Elements (REE - Nd, Dy, Pr)",
        "stage": "4. Component & Precursor Manufacturing",
        "title": "Sintered NdFeB Permanent Magnets for EV Traction",
        "severity": "🔴 Critical National Vulnerability",
        "current_status": "India produces raw REE oxides via IREL, but lacks commercial-scale sintered NdFeB magnet manufacturing, causing 100% EV motor import dependency.",
        "recommended_action": "Establish National Magnet Mission; set up public-private pilot for vacuum induction melting and Dy grain boundary diffusion."
    },
    {
        "mineral": "Lithium (Li)",
        "stage": "3. Refining & High-Purity Chemical Processing",
        "title": "Direct Lithium Extraction (DLE) & Battery-Grade Hydroxide Refining",
        "severity": "🔴 Critical National Vulnerability",
        "current_status": "Heavy concentration of global patents held by foreign multinationals (Albemarle, POSCO). Domestic patents mostly restricted to pegmatite ore leaching.",
        "recommended_action": "Fund DLE adsorbent pilot facilities and pilot electrodialysis testing at domestic clay and brine exploration sites."
    },
    {
        "mineral": "Gallium & Germanium (Ga/Ge)",
        "stage": "3. Refining & High-Purity Chemical Processing",
        "title": "6N+ Semiconductor-Grade Refining from Refinery Liquors",
        "severity": "🔴 Critical National Vulnerability",
        "current_status": "Export controls from foreign suppliers risk India's semiconductor and defense optical supply chain. Indian Bayer liquor extraction remains largely at laboratory TRL 5-6.",
        "recommended_action": "Mandate gallium recovery units in domestic alumina refineries (NALCO, Hindalco) backed by PLI incentive."
    },
    {
        "mineral": "Graphite (C)",
        "stage": "3. Refining & High-Purity Chemical Processing",
        "title": "Non-HF Eco-Friendly Chemical Spheroidization",
        "severity": "🟡 Moderate Vulnerability / Emerging",
        "current_status": "India has good flake graphite reserves, but purification has historically relied on environmentally hazardous hydrofluoric acid. Emerging IIT patents need industrial scaling.",
        "recommended_action": "Incentivize commercial thermal and bio-roasting graphite purification hubs."
    },
    {
        "mineral": "Cobalt (Co)",
        "stage": "1. Exploration & Characterization",
        "title": "Deep-Sea Nodule Extraction & High-Pressure Acid Leaching",
        "severity": "🟡 Moderate Vulnerability",
        "current_status": "Exploration licenses in Central Indian Ocean Basin are active, but deep-sea mining metallurgy requires industrial demonstration under Samudrayaan Mission.",
        "recommended_action": "Accelerate CSIR-NML and NIOT joint demonstration pilot for polymetallic nodule processing."
    }
]

def render_gap_analysis(patents_df: pd.DataFrame):
    """Render technology gap matrix, white space explorer, and R&D simulator."""
    st.markdown("## 🎯 Technology Gap Identification & Strategic White Spaces")
    st.markdown(
        "A multi-dimensional diagnostic matrix identifying **critical domestic technology vulnerabilities**, "
        "foreign intellectual property dependencies, and unexploited research white spaces across India's mineral security landscape."
    )

    tab_matrix, tab_vulnerabilities, tab_simulator = st.tabs([
        "🗺️ Strategic Gap Heatmap",
        "🚨 High-Priority Technology Gaps",
        "💡 R&D Policy Simulator"
    ])

    with tab_matrix:
        st.markdown("### 📊 Mineral vs. Value Chain Stage Vulnerability Matrix")
        st.markdown(
            "Cells indicate patent density and domestic autonomy. **⚠️ marks high vulnerability** (zero patents or heavy foreign patent dominance)."
        )
        st.plotly_chart(plot_gap_matrix(patents_df, CRITICAL_MINERALS, VALUE_CHAIN_STAGES), use_container_width=True)

        st.markdown("#### 💡 Matrix Interpretation Guide:")
        c1, c2, c3 = st.columns(3)
        c1.markdown("🔴 **Critical White Space:** 0 to 1 domestic patents. Supply chain is completely exposed to foreign licensing or embargoes.")
        c2.markdown("🟡 **Emerging Indigenous:** 2 to 4 patents. Lab-scale or early pilot proven (TRL 4-6). Needs commercial scaling bridge.")
        c3.markdown("🟢 **Indigenous Strength:** ≥5 domestic patents (TRL 7+). Ready for large-scale industrial commercialization.")

    with tab_vulnerabilities:
        st.markdown("### 🚨 High-Priority Strategic Vulnerabilities (Policy Action Needed)")
        for gap in STRATEGIC_GAPS:
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border-left: 5px solid {'#EF4444' if 'Critical' in gap['severity'] else '#F59E0B'}; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 16px; font-weight: 700; color: #1E293B;">{gap['title']}</span>
                            <span style="font-size: 12px; font-weight: bold; color: {'#DC2626' if 'Critical' in gap['severity'] else '#D97706'};">{gap['severity']}</span>
                        </div>
                        <div style="font-size: 13px; color: #475569; margin: 4px 0 8px 0;">
                            <b>Target Mineral:</b> {gap['mineral']} &nbsp;|&nbsp; <b>Value Chain Stage:</b> {gap['stage']}
                        </div>
                        <div style="font-size: 13px; color: #334155; margin-bottom: 8px;">
                            <b>Current Vulnerability Assessment:</b> {gap['current_status']}
                        </div>
                        <div style="font-size: 13px; color: #065F46; background-color: #ECFDF5; padding: 6px 10px; border-radius: 4px; border: 1px solid #A7F3D0;">
                            <b>Recommended Policy / R&D Action:</b> {gap['recommended_action']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab_simulator:
        st.markdown("### 🎛️ R&D Strategic Investment & TRL Simulator")
        st.markdown("Simulate how targeted government grant injections could accelerate Technology Readiness Levels (TRL) and patent filings.")
        
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            target_mineral = st.selectbox("Select Target Mineral for Mission Funding:", CRITICAL_MINERALS)
            target_stage = st.selectbox("Select Value Chain Stage:", VALUE_CHAIN_STAGES)
            grant_amount = st.slider("Target R&D Grant Allocation (₹ Crores):", min_value=10, max_value=250, value=75, step=5)
            consortium_type = st.radio("Implementation Mechanism:", ["CSIR-Industry Co-Development Consortium", "National Mission Centre of Excellence (IITs)", "Direct Industry PLI Matched Grant"])

        with sim_col2:
            st.markdown("#### 📈 Projected Technology Outcomes (3-Year Horizon):")
            
            est_patents = int(grant_amount * 0.12 + 2)
            est_trl_gain = min(9, 5 + int(grant_amount / 40))
            jobs_created = grant_amount * 18
            
            st.metric("Estimated New Indian Patents Filed", f"+{est_patents} Patents")
            st.metric("Expected TRL Progression", f"TRL 5 ➔ TRL {est_trl_gain} (Industrial Ready)")
            st.metric("Specialized Metallurgy Engineers Trained", f"~{int(jobs_created)} personnel")
            
            st.success(
                f"**Simulation Summary:** An investment of **₹{grant_amount} Crores** in *{target_mineral}* ({target_stage.split('. ')[1]}) "
                f"via *{consortium_type}* is projected to shift India's status from **Import Dependent** to **Indigenous Pilot Proven** within 36 months."
            )
