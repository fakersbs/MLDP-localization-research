"""Experiment data management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List

from app.database import get_db
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentResponse

router = APIRouter(
    prefix="/api/experiments",
    tags=["experiments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/record", response_model=ExperimentResponse)
async def record_experiment(
    experiment_data: ExperimentCreate,
    db: Session = Depends(get_db)
):
    """
    Record a new experiment with colocalization results.
    
    This endpoint stores:
    - Mutant identity and mutation type
    - Plasmid (pYES2) and fusion tag (eYFP)
    - Colocalization metrics from laser confocal microscopy:
      - Pearson correlation coefficient (-1 to 1)
      - Manders overlap coefficient (0 to 1)
    - Expression levels and experimental metadata
    """
    try:
        # Validate colocalization values
        if experiment_data.pearson_correlation is not None:
            if not -1 <= experiment_data.pearson_correlation <= 1:
                raise ValueError("Pearson correlation must be between -1 and 1")
        
        if experiment_data.manders_coefficient is not None:
            if not 0 <= experiment_data.manders_coefficient <= 1:
                raise ValueError("Manders coefficient must be between 0 and 1")
        
        # Create experiment record
        db_experiment = Experiment(
            id=str(uuid4()),
            name=experiment_data.name,
            mutant_name=experiment_data.mutant_name,
            mutation_type=experiment_data.mutation_type,
            mutations=experiment_data.mutations,
            plasmid=experiment_data.plasmid,
            fusion_tag=experiment_data.fusion_tag,
            expression_level=experiment_data.expression_level,
            pearson_correlation=experiment_data.pearson_correlation,
            manders_coefficient=experiment_data.manders_coefficient,
            overlap_coefficient=experiment_data.overlap_coefficient,
            replicate_number=experiment_data.replicate_number,
            experimental_group=experiment_data.experimental_group,
            notes=experiment_data.notes
        )
        
        db.add(db_experiment)
        db.commit()
        db.refresh(db_experiment)
        
        return db_experiment
    
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error recording experiment: {str(e)}"
        )


@router.get("/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    experiment_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a stored experiment result.
    """
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    return experiment


@router.get("/", response_model=List[ExperimentResponse])
async def list_experiments(
    skip: int = 0,
    limit: int = 100,
    mutant_name: str = None,
    db: Session = Depends(get_db)
):
    """
    List all stored experiments. Optionally filter by mutant name.
    """
    query = db.query(Experiment)
    if mutant_name:
        query = query.filter(Experiment.mutant_name.ilike(f"%{mutant_name}%"))
    
    experiments = query.offset(skip).limit(limit).all()
    return experiments


@router.get("/compare/wt-vs-mutants")
async def compare_wt_vs_mutants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Compare wild-type and mutant colocalization results.
    """
    try:
        wt_results = db.query(Experiment).filter(
            Experiment.mutation_type == "WT"
        ).all()
        
        mutant_results = db.query(Experiment).filter(
            Experiment.mutation_type != "WT"
        ).offset(skip).limit(limit).all()
        
        return {
            "wild_type": wt_results,
            "mutants": mutant_results,
            "comparison": {
                "wt_avg_pearson": sum([e.pearson_correlation or 0 for e in wt_results]) / len(wt_results) if wt_results else None,
                "mutant_avg_pearson": sum([e.pearson_correlation or 0 for e in mutant_results]) / len(mutant_results) if mutant_results else None
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error comparing results: {str(e)}"
        )
