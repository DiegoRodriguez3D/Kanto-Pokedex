"""Pokemon API endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.pokemon import PokemonListItem, PokemonDetail, PokemonListResponse, EvolutionChain
from services.pokeapi_service import pokeapi_service


router = APIRouter(prefix="/pokemon", tags=["pokemon"])


class CompareRequest(BaseModel):
    """Request model for comparing Pokemon."""
    ids: list[int]


class CompareResponse(BaseModel):
    """Response model for Pokemon comparison."""
    pokemon: list[PokemonDetail]


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


@router.post("/compare", response_model=CompareResponse)
async def compare_pokemon(request: CompareRequest):
    """
    Compare multiple Pokemon side by side.
    
    Args:
        request: CompareRequest containing list of Pokemon IDs (2-6)
        
    Returns:
        List of detailed Pokemon information for comparison.
    """
    if len(request.ids) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 Pokemon IDs are required for comparison"
        )
    
    if len(request.ids) > 6:
        raise HTTPException(
            status_code=400,
            detail="Maximum 6 Pokemon can be compared at once"
        )
    
    # Validate all IDs are in Kanto range
    for pid in request.ids:
        if pid < 1 or pid > 151:
            raise HTTPException(
                status_code=400,
                detail=f"Pokemon ID {pid} must be between 1 and 151 (Kanto region only)"
            )
    
    try:
        pokemon_list = await pokeapi_service.get_multiple_pokemon(request.ids)
        if len(pokemon_list) == 0:
            raise HTTPException(
                status_code=404,
                detail="No Pokemon found for the provided IDs"
            )
        return CompareResponse(pokemon=pokemon_list)
    except HTTPException:
        raise
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


@router.get("/{pokemon_id}/evolution", response_model=EvolutionChain)
async def get_pokemon_evolution(pokemon_id: int):
    """
    Get the evolution chain for a specific Pokemon.
    
    Args:
        pokemon_id: The Pokemon ID (1-151 for Kanto)
        
    Returns:
        Evolution chain showing all evolution stages.
    """
    if pokemon_id < 1 or pokemon_id > 151:
        raise HTTPException(
            status_code=400,
            detail="Pokemon ID must be between 1 and 151 (Kanto region only)"
        )
    
    try:
        evolution_chain = await pokeapi_service.get_evolution_chain(pokemon_id)
        if evolution_chain is None:
            raise HTTPException(
                status_code=404,
                detail=f"Evolution chain for Pokemon {pokemon_id} not found"
            )
        return evolution_chain
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch evolution data. Please try again later. Error: {str(e)}"
        )

