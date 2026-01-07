"""Pokemon API endpoints."""
from fastapi import APIRouter, HTTPException

from models.pokemon import PokemonListItem, PokemonDetail, PokemonListResponse
from services.pokeapi_service import pokeapi_service


router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("", response_model=PokemonListResponse)
async def get_pokemon_list():
    """
    Get list of all 151 Kanto Pokemon with basic information.
    
    Returns a list of Pokemon with ID, name, image URL, and types.
    Ideal for displaying in a grid/list view.
    """
    try:
        pokemon_list = await pokeapi_service.get_pokemon_list(limit=151)
        return PokemonListResponse(
            count=len(pokemon_list),
            pokemon=pokemon_list,
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch Pokemon data. Please try again later. Error: {str(e)}"
        )


@router.get("/{pokemon_id}", response_model=PokemonDetail)
async def get_pokemon_detail(pokemon_id: int):
    """
    Get detailed information about a specific Pokemon.
    
    Args:
        pokemon_id: The Pokemon ID (1-151 for Kanto)
        
    Returns:
        Detailed Pokemon information including stats and description.
    """
    if pokemon_id < 1 or pokemon_id > 151:
        raise HTTPException(
            status_code=400,
            detail="Pokemon ID must be between 1 and 151 (Kanto region only)"
        )
    
    try:
        pokemon = await pokeapi_service.get_pokemon_detail(pokemon_id)
        if pokemon is None:
            raise HTTPException(
                status_code=404,
                detail=f"Pokemon with ID {pokemon_id} not found"
            )
        return pokemon
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch Pokemon data. Please try again later. Error: {str(e)}"
        )
