import os, json
import asyncio
from fastmcp import Client

class DataFetcher:
    """
    Orchestrates fetching raw data from MCP tools.
    """
    def __init__(self, server_script: str):
        self.server = server_script

    async def fetch(self, keyword: str="ai agent") -> dict:
        async with Client(self.server) as client:
            articles = (await client.call_tool("newsapi", {})).data
            papers   = (await client.call_tool("papers", {})).data
            repos    = (await client.call_tool("github", {})).data

            for article in articles:
                title = article.get('title', '')
                desc  = article.get('description', '')
                
                # Fetch tweets using extracted topic
                tweets = []
                try:
                    tweets = (await client.call_tool("twitter", {"query": title})).data[:5]
                except Exception:
                    tweets = []
                lines = []
                for idx, tweet in enumerate(tweets):
                    text = tweet.get('text', '')
                    lines.append(f"tweet{idx}: {text}")
                tweets = '\n'.join(lines)
                #art['keyword'] = topic
                article['tweets'] = tweets
        return {"keyword": keyword, "articles": articles, "papers": papers, "repos": repos}

    def save(self, data: dict, path: str="output/newsletter_data.json"):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        