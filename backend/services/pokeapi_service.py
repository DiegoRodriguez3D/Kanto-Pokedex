"""PokéAPI service for fetching Pokemon data."""
import asyncio
from typing import Optional

import httpx

from models.pokemon import (
    PokemonListItem,
    PokemonDetail,
    PokemonStats,
)
from services.cache_service import cache


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
OFFICIAL_ARTWORK_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"

# Cache TTL in seconds
LIST_CACHE_TTL = 3600  # 1 hour
DETAIL_CACHE_TTL = 1800  # 30 minutes


class PokeAPIService:
    """Service for interacting with the PokéAPI."""
    
    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=POKEAPI_BASE_URL,
                timeout=30.0,
            )
        return self.client
    
    async def close(self) -> None:
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            self.client = None
    
    async def _fetch_pokemon_basic(self, url: str) -> Optional[dict]:
        """Fetch basic Pokemon data from a URL."""
        try:
            client = await self._get_client()
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None
    
    async def get_pokemon_list(self, limit: int = 151) -> list[PokemonListItem]:
        """
        Get list of Pokemon with basic info for grid display.
        
        Args:
            limit: Number of Pokemon to fetch (default: 151 for Gen 1)
            
        Returns:
            List of PokemonListItem objects
        """
        cache_key = f"pokemon_list_{limit}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        client = await self._get_client()
        
        # Get the list of Pokemon URLs
        response = await client.get(f"/pokemon?limit={limit}")
        response.raise_for_status()
        data = response.json()
        
        # Fetch details for each Pokemon in parallel
        tasks = [
            self._fetch_pokemon_basic(pokemon["url"])
            for pokemon in data["results"]
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        pokemon_list = []
        for result in results:
            if isinstance(result, dict):
                pokemon_item = PokemonListItem(
                    id=result["id"],
                    name=result["name"].capitalize(),
                    image=OFFICIAL_ARTWORK_URL.format(id=result["id"]),
                    types=[t["type"]["name"] for t in result["types"]],
                )
                pokemon_list.append(pokemon_item)
        
        # Sort by ID to ensure correct order
        pokemon_list.sort(key=lambda p: p.id)
        
        # Cache the result
        cache.set(cache_key, pokemon_list, LIST_CACHE_TTL)
        
        return pokemon_list
    
    async def get_pokemon_detail(self, pokemon_id: int) -> Optional[PokemonDetail]:
        """
        Get detailed information about a specific Pokemon.
        
        Args:
            pokemon_id: The Pokemon ID
            
        Returns:
            PokemonDetail object or None if not found
        """
        cache_key = f"pokemon_detail_{pokemon_id}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            client = await self._get_client()
            
            # Fetch Pokemon data
            response = await client.get(f"/pokemon/{pokemon_id}")
            response.raise_for_status()
            pokemon_data = response.json()
            
            # Fetch species data for description
            species_response = await client.get(f"/pokemon-species/{pokemon_id}")
            species_response.raise_for_status()
            species_data = species_response.json()
            
            # Extract English flavor text
            description = ""
            for entry in species_data.get("flavor_text_entries", []):
                if entry["language"]["name"] == "en":
                    # Clean up the text (remove special characters)
                    description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                    break
            
            # Extract stats
            stats_map = {}
            for stat in pokemon_data["stats"]:
                stat_name = stat["stat"]["name"]
                stats_map[stat_name] = stat["base_stat"]
            
            stats = PokemonStats(
                hp=stats_map.get("hp", 0),
                attack=stats_map.get("attack", 0),
                defense=stats_map.get("defense", 0),
                special_attack=stats_map.get("special-attack", 0),
                special_defense=stats_map.get("special-defense", 0),
                speed=stats_map.get("speed", 0),
            )
            
            pokemon_detail = PokemonDetail(
                id=pokemon_data["id"],
                name=pokemon_data["name"].capitalize(),
                image=OFFICIAL_ARTWORK_URL.format(id=pokemon_data["id"]),
                types=[t["type"]["name"] for t in pokemon_data["types"]],
                stats=stats,
                height=pokemon_data["height"],
                weight=pokemon_data["weight"],
                description=description,
            )
            
            # Cache the result
            cache.set(cache_key, pokemon_detail, DETAIL_CACHE_TTL)
            
            return pokemon_detail
            
        except httpx.HTTPError:
            return None


# Global service instance
pokeapi_service = PokeAPIService()
