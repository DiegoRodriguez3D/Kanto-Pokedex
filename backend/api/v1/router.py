"""API v1 router."""
from fastapi import APIRouter

from api.v1.endpoints import pokemon


router = APIRouter(prefix="/api/v1")
router.include_router(pokemon.router)
