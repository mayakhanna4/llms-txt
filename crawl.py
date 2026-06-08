import os
from typing import Dict, Any, Optional, List
from firecrawl import Firecrawl
from openai import OpenAI

def scrape_url_to_markdown_firecrawl(target_url: str) -> Optional[str]:
    """
    Scrapes a target URL using Firecrawl and returns clean Markdown.
    Assumes FIRECRAWL_API_KEY is set in your environment variables.
    """
    # Initialize the client. It automatically picks up os.environ.get("FIRECRAWL_API_KEY")
    # if you leave the api_key parameter empty or specify it manually.
    api_key = ""
    if not api_key:
        raise ValueError("Please set the FIRECRAWL_API_KEY environment variable.")
        
    app = Firecrawl(api_key=api_key)
    
    try:
        # We request 'markdown' explicitly.
        # Firecrawl drops headers, footers, and nav menus by default.
        scrape_result = app.scrape(
            url=target_url, 
            formats=["markdown"]
        )
        
        # Extracted markdown content is nested inside the response dictionary
        return scrape_result.markdown
        
    except Exception as e:
        print(f"Error scraping {target_url} with Firecrawl: {e}")
        return None

def extract_page_metadata(raw_markdown: str, url: str) -> Dict[str, str]:
    """
    Uses a fast LLM to extract a clean title and a crisp 1-sentence description
    from raw markdown content for the llms.txt index.
    """
    # To save tokens and avoid context overflow, we only send the first 3000 characters
    sample_text = raw_markdown[:3000]
    
    prompt = f"""
    Analyze the following website markdown content from URL: {url}
    Extract:
    1. A clean, human-readable page title (without SEO stuffing).
    2. A crisp, exact one-sentence description of what this page covers.

    Respond STRICTLY in this format:
    Title: <title>
    Description: <description>
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        lines = response.choices[0].message.content.strip().split("\n")
        title = lines[0].replace("Title:", "").strip()
        description = lines[1].replace("Description:", "").strip()
        
        return {"title": title, "description": description, "url": url}
    except Exception as e:
        # Fallback if the LLM call fails
        return {"title": "Documentation Page", "description": "Resource page.", "url": url}


def compile_llms_files(project_name: str, main_summary: str, pages_data: List[Dict[str, str]]) -> tuple[str, str]:
    """
    Compiles individual page data into standard llms.txt and llms-full.txt formats.
    
    pages_data structure: [{'title':..., 'description':..., 'url':..., 'content':...}]
    """
    # --- 1. BUILD THE LLMS.TXT INDEX ---
    llms_txt = f"# {project_name}\n\n"
    llms_txt += f"> {main_summary}\n\n"
    llms_txt += "## Documentation\n\n"
    
    for page in pages_data:
        llms_txt += f"- [{page['title']}]({page['url']}): {page['description']}\n"
        
    # --- 2. BUILD THE LLMS-FULL.TXT BUNDLE ---
    llms_full_txt = f"# {project_name} (Full Content Bundle)\n\n"
    llms_full_txt += "This file contains the complete markdown text documentation for all crawled links.\n\n"
    
    for page in pages_data:
        llms_full_txt += "---\n"  # Markdown rule divider
        llms_full_txt += f"## {page['title']}\n"
        llms_full_txt += f"Source: {page['url']}\n\n"
        llms_full_txt += f"{page['content']}\n\n"
        
    return llms_txt, llms_full_txt

if __name__ == "__main__":
    url = "https://app.notion.com/p/Catskills-July-4th-2026-369d1e060aa5804ba482e9a1ab96ee4a"
    
    # get markdown content
    markdown_content = scrape_url_to_markdown_firecrawl(url)
    if markdown_content:
        print(f"--- Successfully scraped {url} ---")
        print(markdown_content[:500]) # Print first 500 characters


    # Use LLM to compress it
    client = OpenAI(
    )

    scraped_pages_raw = [
        {
            "url": url,
            "content": markdown_content
        }
    ]
    
    compiled_pages = []

    # Process each page through the metadata extractor
    for page in scraped_pages_raw:
        print(f"Processing metadata for {page['url']}...")
        metadata = extract_page_metadata(page["content"], page["url"])
        
        # Combine everything together
        compiled_pages.append({
            "title": metadata["title"],
            "description": metadata["description"],
            "url": page["url"],
            "content": page["content"]
        })
        
    # Compile the final strings
    llms_index, llms_bundle = compile_llms_files(
        project_name="DataFlow API",
        main_summary="An automated data processing pipeline engine designed for enterprise developers.",
        pages_data=compiled_pages
    )
    
    # Save the output files
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_index)
        
    with open("llms-full.txt", "w", encoding="utf-8") as f:
        f.write(llms_bundle)
        
    print("✨ Successfully generated llms.txt and llms-full.txt!")