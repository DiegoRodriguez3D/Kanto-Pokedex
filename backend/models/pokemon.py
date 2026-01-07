"""Pydantic models for Pokemon data."""
from pydantic import BaseModel, Field


class PokemonType(BaseModel):
    """Pokemon type information."""
    name: str
    color: str


class PokemonStats(BaseModel):
    """Pokemon base stats."""
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class PokemonListItem(BaseModel):
    """Simplified Pokemon data for list/grid view."""
    id: int
    name: str
    image: str
    types: list[str]


class PokemonDetail(BaseModel):
    """Full Pokemon details for detail view."""
    id: int
    name: str
    image: str
    types: list[str]
    stats: PokemonStats
    height: int = Field(description="Height in decimeters")
    weight: int = Field(description="Weight in hectograms")
    description: str = ""
    

class PokemonListResponse(BaseModel):
    """Response model for pokemon list endpoint."""
    count: int
    pokemon: list[PokemonListItem]


class EvolutionStage(BaseModel):
    """Single stage in an evolution chain."""
    id: int
    name: str
    image: str
    trigger: str = ""  # e.g., "level-up", "use-item", "trade"
    min_level: int | None = None
    trigger_item: str | None = None


class EvolutionChain(BaseModel):
    """Complete evolution chain for a Pokemon."""
    chain: list[EvolutionStage]
