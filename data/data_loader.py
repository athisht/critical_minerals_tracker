"""
Data loader and live API connector for the Critical Minerals Tracker.
Loads curated Indian patent & R&D benchmark datasets and interfaces with OpenAlex API.
"""

import json
import os
import streamlit as st
import pandas as pd
import requests

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PATENTS_FILE = os.path.join(DATA_DIR, "indian_patents.json")
PUBLICATIONS_FILE = os.path.join(DATA_DIR, "rd_publications.json")

@st.cache_data
def load_patents_df() -> pd.DataFrame:
    """Load Indian patents dataset into a Pandas DataFrame."""
    with open(PATENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["filing_year"] = pd.to_numeric(df["filing_year"], errors="coerce")
    df["citations_count"] = pd.to_numeric(df["citations_count"], errors="coerce").fillna(0).astype(int)
    df["trl"] = pd.to_numeric(df["trl"], errors="coerce").fillna(5).astype(int)
    return df

@st.cache_data
def load_publications_df() -> pd.DataFrame:
    """Load Indian R&D publications dataset into a Pandas DataFrame."""
    with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["citations"] = pd.to_numeric(df["citations"], errors="coerce").fillna(0).astype(int)
    return df

def search_openalex_live(query: str, mineral: str = None, max_results: int = 8) -> list:
    """
    Search OpenAlex API for live scholarly works affiliated with Indian institutions.
    OpenAlex is open-access and requires no authentication for basic academic queries.
    """
    search_term = f"{mineral or ''} {query} critical mineral India".strip()
    url = "https://api.openalex.org/works"
    params = {
        "filter": "institutions.country_code:IN",
        "search": search_term,
        "per-page": max_results,
        "sort": "publication_year:desc"
    }
    headers = {
        "User-Agent": "CriticalMineralsTracker/1.0 (mailto:contact@smarttracker.in)"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=6)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            parsed = []
            for item in results:
                authorships = item.get("authorships", [])
                authors = [a.get("author", {}).get("display_name", "") for a in authorships[:3]]
                inst_list = []
                for a in authorships:
                    for inst in a.get("institutions", []):
                        inst_name = inst.get("display_name")
                        if inst_name and inst_name not in inst_list:
                            inst_list.append(inst_name)
                
                doi = item.get("doi") or "N/A"
                title = item.get("title") or "Untitled Publication"
                pub_year = item.get("publication_year")
                cite_count = item.get("cited_by_count", 0)
                
                # Primary topic / concept
                primary_concept = "Critical Mineral Technology"
                concepts = item.get("concepts", [])
                if concepts:
                    primary_concept = concepts[0].get("display_name", primary_concept)
                
                parsed.append({
                    "title": title,
                    "doi": doi,
                    "year": pub_year,
                    "authors": authors,
                    "institutions": inst_list[:2],
                    "citations": cite_count,
                    "concept": primary_concept,
                    "open_access": item.get("open_access", {}).get("is_oa", False),
                    "landing_page_url": item.get("primary_location", {}).get("landing_page_url") or doi
                })
            return parsed
        else:
            return []
    except Exception as e:
        # Graceful fallback if network unavailable
        return []
