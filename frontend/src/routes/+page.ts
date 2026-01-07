import type { PageLoad } from './$types';
import { fetchPokemonList, type PokemonListResponse } from '$lib/api';

export const load: PageLoad = async ({ fetch }) => {
    try {
        const data: PokemonListResponse = await fetchPokemonList();
        return {
            pokemon: data.pokemon,
            error: null
        };
    } catch (error) {
        console.error('Failed to load Pokemon list:', error);
        return {
            pokemon: [],
            error: 'Failed to load Pokemon data. Please make sure the backend server is running.'
        };
    }
};
