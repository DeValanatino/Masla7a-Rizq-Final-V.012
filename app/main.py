from app.database import engine, Base
import app.models # Import your models here so Base knows about them

# This commands Render to create the tables if they don't exist
Base.metadata.create_all(bind=engine)
"""
Msla7a Rizq (مصلحة رزق) — FastAPI Application Entry Point.

B2B Industrial Manufacturing Marketplace for Egypt.

Architecture:
  routers/     → HTTP layer (thin controllers)
  services/    → business logic
  repositories/→ data access (in-memory now, Supabase later)
  models/      → domain entities
  schemas/     → Pydantic request/response DTOs
  dependencies/→ auth gatekeeper + subscription gatekeeper
"""

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app import __version__
from app.repositories.asset_repository import AssetRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.routers import assets, auth, feed, projects

# ---------------------------------------------------------------------------
# Shared in-memory stores (singletons — swap for Supabase client pool later)
# ---------------------------------------------------------------------------
user_repo = UserRepository()
project_repo = ProjectRepository()
asset_repo = AssetRepository()
session_repo = SessionRepository()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown hooks."""
    # Future: initialize Supabase client, run migrations, warm caches
    yield
    # Future: close DB connections gracefully


app = FastAPI(
    title="Msla7a Rizq API",
    description=(
        "مصلحة رزق — B2B Industrial Manufacturing Marketplace for Egypt. "
        "Unified dashboard with Pipeline and Asset tracks, "
        "protected by phone authentication and a 200 EGP subscription gate."
    ),
    version=__version__,
    lifespan=lifespan,
)

# CORS — tighten origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(assets.router)
app.include_router(feed.router)


@app.get("/", response_class=HTMLResponse, tags=["Waitlist"])
def root():
    """Serve the illiterate-first mobile waitlist page."""
    filepath = os.path.join(os.path.dirname(__file__), "static", "waitlist.html")
    with open(filepath, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/waitlist", response_class=HTMLResponse, tags=["Waitlist"])
def waitlist():
    """Serve the illiterate-first mobile waitlist page."""
    return root()


@app.get("/health", tags=["Health"])
def health_check():
    """Simple liveness probe for deployment orchestrators."""
    return {"status": "healthy"}

