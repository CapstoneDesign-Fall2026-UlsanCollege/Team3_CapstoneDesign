"""Single-origin cloud entrypoint; the ordinary Docker entrypoint is unchanged."""
import os
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Managed PostgreSQL providers supply a standard URL; use the installed psycopg driver.
database_url = os.environ.get("DATABASE_URL", "")
for prefix in ("postgres://", "postgresql://"):
    if database_url.startswith(prefix):
        os.environ["DATABASE_URL"] = database_url.replace(prefix, "postgresql+psycopg://", 1)
        break

from app.main import app  # noqa: E402

# Register last so API routes keep priority over the frontend.
dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@app.get("/etalogin", include_in_schema=False)
@app.get("/etalogin/", include_in_schema=False)
def owner_page():
    return FileResponse(dist / "index.html")


app.mount("/", StaticFiles(directory=dist, html=True), name="frontend")
