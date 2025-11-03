from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.hoarder.utils.settings import settings
from src.hoarder.api.job_collection import router as jc_router

app = FastAPI(title="Job Scraper API")
app.include_router(jc_router)

# Add CORS middleware to allow Chrome extension requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Chrome extension origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JobPageRequest(BaseModel):
    url: str
    page_html: str


class JobPageResponse(BaseModel):
    page_id: int
    url: str
    message: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Job Scraper API is running"}


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server"""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
