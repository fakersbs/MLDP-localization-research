"""Mutation schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MutationCreate(BaseModel):
    """Schema for creating a new mutation"""
    mutation_name: str
    wild_type_residue: str
    mutant_residue: str
    position: int
    helix_start: Optional[int] = None
    helix_end: Optional[int] = None
    in_hydrophobic_face: Optional[str] = None
    rationale: Optional[str] = None
    design_strategy: Optional[str] = None


class MutationResponse(BaseModel):
    """Schema for mutation response"""
    id: str
    mutation_name: str
    wild_type_residue: str
    mutant_residue: str
    position: int
    helix_start: Optional[int]
    helix_end: Optional[int]
    in_hydrophobic_face: Optional[str]
    hydrophobicity_change: Optional[float]
    charge_change: Optional[float]
    structure_stability_score: Optional[float]
    predicted_effect: Optional[str]
    rationale: Optional[str]
    design_strategy: Optional[str]
    status: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
