import type { PageLoad } from './$types';
import { fetchPokemonDetail, type PokemonDetail } from '$lib/api';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params }) => {
    const id = parseInt(params.id, 10);

    if (isNaN(id) || id < 1 || id > 151) {
        throw error(404, 'Pokemon not found. ID must be between 1 and 151.');
    }

    try {
        const pokemon: PokemonDetail = await fetchPokemonDetail(id);
        return {
            pokemon,
            error: null
        };
    } catch (err) {
        console.error('Failed to load Pokemon details:', err);
        return {
            pokemon: null,
            error: 'Failed to load Pokemon data. Please make sure the backend server is running.'
        };
    }
};
