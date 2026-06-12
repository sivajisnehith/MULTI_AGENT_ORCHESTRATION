# tools/search.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from config import MAX_WEB_RESULTS

# basic = returns one string
basic_search = DuckDuckGoSearchRun()

# advanced = returns list of dicts with title, url, snippet
advanced_search = DuckDuckGoSearchAPIWrapper(
    max_results=5
)

def web_search(query: str) -> list:
    results = advanced_search.results(query, 5)
    
    formatted = []
    for r in results:
        formatted.append(
            f"Title: {r.get('title', 'Unknown')}\n"
            f"URL: {r.get('link', 'Unknown')}\n"  
            f"Content: {r.get('snippet', 'No content')}"
        )
    
    return formatted