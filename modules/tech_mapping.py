"""
Technology Mapping Module: Interactive Value Chain and IPC Classification Explorer.
"""

import streamlit as st
import pandas as pd
from utils.visualizations import plot_technology_treemap
from config import CRITICAL_MINERALS, VALUE_CHAIN_STAGES, VALUE_CHAIN_DESCRIPTIONS, IPC_CLASSES

def render_tech_mapping(patents_df: pd.DataFrame):
    """Render technology mapping across value chain and IPC codes."""
    st.markdown("## 🗺️ Technology Mapping Across Critical Minerals Value Chain")
    st.markdown(
        "Explore how Indian patents and technological advancements map onto each phase of the critical minerals "
        "lifecycle—from geological exploration and refining to battery component synthesis and circular recycling."
    )

    # Filter Bar
    col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
    with col_f1:
        selected_mineral = st.selectbox("Filter by Mineral:", ["All Minerals"] + CRITICAL_MINERALS)
    with col_f2:
        selected_stage = st.selectbox("Filter by Value Chain Stage:", ["All Stages"] + VALUE_CHAIN_STAGES)
    with col_f3:
        search_query = st.text_input("🔍 Search Title / Abstract / IPC:", "")

    # Apply filters
    filtered_df = patents_df.copy()
    if selected_mineral != "All Minerals":
        filtered_df = filtered_df[filtered_df["critical_mineral"] == selected_mineral]
    if selected_stage != "All Stages":
        filtered_df = filtered_df[filtered_df["value_chain_stage"] == selected_stage]
    if search_query:
        q = search_query.lower()
        filtered_df = filtered_df[
            filtered_df["title"].str.lower().str.contains(q) |
            filtered_df["abstract"].str.lower().str.contains(q) |
            filtered_df["ipc_classes"].apply(lambda classes: any(q in c.lower() for c in classes)) |
            filtered_df["assignee"].str.lower().str.contains(q)
        ]

    st.markdown("---")

    # Value Chain Visual Cards
    st.markdown("### 🔄 5-Stage Value Chain Blueprint")
    cols = st.columns(5)
    for idx, (col, stage) in enumerate(zip(cols, VALUE_CHAIN_STAGES)):
        count = len(patents_df[patents_df["value_chain_stage"] == stage])
        with col:
            st.markdown(
                f"""
                <div style="background-color: #F1F5F9; border-radius: 8px; padding: 12px; border-top: 4px solid #1E3A8A; height: 160px;">
                    <div style="font-weight: 700; font-size: 13px; color: #1E3A8A;">{stage}</div>
                    <div style="font-size: 22px; font-weight: bold; margin: 8px 0; color: #0F172A;">{count} <span style="font-size: 12px; font-weight: normal; color: #64748B;">patents</span></div>
                    <div style="font-size: 11px; color: #475569; line-height: 1.3;">{VALUE_CHAIN_DESCRIPTIONS[stage][:80]}...</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Treemap of Technology Hierarchy
    st.markdown("### 🌲 Technology Classification Treemap")
    st.plotly_chart(plot_technology_treemap(filtered_df), use_container_width=True)

    # IPC Classification Guide
    with st.expander("📚 Key IPC / CPC Classification Codes Guide for Critical Minerals"):
        ipc_df = pd.DataFrame(list(IPC_CLASSES.items()), columns=["IPC Code", "Domain Description"])
        st.dataframe(ipc_df, use_container_width=True, hide_index=True)

    st.markdown(f"### 📋 Matched Patent Records ({len(filtered_df)} results)")
    
    if filtered_df.empty:
        st.warning("No patents found matching your selected criteria.")
    else:
        for _, row in filtered_df.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline;">
                            <span style="font-weight: bold; font-size: 16px; color: #1E3A8A;">{row['title']}</span>
                            <span style="background-color: {'#D1FAE5' if row['status'] == 'Granted' else '#DBEAFE'}; color: {'#065F46' if row['status'] == 'Granted' else '#1E40AF'}; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{row['status']}</span>
                        </div>
                        <div style="font-size: 13px; color: #475569; margin: 6px 0;">
                            <b>Patent ID:</b> {row['patent_id']} | <b>Assignee:</b> {row['assignee']} ({row['assignee_type']}) | <b>State:</b> {row['assignee_state']} | <b>Filing Year:</b> {row['filing_year']}
                        </div>
                        <div style="font-size: 12px; color: #334155; margin-bottom: 8px;">
                            <b>Mineral:</b> <span style="color: #D97706; font-weight: 600;">{row['critical_mineral']}</span> &nbsp;|&nbsp; 
                            <b>Stage:</b> {row['value_chain_stage']} &nbsp;|&nbsp; 
                            <b>TRL:</b> <span style="background-color: #FEF3C7; padding: 2px 6px; border-radius: 3px; font-weight: 600;">Level {row['trl']}</span> &nbsp;|&nbsp; 
                            <b>IPC:</b> <code>{', '.join(row['ipc_classes'])}</code> &nbsp;|&nbsp; 
                            <b>Citations:</b> {row['citations_count']}
                        </div>
                        <div style="font-size: 13px; color: #1E293B; line-height: 1.4;">
                            {row['abstract']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
