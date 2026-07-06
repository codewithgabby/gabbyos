const Reflections = {
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        try {
            const reflection = await ApiClient.getTodayReflection();
            return `
                <div class="page">
                    <div class="section-header"><h2 class="section-title">Today's Reflection</h2></div>
                    ${reflection ? `
                        <div class="card mb-md"><div class="card-header"><span class="card-title">Wins</span></div><p>${reflection.wins || 'Not yet written'}</p></div>
                        <div class="card mb-md"><div class="card-header"><span class="card-title">Challenges</span></div><p>${reflection.challenges || 'Not yet written'}</p></div>
                        <div class="card mb-md"><div class="card-header"><span class="card-title">Gratitude</span></div><p>${reflection.gratitude || 'Not yet written'}</p></div>
                        <div class="card"><div class="card-header"><span class="card-title">Tomorrow's Focus</span></div><p>${reflection.tomorrow_focus || 'Not yet written'}</p></div>
                    ` : '<div class="empty-state"><h3>No reflection today</h3><p>Take a moment to reflect on your day.</p></div>'}
                </div>
            `;
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Reflections</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    }
};