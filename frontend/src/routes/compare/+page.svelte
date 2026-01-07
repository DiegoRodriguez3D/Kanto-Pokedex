<script lang="ts">
    import TypeBadge from "$lib/components/TypeBadge.svelte";
    import StatBar from "$lib/components/StatBar.svelte";
    import ThemeToggle from "$lib/components/ThemeToggle.svelte";
    import { getTypeGradient } from "$lib/typeColors";
    import {
        comparePokemon,
        fetchPokemonList,
        type PokemonDetail,
        type PokemonListItem,
    } from "$lib/api";
    import { onMount } from "svelte";

    // All pokemon for selection
    let allPokemon: PokemonListItem[] = $state([]);
    let loading = $state(true);
    let comparing = $state(false);
    let error = $state<string | null>(null);

    // Selected Pokemon (up to 3 slots)
    let selectedIds: (number | null)[] = $state([null, null, null]);
    let comparedPokemon: PokemonDetail[] = $state([]);

    onMount(async () => {
        try {
            const response = await fetchPokemonList();
            allPokemon = response.pokemon;
        } catch (err) {
            error = "Failed to load Pokemon list";
            console.error(err);
        } finally {
            loading = false;
        }
    });

    function handleSelect(index: number, id: string) {
        const numId = id ? parseInt(id, 10) : null;
        selectedIds[index] = numId;
        // Clear comparison when selection changes
        comparedPokemon = [];
    }

    async function handleCompare() {
        const ids = selectedIds.filter((id): id is number => id !== null);

        if (ids.length < 2) {
            error = "Please select at least 2 Pokemon to compare";
            return;
        }

        comparing = true;
        error = null;

        try {
            const response = await comparePokemon(ids);
            comparedPokemon = response.pokemon;
        } catch (err) {
            error = "Failed to compare Pokemon";
            console.error(err);
        } finally {
            comparing = false;
        }
    }

    function getMaxStat(statName: keyof PokemonDetail["stats"]): number {
        if (comparedPokemon.length === 0) return 0;
        return Math.max(...comparedPokemon.map((p) => p.stats[statName]));
    }

    function isHighestStat(
        pokemon: PokemonDetail,
        statName: keyof PokemonDetail["stats"],
    ): boolean {
        const max = getMaxStat(statName);
        return pokemon.stats[statName] === max && comparedPokemon.length > 1;
    }

    function formatId(id: number): string {
        return `#${id.toString().padStart(3, "0")}`;
    }

    const statLabels: { key: keyof PokemonDetail["stats"]; label: string }[] = [
        { key: "hp", label: "HP" },
        { key: "attack", label: "Attack" },
        { key: "defense", label: "Defense" },
        { key: "special_attack", label: "Sp. Atk" },
        { key: "special_defense", label: "Sp. Def" },
        { key: "speed", label: "Speed" },
    ];
</script>

<svelte:head>
    <title>Compare Pokémon - Kanto Pokédex</title>
    <meta
        name="description"
        content="Compare stats of multiple Kanto Pokemon side by side"
    />
</svelte:head>

<div class="compare-page">
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
        <h1 class="page-title">Compare Pokémon</h1>
        <ThemeToggle />
    </nav>

    <main class="content">
        {#if loading}
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p>Loading Pokémon...</p>
            </div>
        {:else if error && comparedPokemon.length === 0}
            <div class="error-message">{error}</div>
        {:else}
            <!-- Selection Panel -->
            <div class="selection-panel">
                <h2 class="section-title">Select Pokémon to Compare</h2>
                <div class="selectors">
                    {#each [0, 1, 2] as index}
                        <div class="selector-slot">
                            <select
                                class="pokemon-select"
                                value={selectedIds[index]?.toString() || ""}
                                onchange={(e) =>
                                    handleSelect(index, e.currentTarget.value)}
                            >
                                <option value=""
                                    >Select Pokémon {index + 1}</option
                                >
                                {#each allPokemon as pokemon}
                                    <option value={pokemon.id.toString()}>
                                        {formatId(pokemon.id)}
                                        {pokemon.name}
                                    </option>
                                {/each}
                            </select>
                            {#if selectedIds[index]}
                                {@const selectedPoke = allPokemon.find(
                                    (p) => p.id === selectedIds[index],
                                )}
                                {#if selectedPoke}
                                    <img
                                        src={selectedPoke.image}
                                        alt={selectedPoke.name}
                                        class="preview-image"
                                    />
                                {/if}
                            {/if}
                        </div>
                    {/each}
                </div>
                <button
                    class="compare-button"
                    onclick={handleCompare}
                    disabled={comparing ||
                        selectedIds.filter((id) => id !== null).length < 2}
                >
                    {comparing ? "Comparing..." : "Compare"}
                </button>
            </div>

            <!-- Comparison Results -->
            {#if comparedPokemon.length > 0}
                <div class="comparison-results">
                    <!-- Pokemon Headers -->
                    <div class="pokemon-headers">
                        {#each comparedPokemon as pokemon}
                            <a
                                href="/pokemon/{pokemon.id}"
                                class="pokemon-header"
                                style="background: {getTypeGradient(
                                    pokemon.types,
                                )}"
                            >
                                <img
                                    src={pokemon.image}
                                    alt={pokemon.name}
                                    class="header-image"
                                />
                                <h3 class="header-name">{pokemon.name}</h3>
                                <span class="header-id"
                                    >{formatId(pokemon.id)}</span
                                >
                                <div class="header-types">
                                    {#each pokemon.types as type}
                                        <TypeBadge {type} />
                                    {/each}
                                </div>
                            </a>
                        {/each}
                    </div>

                    <!-- Stats Comparison -->
                    <div class="stats-comparison">
                        <h2 class="section-title">Base Stats Comparison</h2>
                        <div class="stats-grid">
                            {#each statLabels as { key, label }}
                                <div class="stat-row">
                                    <span class="stat-label">{label}</span>
                                    <div class="stat-bars">
                                        {#each comparedPokemon as pokemon}
                                            <div
                                                class="stat-bar-container"
                                                class:highest={isHighestStat(
                                                    pokemon,
                                                    key,
                                                )}
                                            >
                                                <StatBar
                                                    label=""
                                                    value={pokemon.stats[key]}
                                                    showLabel={false}
                                                />
                                                <span class="stat-value"
                                                    >{pokemon.stats[key]}</span
                                                >
                                            </div>
                                        {/each}
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>

                    <!-- Total Stats -->
                    <div class="total-stats">
                        <h2 class="section-title">Total Base Stats</h2>
                        <div class="totals-row">
                            {#each comparedPokemon as pokemon}
                                {@const total = Object.values(
                                    pokemon.stats,
                                ).reduce((sum, val) => sum + val, 0)}
                                <div class="total-card">
                                    <span class="total-name"
                                        >{pokemon.name}</span
                                    >
                                    <span class="total-value">{total}</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>
            {/if}
        {/if}
    </main>
</div>

<style>
    .compare-page {
        min-height: 100vh;
        background: var(--bg-primary);
        padding: 1rem;
    }

    .nav {
        max-width: 1200px;
        margin: 0 auto;
        padding-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .back-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-primary);
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        background: var(--card-bg);
        transition: background 0.2s;
    }

    .back-link:hover {
        background: var(--border-color);
    }

    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    .content {
        max-width: 1200px;
        margin: 0 auto;
    }

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

    .error-message {
        text-align: center;
        padding: 1rem;
        background: #fee2e2;
        color: #dc2626;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }

    :global(.dark) .error-message {
        background: rgba(220, 38, 38, 0.2);
        color: #fca5a5;
    }

    /* Selection Panel */
    .selection-panel {
        background: var(--card-bg);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .section-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 1rem;
    }

    .selectors {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .selector-slot {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
    }

    .pokemon-select {
        width: 100%;
        padding: 0.75rem;
        border: 2px solid var(--border-color);
        border-radius: 0.5rem;
        background: var(--bg-primary);
        color: var(--text-primary);
        font-size: 0.875rem;
        cursor: pointer;
    }

    .pokemon-select:focus {
        outline: none;
        border-color: #ef4444;
    }

    .preview-image {
        width: 80px;
        height: 80px;
        object-fit: contain;
    }

    .compare-button {
        display: block;
        width: 100%;
        max-width: 200px;
        margin: 0 auto;
        padding: 0.875rem 1.5rem;
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition:
            transform 0.2s,
            box-shadow 0.2s;
    }

    .compare-button:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }

    .compare-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* Comparison Results */
    .comparison-results {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .pokemon-headers {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
    }

    .pokemon-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1.5rem;
        border-radius: 1rem;
        text-decoration: none;
        transition: transform 0.2s;
    }

    .pokemon-header:hover {
        transform: translateY(-4px);
    }

    .header-image {
        width: 100px;
        height: 100px;
        object-fit: contain;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
    }

    .header-name {
        color: white;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0.5rem 0 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .header-id {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.875rem;
        font-weight: 600;
    }

    .header-types {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    /* Stats Comparison */
    .stats-comparison {
        background: var(--card-bg);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stats-grid {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .stat-row {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .stat-label {
        flex: 0 0 80px;
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    .stat-bars {
        flex: 1;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 0.75rem;
    }

    .stat-bar-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem;
        border-radius: 0.25rem;
    }

    .stat-bar-container.highest {
        background: rgba(34, 197, 94, 0.1);
    }

    :global(.dark) .stat-bar-container.highest {
        background: rgba(34, 197, 94, 0.2);
    }

    .stat-value {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        min-width: 30px;
    }

    /* Total Stats */
    .total-stats {
        background: var(--card-bg);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .totals-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
    }

    .total-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1rem;
        background: var(--bg-primary);
        border-radius: 0.75rem;
        gap: 0.25rem;
    }

    .total-name {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }

    .total-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    @media (max-width: 640px) {
        .page-title {
            font-size: 1rem;
        }

        .stat-label {
            flex: 0 0 60px;
            font-size: 0.75rem;
        }
    }
</style>
