import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configure new Gemini API SDK
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Warning: GEMINI_API_KEY not found. Please set it to run the engine.")
    # For local dry run without API key
    class MockModel:
        def generate_content(self, model, contents):
            class MockResponse:
                def __init__(self):
                    self.text = "# Mock AI Review\n\nThis is a generated mock review because no API key was found."
            return MockResponse()
    client = MockModel()
else:
    client = genai.Client(api_key=API_KEY)

# Use a more stable, highly-available model
MODEL_ID = 'gemini-2.0-flash'

def agent_researcher(topic_data):
    """Agent 1: Extracts key facts and pain points from raw data."""
    prompt = f"""
    You are an expert market researcher. Analyze this trending topic:
    Title: {topic_data['title']}
    Context: {topic_data['selftext']}
    
    Extract the core problem the user is trying to solve, 3 key pain points, and suggest 2 real-world software tools that solve this problem.
    Output only a JSON object with keys: "core_problem", "pain_points", "suggested_tools".
    """
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    try:
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        return {
            "core_problem": "Finding the right tool",
            "pain_points": ["Overwhelm", "Cost", "Integration"],
            "suggested_tools": ["Jasper", "SurferSEO"]
        }

def agent_copywriter(research_data, topic_title):
    """Agent 2: Drafts the SEO-optimized article."""
    
    # Safely convert to string in case the AI returns a dictionary instead of a plain string
    pain_points_str = ', '.join([str(p) for p in research_data.get('pain_points', [])])
    tools_str = ', '.join([str(t) for t in research_data.get('suggested_tools', [])])
    
    prompt = f"""
    You are an elite B2B SaaS copywriter. Write a 600-word SEO-optimized blog post based on this research:
    Topic: {topic_title}
    Core Problem: {research_data.get('core_problem', 'Solving the issue')}
    Pain Points: {pain_points_str}
    Suggested Tools: {tools_str}
    
    Use the PAS (Problem, Agitation, Solution) framework.
    Include Markdown headings (H2, H3).
    Do NOT include a title (H1) at the top, just start the article.
    """
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
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
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return response.text

if __name__ == "__main__":
    print("Starting AACE Multi-Agent Engine...")
    
    try:
        with open("data/trending_topics.json", "r") as f:
            topics = json.load(f)
    except FileNotFoundError:
        print("No ingestion data found. Exiting.")
        exit(1)
        
    if not topics:
        print("No topics to process.")
        exit(0)
        
    top_topic = topics[0]
    print(f"Processing Topic: {top_topic['title']}")
    
    import time
    
    print("Running Agent 1: Researcher...")
    research = agent_researcher(top_topic)
    
    print("Waiting 15 seconds to prevent free-tier rate limits...")
    time.sleep(15)
    
    print("Running Agent 2: Copywriter...")
    draft = agent_copywriter(research, top_topic['title'])
    
    print("Waiting 15 seconds to prevent free-tier rate limits...")
    time.sleep(15)
    
    print("Running Agent 3: Editor...")
    final_article = agent_editor(draft)
    
    os.makedirs("data", exist_ok=True)
    with open("data/generated_article.md", "w", encoding='utf-8') as f:
        f.write(top_topic['title'] + "\n---\n")
        f.write(final_article)
        
    print("Engine finished successfully.")
