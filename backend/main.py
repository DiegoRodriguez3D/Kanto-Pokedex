"""
Kanto Pokedex - FastAPI Backend

A Backend for Frontend (BFF) that serves as an intermediary between
the SvelteKit frontend and the PokéAPI.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import router as api_v1_router
from services.pokeapi_service import pokeapi_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    yield
    # Shutdown
    await pokeapi_service.close()


app = FastAPI(
    title="Kanto Pokedex API",
    description="API backend for the Kanto Pokedex web application. Provides Pokemon data for the first 151 Pokemon.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # SvelteKit dev server
        "http://localhost:4173",  # SvelteKit preview
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_v1_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "kanto-pokedex-api"}
