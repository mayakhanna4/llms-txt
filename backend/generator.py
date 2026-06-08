from typing import Dict, List
from openai import OpenAI

client = OpenAI()


def extract_page_metadata(raw_markdown: str, url: str) -> Dict[str, str]:
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
            temperature=0.3,
        )

        lines = response.choices[0].message.content.strip().split("\n")
        title = lines[0].replace("Title:", "").strip()
        description = lines[1].replace("Description:", "").strip()

        return {"title": title, "description": description, "url": url}
    except Exception as e:
        print(f"Error extracting metadata for {url}: {e}")
        return {"title": "Documentation Page", "description": "Resource page.", "url": url}


def compile_llms_files(
    project_name: str, main_summary: str, pages_data: List[Dict[str, str]]
) -> tuple[str, str]:
    llms_txt = f"# {project_name}\n\n"
    llms_txt += f"> {main_summary}\n\n"
    llms_txt += "## Documentation\n\n"

    for page in pages_data:
        llms_txt += f"- [{page['title']}]({page['url']}): {page['description']}\n"

    llms_full_txt = f"# {project_name} (Full Content Bundle)\n\n"
    llms_full_txt += "This file contains the complete markdown text documentation for all crawled links.\n\n"

    for page in pages_data:
        llms_full_txt += "---\n"
        llms_full_txt += f"## {page['title']}\n"
        llms_full_txt += f"Source: {page['url']}\n\n"
        llms_full_txt += f"{page['content']}\n\n"

    return llms_txt, llms_full_txt
