"""Report generation API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.report_generator import generate_research_report

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def generate_report(
    title: str,
    experiment_ids: list,
    format: str = "pdf",
    db: Session = Depends(get_db)
):
    """
    Generate an automated research report.
    
    Supported formats:
    - pdf: PDF document
    - docx: Microsoft Word
    - html: HTML webpage
    - md: Markdown
    
    Report includes:
    - Abstract
    - Introduction
    - Methods
    - Results (with data visualization)
    - Discussion
    - Conclusions
    - References
    """
    try:
        if format not in ["pdf", "docx", "html", "md"]:
            raise ValueError(f"Unsupported format: {format}")
        
        report = generate_research_report(
            title=title,
            experiment_ids=experiment_ids,
            format=format,
            db=db
        )
        
        return report
    
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )
