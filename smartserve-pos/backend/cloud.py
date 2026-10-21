"""Serve the built frontend and FastAPI routes from one public origin."""
import os
from pathlib import Path

from fastapi.staticfiles import StaticFiles

# Neon supplies standard PostgreSQL URLs. Select the installed psycopg driver
# before app.database creates its SQLAlchemy engine.
database_url = os.environ.get("DATABASE_URL", "")
for prefix in ("postgres://", "postgresql://"):
    if database_url.startswith(prefix):
        os.environ["DATABASE_URL"] = database_url.replace(prefix, "postgresql+psycopg://", 1)
        break

from app.main import app  # noqa: E402

# Register last so existing API routes take priority over static frontend files.
dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=dist, html=True), name="frontend")
