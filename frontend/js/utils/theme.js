/* ─── GabbyOS Theme Manager ─── */

const ThemeManager = {
    init() {
        // Load saved theme or default to light
        const saved = localStorage.getItem('gabbyos-theme');
        if (saved) {
            this.setTheme(saved);
        } else {
            // Check system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.setTheme(prefersDark ? 'dark' : 'light');
        }
        
        // Toggle button
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    },
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        const lightStylesheet = document.getElementById('theme-light');
        const darkStylesheet = document.getElementById('theme-dark');
        
        if (theme === 'dark') {
            lightStylesheet.disabled = true;
            darkStylesheet.disabled = false;
        } else {
            lightStylesheet.disabled = false;
            darkStylesheet.disabled = true;
        }
        
        localStorage.setItem('gabbyos-theme', theme);
    },
    
    toggle() {
        const current = document.documentElement.getAttribute('data-theme');
        this.setTheme(current === 'dark' ? 'light' : 'dark');
    },
    
    getCurrent() {
        return document.documentElement.getAttribute('data-theme') || 'light';
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => ThemeManager.init());