# AI-Agent Newsletter CLI

This project fetches the latest AI-agent news, top papers, and trending GitHub repositories, summarizes user reactions using OpenAI, and emails a polished newsletter.

## Prerequisites

* **Python** 3.10 or newer
* **pip** package manager

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/sameedhayat/Newsletter.git
   cd Newsletter
   ```
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate    # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the project root and populate with the following keys:

```dotenv
# SMTP (Email Delivery)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_smtp_username
SMTP_PASS=your_smtp_password
EMAIL_SENDER=sender@example.com
EMAIL_RECIPIENT=recipient@example.com

# OpenAI (LLM Summaries)
OPENAI_API_KEY=your_openai_api_key

# News API (Technology News)
NEWS_API_KEY=your_newsapi_key

# Semantic Scholar (Paper citation counts)
S2_API_KEY=your_semanticscholar_key

# GitHub (Trending repos)
GITHUB_TOKEN=your_github_token

# Twikit (Twitter fetch) – Optional
TWIKIT_USERNAME=your_twikit_username
TWIKIT_EMAIL=your_email@example.com
TWIKIT_PASSWORD=your_twikit_password
```

> **Note:** If you skip the Twitter integration, omit the `TWIKIT_*` variables and remove or disable the `twitter` tool.

## Directory Structure

```
├── server.py           # FastMCP server exposing tools
├── data_fetcher.py     # Fetch raw data from MCP tools
├── llm_processor.py    # OpenAI-based processing (summaries, keywords)
├── renderer.py         # Jinja2 renderer for Markdown & HTML
├── email_sender.py     # SMTP email delivery
├── main.py             # Orchestrator: fetch → process → render → send
├── templates/          # Jinja2 templates for newsletter
│   ├── newsletter.md.j2
│   └── newsletter.html.j2
├── newsletter_data.json # Cached data (generated)
└── requirements.txt    # Python dependencies
```

## Usage

Simply run the orchestrator:

```bash
python main.py "ai agent"
```

* The optional CLI argument (`"ai agent"`) is used for Twitter keyword extraction if Twitter integration is enabled.
* This will:

  1. Spin up the FastMCP server (`server.py`) in the background
  2. Fetch news, papers, and GitHub data
  3. Use OpenAI to generate summary and tweet reactions
  4. Render Markdown & HTML via Jinja2 templates
  5. Send the email via SMTP

You should see a confirmation:

```
Newsletter sent to recipient@example.com
```

## Customization

* **Templates:** Edit `templates/newsletter.md.j2` or `templates/newsletter.html.j2` to change formatting.
* **Pipeline logic:** Modify `llm_processor.py` for custom prompts or additional LLM steps.
* **Tools:** Extend or customize MCP tools in `tools/` and restart the server.

## License

MIT © Sameed Hayat
