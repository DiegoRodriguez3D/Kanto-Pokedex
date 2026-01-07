<script lang="ts">
	import "./layout.css";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link
		rel="preconnect"
		href="https://fonts.gstatic.com"
		crossorigin="anonymous"
	/>
	<link
		href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
		rel="stylesheet"
	/>
	<meta
		name="description"
		content="Kanto Pokedex - Explore all 151 original Pokémon with detailed stats, types, and descriptions."
	/>
</svelte:head>

{@render children()}
