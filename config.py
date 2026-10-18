"""
Configuration and constants for the Smart Technology and Patent Tracker for Critical Minerals.
Aligned with Ministry of Mines (India) Critical Minerals Strategy and Indian Patent Classification (InPASS/IPC).
"""

CRITICAL_MINERALS = [
    "Lithium (Li)",
    "Cobalt (Co)",
    "Nickel (Ni)",
    "Rare Earth Elements (REE - Nd, Dy, Pr)",
    "Graphite (C)",
    "Titanium (Ti)",
    "Vanadium (V)",
    "Niobium & Tantalum (Nb/Ta)",
    "Gallium & Germanium (Ga/Ge)",
    "Platinum Group Metals (PGM)"
]

VALUE_CHAIN_STAGES = [
    "1. Exploration & Characterization",
    "2. Beneficiation & Extraction",
    "3. Refining & High-Purity Chemical Processing",
    "4. Component & Precursor Manufacturing",
    "5. Recycling & Secondary Recovery"
]

ORGANIZATION_TYPES = [
    "CSIR / National R&D Labs",
    "Premier Academic (IITs/IISc)",
    "PSU / Public Sector Enterprise",
    "Indian Private Industry",
    "Foreign Assignee in India"
]

INDIAN_STATES = [
    "Odisha",
    "Jharkhand",
    "Karnataka",
    "Tamil Nadu",
    "Maharashtra",
    "Telangana",
    "Gujarat",
    "West Bengal",
    "Delhi NCR",
    "Chhattisgarh",
    "Rajasthan",
    "Kerala"
]

IPC_CLASSES = {
    "C22B": "Production and refining of metals; alloys",
    "H01M": "Processes/means for direct conversion of chemical to electrical energy (Batteries)",
    "C01D": "Compounds of alkali metals (Lithium, Sodium, Potassium)",
    "C01G": "Compounds of heavy metals (Cobalt, Nickel, Titanium, Vanadium)",
    "B03B": "Separating solid materials using liquids or wet processes",
    "B03D": "Flotation processes for mineral beneficiation",
    "B09B": "Disposal of solid waste; recycling of manufactured items",
    "H01F": "Magnets, inductors, transformers (Rare earth permanent magnets)",
    "C25C": "Electrolytic production or refining of metals",
    "C04B": "Lime, magnesia, slag, cermets, ceramics"
}

# Value chain definitions with descriptions
VALUE_CHAIN_DESCRIPTIONS = {
    "1. Exploration & Characterization": "Geological exploration, remote sensing, AI mineral mapping, spectroscopic characterization of deposits.",
    "2. Beneficiation & Extraction": "Crushing, froth flotation, magnetic separation, pyrometallurgical smelting, bio-leaching.",
    "3. Refining & High-Purity Chemical Processing": "Hydrometallurgy, solvent extraction, acid leaching, conversion to battery-grade lithium carbonate/hydroxide.",
    "4. Component & Precursor Manufacturing": "NMC/LFP cathode active materials, synthetic graphite anodes, sintered NdFeB permanent magnets.",
    "5. Recycling & Secondary Recovery": "Hydrometallurgical black mass recycling, direct cathode-to-cathode regeneration, spent catalyst recovery."
}
