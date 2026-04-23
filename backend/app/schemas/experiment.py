"""Experiment schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExperimentCreate(BaseModel):
    """Schema for creating a new experiment"""
    name: str
    mutant_name: str
    mutation_type: Optional[str] = None
    mutations: Optional[str] = None
    plasmid: Optional[str] = None
    fusion_tag: Optional[str] = None
    expression_level: Optional[float] = None
    pearson_correlation: Optional[float] = None
    manders_coefficient: Optional[float] = None
    overlap_coefficient: Optional[float] = None
    replicate_number: Optional[int] = None
    experimental_group: Optional[str] = None
    notes: Optional[str] = None


class ExperimentResponse(BaseModel):
    """Schema for experiment response"""
    id: str
    name: str
    mutant_name: str
    mutation_type: Optional[str]
    plasmid: Optional[str]
    fusion_tag: Optional[str]
    expression_level: Optional[float]
    pearson_correlation: Optional[float]
    manders_coefficient: Optional[float]
    overlap_coefficient: Optional[float]
    replicate_number: Optional[int]
    experimental_group: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
