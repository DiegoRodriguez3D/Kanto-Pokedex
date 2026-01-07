/**
 * API client for communicating with the FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

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

export interface EvolutionStage {
    id: number;
    name: string;
    image: string;
    trigger: string;
    min_level: number | null;
    trigger_item: string | null;
}

export interface EvolutionChain {
    chain: EvolutionStage[];
}

export interface CompareResponse {
    pokemon: PokemonDetail[];
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

/**
 * Fetch evolution chain for a specific Pokemon.
 */
export async function fetchEvolutionChain(id: number): Promise<EvolutionChain> {
    const response = await fetch(`${API_BASE_URL}/pokemon/${id}/evolution`);

    if (!response.ok) {
        throw new Error(`Failed to fetch evolution chain: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Compare multiple Pokemon by their IDs.
 */
export async function comparePokemon(ids: number[]): Promise<CompareResponse> {
    const response = await fetch(`${API_BASE_URL}/pokemon/compare`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ids }),
    });

    if (!response.ok) {
        throw new Error(`Failed to compare Pokemon: ${response.statusText}`);
    }

    return response.json();
}

