<script lang="ts">
    import { getTypeColor } from "$lib/typeColors";
    import TypeBadge from "./TypeBadge.svelte";
    import type { PokemonListItem } from "$lib/api";

    interface Props {
        pokemon: PokemonListItem;
    }

    let { pokemon }: Props = $props();

    // Get background color from primary type
    const bgColor = $derived(
        pokemon.types.length > 0
            ? getTypeColor(pokemon.types[0]).bg
            : "#f8fafc",
    );

    // Darker version for dark mode
    const darkBgColor = $derived(
        pokemon.types.length > 0
            ? getTypeColor(pokemon.types[0]).main + "33" // 20% opacity
            : "#1e293b",
    );

    // Format Pokemon ID with leading zeros
    function formatId(id: number): string {
        return `#${id.toString().padStart(3, "0")}`;
    }
</script>

<a
    href="/pokemon/{pokemon.id}"
    class="pokemon-card"
    style="--bg-light: {bgColor}; --bg-dark: {darkBgColor};"
>
    <div class="card-content">
        <div class="pokemon-image-container">
            <img
                src={pokemon.image}
                alt={pokemon.name}
                class="pokemon-image"
                loading="lazy"
            />
        </div>

        <div class="pokemon-info">
            <span class="pokemon-id">{formatId(pokemon.id)}</span>
            <h2 class="pokemon-name">{pokemon.name}</h2>

            <div class="pokemon-types">
                {#each pokemon.types as type}
                    <TypeBadge {type} />
                {/each}
            </div>
        </div>
    </div>
</a>

<style>
    .pokemon-card {
        display: block;
        border-radius: 1rem;
        padding: 1rem;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
        box-shadow:
            0 4px 6px -1px rgba(0, 0, 0, 0.1),
            0 2px 4px -1px rgba(0, 0, 0, 0.06);
        background-color: var(--bg-light);
    }

    :global(.dark) .pokemon-card {
        background-color: var(--bg-dark);
        box-shadow:
            0 4px 6px -1px rgba(0, 0, 0, 0.3),
            0 2px 4px -1px rgba(0, 0, 0, 0.2);
    }

    .pokemon-card:hover {
        transform: translateY(-4px);
        box-shadow:
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    :global(.dark) .pokemon-card:hover {
        box-shadow:
            0 20px 25px -5px rgba(0, 0, 0, 0.4),
            0 10px 10px -5px rgba(0, 0, 0, 0.2);
    }

    .card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .pokemon-image-container {
        width: 120px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.5rem;
    }

    .pokemon-image {
        width: 100%;
        height: 100%;
        object-fit: contain;
        transition: transform 0.3s ease;
    }

    .pokemon-card:hover .pokemon-image {
        transform: scale(1.1);
    }

    .pokemon-info {
        text-align: center;
        width: 100%;
    }

    .pokemon-id {
        font-size: 0.75rem;
        font-weight: 500;
        color: #64748b;
    }

    :global(.dark) .pokemon-id {
        color: #94a3b8;
    }

    .pokemon-name {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.25rem 0 0.5rem;
        text-transform: capitalize;
    }

    :global(.dark) .pokemon-name {
        color: #f1f5f9;
    }

    .pokemon-types {
        display: flex;
        gap: 0.375rem;
        justify-content: center;
        flex-wrap: wrap;
    }
</style>
