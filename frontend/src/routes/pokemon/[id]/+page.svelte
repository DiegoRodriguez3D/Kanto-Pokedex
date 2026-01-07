<script lang="ts">
    import TypeBadge from "$lib/components/TypeBadge.svelte";
    import StatBar from "$lib/components/StatBar.svelte";
    import { getTypeGradient } from "$lib/typeColors";
    import type { PokemonDetail } from "$lib/api";

    interface Props {
        data: {
            pokemon: PokemonDetail | null;
            error: string | null;
        };
    }

    let { data }: Props = $props();

    const pokemon = $derived(data.pokemon);
    const gradient = $derived(pokemon ? getTypeGradient(pokemon.types) : "");

    function formatId(id: number): string {
        return `#${id.toString().padStart(3, "0")}`;
    }

    function formatHeight(decimeters: number): string {
        const meters = decimeters / 10;
        return `${meters.toFixed(1)} m`;
    }

    function formatWeight(hectograms: number): string {
        const kg = hectograms / 10;
        return `${kg.toFixed(1)} kg`;
    }
</script>

<svelte:head>
    {#if pokemon}
        <title>{pokemon.name} - Kanto Pokédex</title>
        <meta name="description" content={pokemon.description} />
    {:else}
        <title>Pokemon Not Found - Kanto Pokédex</title>
    {/if}
</svelte:head>

{#if data.error || !pokemon}
    <div class="error-page">
        <div class="error-content">
            <h1 class="error-title">Unable to load Pokémon</h1>
            <p class="error-message">{data.error || "Pokemon not found"}</p>
            <a href="/" class="back-button">← Back to Pokédex</a>
        </div>
    </div>
{:else}
    <div class="detail-page" style="background: {gradient};">
        <!-- Navigation -->
        <nav class="nav">
            <a href="/" class="back-link">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <path d="m15 18-6-6 6-6" />
                </svg>
                <span>Back</span>
            </a>
        </nav>

        <main class="content">
            <!-- Pokemon Image -->
            <div class="image-container">
                <img
                    src={pokemon.image}
                    alt={pokemon.name}
                    class="pokemon-image"
                />
            </div>

            <!-- Pokemon Info Card (Glassmorphism) -->
            <div class="info-card">
                <!-- Header -->
                <div class="info-header">
                    <h1 class="pokemon-name">{pokemon.name}</h1>
                    <span class="pokemon-id">{formatId(pokemon.id)}</span>
                </div>

                <!-- Types -->
                <div class="types-row">
                    {#each pokemon.types as type}
                        <TypeBadge {type} />
                    {/each}
                </div>

                <!-- Physical Stats -->
                <div class="physical-stats">
                    <div class="physical-stat">
                        <span class="physical-value"
                            >{formatHeight(pokemon.height)}</span
                        >
                        <span class="physical-label">Height</span>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="physical-stat">
                        <span class="physical-value"
                            >{formatWeight(pokemon.weight)}</span
                        >
                        <span class="physical-label">Weight</span>
                    </div>
                </div>

                <!-- Base Stats -->
                <div class="stats-section">
                    <h2 class="section-title">Base Stats</h2>
                    <div class="stats-container">
                        <StatBar label="HP" value={pokemon.stats.hp} />
                        <StatBar label="Attack" value={pokemon.stats.attack} />
                        <StatBar
                            label="Defense"
                            value={pokemon.stats.defense}
                        />
                        <StatBar
                            label="Sp. Atk"
                            value={pokemon.stats.special_attack}
                        />
                        <StatBar
                            label="Sp. Def"
                            value={pokemon.stats.special_defense}
                        />
                        <StatBar label="Speed" value={pokemon.stats.speed} />
                    </div>
                </div>

                <!-- Description -->
                {#if pokemon.description}
                    <div class="description-section">
                        <h2 class="section-title">Description</h2>
                        <p class="description-text">{pokemon.description}</p>
                    </div>
                {/if}

                <!-- Navigation between Pokemon -->
                <div class="pokemon-nav">
                    {#if pokemon.id > 1}
                        <a
                            href="/pokemon/{pokemon.id - 1}"
                            class="nav-button prev"
                        >
                            ← Previous
                        </a>
                    {:else}
                        <div></div>
                    {/if}

                    {#if pokemon.id < 151}
                        <a
                            href="/pokemon/{pokemon.id + 1}"
                            class="nav-button next"
                        >
                            Next →
                        </a>
                    {/if}
                </div>
            </div>
        </main>
    </div>
{/if}

<style>
    .detail-page {
        min-height: 100vh;
        padding: 1rem;
    }

    .nav {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    .back-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: white;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        transition: background 0.2s;
    }

    .back-link:hover {
        background: rgba(255, 255, 255, 0.3);
    }

    .content {
        max-width: 800px;
        margin: 0 auto;
    }

    .image-container {
        display: flex;
        justify-content: center;
        padding: 1rem;
    }

    .pokemon-image {
        width: 250px;
        height: 250px;
        object-fit: contain;
        filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.3));
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }

    /* Glassmorphism Card */
    .info-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 2rem 2rem 1rem 1rem;
        padding: 2rem 1.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }

    .info-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .pokemon-name {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
        margin: 0;
        text-transform: capitalize;
    }

    .pokemon-id {
        font-size: 1.25rem;
        font-weight: 600;
        color: #64748b;
    }

    .types-row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .physical-stats {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
    }

    .physical-stat {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
    }

    .physical-value {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1e293b;
    }

    .physical-label {
        font-size: 0.875rem;
        color: #64748b;
    }

    .stat-divider {
        width: 1px;
        height: 40px;
        background: #e2e8f0;
    }

    .section-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 1rem;
    }

    .stats-section {
        margin-bottom: 1.5rem;
    }

    .stats-container {
        display: flex;
        flex-direction: column;
    }

    .description-section {
        margin-bottom: 1.5rem;
    }

    .description-text {
        color: #475569;
        line-height: 1.6;
        margin: 0;
    }

    .pokemon-nav {
        display: flex;
        justify-content: space-between;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }

    .nav-button {
        padding: 0.75rem 1.25rem;
        background: #f1f5f9;
        color: #475569;
        text-decoration: none;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s;
    }

    .nav-button:hover {
        background: #e2e8f0;
        color: #1e293b;
    }

    /* Error Page */
    .error-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f8fafc;
    }

    .error-content {
        text-align: center;
        padding: 2rem;
    }

    .error-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }

    .error-message {
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    .back-button {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        text-decoration: none;
        border-radius: 0.5rem;
        font-weight: 600;
    }

    /* Responsive */
    @media (min-width: 640px) {
        .pokemon-image {
            width: 300px;
            height: 300px;
        }

        .info-card {
            padding: 2.5rem;
        }

        .pokemon-name {
            font-size: 2.5rem;
        }
    }
</style>
