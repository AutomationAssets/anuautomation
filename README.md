# Apex Autonomous Content Engine (AACE)

This repository contains the automation scripts and static site configuration for a zero-cost, fully automated content arbitrage and affiliate marketing system.

## How It Works

1. **GitHub Actions**: Wakes up daily at 12:00 PM UTC (`.github/workflows/main.yml`).
2. **Ingestion (`scripts/ingestion.py`)**: Scrapes Reddit trending topics to find high-intent questions in the B2B SaaS niche.
3. **Engine (`scripts/engine.py`)**: Runs a 3-agent pipeline via Google Gemini API:
   - **Researcher**: Extracts facts and identifies solutions.
   - **Copywriter**: Drafts an SEO-optimized article.
   - **Editor**: Refines the draft and inserts affiliate link placeholders.
4. **Formatter (`scripts/formatter.py`)**: Replaces placeholders with actual affiliate links and generates Hugo markdown with metadata.
5. **Deployment**: GitHub Actions commits the new Markdown file, builds the Hugo site, and deploys it to GitHub Pages.

## Setup Instructions

To activate this system, you must configure the following repository secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

1. `GEMINI_API_KEY`: Get this for free from [Google AI Studio](https://aistudio.google.com/).
2. `REDDIT_CLIENT_ID`: Create an app at [Reddit Prefs](https://www.reddit.com/prefs/apps).
3. `REDDIT_CLIENT_SECRET`: From your Reddit app.
4. `GITHUB_TOKEN`: This is provided automatically by GitHub Actions, but ensure that your workflow permissions allow reading and writing to the repository (`Settings > Actions > General > Workflow permissions`).

### Affiliate Links Configuration
Update the `AFFILIATE_LINKS` dictionary in `scripts/formatter.py` with your actual affiliate tracking URLs.

## Local Testing
1. Install dependencies: `pip install -r scripts/requirements.txt`
2. Run ingestion: `python scripts/ingestion.py`
3. Run engine: `python scripts/engine.py`
4. Run formatter: `python scripts/formatter.py`
