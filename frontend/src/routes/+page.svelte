<script lang="ts">
    import PokemonCard from "$lib/components/PokemonCard.svelte";
    import ThemeToggle from "$lib/components/ThemeToggle.svelte";
    import SearchBar from "$lib/components/SearchBar.svelte";
    import type { PokemonListItem } from "$lib/api";

    interface Props {
        data: {
            pokemon: PokemonListItem[];
            error: string | null;
        };
    }

    let { data }: Props = $props();

    // Search state
    let searchQuery = $state("");

    // Filter Pokemon based on search query
    const filteredPokemon = $derived(
        data.pokemon.filter(
            (pokemon) =>
                pokemon.name
                    .toLowerCase()
                    .includes(searchQuery.toLowerCase()) ||
                pokemon.id.toString().includes(searchQuery) ||
                pokemon.types.some((type) =>
                    type.toLowerCase().includes(searchQuery.toLowerCase()),
                ),
        ),
    );

    function handleSearch(value: string) {
        searchQuery = value;
    }
</script>

<svelte:head>
    <title>Kanto Pokédex - Explore the Original 151 Pokémon</title>
</svelte:head>

<div class="app-container">
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <div class="header-top">
                <div class="header-spacer"></div>
                <div class="title-section">
                    <h1 class="title">
                        Kanto <span class="title-highlight">Pokédex</span>
                    </h1>
                    <p class="subtitle">Explore all 151 original Pokémon</p>
                </div>
                <div class="header-actions">
                    <ThemeToggle />
                </div>
            </div>

            <!-- Search Bar -->
            {#if data.pokemon.length > 0}
                <div class="search-section">
                    <SearchBar value={searchQuery} onInput={handleSearch} />
                </div>
            {/if}
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        {#if data.error}
            <div class="error-container">
                <div class="error-icon">⚠️</div>
                <h2 class="error-title">Unable to load Pokémon</h2>
                <p class="error-message">{data.error}</p>
                <button class="retry-button" onclick={() => location.reload()}>
                    Try Again
                </button>
            </div>
        {:else if data.pokemon.length === 0}
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading-text">Loading Pokémon...</p>
            </div>
        {:else if filteredPokemon.length === 0}
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h2 class="no-results-title">No Pokémon found</h2>
                <p class="no-results-message">
                    Try searching with a different name, ID, or type.
                </p>
            </div>
        {:else}
            <div class="results-info">
                {#if searchQuery}
                    <p>
                        Showing {filteredPokemon.length} of {data.pokemon
                            .length} Pokémon
                    </p>
                {/if}
            </div>
            <div class="pokemon-grid">
                {#each filteredPokemon as pokemon (pokemon.id)}
                    <PokemonCard {pokemon} />
                {/each}
            </div>
        {/if}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <p>
            Data provided by <a
                href="https://pokeapi.co"
                target="_blank"
                rel="noopener noreferrer">PokéAPI</a
            >
        </p>
    </footer>
</div>

<style>
    .app-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .header {
        background: linear-gradient(
            135deg,
            var(--header-gradient-start) 0%,
            var(--header-gradient-end) 100%
        );
        padding: 1.5rem 1rem 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .header-content {
        max-width: 1400px;
        margin: 0 auto;
    }

    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.5rem;
    }

    .header-spacer {
        width: 40px;
    }

    .title-section {
        flex: 1;
    }

    .header-actions {
        display: flex;
        align-items: center;
    }

    .title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: -0.025em;
    }

    .title-highlight {
        color: #fef08a;
    }

    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        font-size: 1.125rem;
    }

    .search-section {
        display: flex;
        justify-content: center;
    }

    .main-content {
        flex: 1;
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem 1rem;
        width: 100%;
    }

    .results-info {
        text-align: center;
        margin-bottom: 1rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    .pokemon-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 1.25rem;
    }

    @media (min-width: 640px) {
        .pokemon-grid {
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1.5rem;
        }
    }

    @media (min-width: 1024px) {
        .pokemon-grid {
            grid-template-columns: repeat(5, 1fr);
        }
    }

    @media (min-width: 1280px) {
        .pokemon-grid {
            grid-template-columns: repeat(6, 1fr);
        }
    }

    /* Error State */
    .error-container {
        text-align: center;
        padding: 4rem 1rem;
    }

    .error-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .error-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.5rem;
    }

    .error-message {
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
    }

    .retry-button {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition:
            transform 0.2s,
            box-shadow 0.2s;
    }

    .retry-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }

    /* Loading State */
    .loading-container {
        text-align: center;
        padding: 4rem 1rem;
    }

    .loading-spinner {
        width: 48px;
        height: 48px;
        border: 4px solid var(--border-color);
        border-top-color: #ef4444;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .loading-text {
        color: var(--text-secondary);
        font-size: 1.125rem;
    }

    /* No Results State */
    .no-results {
        text-align: center;
        padding: 4rem 1rem;
    }

    .no-results-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .no-results-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.5rem;
    }

    .no-results-message {
        color: var(--text-secondary);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem 1rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
        border-top: 1px solid var(--border-color);
    }

    .footer a {
        color: #ef4444;
        text-decoration: none;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
    }
</style>
