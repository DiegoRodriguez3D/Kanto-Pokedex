<script lang="ts">
    import { toggleTheme, isDarkMode } from "$lib/theme.svelte";

    const dark = $derived(isDarkMode());
</script>

<button
    class="theme-toggle"
    onclick={toggleTheme}
    aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
    title={dark ? "Switch to light mode" : "Switch to dark mode"}
>
    {#if dark}
        <!-- Sun icon for dark mode -->
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
            <circle cx="12" cy="12" r="4"></circle>
            <path d="M12 2v2"></path>
            <path d="M12 20v2"></path>
            <path d="m4.93 4.93 1.41 1.41"></path>
            <path d="m17.66 17.66 1.41 1.41"></path>
            <path d="M2 12h2"></path>
            <path d="M20 12h2"></path>
            <path d="m6.34 17.66-1.41 1.41"></path>
            <path d="m19.07 4.93-1.41 1.41"></path>
        </svg>
    {:else}
        <!-- Moon icon for light mode -->
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
            <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>
        </svg>
    {/if}
</button>

<style>
    .theme-toggle {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        transition: all 0.2s ease;
        background: rgba(255, 255, 255, 0.2);
        color: white;
    }

    .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }

    :global(.dark) .theme-toggle {
        background: rgba(255, 255, 255, 0.1);
        color: #fef08a;
    }

    :global(.dark) .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.2);
    }
</style>
