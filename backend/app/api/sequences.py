"""Sequence analysis API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List

from app.database import get_db
from app.models.sequence import Sequence
from app.schemas.sequence import SequenceCreate, SequenceResponse
from app.services.helix_prediction import predict_helices, calculate_properties

router = APIRouter(
    prefix="/api/sequences",
    tags=["sequences"],
    responses={404: {"description": "Not found"}},
)


@router.post("/analyze", response_model=SequenceResponse)
async def analyze_sequence(
    sequence_data: SequenceCreate,
    db: Session = Depends(get_db)
):
    """
    Analyze a protein sequence for amphipathic helix prediction.
    
    This endpoint:
    - Predicts α-helical regions
    - Identifies hydrophobic and hydrophilic residues
    - Calculates charge distribution
    - Stores results in the database
    """
    try:
        # Validate sequence
        sequence_upper = sequence_data.sequence.upper()
        valid_chars = set("ACDEFGHIKLMNPQRSTVWY")
        if not all(c in valid_chars for c in sequence_upper):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid amino acid sequence"
            )
        
        # Predict helices
        helix_results = predict_helices(sequence_upper)
        
        # Calculate properties
        properties = calculate_properties(sequence_upper)
        
        # Create database record
        db_sequence = Sequence(
            id=str(uuid4()),
            name=sequence_data.name,
            sequence=sequence_upper,
            organism=sequence_data.organism,
            description=sequence_data.description,
            helix_regions=helix_results.get("regions_json"),
            helix_score=helix_results.get("score"),
            helix_confidence=helix_results.get("confidence"),
            hydrophobic_residues=properties.get("hydrophobic_count"),
            hydrophilic_residues=properties.get("hydrophilic_count"),
            charge=properties.get("charge")
        )
        
        db.add(db_sequence)
        db.commit()
        db.refresh(db_sequence)
        
        return db_sequence
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing sequence: {str(e)}"
        )


@router.get("/{sequence_id}", response_model=SequenceResponse)
async def get_sequence(
    sequence_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a stored sequence analysis result.
    """
    db_sequence = db.query(Sequence).filter(Sequence.id == sequence_id).first()
    if not db_sequence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sequence not found"
        )
    return db_sequence


@router.get("/", response_model=List[SequenceResponse])
async def list_sequences(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all stored sequences.
    """
    sequences = db.query(Sequence).offset(skip).limit(limit).all()
    return sequences
