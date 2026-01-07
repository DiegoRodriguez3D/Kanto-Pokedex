"""PokéAPI service for fetching Pokemon data."""
import asyncio
from typing import Optional

import httpx

from models.pokemon import (
    PokemonListItem,
    PokemonDetail,
    PokemonStats,
    EvolutionChain,
    EvolutionStage,
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
        """Lazy-initialize and return HTTP client."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                base_url=POKEAPI_BASE_URL,
                timeout=30.0,
            )
        return self.client
    
    async def close(self) -> None:
        """Cleanup HTTP client on shutdown."""
        if self.client:
            await self.client.aclose()
            self.client = None
    
    async def _fetch_pokemon_basic(self, url: str) -> Optional[dict]:
        try:
            client = await self._get_client()
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None
    
    async def get_pokemon_list(self, limit: int = 151) -> list[PokemonListItem]:
        """Fetch list of Pokemon for grid display. Cached for 1 hour."""
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
        """Fetch full Pokemon details including stats and description. Cached for 30 min."""
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
    
    async def get_evolution_chain(self, pokemon_id: int) -> Optional[EvolutionChain]:
        """Fetch evolution chain, filtering to Kanto Pokemon only. Cached for 30 min."""
        cache_key = f"evolution_chain_{pokemon_id}"
        
        # Check cache first
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            client = await self._get_client()
            
            # First get the species to find the evolution chain URL
            species_response = await client.get(f"/pokemon-species/{pokemon_id}")
            species_response.raise_for_status()
            species_data = species_response.json()
            
            # Get the evolution chain
            evolution_chain_url = species_data["evolution_chain"]["url"]
            # Extract relative path from full URL
            evolution_path = evolution_chain_url.replace(POKEAPI_BASE_URL, "")
            
            chain_response = await client.get(evolution_path)
            chain_response.raise_for_status()
            chain_data = chain_response.json()
            
            # Parse the evolution chain
            stages: list[EvolutionStage] = []
            
            def parse_chain(chain_node: dict) -> None:
                species_name = chain_node["species"]["name"]
                # Extract ID from URL
                species_url = chain_node["species"]["url"]
                species_id = int(species_url.rstrip("/").split("/")[-1])
                
                # Only include Kanto Pokemon (ID 1-151)
                if species_id > 151:
                    return
                
                # Get evolution details (if not the base form)
                trigger = ""
                min_level = None
                trigger_item = None
                
                if chain_node["evolution_details"]:
                    details = chain_node["evolution_details"][0]
                    trigger = details.get("trigger", {}).get("name", "")
                    min_level = details.get("min_level")
                    if details.get("item"):
                        trigger_item = details["item"]["name"].replace("-", " ").title()
                
                stages.append(EvolutionStage(
                    id=species_id,
                    name=species_name.capitalize(),
                    image=OFFICIAL_ARTWORK_URL.format(id=species_id),
                    trigger=trigger,
                    min_level=min_level,
                    trigger_item=trigger_item,
                ))
                
                # Process next evolutions
                for evolution in chain_node.get("evolves_to", []):
                    parse_chain(evolution)
            
            parse_chain(chain_data["chain"])
            
            evolution_chain = EvolutionChain(chain=stages)
            
            # Cache the result
            cache.set(cache_key, evolution_chain, DETAIL_CACHE_TTL)
            
            return evolution_chain
            
        except httpx.HTTPError:
            return None
    
    async def get_multiple_pokemon(self, pokemon_ids: list[int]) -> list[PokemonDetail]:
        """Fetch multiple Pokemon in parallel for comparison."""
        tasks = [self.get_pokemon_detail(pid) for pid in pokemon_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None values and exceptions
        pokemon_list = []
        for result in results:
            if isinstance(result, PokemonDetail):
                pokemon_list.append(result)
        
        return pokemon_list


pokeapi_service = PokeAPIService()

