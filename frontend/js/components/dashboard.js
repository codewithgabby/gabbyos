/* ─── GabbyOS Dashboard Component ─── */

const Dashboard = {
    async render() {
        if (!ApiClient.isAuthenticated()) {
            return AuthPage.render();
        }
        
        try {
            const [data, streaksData] = await Promise.all([
                ApiClient.getDashboard(),
                ApiClient.getStreaks()
            ]);
            return this.template(data, streaksData);
        } catch (error) {
            return this.errorTemplate(error.message);
        }
    },
    
    template(data, streaksData = []) {
        const { greeting, current_date, day_of_week, identity_statement, today_routines, completion_percentage, completed_count, total_count, quote } = data;
        
        const activeStreaks = streaksData.filter(s => s.current_streak > 0);
        const streaksHtml = activeStreaks.length > 0 ? `
            <div class="section-header mt-lg">
                <h2 class="section-title">Active Streaks</h2>
            </div>
            <div class="cards-grid cards-grid-3 mb-lg">
                ${activeStreaks.slice(0, 6).map(s => `
                    <div class="card stat-card">
                        <div class="stat-value" style="font-size:20px">${s.current_streak} ${Icons.streak}</div>
                        <div class="stat-label">${s.routine_title || 'Routine'}</div>
                        <div style="font-size:11px;color:var(--text-tertiary)">Best: ${s.longest_streak} days</div>
                    </div>
                `).join('')}
            </div>
        ` : '';
        
        const routinesHtml = today_routines && today_routines.length > 0 
            ? today_routines.map(r => this.routineCard(r)).join('')
            : this.emptyRoutines();
        
        return `
            <div class="page" id="page-dashboard">
                <div class="dashboard-header">
                    <h1 class="greeting">${greeting || 'Good Morning'}</h1>
                    <p class="date-text">${day_of_week || ''}, ${this.formatDate(current_date)}</p>
                </div>
                
                ${identity_statement ? `
                    <div class="identity-statement">
                        "${identity_statement}"
                    </div>
                ` : ''}
                
                <div class="progress-section">
                    <div class="progress-label">
                        <span>Today's Progress</span>
                        <span>${completed_count || 0}/${total_count || 0} complete</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${completion_percentage || 0}%"></div>
                    </div>
                </div>
                
                <div class="section-header">
                    <h2 class="section-title">Today's Routines</h2>
                </div>
                
                <div class="routines-grid">
                    ${routinesHtml}
                </div>
                
                                ${streaksHtml}
                
                ${quote ? `
                    <div class="daily-quote">
                        <p class="quote-text">${quote}</p>
                    </div>
                ` : ''}
            </div>
        `;
    },
    
    routineCard(routine) {
        const statusClass = `status-${routine.status || 'not_started'}`;
        const statusLabels = {
            'not_started': 'Not Started',
            'in_progress': 'In Progress',
            'completed': 'Completed',
            'skipped': 'Skipped'
        };
        
        return `
            <div class="routine-card" onclick="Dashboard.cycleStatus('${routine.log_id}', '${routine.status}')">
                <div class="routine-card-header">
                    <span class="routine-title">${routine.title || 'Untitled'}</span>
                    ${routine.category_name ? `<span class="routine-category">${routine.category_name}</span>` : ''}
                </div>
                <div class="routine-meta">
                    <span>${Icons.clock} ${routine.duration_minutes || 0}min</span>
                    <span class="status-badge ${statusClass}">
                        ${statusLabels[routine.status] || routine.status || 'Not Started'}
                    </span>
                </div>
            </div>
        `;
    },
    
    emptyRoutines() {
        return `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3">
                    <rect x="3" y="4" width="18" height="18" rx="2"/>
                    <path d="M16 2v4M8 2v4M3 10h18"/>
                </svg>
                <h3>No routines planned for today</h3>
                <p>Create a weekly plan to see your routines here.</p>
            </div>
        `;
    },
    
    async cycleStatus(logId, currentStatus) {
        const nextStatus = {
            'not_started': 'in_progress',
            'in_progress': 'completed',
            'completed': 'not_started'
        };
        
        const newStatus = nextStatus[currentStatus] || 'in_progress';
        
        try {
            await ApiClient.updateLog(logId, { status: newStatus });
            App.clearAllCache();
            App.router.navigate('dashboard', true);
        } catch (error) {
            console.error('Failed to update status:', error);
        }
    },
    
    formatDate(dateStr) {
        if (!dateStr) return '';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateStr).toLocaleDateString('en-US', options);
    },
    
    errorTemplate(message) {
        return `
            <div class="page" style="padding:48px">
                <div class="empty-state">
                    <h3>Couldn't load dashboard</h3>
                    <p>${message}</p>
                </div>
            </div>
        `;
    }
};