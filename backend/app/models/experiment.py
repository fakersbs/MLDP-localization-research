"""Experiment model"""
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, JSON
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class Experiment(Base):
    """Experiment data model for storing colocalization results"""
    
    __tablename__ = "experiments"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sequence_id = Column(String, nullable=True)
    
    # Experiment details
    mutant_name = Column(String(255), nullable=False)
    mutation_type = Column(String(50), nullable=True)  # WT, Point mutation, etc.
    mutations = Column(Text, nullable=True)  # JSON list of mutations
    
    # Plasmid and expression
    plasmid = Column(String(255), nullable=True)  # e.g., pYES2
    fusion_tag = Column(String(255), nullable=True)  # e.g., eYFP
    expression_level = Column(Float, nullable=True)  # 0-100%
    
    # Colocalization results (from laser confocal microscopy)
    pearson_correlation = Column(Float, nullable=True)  # -1 to 1
    manders_coefficient = Column(Float, nullable=True)  # 0 to 1
    overlap_coefficient = Column(Float, nullable=True)  # 0 to 1
    
    # Imaging details
    imaging_date = Column(DateTime, nullable=True)
    microscope_type = Column(String(255), nullable=True)  # e.g., Laser confocal
    imaging_notes = Column(Text, nullable=True)
    
    # Additional data
    replicate_number = Column(Integer, nullable=True)
    experimental_group = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Experiment(id={self.id}, mutant={self.mutant_name})>"
