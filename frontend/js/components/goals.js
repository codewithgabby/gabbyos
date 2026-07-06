const Goals = {
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        try {
            const goals = await ApiClient.getGoals();
            const html = goals.length > 0
                ? goals.map(g => `<div class="card"><div class="card-header"><span class="card-title">${g.title}</span><span class="tag">${g.status}</span></div><p class="card-subtitle">${g.current_progress || '0'} / ${g.target_value || 'TBD'}</p></div>`).join('')
                : '<div class="empty-state"><h3>No goals yet</h3><p>Set long-term goals to guide your journey.</p></div>';
            return `<div class="page"><div class="section-header"><h2 class="section-title">Goals</h2></div>${html}</div>`;
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Goals</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    }
};