"""Sequence schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SequenceCreate(BaseModel):
    """Schema for creating a new sequence"""
    name: str
    sequence: str
    organism: Optional[str] = None
    description: Optional[str] = None


class SequenceResponse(BaseModel):
    """Schema for sequence response"""
    id: str
    name: str
    sequence: str
    organism: Optional[str]
    description: Optional[str]
    helix_score: Optional[float]
    helix_confidence: Optional[float]
    hydrophobic_residues: Optional[int]
    hydrophilic_residues: Optional[int]
    charge: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
