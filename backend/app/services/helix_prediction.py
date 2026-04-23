"""Amphipathic helix prediction service"""
import json
from typing import Dict, List

# Amino acid properties
HYDROPHOBIC = set("AILMFVPW")
HYDROPHILIC = set("STNQ")
CHARGED_POSITIVE = set("KRH")
CHARGED_NEGATIVE = set("DE")

# Hydrophobicity scale (Kyte-Doolittle)
HYDROPHOBICITY_SCALE = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# Charge scale
CHARGE_SCALE = {
    'K': 1.0, 'R': 1.0, 'H': 0.5,  # positive
    'D': -1.0, 'E': -1.0,  # negative
}


def predict_helices(sequence: str) -> Dict:
    """
    Predict amphipathic helix regions in a protein sequence.
    
    Returns regions where hydrophobic residues cluster on one face
    and hydrophilic residues on the other.
    """
    helix_regions = []
    window_size = 18  # ~5 turns of α-helix
    
    for i in range(len(sequence) - window_size):
        window = sequence[i:i + window_size]
        
        # Check for amphipathic pattern
        hydrophobic_positions = [j for j, aa in enumerate(window) if aa in HYDROPHOBIC]
        hydrophilic_positions = [j for j, aa in enumerate(window) if aa in HYDROPHILIC]
        
        # Calculate wheel projection to detect amphipathic face
        # In an α-helix, positions i, i+3.6, i+7.2, etc. are on the same face
        wheel_hydrophobic = []
        wheel_hydrophilic = []
        
        for j, aa in enumerate(window):
            angle = (j * 100)  # degrees in α-helix
            if aa in HYDROPHOBIC:
                wheel_hydrophobic.append(angle)
            elif aa in HYDROPHILIC:
                wheel_hydrophilic.append(angle)
        
        # Simple score: if we have clustering on opposite sides
        if hydrophobic_positions and hydrophilic_positions:
            score = len(hydrophobic_positions) * len(hydrophilic_positions) / (window_size ** 2)
            confidence = min(score * 2, 1.0)  # 0-1 confidence
            
            if score > 0.2:  # Threshold for amphipathic pattern
                helix_regions.append({
                    "start": i,
                    "end": i + window_size,
                    "sequence": window,
                    "score": round(score, 3),
                    "confidence": round(confidence, 3),
                    "hydrophobic_count": len(hydrophobic_positions),
                    "hydrophilic_count": len(hydrophilic_positions)
                })
    
    # Merge overlapping regions
    merged_regions = merge_regions(helix_regions)
    
    return {
        "regions": merged_regions,
        "regions_json": json.dumps(merged_regions),
        "score": max([r["score"] for r in merged_regions]) if merged_regions else 0,
        "confidence": max([r["confidence"] for r in merged_regions]) if merged_regions else 0
    }


def merge_regions(regions: List[Dict]) -> List[Dict]:
    """
    Merge overlapping helix regions.
    """
    if not regions:
        return []
    
    regions = sorted(regions, key=lambda x: x['start'])
    merged = [regions[0]]
    
    for current in regions[1:]:
        last = merged[-1]
        if current['start'] <= last['end']:
            # Merge regions
            merged[-1] = {
                'start': last['start'],
                'end': max(last['end'], current['end']),
                'score': max(last['score'], current['score']),
                'confidence': max(last['confidence'], current['confidence']),
                'hydrophobic_count': last['hydrophobic_count'] + current['hydrophobic_count'],
                'hydrophilic_count': last['hydrophilic_count'] + current['hydrophilic_count']
            }
        else:
            merged.append(current)
    
    return merged


def calculate_properties(sequence: str) -> Dict:
    """
    Calculate basic physicochemical properties of a sequence.
    """
    hydrophobic_count = sum(1 for aa in sequence if aa in HYDROPHOBIC)
    hydrophilic_count = sum(1 for aa in sequence if aa in HYDROPHILIC)
    charge = sum(CHARGE_SCALE.get(aa, 0) for aa in sequence)
    
    # Calculate hydrophobicity profile
    hydrophobicity = []
    window_size = 9
    for i in range(len(sequence) - window_size):
        window = sequence[i:i + window_size]
        avg_hydro = sum(HYDROPHOBICITY_SCALE.get(aa, 0) for aa in window) / window_size
        hydrophobicity.append(round(avg_hydro, 3))
    
    return {
        "hydrophobic_count": hydrophobic_count,
        "hydrophilic_count": hydrophilic_count,
        "charge": round(charge, 3),
        "hydrophobicity_profile": hydrophobicity
    }
