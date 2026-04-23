"""Sequence model"""
from sqlalchemy import Column, String, Text, DateTime, Float, Integer
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime


class Sequence(Base):
    """Protein sequence model for MLDP analysis"""
    
    __tablename__ = "sequences"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sequence = Column(Text, nullable=False)
    organism = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Helix prediction results
    helix_regions = Column(Text, nullable=True)  # JSON
    helix_score = Column(Float, nullable=True)
    helix_confidence = Column(Float, nullable=True)
    
    # Physical properties
    hydrophobic_residues = Column(Integer, nullable=True)
    hydrophilic_residues = Column(Integer, nullable=True)
    charge = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Sequence(id={self.id}, name={self.name})>"
