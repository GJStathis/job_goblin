"""API Server Entry Point"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.hoarder.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
