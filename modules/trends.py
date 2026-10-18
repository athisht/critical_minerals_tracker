"""
Trends Module: Technology Trends, Filing Growth Velocity, and Technology Lifecycle Assessment.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import CRITICAL_MINERALS

def calculate_cagr(start_val: float, end_val: float, years: int) -> float:
    """Calculate Compound Annual Growth Rate (CAGR)."""
    if start_val <= 0 or years <= 0:
        return 0.0
    return round(((end_val / start_val) ** (1 / years) - 1) * 100, 1)

def render_trends(patents_df: pd.DataFrame):
    """Render trends analysis and technology lifecycles."""
    st.markdown("## 📈 Technology Trends & Filing Velocity Analysis")
    st.markdown(
        "Monitor the evolutionary momentum of intellectual property across critical minerals. "
        "Identify high-acceleration domains through filing velocity, CAGR metrics, and technology lifecycle modeling."
    )

    # Multi-mineral trend line chart
    st.markdown("### 🔍 Historical Patent Filing Trends by Mineral (2017–2024)")
    
    pivot_trends = patents_df.pivot_table(
        index="filing_year",
        columns="critical_mineral",
        values="patent_id",
        aggfunc="count",
        fill_value=0
    ).reset_index()

    selected_minerals = st.multiselect(
        "Select minerals to compare on timeline:",
        CRITICAL_MINERALS,
        default=CRITICAL_MINERALS[:4]
    )

    if selected_minerals:
        fig_trend = go.Figure()
        for mineral in selected_minerals:
            if mineral in pivot_trends.columns:
                fig_trend.add_trace(
                    go.Scatter(
                        x=pivot_trends["filing_year"],
                        y=pivot_trends[mineral],
                        mode="lines+markers",
                        name=mineral,
                        line=dict(width=2.5)
                    )
                )
        fig_trend.update_layout(
            template="plotly_white",
            xaxis=dict(title="Year of Filing", dtick=1),
            yaxis=dict(title="Patents Filed"),
            hovermode="x unified",
            height=400,
            margin=dict(l=40, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Select at least one mineral from the selector above to visualize trends.")

    st.markdown("---")

    # Technology Lifecycle Classification
    st.markdown("### 🧬 Technology Lifecycle Dynamics & Growth Matrix")
    
    # Calculate CAGR and acceleration metrics
    lifecycle_records = []
    min_year, max_year = 2018, 2023
    years_span = max_year - min_year
    
    for mineral in CRITICAL_MINERALS:
        m_df = patents_df[patents_df["critical_mineral"] == mineral]
        count_start = len(m_df[m_df["filing_year"] <= 2019])
        count_end = len(m_df[m_df["filing_year"] >= 2022])
        total_pats = len(m_df)
        granted_pats = len(m_df[m_df["status"] == "Granted"])
        
        # Estimate annualized growth
        cagr = calculate_cagr(max(1, count_start), max(1, count_end), 4)
        
        # Lifecycle heuristic
        if cagr > 30 and total_pats >= 5:
            lifecycle = "🚀 High Growth / Emerging"
            rec = "Accelerate capital expenditure & industrial testing"
        elif cagr > 10:
            lifecycle = "📈 Maturing Expansion"
            rec = "Support standard-setting and pilot scaling"
        elif cagr >= 0:
            lifecycle = "⚖️ Steady / Moderate"
            rec = "Evaluate IP modernization and international partnerships"
        else:
            lifecycle = "⚠️ Stagnant / At Risk"
            rec = "Prioritize targeted R&D mission interventions"

        lifecycle_records.append({
            "Critical Mineral": mineral,
            "Total Patents": total_pats,
            "Granted Patents": granted_pats,
            "Early Period (≤2019)": count_start,
            "Recent Period (≥2022)": count_end,
            "Filing Growth Rate": f"+{cagr}%" if cagr > 0 else f"{cagr}%",
            "Lifecycle Status": lifecycle,
            "Strategic Recommendation": rec
        })

    lifecycle_df = pd.DataFrame(lifecycle_records)
    
    st.dataframe(
        lifecycle_df,
        column_config={
            "Critical Mineral": st.column_config.TextColumn("Critical Mineral", width="medium"),
            "Total Patents": st.column_config.NumberColumn("Total Patents", format="%d"),
            "Filing Growth Rate": st.column_config.TextColumn("Acceleration Rate"),
            "Lifecycle Status": st.column_config.TextColumn("Lifecycle Phase", width="medium"),
            "Strategic Recommendation": st.column_config.TextColumn("Strategic Action", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Value Chain Acceleration Comparison
    st.markdown("### 📊 Patent Filing Momentum by Value Chain Stage")
    stage_trend = patents_df.pivot_table(
        index="filing_year",
        columns="value_chain_stage",
        values="patent_id",
        aggfunc="count",
        fill_value=0
    ).reset_index()

    fig_stage = px.area(
        stage_trend,
        x="filing_year",
        y=[c for c in stage_trend.columns if c != "filing_year"],
        title="<b>Value Chain Shift: Acceleration in Precursor Manufacturing & Recycling</b>",
        labels={"filing_year": "Year", "value": "Number of Filings", "variable": "Value Chain Stage"},
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_stage.update_layout(template="plotly_white", height=380, margin=dict(l=40, r=20, t=50, b=40))
    st.plotly_chart(fig_stage, use_container_width=True)
