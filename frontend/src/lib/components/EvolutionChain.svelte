<script lang="ts">
    import type { EvolutionStage } from "$lib/api";

    interface Props {
        chain: EvolutionStage[];
    }

    let { chain }: Props = $props();

    function getEvolutionTrigger(stage: EvolutionStage): string {
        if (!stage.trigger) return "";

        if (stage.min_level) {
            return `Lv. ${stage.min_level}`;
        }
        if (stage.trigger_item) {
            return stage.trigger_item;
        }
        if (stage.trigger === "trade") {
            return "Trade";
        }
        if (stage.trigger === "level-up") {
            return "Level Up";
        }
        return stage.trigger.replace("-", " ");
    }
</script>

{#if chain.length > 1}
    <div class="evolution-section">
        <h2 class="section-title">Evolution Chain</h2>
        <div class="evolution-chain">
            {#each chain as stage, index}
                <a href="/pokemon/{stage.id}" class="evolution-stage">
                    <div class="stage-image-container">
                        <img
                            src={stage.image}
                            alt={stage.name}
                            class="stage-image"
                            loading="lazy"
                        />
                    </div>
                    <span class="stage-name">{stage.name}</span>
                    {#if index > 0}
                        <span class="stage-trigger"
                            >{getEvolutionTrigger(stage)}</span
                        >
                    {/if}
                </a>
                {#if index < chain.length - 1}
                    <div class="evolution-arrow">
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
                            <path d="m9 18 6-6-6-6" />
                        </svg>
                    </div>
                {/if}
            {/each}
        </div>
    </div>
{/if}

<style>
    .evolution-section {
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 1rem;
    }

    :global(.dark) .section-title {
        color: #f1f5f9;
    }

    .evolution-chain {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 1rem;
    }

    :global(.dark) .evolution-chain {
        background: rgba(15, 23, 42, 0.5);
    }

    .evolution-stage {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        padding: 0.75rem;
        border-radius: 0.75rem;
        transition: all 0.2s ease;
        min-width: 80px;
    }

    .evolution-stage:hover {
        background: rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }

    :global(.dark) .evolution-stage:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .stage-image-container {
        width: 70px;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .stage-image {
        width: 100%;
        height: 100%;
        object-fit: contain;
        transition: transform 0.2s ease;
    }

    .evolution-stage:hover .stage-image {
        transform: scale(1.1);
    }

    .stage-name {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 0.25rem;
    }

    :global(.dark) .stage-name {
        color: #f1f5f9;
    }

    .stage-trigger {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.125rem;
    }

    :global(.dark) .stage-trigger {
        color: #94a3b8;
    }

    .evolution-arrow {
        color: #94a3b8;
        display: flex;
        align-items: center;
    }

    :global(.dark) .evolution-arrow {
        color: #64748b;
    }

    @media (max-width: 480px) {
        .stage-image-container {
            width: 55px;
            height: 55px;
        }

        .stage-name {
            font-size: 0.75rem;
        }

        .evolution-arrow svg {
            width: 18px;
            height: 18px;
        }
    }
</style>
