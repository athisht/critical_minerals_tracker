"""
Policy Dossier Module: Automated Technology Intelligence and Executive Policy Briefing Dossiers.
"""

import streamlit as st
import pandas as pd
from config import CRITICAL_MINERALS

def generate_dossier_text(mineral: str, patents_df: pd.DataFrame, pubs_df: pd.DataFrame) -> str:
    """Generate structured markdown policy briefing for government and R&D decision makers."""
    m_pats = patents_df[patents_df["critical_mineral"] == mineral] if mineral != "All Minerals" else patents_df
    m_pubs = pubs_df[pubs_df["critical_mineral"] == mineral] if mineral != "All Minerals" else pubs_df
    
    total = len(m_pats)
    granted = len(m_pats[m_pats["status"] == "Granted"])
    dom = len(m_pats[m_pats["assignee_type"] != "Foreign Assignee in India"])
    dom_pct = round((dom / total * 100), 1) if total > 0 else 0
    foreign_pct = round(100 - dom_pct, 1)
    
    top_assignees = m_pats["assignee"].value_counts().head(3).to_dict()
    assignee_str = ", ".join([f"{k} ({v} filings)" for k, v in top_assignees.items()]) or "Emerging national actors"
    
    # Stage breakdown
    stage_counts = m_pats["value_chain_stage"].value_counts().to_dict()
    stage_str = "\n".join([f"  - **{k}:** {v} patent filings" for k, v in stage_counts.items()]) or "  - Limited filings"

    report = f"""# NATIONAL TECHNOLOGY INTELLIGENCE BRIEFING: {mineral.upper()}
**Prepared for:** Ministry of Mines, Department of Science & Technology (DST), NITI Aayog
**System:** Smart Technology and Patent Tracker for Critical Minerals
**Jurisdiction:** Republic of India (IPO / InPASS Data Integration)

---

## 1. Executive Summary & Strategic Importance
Securing sovereign access and technological autonomy over **{mineral}** is essential for India's clean energy transition, defense electronics, and the national Net-Zero 2070 roadmap. Current reliance on foreign supply chains poses profound geopolitical vulnerability. 

This intelligence briefing analyzes India's intellectual property trajectory, identifies domestic institutional leaders, and provides actionable policy interventions.

---

## 2. Patent Portfolio & Domestic Autonomy Metrics
- **Total Tracked Indian Patents:** {total}
- **Patents Granted by Indian Patent Office (IPO):** {granted}
- **Domestic Self-Reliance Share:** {dom_pct}% (Indian entities)
- **Foreign Intellectual Property Share:** {foreign_pct}% (Multinationals filing in India)
- **Leading Domestic Assignees:** {assignee_str}

### Value Chain Distribution:
{stage_str}

---

## 3. Technology Gap & Vulnerability Assessment
1. **Upstream Refining Bottleneck:** While exploration efforts by GSI and AMD have identified reserves, the critical bottleneck resides in chemical refining to battery/semiconductor purity.
2. **Foreign Patent Encirclement:** Multinational corporations maintain substantial patent families in India for solvent extraction and advanced precursor manufacturing, risking future domestic production freedom-to-operate (FTO).
3. **TRL Bridge Disconnect:** Academic research from premier institutions (IITs, CSIR) is often confined to TRL 4-5 without adequate scale-up capital for commercial pilot plants (TRL 7+).

---

## 4. Policy Recommendations & Strategic Interventions
- **Recommendation 1: Launch National Mission Centre of Excellence (CoE)**
  Establish dedicated pilot facilities at CSIR-NML / CSIR-IMMT co-funded by KABIL (Khanij Bidesh India Ltd) to advance high-purity chemical processing.
  
- **Recommendation 2: Intellectual Property Patent Box & Fast-Track Examination**
  Provide green-channel fast-tracking for Indian critical mineral patent applications and tax incentives on royalties derived from domestic mineral patents.

- **Recommendation 3: Extended Producer Responsibility (EPR) & Recycling Mandates**
  Enforce domestic closed-loop recycling mandates with minimum recycled content requirements to stimulate indigenous hydrometallurgical recycling patents.

---
*Report generated autonomously by the Smart Technology and Patent Tracker Platform.*
"""
    return report

def render_policy_dossier(patents_df: pd.DataFrame, pubs_df: pd.DataFrame):
    """Render policy briefing generator."""
    st.markdown("## 📜 Policy Dossier & R&D Strategic Planning Engine")
    st.markdown(
        "Generate automated, data-driven **Executive Policy Briefings** for the Ministry of Mines, DST, and NITI Aayog. "
        "Synthesizes patent filing data, foreign IP exposure, domestic champions, and strategic recommendations."
    )

    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        selected_mineral = st.selectbox("Select Target Mineral for Dossier Generation:", ["All Minerals"] + CRITICAL_MINERALS)
    with col_sel2:
        st.write("")
        st.write("")
        regen = st.button("🔄 Generate Briefing", type="primary")

    dossier_content = generate_dossier_text(selected_mineral, patents_df, pubs_df)

    st.markdown("---")
    
    # Download Button
    st.download_button(
        label="📥 Download Official Policy Dossier (.md)",
        data=dossier_content,
        file_name=f"Policy_Dossier_{selected_mineral.replace(' ', '_').replace('/', '_')}.md",
        mime="text/markdown"
    )

    # Display Report in Markdown container
    st.markdown(dossier_content)
