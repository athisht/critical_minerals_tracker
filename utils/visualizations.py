"""
Visualization utilities for the Critical Minerals Smart Tracker.
Generates interactive Plotly charts, heatmaps, treemaps, and network graphs.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import networkx as nx

# Consistent professional color palette
COLOR_PALETTE = {
    "primary": "#1E3A8A",      # Deep Blue
    "secondary": "#0D9488",    # Teal
    "accent": "#F59E0B",       # Amber
    "warning": "#EF4444",      # Red (for gaps)
    "success": "#10B981",      # Green (for indigenous strengths)
    "background": "#F8FAFC",
    "card_bg": "#FFFFFF"
}

ORG_TYPE_COLORS = {
    "CSIR / National R&D Labs": "#2563EB",       # Blue
    "Premier Academic (IITs/IISc)": "#7C3AED",   # Purple
    "PSU / Public Sector Enterprise": "#059669", # Green
    "Indian Private Industry": "#D97706",        # Amber
    "Foreign Assignee in India": "#DC2626"       # Red
}

def plot_filing_trends(df: pd.DataFrame) -> go.Figure:
    """Line & bar chart of patent filing velocity over years with status breakdown."""
    if df.empty:
        return go.Figure()
    
    trend_data = df.groupby(["filing_year", "status"]).size().reset_index(name="count")
    
    fig = px.bar(
        trend_data,
        x="filing_year",
        y="count",
        color="status",
        barmode="stack",
        title="<b>Indian Patent Filing & Grant Velocity (2017–2025)</b>",
        labels={"filing_year": "Filing Year", "count": "Number of Patents", "status": "Patent Status"},
        color_discrete_map={
            "Granted": "#10B981",
            "Published / Under Examination": "#3B82F6",
            "Abandoned": "#9CA3AF"
        }
    )
    
    # Add cumulative line
    yearly_totals = df.groupby("filing_year").size().cumsum().reset_index(name="cumulative")
    fig.add_trace(
        go.Scatter(
            x=yearly_totals["filing_year"],
            y=yearly_totals["cumulative"],
            name="Cumulative Filings",
            mode="lines+markers",
            line=dict(color="#1E293B", width=3, dash="dot"),
            yaxis="y2"
        )
    )
    
    fig.update_layout(
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis2=dict(title="Cumulative Patents", overlaying="y", side="right", showgrid=False),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def plot_gap_matrix(df: pd.DataFrame, minerals: list, stages: list) -> go.Figure:
    """
    Centerpiece: Technology Gap Matrix.
    Computes patent concentration and domestic autonomy for each (Mineral x Stage) intersection.
    """
    # Create empty matrix
    matrix_counts = np.zeros((len(minerals), len(stages)))
    domestic_pct = np.zeros((len(minerals), len(stages)))
    
    for i, mineral in enumerate(minerals):
        for j, stage in enumerate(stages):
            sub = df[(df["critical_mineral"] == mineral) & (df["value_chain_stage"] == stage)]
            count = len(sub)
            matrix_counts[i, j] = count
            if count > 0:
                dom_count = len(sub[sub["assignee_type"] != "Foreign Assignee in India"])
                domestic_pct[i, j] = (dom_count / count) * 100
            else:
                domestic_pct[i, j] = 0

    # Custom text for hover and annotations
    annotations = []
    text_matrix = []
    for i in range(len(minerals)):
        row_text = []
        for j in range(len(stages)):
            c = int(matrix_counts[i, j])
            d = int(domestic_pct[i, j])
            if c == 0:
                status_label = "CRITICAL GAP (0 patents)"
            elif d < 40:
                status_label = f"HIGH FOREIGN DEP ({d}% Dom)"
            elif c >= 4 and d >= 75:
                status_label = f"INDIGENOUS CORE ({c} pats)"
            else:
                status_label = f"EMERGING ({c} pats)"
            
            row_text.append(f"Patents: {c}<br>Domestic: {d}%<br>Status: {status_label}")
        text_matrix.append(row_text)

    # Simplified labels for axis display
    short_stages = ["1. Exploration", "2. Extraction", "3. Refining", "4. Component Mfg", "5. Recycling"]
    short_minerals = [m.split(" (")[0] for m in minerals]

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix_counts,
            x=short_stages,
            y=short_minerals,
            text=text_matrix,
            hoverinfo="text",
            colorscale=[
                [0.0, "#FEE2E2"],   # Zero patents (Very soft red)
                [0.2, "#FEF3C7"],   # Low patents (Light yellow)
                [0.5, "#BAE6FD"],   # Moderate (Light sky blue)
                [0.8, "#60A5FA"],   # Good (Vibrant blue)
                [1.0, "#1E3A8A"]    # High density (Deep Navy)
            ],
            colorbar=dict(title="Patent Count")
        )
    )

    # Add numeric count overlays
    for i in range(len(minerals)):
        for j in range(len(stages)):
            val = int(matrix_counts[i, j])
            dom = int(domestic_pct[i, j])
            color = "white" if val >= 5 else "#1F2937"
            marker = "⚠️" if val == 0 or dom < 40 else "✓" if val >= 4 else "•"
            fig.add_annotation(
                x=short_stages[j],
                y=short_minerals[i],
                text=f"<b>{val}</b> <span style='font-size:10px;'>({marker})</span>",
                showarrow=False,
                font=dict(color=color, size=12)
            )

    fig.update_layout(
        title="<b>Critical Minerals Technology Gap Matrix (Patents & Vulnerability)</b>",
        xaxis_title="Value Chain Stage",
        yaxis_title="Critical Mineral",
        template="plotly_white",
        margin=dict(l=50, r=30, t=50, b=40),
        height=520
    )
    return fig

def plot_technology_treemap(df: pd.DataFrame) -> go.Figure:
    """Treemap of Critical Mineral -> Value Chain Stage -> Assignee."""
    if df.empty:
        return go.Figure()
    
    fig = px.treemap(
        df,
        path=[px.Constant("All Critical Minerals"), "critical_mineral", "value_chain_stage", "assignee"],
        values="citations_count",
        color="trl",
        color_continuous_scale="Viridis",
        title="<b>Technology Landscape Hierarchy (Sized by Citations, Colored by TRL)</b>"
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=460)
    return fig

def plot_top_organizations(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart of top patent holders with organization type breakdown."""
    if df.empty:
        return go.Figure()
    
    top_orgs = df.groupby(["assignee", "assignee_type"]).size().reset_index(name="count")
    top_orgs = top_orgs.sort_values(by="count", ascending=True).tail(top_n)
    
    fig = px.bar(
        top_orgs,
        x="count",
        y="assignee",
        color="assignee_type",
        orientation="h",
        title=f"<b>Top {top_n} Leading Patent Assignees in India</b>",
        labels={"count": "Number of Patents", "assignee": "Organization", "assignee_type": "Sector"},
        color_discrete_map=ORG_TYPE_COLORS
    )
    
    fig.update_layout(
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=30),
        height=420
    )
    return fig

def plot_state_distribution(df: pd.DataFrame) -> go.Figure:
    """Bar chart of patents distribution across Indian States."""
    if df.empty:
        return go.Figure()
    
    state_df = df.groupby("assignee_state").size().reset_index(name="count").sort_values(by="count", ascending=False)
    
    fig = px.bar(
        state_df,
        x="assignee_state",
        y="count",
        color="count",
        color_continuous_scale="Blues",
        title="<b>Geographic Distribution of Critical Mineral R&D Hubs (by State)</b>",
        labels={"assignee_state": "State", "count": "Patents Count"}
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=30), height=350)
    return fig

def plot_trl_distribution(df: pd.DataFrame) -> go.Figure:
    """Distribution of Technology Readiness Levels (TRL 1 to 9)."""
    if df.empty:
        return go.Figure()
        
    trl_df = df.groupby("trl").size().reset_index(name="count")
    
    colors = ["#EF4444" if t <= 3 else "#F59E0B" if t <= 6 else "#10B981" for t in trl_df["trl"]]
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=[f"TRL {t}" for t in trl_df["trl"]],
                y=trl_df["count"],
                marker_color=colors,
                text=trl_df["count"],
                textposition="auto"
            )
        ]
    )
    fig.update_layout(
        title="<b>Technology Readiness Level (TRL) Breakdown</b><br><span style='font-size:11px;'>Red: Lab (TRL 1-3) | Amber: Prototype (TRL 4-6) | Green: Industrial Pilot (TRL 7-9)</span>",
        xaxis_title="TRL Stage",
        yaxis_title="Patents Count",
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=30),
        height=320
    )
    return fig

def plot_collaboration_network(df: pd.DataFrame) -> go.Figure:
    """
    R&D & Industry Collaboration Network Graph.
    Constructs an undirected graph connecting institutions sharing patents or technologies.
    """
    G = nx.Graph()
    
    # Identify unique assignees and add as nodes
    assignee_meta = df.drop_duplicates(subset=["assignee"])[["assignee", "assignee_type"]].set_index("assignee").to_dict()["assignee_type"]
    
    for assignee, org_type in assignee_meta.items():
        pat_count = len(df[df["assignee"] == assignee])
        G.add_node(assignee, org_type=org_type, size=max(12, pat_count * 5))
        
    # Create edges between assignees that work on the same mineral + stage
    grouped = df.groupby(["critical_mineral", "value_chain_stage"])
    edge_weights = {}
    for _, group in grouped:
        assignees = list(group["assignee"].unique())
        for i in range(len(assignees)):
            for j in range(i + 1, len(assignees)):
                u, v = sorted([assignees[i], assignees[j]])
                edge_weights[(u, v)] = edge_weights.get((u, v), 0) + 1
                
    for (u, v), weight in edge_weights.items():
        if weight >= 1:
            G.add_edge(u, v, weight=weight)
            
    # Calculate Spring layout positions
    pos = nx.spring_layout(G, k=0.55, seed=42)
    
    # Edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.2, color="#CBD5E1"),
        hoverinfo="none",
        mode="lines"
    )
    
    # Node traces by org type for clean legend
    node_traces = []
    for org_type, color in ORG_TYPE_COLORS.items():
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        for node in G.nodes():
            if G.nodes[node].get("org_type") == org_type:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                degree = G.degree[node]
                node_size.append(G.nodes[node]["size"])
                node_text.append(f"<b>{node}</b><br>Type: {org_type}<br>Tech Overlaps/Connections: {degree}")
                
        if node_x:
            trace = go.Scatter(
                x=node_x, y=node_y,
                mode="markers+text",
                name=org_type,
                marker=dict(
                    size=node_size,
                    color=color,
                    line=dict(width=1.5, color="#FFFFFF")
                ),
                text=[n.split("(")[0].strip()[:18] for n in G.nodes() if G.nodes[n].get("org_type") == org_type],
                textposition="bottom center",
                textfont=dict(size=9),
                hovertext=node_text,
                hoverinfo="text"
            )
            node_traces.append(trace)
            
    fig = go.Figure(
        data=[edge_trace] + node_traces,
        layout=go.Layout(
            title="<b>National Critical Minerals Technology & Collaboration Network</b><br><span style='font-size:11px;'>Nodes sized by patent portfolio; Edges represent shared mineral domain / co-specialization</span>",
            showlegend=True,
            hovermode="closest",
            margin=dict(b=20, l=10, r=10, t=50),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template="plotly_white",
            height=550
        )
    )
    return fig
