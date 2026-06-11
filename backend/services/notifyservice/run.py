import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=7070,
        log_level="info"
    )