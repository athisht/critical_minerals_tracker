"""
Live Search Module: Unified Indian Patents and Live OpenAlex Academic Literature Finder.
"""

import streamlit as st
import pandas as pd
from data.data_loader import search_openalex_live
from config import CRITICAL_MINERALS

def render_live_search(patents_df: pd.DataFrame, pubs_df: pd.DataFrame):
    """Render unified search interface with live API querying."""
    st.markdown("## 🔎 Unified Intelligence Search & Live Literature Finder")
    st.markdown(
        "Search indexed Indian patent applications, peer-reviewed publications, "
        "or query **OpenAlex live REST API** for the latest scholarly preprints and research papers affiliated with Indian institutions."
    )

    search_mode = st.radio(
        "Select Search Mode:",
        ["📚 Indexed Indian Patents & R&D Database", "🌐 Live OpenAlex API (Real-Time Indian Academic Search)"],
        horizontal=True
    )

    if search_mode == "📚 Indexed Indian Patents & R&D Database":
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            query = st.text_input("Enter Search Terms (e.g. 'lithium recycling', 'NdFeB', 'bayer liquor', 'NMC-811'):", "")
        with col_s2:
            mineral_filter = st.selectbox("Mineral Filter:", ["All"] + CRITICAL_MINERALS)

        # Tab results for Patents vs Publications
        tab_pat, tab_pub = st.tabs(["📄 Indian Patents", "📑 R&D Publications"])

        with tab_pat:
            filtered_p = patents_df.copy()
            if mineral_filter != "All":
                filtered_p = filtered_p[filtered_p["critical_mineral"] == mineral_filter]
            if query:
                q = query.lower()
                filtered_p = filtered_p[
                    filtered_p["title"].str.lower().str.contains(q) |
                    filtered_p["abstract"].str.lower().str.contains(q) |
                    filtered_p["assignee"].str.lower().str.contains(q)
                ]
            
            st.markdown(f"**Found {len(filtered_p)} matching Indian patents**")
            for _, r in filtered_p.iterrows():
                with st.expander(f"🔹 [{r['patent_id']}] {r['title']}"):
                    st.markdown(f"**Assignee:** {r['assignee']} | **Filing Year:** {r['filing_year']} | **Status:** {r['status']}")
                    st.markdown(f"**Critical Mineral:** {r['critical_mineral']} | **Stage:** {r['value_chain_stage']}")
                    st.markdown(f"**Abstract:** {r['abstract']}")
                    st.markdown(f"**IPC Classes:** `{', '.join(r['ipc_classes'])}` | **TRL Level:** {r['trl']}/9")

        with tab_pub:
            filtered_pub = pubs_df.copy()
            if mineral_filter != "All":
                filtered_pub = filtered_pub[filtered_pub["critical_mineral"] == mineral_filter]
            if query:
                q = query.lower()
                filtered_pub = filtered_pub[
                    filtered_pub["title"].str.lower().str.contains(q) |
                    filtered_pub["institution"].str.lower().str.contains(q)
                ]

            st.markdown(f"**Found {len(filtered_pub)} indexed Indian R&D papers**")
            for _, r in filtered_pub.iterrows():
                with st.expander(f"📑 [{r['year']}] {r['title']}"):
                    st.markdown(f"**Institution:** {r['institution']} | **Journal:** {r['journal']}")
                    st.markdown(f"**Authors:** {', '.join(r['authors'])} | **Citations:** {r['citations']}")
                    st.markdown(f"**Mineral:** {r['critical_mineral']} | **Stage:** {r['value_chain_stage']}")
                    st.markdown(f"**DOI:** [{r['doi']}](https://doi.org/{r['doi']})")

    else:
        # Live OpenAlex API search
        st.markdown("### 🌐 Real-Time Academic Research from Indian Institutions (OpenAlex API)")
        col_api1, col_api2, col_api3 = st.columns([3, 2, 1])
        with col_api1:
            live_term = st.text_input("Enter Technology Keywords:", "Lithium battery recycling")
        with col_api2:
            live_mineral = st.selectbox("Associated Mineral:", [""] + [m.split(" (")[0] for m in CRITICAL_MINERALS])
        with col_api3:
            st.write("")
            st.write("")
            trigger_search = st.button("🚀 Fetch Live", type="primary")

        if trigger_search or live_term:
            with st.spinner("Connecting to OpenAlex API (filtering by Indian Institutions)..."):
                live_results = search_openalex_live(query=live_term, mineral=live_mineral, max_results=8)
                
            if live_results:
                st.success(f"Successfully retrieved **{len(live_results)} live research papers** from OpenAlex:")
                for paper in live_results:
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                                <div style="font-weight: 700; font-size: 15px; color: #1E3A8A;">
                                    <a href="{paper['landing_page_url']}" target="_blank" style="text-decoration: none; color: #1E3A8A;">{paper['title']} 🔗</a>
                                </div>
                                <div style="font-size: 12px; color: #475569; margin: 4px 0;">
                                    <b>Year:</b> {paper['year']} &nbsp;|&nbsp; 
                                    <b>Authors:</b> {', '.join(paper['authors']) if paper['authors'] else 'Indian Research Team'} &nbsp;|&nbsp; 
                                    <b>Citations:</b> {paper['citations']} &nbsp;|&nbsp;
                                    <b>Domain:</b> <span style="background-color: #EDE9FE; color: #6D28D9; padding: 1px 6px; border-radius: 3px;">{paper['concept']}</span>
                                </div>
                                <div style="font-size: 12px; color: #0F766E;">
                                    <b>Affiliated Indian Institutions:</b> {', '.join(paper['institutions']) if paper['institutions'] else 'National Laboratory / University'}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("No live papers returned or network request timed out. You can also search the pre-indexed benchmark database above.")
