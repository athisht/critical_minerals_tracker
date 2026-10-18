# Smart Technology & Patent Tracker for Critical Minerals ⛏️🇮🇳

A software and web-based intelligence platform integrating publicly available information on **Indian Patents (IPO / InPASS)** and **R&D Activities** related to **Critical Minerals** (Lithium, Rare Earths, Cobalt, Nickel, Graphite, Titanium, Vanadium, Niobium, Gallium, etc.).

---

## 🎯 Key Features Aligned with Problem Statement

1. **Technology Mapping Across the 5-Stage Value Chain:**
   - Exploration & Characterization
   - Beneficiation & Extraction
   - Chemical Refining & High-Purity Processing
   - Precursor & Component Manufacturing
   - Recycling & Secondary Urban Mining
   - Interactive Treemap and IPC classification code indexing (`C22B`, `H01M`, `C01D`, `C01G`, `B03B`, etc.).

2. **Trends & Growth Velocity:**
   - Time-series patent filing dynamics (2017–2025).
   - Compound Annual Growth Rate (CAGR) calculation.
   - Technology Lifecycle Classification (Emerging, Growth, Maturing, Stagnant).

3. **Leading Organisations and Research Areas:**
   - Multi-sector leaderboards: CSIR Labs, Premier Academia (IITs/IISc), PSUs (IREL, NALCO, HCL), and Private Industry (Tata, Reliance, Lohum, Epsilon).
   - Interactive Network Graph showing technological co-specialization and institutional linkages.
   - Institutional Profile deep-dive with portfolio and TRL distribution.

4. **Identification of Technology Gaps & Emerging Areas:**
   - **Critical Minerals Technology Gap Matrix (Heatmap)** comparing Minerals vs. Value Chain Stages with vulnerability flagging (`⚠️`).
   - Strategic White Space alerts (e.g. Sintered NdFeB permanent magnets, Direct Lithium Extraction).
   - Interactive R&D policy investment and TRL simulator.

5. **Technology Intelligence for R&D Planning & Policy Decisions:**
   - One-click Executive Policy Dossier generator for Ministry of Mines, DST, and NITI Aayog.
   - Live integration with the **OpenAlex REST API** to query real-time scholarly papers from Indian researchers.
   - Direct export of briefings to Markdown.

---

## 🚀 How to Run the Prototype

### Option 1: Double-Click Launcher (Windows)
Double-click on [`run_tracker.bat`](file:///C:/Users/Athish%20T/critical_minerals_tracker/run_tracker.bat) inside the project folder.

### Option 2: Terminal Command
Open PowerShell or Command Prompt, navigate to the folder, and run:
```powershell
cd "C:\Users\Athish T\critical_minerals_tracker"
python -m streamlit run app.py
```
The application will launch at `http://localhost:8501`.

---

## 📁 Project Structure

```
critical_minerals_tracker/
├── app.py                      # Main Streamlit dashboard application
├── config.py                   # Minerals, value chain stages, and IPC mappings
├── run_tracker.bat             # 1-Click Windows launcher
├── data/
│   ├── indian_patents.json     # Curated benchmark dataset of Indian patents
│   ├── rd_publications.json   # Curated Indian R&D publications
│   ├── data_loader.py          # Data ingestion and live OpenAlex API client
│   └── generate_dataset.py     # Dataset generation script
├── modules/
│   ├── overview.py             # Executive KPIs & Overview
│   ├── tech_mapping.py         # Technology Mapping & Value Chain Treemap
│   ├── trends.py               # Filing Trends, CAGR & Lifecycle modeling
│   ├── org_intelligence.py     # Organizations, Inventors & Network Graph
│   ├── gap_analysis.py         # Technology Gap Matrix & R&D Simulator
│   ├── live_search.py          # Unified Indian DB search + Live OpenAlex API
│   └── policy_dossier.py       # Automated Policy Briefing Generator
└── utils/
    └── visualizations.py       # Plotly chart utilities (Heatmaps, Networks, Bars)
```
