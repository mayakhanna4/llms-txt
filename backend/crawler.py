from typing import Optional
from firecrawl import Firecrawl


def scrape_url_to_markdown(target_url: str) -> Optional[str]:
    api_key = ""
    if not api_key:
        raise ValueError("Please set the FIRECRAWL_API_KEY environment variable.")

    app = Firecrawl(api_key=api_key)

    try:
        scrape_result = app.scrape(url=target_url, formats=["markdown"])
        return scrape_result.markdown
    except Exception as e:
        print(f"Error scraping {target_url} with Firecrawl: {e}")
        return None
