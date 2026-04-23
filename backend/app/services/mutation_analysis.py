"""Mutation design and analysis service"""
from typing import List, Dict
from app.services.helix_prediction import HYDROPHOBIC, HYDROPHILIC, CHARGE_SCALE, HYDROPHOBICITY_SCALE

# Conversion cost matrix
AA_PROPERTIES = {
    'L': {'hydro': 3.8, 'charge': 0, 'type': 'hydrophobic'},
    'I': {'hydro': 4.5, 'charge': 0, 'type': 'hydrophobic'},
    'V': {'hydro': 4.2, 'charge': 0, 'type': 'hydrophobic'},
    'M': {'hydro': 1.9, 'charge': 0, 'type': 'hydrophobic'},
    'F': {'hydro': 2.8, 'charge': 0, 'type': 'hydrophobic'},
    'W': {'hydro': -0.9, 'charge': 0, 'type': 'hydrophobic'},
    'P': {'hydro': -1.6, 'charge': 0, 'type': 'hydrophobic'},
    'A': {'hydro': 1.8, 'charge': 0, 'type': 'hydrophobic'},
    'K': {'hydro': -3.9, 'charge': 1.0, 'type': 'positive'},
    'R': {'hydro': -4.5, 'charge': 1.0, 'type': 'positive'},
    'D': {'hydro': -3.5, 'charge': -1.0, 'type': 'negative'},
    'E': {'hydro': -3.5, 'charge': -1.0, 'type': 'negative'},
    'N': {'hydro': -3.5, 'charge': 0, 'type': 'polar'},
    'Q': {'hydro': -3.5, 'charge': 0, 'type': 'polar'},
    'S': {'hydro': -0.8, 'charge': 0, 'type': 'polar'},
    'T': {'hydro': -0.7, 'charge': 0, 'type': 'polar'},
    'C': {'hydro': 2.5, 'charge': 0, 'type': 'cysteine'},
    'G': {'hydro': -0.4, 'charge': 0, 'type': 'glycine'},
    'H': {'hydro': -3.2, 'charge': 0.5, 'type': 'positive'},
    'Y': {'hydro': -1.3, 'charge': 0, 'type': 'aromatic'},
}


def predict_mutations(
    sequence: str,
    helix_start: int,
    helix_end: int,
    target_residues: str = "LIV"
) -> List[Dict]:
    """
    Predict mutations to disrupt the hydrophobic face of an amphipathic helix.
    
    Strategy: Replace hydrophobic residues (L, I, V) with charged residues (K)
    to disrupt the amphipathic nature.
    """
    mutations = []
    helix_seq = sequence[helix_start:helix_end]
    
    for pos, aa in enumerate(helix_seq):
        if aa in target_residues:
            # Position in full sequence
            full_pos = helix_start + pos
            
            # Propose L→K, I→K, V→K mutations
            for target_aa in ['K', 'R', 'E']:
                if aa != target_aa:
                    wt_props = AA_PROPERTIES.get(aa, {})
                    mut_props = AA_PROPERTIES.get(target_aa, {})
                    
                    hydro_change = wt_props.get('hydro', 0) - mut_props.get('hydro', 0)
                    charge_change = mut_props.get('charge', 0) - wt_props.get('charge', 0)
                    
                    # Stability score based on property changes
                    stability = calculate_stability_score(hydro_change, charge_change)
                    
                    # Effect prediction
                    if hydro_change > 5:
                        effect = "high"
                    elif hydro_change > 2:
                        effect = "medium"
                    else:
                        effect = "low"
                    
                    mutation = {
                        "name": f"{aa}{full_pos+1}{target_aa}",
                        "wt": aa,
                        "mut": target_aa,
                        "position": full_pos + 1,  # 1-indexed
                        "in_hydrophobic_face": "yes",
                        "hydrophobicity_change": round(hydro_change, 3),
                        "charge_change": round(charge_change, 3),
                        "stability_score": round(stability, 3),
                        "effect": effect,
                        "rationale": f"Replace hydrophobic {aa} with charged {target_aa} to disrupt amphipathic helix"
                    }
                    mutations.append(mutation)
    
    # Sort by stability score (best first)
    mutations = sorted(mutations, key=lambda x: x['stability_score'], reverse=True)
    return mutations[:10]  # Return top 10


def calculate_stability_score(hydro_change: float, charge_change: float) -> float:
    """
    Calculate structural stability score for a mutation.
    
    Higher score = more likely to disrupt localization
    """
    # Weighted combination
    # Hydrophobicity change is more important (80%)
    # Charge change helps (20%)
    score = (hydro_change * 0.8 + abs(charge_change) * 0.2) / 10
    return max(0, min(1, score))  # Clamp to 0-1


def analyze_mutation_effect(
    wild_type_seq: str,
    mutant_seq: str
) -> Dict:
    """
    Analyze the predicted effect of a mutation on protein properties.
    """
    wt_hydro = sum(AA_PROPERTIES.get(aa, {}).get('hydro', 0) for aa in wild_type_seq)
    mut_hydro = sum(AA_PROPERTIES.get(aa, {}).get('hydro', 0) for aa in mutant_seq)
    
    wt_charge = sum(AA_PROPERTIES.get(aa, {}).get('charge', 0) for aa in wild_type_seq)
    mut_charge = sum(AA_PROPERTIES.get(aa, {}).get('charge', 0) for aa in mutant_seq)
    
    return {
        "wt_hydrophobicity": round(wt_hydro, 3),
        "mutant_hydrophobicity": round(mut_hydro, 3),
        "hydrophobicity_change": round(mut_hydro - wt_hydro, 3),
        "wt_charge": round(wt_charge, 3),
        "mutant_charge": round(mut_charge, 3),
        "charge_change": round(mut_charge - wt_charge, 3)
    }
