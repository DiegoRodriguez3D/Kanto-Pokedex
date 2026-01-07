/**
 * Theme store for managing dark/light mode across the application.
 * Uses Svelte 5 runes and persists preference to localStorage.
 */

import { browser } from '$app/environment';

// Initialize theme from localStorage or system preference
function getInitialTheme(): 'light' | 'dark' {
    if (!browser) return 'light';

    const stored = localStorage.getItem('theme');
    if (stored === 'dark' || stored === 'light') {
        return stored;
    }

    // Check system preference
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }

    return 'light';
}

// Create reactive theme state
let currentTheme = $state<'light' | 'dark'>(getInitialTheme());

export function getTheme(): 'light' | 'dark' {
    return currentTheme;
}

export function setTheme(theme: 'light' | 'dark'): void {
    currentTheme = theme;
    if (browser) {
        localStorage.setItem('theme', theme);
        updateDocumentClass(theme);
    }
}

export function toggleTheme(): void {
    setTheme(currentTheme === 'light' ? 'dark' : 'light');
}

export function isDarkMode(): boolean {
    return currentTheme === 'dark';
}

function updateDocumentClass(theme: 'light' | 'dark'): void {
    if (browser) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }
}

// Initialize on load
if (browser) {
    updateDocumentClass(getInitialTheme());
}
