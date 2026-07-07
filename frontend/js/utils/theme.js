/* ─── GabbyOS Theme Manager ─── */

const ThemeManager = {
    init() {
        const saved = localStorage.getItem('gabbyos-theme');
        if (saved) {
            this.setTheme(saved);
        } else {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.setTheme(prefersDark ? 'dark' : 'light');
        }
        
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    },
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
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