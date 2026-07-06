/* ─── GabbyOS App ─── */

const App = {
    router: {
        routes: {},
        
        initRoutes() {
            this.routes = {
                'dashboard': Dashboard,
                'planner': Planner,
                'routines': Routines,
                'knowledge': Knowledge,
                'projects': Projects,
                'goals': Goals,
                'reflections': Reflections,
                'categories': Categories,
                'analytics': Analytics,
                'inbox': Inbox,
            };
        },
        
        async navigate(page) {
            const mainContent = document.getElementById('main-content');
            if (!mainContent) return;
            
            // Update active nav
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.toggle('active', item.dataset.page === page);
            });
            
            // Show loading
            mainContent.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-tertiary);font-family:Inter,sans-serif">Loading...</div>';
            
            // Get component
            const component = this.routes[page];
            if (component && typeof component.render === 'function') {
                try {
                    const html = await component.render();
                    mainContent.innerHTML = html;
                } catch (err) {
                    mainContent.innerHTML = `<div class="page" style="padding:48px"><h2>Error</h2><p style="color:var(--text-secondary)">${err.message}</p></div>`;
                }
            }
            
            // Update URL hash
            window.location.hash = page;
        },
        
        init() {
            this.initRoutes();
            
            // Handle navigation clicks
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.navigate(item.dataset.page);
                });
            });
            
            // Handle browser back/forward
            window.addEventListener('hashchange', () => {
                const page = window.location.hash.replace('#', '') || 'dashboard';
                this.navigate(page);
            });
            
            // Load initial page
            const initialPage = window.location.hash.replace('#', '') || 'dashboard';
            this.navigate(initialPage);
        }
    },
    
    init() {
        ThemeManager.init();
        this.router.init();
    }
};

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}