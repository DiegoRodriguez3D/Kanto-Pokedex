<script lang="ts">
    interface Props {
        label: string;
        value: number;
        maxValue?: number;
    }

    let { label, value, maxValue = 255 }: Props = $props();

    // Calculate percentage (max base stat is around 255)
    const percentage = $derived(Math.min((value / maxValue) * 100, 100));

    // Determine bar color based on stat value
    function getBarColor(val: number): string {
        if (val < 50) return "#ef4444"; // Red
        if (val < 80) return "#f97316"; // Orange
        if (val < 100) return "#eab308"; // Yellow
        if (val < 130) return "#84cc16"; // Lime
        return "#22c55e"; // Green
    }

    const barColor = $derived(getBarColor(value));
</script>

<div class="stat-row">
    <span class="stat-label">{label}</span>
    <div class="stat-bar-container">
        <div
            class="stat-bar"
            style="width: {percentage}%; background-color: {barColor};"
        ></div>
    </div>
    <span class="stat-value">{value}</span>
</div>

<style>
    .stat-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        width: 5rem;
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-align: left;
    }

    :global(.dark) .stat-label {
        color: #94a3b8;
    }

    .stat-bar-container {
        flex: 1;
        height: 0.625rem;
        background-color: #e2e8f0;
        border-radius: 9999px;
        overflow: hidden;
    }

    :global(.dark) .stat-bar-container {
        background-color: #334155;
    }

    .stat-bar {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.5s ease-out;
    }

    .stat-value {
        width: 2.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        color: #334155;
        text-align: right;
    }

    :global(.dark) .stat-value {
        color: #e2e8f0;
    }
</style>
