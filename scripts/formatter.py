import os
import re
from datetime import datetime

# Affiliate Link Database
AFFILIATE_LINKS = {
    "Jasper": "https://jasper.ai/?utm_source=aace_affiliate",
    "SurferSEO": "https://surferseo.com/?utm_source=aace_affiliate",
    "Notion": "https://notion.so/?aff=aace123",
    "Shopify": "https://shopify.com/?ref=aace",
    # Add more as needed
}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def format_affiliate_links(content):
    """Replaces placeholders with actual affiliate links."""
    for tool, link in AFFILIATE_LINKS.items():
        # The editor agent leaves placeholders like [Jasper](AFFILIATE_LINK_PLACEHOLDER_JASPER)
        placeholder = f"AFFILIATE_LINK_PLACEHOLDER_{tool.upper()}"
        content = content.replace(placeholder, link)
    return content

if __name__ == "__main__":
    print("Starting AACE Formatter...")
    
    try:
        with open("data/generated_article.md", "r", encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 3:
                print("Generated article format is invalid.")
                exit(1)
                
            title = lines[0].strip()
            content = "".join(lines[2:]) # Skip the title and the '---' separator
    except FileNotFoundError:
        print("No generated article found. Exiting.")
        exit(1)
        
    # Inject affiliate links
    content_with_links = format_affiliate_links(content)
    
    # Generate Hugo Frontmatter
    date_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    # Provide a default timezone offset if empty
    if not date_str[-5:]:
        date_str += "+00:00"
        
    slug = slugify(title)[:50] # Keep slug reasonable length
    
    frontmatter = f"""---
title: "{title.replace('"', '')}"
date: {date_str}
draft: false
slug: "{slug}"
tags: ["SaaS", "AI Tools", "Review"]
categories: ["Software Reviews"]
---

"""
    
    final_markdown = frontmatter + content_with_links
    
    # Ensure content directory exists
    os.makedirs("content/posts", exist_ok=True)
    
    filename = f"content/posts/{slug}.md"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(final_markdown)
        
    print(f"Successfully formatted and saved to {filename}")
