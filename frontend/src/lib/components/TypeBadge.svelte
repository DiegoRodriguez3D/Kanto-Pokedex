<script lang="ts">
    import { getTypeColor } from '$lib/typeColors';
    
    interface Props {
        type: string;
    }
    
    let { type }: Props = $props();
    
    const colors = $derived(getTypeColor(type));
</script>

<span 
    class="type-badge"
    style="background-color: {colors.main}; color: white;"
>
    {type.charAt(0).toUpperCase() + type.slice(1)}
</span>

<style>
    .type-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: capitalize;
        letter-spacing: 0.025em;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
</style>
