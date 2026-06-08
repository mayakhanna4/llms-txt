from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crawler import scrape_url_to_markdown
from generator import extract_page_metadata, compile_llms_files

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    url: str

@app.post("/generate")
def generate(req: GenerateRequest):
    markdown_content = scrape_url_to_markdown(req.url)
    if not markdown_content:
        raise HTTPException(status_code=422, detail="Failed to scrape the URL.")

    metadata = extract_page_metadata(markdown_content, req.url)
    pages = [{
        "title": metadata["title"],
        "description": metadata["description"],
        "url": req.url,
        "content": markdown_content,
    }]

    llms_txt, llms_full_txt = compile_llms_files(
        project_name=metadata["title"],
        main_summary=metadata["description"],
        pages_data=pages,
    )

    return {"llms_txt": llms_txt, "llms_full_txt": llms_full_txt, "summary": metadata["description"]}
