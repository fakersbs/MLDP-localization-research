"""Mutation design API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List

from app.database import get_db
from app.models.mutation import Mutation
from app.schemas.mutation import MutationCreate, MutationResponse
from app.services.mutation_analysis import predict_mutations, analyze_mutation_effect

router = APIRouter(
    prefix="/api/mutations",
    tags=["mutations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict", response_model=List[MutationResponse])
async def predict_mutations_endpoint(
    sequence: str,
    helix_start: int,
    helix_end: int,
    db: Session = Depends(get_db)
):
    """
    Predict mutations to disrupt the hydrophobic face of an amphipathic helix.
    
    This endpoint:
    - Identifies hydrophobic residues in the helix
    - Proposes L→K, I→K, V→K mutations
    - Predicts structural impact
    - Returns ranked mutation suggestions
    """
    try:
        # Predict mutations
        mutation_predictions = predict_mutations(
            sequence=sequence.upper(),
            helix_start=helix_start,
            helix_end=helix_end
        )
        
        # Save to database
        saved_mutations = []
        for pred in mutation_predictions:
            mutation = Mutation(
                id=str(uuid4()),
                mutation_name=pred["name"],
                wild_type_residue=pred["wt"],
                mutant_residue=pred["mut"],
                position=pred["position"],
                helix_start=helix_start,
                helix_end=helix_end,
                in_hydrophobic_face=pred["in_hydrophobic_face"],
                hydrophobicity_change=pred["hydrophobicity_change"],
                charge_change=pred["charge_change"],
                structure_stability_score=pred["stability_score"],
                predicted_effect=pred["effect"],
                rationale=pred["rationale"],
                design_strategy="Disrupting hydrophobic face"
            )
            db.add(mutation)
            saved_mutations.append(mutation)
        
        db.commit()
        for m in saved_mutations:
            db.refresh(m)
        
        return saved_mutations
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting mutations: {str(e)}"
        )


@router.get("/{mutation_id}", response_model=MutationResponse)
async def get_mutation(
    mutation_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a stored mutation design result.
    """
    mutation = db.query(Mutation).filter(Mutation.id == mutation_id).first()
    if not mutation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mutation not found"
        )
    return mutation


@router.get("/", response_model=List[MutationResponse])
async def list_mutations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all stored mutation designs.
    """
    mutations = db.query(Mutation).offset(skip).limit(limit).all()
    return mutations
