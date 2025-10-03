from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()

# Mount static subfolders
app.mount("/styles", StaticFiles(directory=STATIC_DIR / "styles"), name="styles")
app.mount("/images", StaticFiles(directory=STATIC_DIR / "images"), name="images")
app.mount("/pages", StaticFiles(directory=STATIC_DIR / "pages"), name="pages")

# Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

# Catch-all route for cleaner URLs (/history → pages/history.html)
@app.get("/{page_name}")
async def serve_clean_page(page_name: str):
    file_path = STATIC_DIR / "pages" / f"{page_name}.html"
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": f"Page '{page_name}' not found"}
