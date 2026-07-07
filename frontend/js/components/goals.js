const Goals = {
    goals: [],
    categories: [],
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        try {
            const [goals, categories] = await Promise.all([
                ApiClient.getGoals(),
                ApiClient.getCategories()
            ]);
            this.goals = goals;
            this.categories = categories;
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Goals</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template() {
        const goalsHtml = this.goals.length > 0
            ? this.goals.map(g => this.goalCard(g)).join('')
            : '<div class="empty-state"><h3>No goals yet</h3><p>Set long-term goals to guide your journey.</p></div>';
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Goals</h2>
                    <button class="btn btn-primary" onclick="Goals.showCreateForm()">${Icons.plus} New Goal</button>
                </div>
                <p class="text-secondary mb-lg">Long-term goals that give purpose to your daily routines.</p>
                <div class="cards-grid cards-grid-2">${goalsHtml}</div>
                <div id="goal-modal"></div>
            </div>
        `;
    },
    
    goalCard(goal) {
        const statusLabels = {
            'not_started': 'Not Started', 'in_progress': 'In Progress',
            'completed': 'Completed', 'abandoned': 'Abandoned'
        };
        
        const category = this.categories.find(c => c.id === goal.category_id);
        const progress = goal.target_value ? `${goal.current_progress || 0} / ${goal.target_value}` : `${goal.current_progress || 0}`;
        
        return `
                        <div class="card">
                <div class="card-header">
                    <span class="card-title" style="cursor:pointer;flex:1" onclick="Goals.showDetail('${goal.id}')">${goal.title}</span>
                    <div style="display:flex;gap:4px;align-items:center">
                        <span class="status-badge ${goal.status === 'in_progress' ? 'status-in_progress' : 'status-not_started'}">${statusLabels[goal.status] || goal.status}</span>
                        <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();Goals.deleteGoal('${goal.id}')" title="Delete">
                            ${Icons.trash}
                        </button>
                    </div>
                </div>
                ${goal.description ? `<p class="card-subtitle">${goal.description}</p>` : ''}
                <div class="card-body">
                    <div class="progress-section">
                        <div class="progress-label"><span>Progress</span><span>${progress}</span></div>
                        <div class="progress-bar"><div class="progress-fill" style="width:50%"></div></div>
                    </div>
                    <div style="font-size:12px;color:var(--text-tertiary);margin-top:8px">
                        ${category ? `Category: ${category.name}` : ''}
                        ${goal.deadline ? ` • Deadline: ${goal.deadline}` : ''}
                    </div>
                </div>
            </div>
        `;
    },
    
    showCreateForm(goalData = null) {
        const modal = document.getElementById('goal-modal');
        if (!modal) return;
        
        const g = goalData || {};
        const categoryOptions = this.categories.map(c => `<option value="${c.id}" ${g.category_id === c.id ? 'selected' : ''}>${c.name}</option>`).join('');
        
        const statusOptions = ['not_started', 'in_progress', 'completed', 'abandoned']
            .map(s => `<option value="${s}" ${g.status === s ? 'selected' : ''}>${s.replace('_', ' ')}</option>`).join('');
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Goals.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3 class="modal-title">${g.id ? 'Edit' : 'New'} Goal</h3>
                        <button class="modal-close" onclick="Goals.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Goals.handleSave(event, '${g.id || ''}')">
                        <div class="form-group"><label class="form-label">Title</label><input type="text" class="form-input" id="g-title" value="${g.title || ''}" required></div>
                        <div class="form-group"><label class="form-label">Description</label><input type="text" class="form-input" id="g-desc" value="${g.description || ''}"></div>
                        <div class="form-group"><label class="form-label">Category</label><select class="form-select" id="g-category"><option value="">None</option>${categoryOptions}</select></div>
                        <div class="form-group"><label class="form-label">Target Value</label><input type="text" class="form-input" id="g-target" value="${g.target_value || ''}" placeholder="e.g., ₦5M, 5 projects"></div>
                        <div class="form-group"><label class="form-label">Current Progress</label><input type="text" class="form-input" id="g-progress" value="${g.current_progress || ''}" placeholder="e.g., ₦500K, 2 projects"></div>
                        <div class="form-group"><label class="form-label">Status</label><select class="form-select" id="g-status">${statusOptions}</select></div>
                        <div class="form-group"><label class="form-label">Deadline</label><input type="date" class="form-input" id="g-deadline" value="${g.deadline || ''}"></div>
                        <button type="submit" class="btn btn-primary btn-block">Save Goal</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    showDetail(goalId) {
        const goal = this.goals.find(g => g.id === goalId);
        if (goal) this.showCreateForm(goal);
    },
    
    async handleSave(e, goalId) {
        e.preventDefault();
        
        const data = {
            title: document.getElementById('g-title').value,
            description: document.getElementById('g-desc').value,
            category_id: document.getElementById('g-category').value || null,
            target_value: document.getElementById('g-target').value,
            current_progress: document.getElementById('g-progress').value,
            status: document.getElementById('g-status').value,
            deadline: document.getElementById('g-deadline').value || null
        };
        
        try {
            if (goalId) {
                await ApiClient.request('PATCH', `/goals/${goalId}`, data);
            } else {
                await ApiClient.request('POST', '/goals', data);
            }
            Goals.closeModal();
            App.clearAllCache();
            App.router.navigate('goals', true);
        } catch (error) {
            alert(error.message);
        }
    },

    async deleteGoal(goalId) {
        if (confirm('Delete this goal?')) {
            try {
                await ApiClient.request('DELETE', `/goals/${goalId}`);
                App.clearAllCache();
                App.router.navigate('goals', true);
            } catch (error) {
                alert(error.message);
            }
        }
    },
    
    closeModal() {
        const modal = document.getElementById('goal-modal');
        if (modal) modal.innerHTML = '';
    }
};