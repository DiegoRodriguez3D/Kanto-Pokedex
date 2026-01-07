import type { PageLoad } from './$types';
import { fetchPokemonDetail, fetchEvolutionChain, type PokemonDetail, type EvolutionChain } from '$lib/api';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params }) => {
    const id = parseInt(params.id, 10);

    if (isNaN(id) || id < 1 || id > 151) {
        throw error(404, 'Pokemon not found. ID must be between 1 and 151.');
    }

    try {
        const [pokemon, evolutionData] = await Promise.all([
            fetchPokemonDetail(id),
            fetchEvolutionChain(id).catch(() => null)
        ]);

        return {
            pokemon,
            evolution: evolutionData,
            error: null
        };
    } catch (err) {
        console.error('Failed to load Pokemon details:', err);
        return {
            pokemon: null,
            evolution: null,
            error: 'Failed to load Pokemon data. Please make sure the backend server is running.'
        };
    }
};
