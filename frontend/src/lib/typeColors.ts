/**
 * Pokemon type colors for consistent theming throughout the app.
 * Each type has a main color, background color (lighter), and text color.
 */
export const typeColors: Record<string, { main: string; bg: string; text: string }> = {
    normal: { main: '#A8A878', bg: '#e8e8d8', text: '#6D6D4E' },
    fire: { main: '#F08030', bg: '#fde2d4', text: '#9C531F' },
    water: { main: '#6890F0', bg: '#d4e4f5', text: '#445E9C' },
    electric: { main: '#F8D030', bg: '#fdf5d4', text: '#A1871F' },
    grass: { main: '#78C850', bg: '#d4f5d8', text: '#4E8234' },
    ice: { main: '#98D8D8', bg: '#d4f0f0', text: '#638D8D' },
    fighting: { main: '#C03028', bg: '#f5d4d4', text: '#7D1F1A' },
    poison: { main: '#A040A0', bg: '#e8d4e8', text: '#682A68' },
    ground: { main: '#E0C068', bg: '#f5ead8', text: '#927D44' },
    flying: { main: '#A890F0', bg: '#e0d8f8', text: '#6D5E9C' },
    psychic: { main: '#F85888', bg: '#f8d8e0', text: '#A13959' },
    bug: { main: '#A8B820', bg: '#e8ecd4', text: '#6D7815' },
    rock: { main: '#B8A038', bg: '#ece6d4', text: '#786824' },
    ghost: { main: '#705898', bg: '#ddd8e8', text: '#493963' },
    dragon: { main: '#7038F8', bg: '#ddd4f8', text: '#4924A1' },
    dark: { main: '#705848', bg: '#d8d4d0', text: '#49392F' },
    steel: { main: '#B8B8D0', bg: '#e8e8f0', text: '#787887' },
    fairy: { main: '#EE99AC', bg: '#f8e0e8', text: '#9B6470' },
};

/**
 * Get the color scheme for a Pokemon type.
 * Returns a default color if type is not found.
 */
export function getTypeColor(type: string): { main: string; bg: string; text: string } {
    return typeColors[type.toLowerCase()] || typeColors.normal;
}

/**
 * Get gradient CSS for a Pokemon based on its types.
 * Creates a beautiful gradient for the detail view background.
 */
export function getTypeGradient(types: string[]): string {
    if (types.length === 0) {
        return 'linear-gradient(135deg, #A8A878 0%, #C8C8A8 100%)';
    }

    if (types.length === 1) {
        const color = getTypeColor(types[0]);
        return `linear-gradient(135deg, ${color.main} 0%, ${lightenColor(color.main, 20)} 100%)`;
    }

    const color1 = getTypeColor(types[0]);
    const color2 = getTypeColor(types[1]);
    return `linear-gradient(135deg, ${color1.main} 0%, ${color2.main} 100%)`;
}

/**
 * Utility to lighten a hex color.
 */
function lightenColor(hex: string, percent: number): string {
    const num = parseInt(hex.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = ((num >> 8) & 0x00ff) + amt;
    const B = (num & 0x0000ff) + amt;
    return `#${(
        0x1000000 +
        (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
        (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
        (B < 255 ? (B < 1 ? 0 : B) : 255)
    )
        .toString(16)
        .slice(1)}`;
}
