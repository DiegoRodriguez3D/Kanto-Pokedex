/**
 * API client for communicating with the FastAPI backend.
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface PokemonListItem {
    id: number;
    name: string;
    image: string;
    types: string[];
}

export interface PokemonStats {
    hp: number;
    attack: number;
    defense: number;
    special_attack: number;
    special_defense: number;
    speed: number;
}

export interface PokemonDetail {
    id: number;
    name: string;
    image: string;
    types: string[];
    stats: PokemonStats;
    height: number;
    weight: number;
    description: string;
}

export interface PokemonListResponse {
    count: number;
    pokemon: PokemonListItem[];
}

/**
 * Fetch all 151 Kanto Pokemon for the grid view.
 */
export async function fetchPokemonList(): Promise<PokemonListResponse> {
    const response = await fetch(`${API_BASE_URL}/pokemon`);

    if (!response.ok) {
        throw new Error(`Failed to fetch Pokemon list: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Fetch detailed information about a specific Pokemon.
 */
export async function fetchPokemonDetail(id: number): Promise<PokemonDetail> {
    const response = await fetch(`${API_BASE_URL}/pokemon/${id}`);

    if (!response.ok) {
        throw new Error(`Failed to fetch Pokemon details: ${response.statusText}`);
    }

    return response.json();
}
