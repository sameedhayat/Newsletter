from fastmcp import FastMCP
import os
import requests
from datetime import datetime, timedelta
import asyncio
from twikit import Client
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()

# Create a shared FastMCP server instance
mcp = FastMCP(name="Weekly Newsletter")

@mcp.tool
def github()  -> list:
    """Fetch top GitHub repos tagged or described as 'ai agent' from the past week."""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    date_range = f"{week_ago}..{today}"
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f'(topic:ai-agent OR "agent" in:name,description) created:{date_range}',
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    items = r.json().get("items", [])
    
    return [
        {
            "name": repo.get("full_name"),
            "description": repo.get("description"),
            "stars": repo.get("stargazers_count", 0),
            "url": repo.get("html_url"),
        }
        for repo in items
    ]

@mcp.tool
def newsapi() -> list:
    """Fetch top news articles mentioning 'ai agent' from the past week via News API."""
    API_KEY = os.getenv("NEWS_API_KEY")
    
    if not API_KEY:
        raise RuntimeError("Environment variable NEWS_API_KEY not set")

    week_ago = (datetime.utcnow() - timedelta(days=7)).date().isoformat()
    params = {
        "qInTitle": "(agent OR agentic \"agent-based\" OR \"LLM agent\")",
        "from": week_ago,
        "sortBy": "popularity",
        "pageSize": 10,
        "apiKey": API_KEY,
        "language": "en",
    }

    resp = requests.get("https://newsapi.org/v2/everything", params=params)
    resp.raise_for_status()
    articles = resp.json().get("articles", [])

    return [
        {
            "title": art.get("title"),
            "description": art.get("description"),
            "source": art.get("source", {}).get("name"),
            "publishedAt": art.get("publishedAt"),
            "url": art.get("url"),
        }
        for art in articles if art.get("description")
    ]

import time
@mcp.tool
def papers()  -> list:
    """Fetch top cited AI agent papers (Semantic Scholar) from the past week."""
    API_KEY = os.getenv("S2_API_KEY")
    headers = {"x-api-key": API_KEY} if API_KEY else {}

    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    date_range = f"{week_ago}:{today}"
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": "ai agent",
        "limit": 10,
        "fields": "title,authors,year,citationCount,url",
        "sort": "citationCount",
        "publicationDateRange": date_range,
    }

    for _ in range(5):
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            break
        time.sleep(1.5)
    else:
        raise RuntimeError("Semantic Scholar API failed after retries.")

    data = r.json().get("data", [])
    return [
        {
            "title": p.get("title"),
            "year": p.get("year"),
            "citations": p.get("citationCount", 0),
            "url": p.get("url"),
        }
        for p in data
    ]

from twikit import Client

@mcp.tool
async def twitter(query: str) -> list:
    """Fetch top tweets for a given query from the past week using Twikit."""
    # Load Twikit credentials
    USERNAME = os.getenv("TWIKIT_USERNAME")
    EMAIL = os.getenv("TWIKIT_EMAIL")
    PASSWORD = os.getenv("TWIKIT_PASSWORD")
    if not (USERNAME and EMAIL and PASSWORD):
        raise RuntimeError("TWIKIT_USERNAME, TWIKIT_EMAIL, and TWIKIT_PASSWORD must be set in the environment")

    # Initialize and login
    client = Client('en-US')
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

    # Search latest tweets for the query
    try:
        tweets = await client.search_tweet(query, 'Top')  # returns list
        tweets = tweets[:10]  # limit to first 50
    except:
        tweets = []
        
    

    
    # Format results
    result = []
    for t in tweets:
        result.append({
            'user': t.user.name,
            'text': t.text,
            'date': t.created_at.isoformat() if hasattr(t, 'date') else None,
        })
    return result

if __name__ == "__main__":
    mcp.run()