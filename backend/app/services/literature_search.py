"""Literature search service"""
from typing import List, Dict, Optional
import requests
from app.config import settings


def search_pubmed(
    query: str,
    keywords: Optional[List[str]] = None,
    max_results: int = 10
) -> Dict:
    """
    Search PubMed for relevant literature.
    """
    # Build search query
    search_terms = [query]
    if keywords:
        search_terms.extend(keywords)
    
    full_query = " AND ".join(search_terms)
    
    # PubMed API endpoints
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        "db": "pubmed",
        "term": full_query,
        "retmax": max_results,
        "rettype": "json",
        "tool": "MLDP-Research-Assistant",
        "email": settings.pubmed_email or "research@example.com"
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        pmids = data.get("esearchresult", {}).get("idlist", [])
        
        if pmids:
            # Fetch summaries
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(pmids),
                "rettype": "json",
                "tool": "MLDP-Research-Assistant",
                "email": settings.pubmed_email or "research@example.com"
            }
            
            fetch_response = requests.get(fetch_url, params=fetch_params)
            fetch_response.raise_for_status()
            fetch_data = fetch_response.json()
            
            results = []
            for uid, article in fetch_data.get("result", {}).items():
                if uid != "uids":
                    results.append({
                        "pmid": uid,
                        "title": article.get("title", ""),
                        "authors": [a.get("name", "") for a in article.get("authors", [])],
                        "source": article.get("source", ""),
                        "pubdate": article.get("pubdate", ""),
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
                    })
            
            return {
                "query": full_query,
                "total_results": len(pmids),
                "results": results
            }
        
        return {
            "query": full_query,
            "total_results": 0,
            "results": []
        }
    
    except Exception as e:
        return {
            "query": full_query,
            "error": str(e),
            "results": []
        }


def get_paper_summary(pmid: str) -> Dict:
    """
    Get paper abstract and AI-generated summary.
    """
    try:
        # Fetch paper details
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        params = {
            "db": "pubmed",
            "id": pmid,
            "rettype": "json",
            "tool": "MLDP-Research-Assistant",
            "email": settings.pubmed_email or "research@example.com"
        }
        
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        article = data.get("result", {}).get(pmid, {})
        
        # Note: Full abstract would require fetching from PMID directly
        # This is a placeholder for actual abstract retrieval
        
        return {
            "pmid": pmid,
            "title": article.get("title", ""),
            "authors": [a.get("name", "") for a in article.get("authors", [])],
            "abstract": "[Abstract text would go here]",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        }
    
    except Exception as e:
        return {
            "pmid": pmid,
            "error": str(e)
        }
