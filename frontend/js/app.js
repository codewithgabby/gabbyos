/* ─── GabbyOS App ─── */

const App = {
    dataCache: {},
    htmlCache: {},
    
    clearAllCache() {
        this.htmlCache = {};
        this.dataCache = {};
    },

    async handleLogout() {
        try {
            await ApiClient.logout();
        } catch (e) {
            // Ignore errors
        }
        ApiClient.clearToken();
        this.clearAllCache();
        this.router.navigate('dashboard', true);
    },
    
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
                'guide': Guide,
            };
        },
        
        async navigate(page, forceRefresh = false) {
            const mainContent = document.getElementById('main-content');
            if (!mainContent) return;
            
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.toggle('active', item.dataset.page === page);
            });
            
            // On nav clicks, force fresh data. On back/forward, use cache.
            if (forceRefresh) {
                delete App.htmlCache[page];
            }
            
            // Show cached HTML instantly if available
            if (App.htmlCache[page]) {
                mainContent.innerHTML = App.htmlCache[page];
                window.location.hash = page;
                return;
            }
            
            // Show loading
            mainContent.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-tertiary);font-family:Inter,sans-serif">Loading...</div>';
            
            const component = this.routes[page];
            if (component && typeof component.render === 'function') {
                try {
                    const html = await component.render();
                    mainContent.innerHTML = html;
                    if (!forceRefresh) {
                        App.htmlCache[page] = html;
                    }
                                } catch (err) {
                    console.error('Navigation error:', err);
                    // If session expired, clear token and show login
                    if (err.message.includes('Session expired') || err.message.includes('401')) {
                        ApiClient.clearToken();
                        App.clearAllCache();
                        mainContent.innerHTML = '';
                        this.navigate('dashboard', true);
                    } else {
                        mainContent.innerHTML = `<div class="page" style="padding:48px"><h2>Error</h2><p style="color:var(--text-secondary)">${err.message}</p></div>`;
                    }
                }
            }
            
            window.location.hash = page;
        },

        
        
        init() {
            this.initRoutes();
            
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.navigate(item.dataset.page, true);
                });
            });
            
            window.addEventListener('hashchange', () => {
                const page = window.location.hash.replace('#', '') || 'dashboard';
                this.navigate(page, false);
            });
            
            const initialPage = window.location.hash.replace('#', '') || 'dashboard';
            this.navigate(initialPage);
        }
    },
    
    init() {
        ThemeManager.init();
        this.router.init();
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}