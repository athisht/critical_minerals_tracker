"""
Overview Module: Executive Dashboard and High-Level Intelligence for Critical Minerals.
"""

import streamlit as st
import pandas as pd
from utils.visualizations import (
    plot_filing_trends,
    plot_state_distribution,
    plot_trl_distribution
)

def render_overview(patents_df: pd.DataFrame, pubs_df: pd.DataFrame):
    """Render the executive overview dashboard."""
    st.markdown("## 📊 National Critical Minerals Technology Intelligence Dashboard")
    st.markdown(
        "A centralized platform integrating **Indian Patents (IPO / InPASS)** and **Public R&D Activities** "
        "to monitor technology mapping, institutional capabilities, and strategic gaps across India's critical minerals value chain."
    )
    
    # Calculate High-Level Metrics
    total_patents = len(patents_df)
    total_pubs = len(pubs_df)
    
    domestic_patents = len(patents_df[patents_df["assignee_type"] != "Foreign Assignee in India"])
    domestic_share = round((domestic_patents / total_patents) * 100, 1) if total_patents > 0 else 0
    
    granted_count = len(patents_df[patents_df["status"] == "Granted"])
    avg_citations = round(patents_df["citations_count"].mean(), 1) if total_patents > 0 else 0
    high_trl_count = len(patents_df[patents_df["trl"] >= 7])

    # KPI Metric Cards
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric(
            label="Total Indian Patents",
            value=f"{total_patents}",
            delta=f"{granted_count} Granted",
            help="Total tracked patent applications in India"
        )
    with kpi2:
        st.metric(
            label="R&D Publications",
            value=f"{total_pubs}",
            delta="Open Access / CSIR / IIT",
            help="Curated high-impact peer-reviewed Indian publications"
        )
    with kpi3:
        st.metric(
            label="Domestic Autonomy Index",
            value=f"{domestic_share}%",
            delta="Domestic vs Multinational",
            help="% of patents filed by Indian academic, PSU, and private entities"
        )
    with kpi4:
        st.metric(
            label="Industrial Pilot (TRL ≥ 7)",
            value=f"{high_trl_count}",
            delta=f"{round(high_trl_count/total_patents*100)}% of total",
            help="Technologies ready for or currently in pilot / commercial scale"
        )
    with kpi5:
        st.metric(
            label="Avg. Impact (Citations)",
            value=f"{avg_citations}",
            delta="Per Patent",
            help="Average forward and backward citations received"
        )

    st.markdown("---")

    # Main Visualizations Row 1
    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.plotly_chart(plot_filing_trends(patents_df), use_container_width=True)
    with col_right:
        st.plotly_chart(plot_state_distribution(patents_df), use_container_width=True)

    # Row 2: TRL Distribution & Critical Minerals Breakdown
    col_trl, col_min = st.columns([2, 3])
    with col_trl:
        st.plotly_chart(plot_trl_distribution(patents_df), use_container_width=True)
        
    with col_min:
        st.markdown("#### 💎 Patents Concentration by Critical Mineral")
        min_summary = patents_df.groupby("critical_mineral").agg(
            Patents=("patent_id", "count"),
            Granted=("status", lambda s: (s == "Granted").sum()),
            Avg_TRL=("trl", "mean"),
            Avg_Citations=("citations_count", "mean")
        ).reset_index()
        min_summary["Avg_TRL"] = min_summary["Avg_TRL"].round(1)
        min_summary["Avg_Citations"] = min_summary["Avg_Citations"].round(1)
        min_summary = min_summary.sort_values(by="Patents", ascending=False)
        
        st.dataframe(
            min_summary,
            column_config={
                "critical_mineral": "Critical Mineral",
                "Patents": st.column_config.ProgressColumn(
                    "Total Patents",
                    help="Volume of patent filings",
                    format="%d",
                    min_value=0,
                    max_value=int(min_summary["Patents"].max())
                ),
                "Granted": st.column_config.NumberColumn("Granted"),
                "Avg_TRL": st.column_config.NumberColumn("Avg TRL (1-9)"),
                "Avg_Citations": st.column_config.NumberColumn("Avg Citations")
            },
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")
    
    # Recent Strategic Filings Table
    st.markdown("#### ⚡ Featured High-Impact Indian Patent Filings")
    top_patents = patents_df.sort_values(by=["citations_count", "filing_year"], ascending=False).head(5)
    
    for _, row in top_patents.iterrows():
        with st.expander(f"🔹 **{row['patent_id']}**: {row['title']} ({row['assignee']})"):
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**Mineral:** {row['critical_mineral']}")
            c2.markdown(f"**Stage:** {row['value_chain_stage']}")
            c3.markdown(f"**TRL:** {row['trl']}/9 | **Status:** {row['status']}")
            c4.markdown(f"**IPC:** `{', '.join(row['ipc_classes'])}`")
            st.markdown(f"**Abstract:** {row['abstract']}")
            if row.get("commercial_status"):
                st.info(f"**Commercialization Note:** {row['commercial_status']}")
