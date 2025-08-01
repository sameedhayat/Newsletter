import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
class LLMProcessor:
    """
    Performs all LLM-based processing: summaries, keyword extraction.
    """
    def __init__(self):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = key

    def summarize_overview(self, data: dict) -> str:
        prompt = f"Generate a concise weekly newsletter summary (2-3 sentences) based on the data:\n{json.dumps(data)}"
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()

    def extract_keyword(self, title: str, desc: str) -> str:
        prompt = f"Extract 1-3 word keyword from title and description.\nTitle: {title}\nDesc: {desc}\nKeyword:"""
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0
        )
        return resp.choices[0].message.content.strip().strip('"')

    def summarize_tweets(self, texts: list[str]) -> str:
        data = texts.copy()
        
        for i, txt in enumerate(data["articles"]):
            
            if txt["tweets"]:
                prompt = f'Summarize these tweets into one sentence, telling what people are saying about it and whats the opinion:\n{txt["tweets"]}'
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.5
                )
                data["articles"][i]["tweet_summary"] = resp.choices[0].message.content.strip()
            else:
                data["articles"][i]["tweet_summary"] = ""
        return data
        