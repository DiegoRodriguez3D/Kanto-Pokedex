<script lang="ts">
    interface Props {
        value: string;
        placeholder?: string;
        onInput: (value: string) => void;
    }

    let { value, placeholder = "Search Pokémon...", onInput }: Props = $props();

    function handleInput(event: Event) {
        const target = event.target as HTMLInputElement;
        onInput(target.value);
    }

    function clearSearch() {
        onInput("");
    }
</script>

<div class="search-container">
    <div class="search-icon">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
        </svg>
    </div>

    <input
        type="text"
        class="search-input"
        {placeholder}
        {value}
        oninput={handleInput}
    />

    {#if value}
        <button
            class="clear-button"
            onclick={clearSearch}
            aria-label="Clear search"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
            </svg>
        </button>
    {/if}
</div>

<style>
    .search-container {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
        max-width: 400px;
    }

    .search-icon {
        position: absolute;
        left: 1rem;
        color: #94a3b8;
        pointer-events: none;
    }

    .search-input {
        width: 100%;
        padding: 0.75rem 2.5rem 0.75rem 3rem;
        border-radius: 9999px;
        border: 2px solid transparent;
        background: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        color: #1e293b;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .search-input::placeholder {
        color: #94a3b8;
    }

    .search-input:focus {
        outline: none;
        border-color: #ef4444;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
    }

    .clear-button {
        position: absolute;
        right: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.25rem;
        border: none;
        background: transparent;
        color: #94a3b8;
        cursor: pointer;
        border-radius: 50%;
        transition: all 0.2s ease;
    }

    .clear-button:hover {
        color: #64748b;
        background: #f1f5f9;
    }

    /* Dark mode styles */
    :global(.dark) .search-input {
        background: rgba(30, 41, 59, 0.9);
        color: #f1f5f9;
    }

    :global(.dark) .search-input::placeholder {
        color: #64748b;
    }

    :global(.dark) .search-icon {
        color: #64748b;
    }

    :global(.dark) .clear-button {
        color: #64748b;
    }

    :global(.dark) .clear-button:hover {
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.1);
    }
</style>
