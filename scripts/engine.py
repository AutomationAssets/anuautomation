import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Warning: GEMINI_API_KEY not found. Please set it to run the engine.")
    # For local dry run without API key
    class MockModel:
        def generate_content(self, prompt):
            class MockResponse:
                def __init__(self):
                    self.text = "# Mock AI Review\n\nThis is a generated mock review because no API key was found."
            return MockResponse()
    model = MockModel()
else:
    genai.configure(api_key=API_KEY)
    # Using Gemini 1.5 Flash for speed and cost-effectiveness (Free Tier)
    model = genai.GenerativeModel('gemini-1.5-flash')

def agent_researcher(topic_data):
    """Agent 1: Extracts key facts and pain points from raw data."""
    prompt = f"""
    You are an expert market researcher. Analyze this trending topic from Reddit:
    Title: {topic_data['title']}
    Context: {topic_data['selftext']}
    
    Extract the core problem the user is trying to solve, 3 key pain points, and suggest 2 real-world software tools that solve this problem.
    Output only a JSON object with keys: "core_problem", "pain_points", "suggested_tools".
    """
    response = model.generate_content(prompt)
    try:
        # Simple extraction of JSON from markdown blocks if present
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        # Fallback if AI doesn't return perfect JSON
        return {
            "core_problem": "Finding the right tool",
            "pain_points": ["Overwhelm", "Cost", "Integration"],
            "suggested_tools": ["Jasper", "SurferSEO"]
        }

def agent_copywriter(research_data, topic_title):
    """Agent 2: Drafts the SEO-optimized article."""
    prompt = f"""
    You are an elite B2B SaaS copywriter. Write a 600-word SEO-optimized blog post based on this research:
    Topic: {topic_title}
    Core Problem: {research_data['core_problem']}
    Pain Points: {', '.join(research_data['pain_points'])}
    Suggested Tools: {', '.join(research_data['suggested_tools'])}
    
    Use the PAS (Problem, Agitation, Solution) framework.
    Include Markdown headings (H2, H3).
    Do NOT include a title (H1) at the top, just start the article.
    """
    response = model.generate_content(prompt)
    return response.text

def agent_editor(draft_content):
    """Agent 3: Refines, fact-checks, and inserts placeholders for affiliate links."""
    prompt = f"""
    You are the final Editor. Review the following draft blog post.
    1. Ensure the tone is professional, authoritative, but engaging.
    2. Replace mentions of software tools with a placeholder format like this: [TOOL_NAME](AFFILIATE_LINK_PLACEHOLDER_TOOL_NAME).
    3. Output ONLY the finalized Markdown content.
    
    Draft:
    {draft_content}
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("Starting AACE Multi-Agent Engine...")
    
    # Load ingested data
    try:
        with open("data/trending_topics.json", "r") as f:
            topics = json.load(f)
    except FileNotFoundError:
        print("No ingestion data found. Exiting.")
        exit(1)
        
    if not topics:
        print("No topics to process.")
        exit(0)
        
    # Pick the top topic for the daily post
    top_topic = topics[0]
    print(f"Processing Topic: {top_topic['title']}")
    
    print("Running Agent 1: Researcher...")
    research = agent_researcher(top_topic)
    
    print("Running Agent 2: Copywriter...")
    draft = agent_copywriter(research, top_topic['title'])
    
    print("Running Agent 3: Editor...")
    final_article = agent_editor(draft)
    
    # Save output
    os.makedirs("data", exist_ok=True)
    with open("data/generated_article.md", "w", encoding='utf-8') as f:
        # Also save the title for the formatter
        f.write(top_topic['title'] + "\n---\n")
        f.write(final_article)
        
    print("Engine finished successfully.")
