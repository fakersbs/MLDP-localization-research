"""Literature search API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.services.literature_search import search_pubmed, get_paper_summary

router = APIRouter(
    prefix="/api/literature",
    tags=["literature"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search")
async def search_literature(
    query: str,
    keywords: Optional[List[str]] = None,
    max_results: int = 10
):
    """
    Search PubMed for relevant literature.
    
    Keywords suggestions for MLDP research:
    - lipid droplet proteins
    - amphipathic helix
    - protein targeting
    - yeast expression
    - heterologous expression
    """
    try:
        results = search_pubmed(
            query=query,
            keywords=keywords,
            max_results=max_results
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching literature: {str(e)}"
        )


@router.get("/summary/{pmid}")
async def get_paper_abstract(
    pmid: str
):
    """
    Get paper summary using OpenAI for intelligent summarization.
    """
    try:
        summary = get_paper_summary(pmid=pmid)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting paper summary: {str(e)}"
        )
