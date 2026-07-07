const Analytics = {
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            const data = await ApiClient.getAnalytics();
            return this.template(data);
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Analytics</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template(data) {
        const comp = data.completion_rates || {};
        const overview = data.overview || {};
        
        return `
            <div class="page">
                <h2 class="section-title mb-lg">Analytics</h2>
                
                <div class="cards-grid cards-grid-3 mb-lg">
                    <div class="card stat-card">
                        <div class="stat-value">${comp.daily?.percentage || 0}%</div>
                        <div class="stat-label">Daily Completion</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-value">${comp.weekly?.percentage || 0}%</div>
                        <div class="stat-label">Weekly Completion</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-value">${comp.monthly?.percentage || 0}%</div>
                        <div class="stat-label">Monthly Completion</div>
                    </div>
                </div>
                
                <div class="cards-grid cards-grid-3 mb-lg">
                    <div class="card stat-card">
                        <div class="stat-value">${overview.total_routines || 0}</div>
                        <div class="stat-label">Active Routines</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-value">${overview.total_projects || 0}</div>
                        <div class="stat-label">Active Projects</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-value">${data.inbox_count || 0}</div>
                        <div class="stat-label">Inbox Items</div>
                    </div>
                </div>
                
                ${data.hours_by_category && data.hours_by_category.length > 0 ? `
                    <div class="section-header"><h3>Hours by Category</h3></div>
                    ${data.hours_by_category.map(h => `
                        <div class="card mb-sm">
                            <div style="display:flex;justify-content:space-between;align-items:center">
                                <span>${h.category}</span>
                                <span class="tag">${h.hours}h (${h.completed_routines} routines)</span>
                            </div>
                        </div>
                    `).join('')}
                ` : ''}
                
                ${data.current_streaks && data.current_streaks.top_streaks && data.current_streaks.top_streaks.length > 0 ? `
                    <div class="section-header mt-lg"><h3>Top Streaks</h3></div>
                    ${data.current_streaks.top_streaks.map(s => `
                        <div class="card mb-sm">
                            <div style="display:flex;justify-content:space-between">
                                <span>${s.routine}</span>
                                <span class="status-badge status-in_progress">${s.current_streak} day streak</span>
                            </div>
                        </div>
                    `).join('')}
                ` : ''}
                            ${data.top_routines && data.top_routines.length > 0 ? `
                    <div class="section-header mt-lg"><h3>Most Completed Routines</h3></div>
                    ${data.top_routines.map(r => `
                        <div class="card mb-sm">
                            <div style="display:flex;justify-content:space-between;align-items:center">
                                <span>${r.routine}</span>
                                <span class="tag">${r.completions} times</span>
                            </div>
                            <div style="font-size:11px;color:var(--text-tertiary)">${r.category || ''}</div>
                        </div>
                    `).join('')}
                ` : ''}
                
                ${data.bottom_routines && data.bottom_routines.length > 0 ? `
                    <div class="section-header mt-lg"><h3>Least Completed Routines</h3></div>
                    ${data.bottom_routines.map(r => `
                        <div class="card mb-sm">
                            <div style="display:flex;justify-content:space-between;align-items:center">
                                <span>${r.routine}</span>
                                <span class="tag">${r.completions} times</span>
                            </div>
                            <div style="font-size:11px;color:var(--text-tertiary)">${r.category || ''}</div>
                        </div>
                    `).join('')}
                ` : ''}
            </div>
        `;
    }
};