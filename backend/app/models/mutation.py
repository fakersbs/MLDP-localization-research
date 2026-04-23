"""Mutation model"""
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, JSON
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class Mutation(Base):
    """Mutation design and prediction model"""
    
    __tablename__ = "mutations"
    
    id = Column(String, primary_key=True, index=True)
    sequence_id = Column(String, nullable=True)
    
    # Mutation information
    mutation_name = Column(String(255), nullable=False)
    wild_type_residue = Column(String(10), nullable=False)  # e.g., "L"
    mutant_residue = Column(String(10), nullable=False)  # e.g., "K"
    position = Column(Integer, nullable=False)
    
    # Targeting information
    helix_start = Column(Integer, nullable=True)
    helix_end = Column(Integer, nullable=True)
    in_hydrophobic_face = Column(String(50), nullable=True)  # yes/no/maybe
    
    # Effect prediction
    hydrophobicity_change = Column(Float, nullable=True)
    charge_change = Column(Float, nullable=True)
    structure_stability_score = Column(Float, nullable=True)  # 0-1
    predicted_effect = Column(String(50), nullable=True)  # high/medium/low
    
    # Design rationale
    rationale = Column(Text, nullable=True)
    design_strategy = Column(String(255), nullable=True)
    
    # Experimental status
    status = Column(String(50), nullable=True)  # designed/cloned/expressed/analyzed
    experiment_id = Column(String, nullable=True)
    
    # Results
    expression_result = Column(String(255), nullable=True)
    localization_result = Column(String(255), nullable=True)
    conclusions = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Mutation(id={self.id}, name={self.mutation_name})>"
