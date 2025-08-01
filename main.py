import asyncio
from data_fetcher import DataFetcher
from llm_processor import LLMProcessor
from renderer import Renderer
from email_sender import EmailSender
from datetime import datetime
import os
import json
import os

def load_json(path: str) -> dict:
    """
    Load and return the JSON content from `path`.
    Raises FileNotFoundError if the file doesn't exist,
    or json.JSONDecodeError if the contents aren't valid JSON.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data



async def main(keyword: str = "ai agent"):
    
    fetcher = DataFetcher("mcp_server.py")
    raw = await fetcher.fetch(keyword)
    fetcher.save(raw)

    path = "output/newsletter_data.json"
    raw = load_json(path)
    
    processor = LLMProcessor()
    # enrich articles with keywords and tweet summaries as needed...
    overview = processor.summarize_overview(raw)
    raw_summarized_tweets = processor.summarize_tweets(raw)
    
    renderer = Renderer()
    markdown = renderer.render_markdown(raw_summarized_tweets, overview)
    html = renderer.render_html(raw_summarized_tweets, overview)
    
    sender = EmailSender()
    sender.send("Weekly AI-Agent Newsletter", markdown, html)

if __name__ == "__main__":
    import sys
    kw = sys.argv[1] if len(sys.argv)>1 else "ai agent"
    asyncio.run(main(kw))