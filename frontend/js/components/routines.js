const Routines = {
    routines: [],
    categories: [],
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            this.routines = await ApiClient.getRoutines();
            this.categories = await ApiClient.getCategories();
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Routines</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template() {
        const routinesHtml = this.routines.length > 0
            ? this.routines.map(r => this.routineCard(r)).join('')
            : this.emptyState();
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Routines</h2>
                    <button class="btn btn-primary" onclick="Routines.showCreateForm()">
                        ${Icons.plus} New Routine
                    </button>
                </div>
                
                <p class="text-secondary mb-lg">Your daily disciplines with purpose.</p>
                
                <div class="cards-grid cards-grid-2">
                    ${routinesHtml}
                </div>
                
                <div id="routine-modal"></div>
            </div>
        `;
    },
    
    routineCard(routine) {
        const priorityClass = `priority-${routine.priority || 'medium'}`;
        const category = this.categories.find(c => c.id === routine.category_id);
        
        return `
            <div class="card routine-detail-card">
                <div class="card-header">
                    <div>
                        <span class="card-title">${routine.title}</span>
                        ${category ? `<span class="tag" style="margin-left:8px">${category.name}</span>` : ''}
                    </div>
                    <span class="status-badge ${routine.is_active ? 'status-in_progress' : 'status-not_started'}">
                        ${routine.is_active ? 'Active' : 'Inactive'}
                    </span>
                </div>
                
                ${routine.description ? `<p class="card-subtitle">${routine.description}</p>` : ''}
                
                <div class="card-body">
                    ${routine.reason_why ? `<p style="margin-bottom:8px"><strong>Why:</strong> ${routine.reason_why}</p>` : ''}
                    <div class="routine-meta">
                        <span>${Icons.clock} ${routine.duration_minutes} min</span>
                        <span>Priority: ${routine.priority}</span>
                    </div>
                </div>
                
                <div class="card-footer">
                    <button class="btn btn-ghost btn-sm" onclick="Routines.toggleRoutine('${routine.id}')">
                        ${routine.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                    <button class="btn btn-ghost btn-sm" onclick="Routines.deleteRoutine('${routine.id}')">
                        ${Icons.trash} Delete
                    </button>
                </div>
            </div>
        `;
    },
    
    emptyState() {
        return `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                </svg>
                <h3>No routines yet</h3>
                <p>Create your first routine to start building discipline.</p>
            </div>
        `;
    },
    
    showCreateForm() {
        const modal = document.getElementById('routine-modal');
        if (!modal) return;
        
        const categoryOptions = this.categories.map(c => 
            `<option value="${c.id}">${c.name}</option>`
        ).join('');
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Routines.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3 class="modal-title">New Routine</h3>
                        <button class="modal-close" onclick="Routines.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Routines.handleCreate(event)">
                        <div class="form-group">
                            <label class="form-label">Title</label>
                            <input type="text" class="form-input" id="routine-title" placeholder="e.g., AI/ML Class" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Description</label>
                            <input type="text" class="form-input" id="routine-desc" placeholder="Brief description">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Category</label>
                            <select class="form-select" id="routine-category">
                                <option value="">None</option>
                                ${categoryOptions}
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Duration (minutes)</label>
                            <input type="number" class="form-input" id="routine-duration" value="30" min="1" max="1440" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Reason Why</label>
                            <input type="text" class="form-input" id="routine-reason" placeholder="Why are you doing this?">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Priority</label>
                            <select class="form-select" id="routine-priority">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                                <option value="urgent">Urgent</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary btn-block">Create Routine</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleCreate(e) {
        e.preventDefault();
        
        const data = {
            title: document.getElementById('routine-title').value,
            description: document.getElementById('routine-desc').value,
            category_id: document.getElementById('routine-category').value || null,
            duration_minutes: parseInt(document.getElementById('routine-duration').value),
            reason_why: document.getElementById('routine-reason').value,
            priority: document.getElementById('routine-priority').value,
        };
        
        try {
            await ApiClient.createRoutine(data);
            Routines.closeModal();
            App.router.navigate('routines');
        } catch (error) {
            alert(error.message);
        }
    },
    
    async toggleRoutine(id) {
        try {
            await ApiClient.toggleRoutine(id);
            App.router.navigate('routines');
        } catch (error) {
            alert(error.message);
        }
    },
    
    async deleteRoutine(id) {
        if (confirm('Delete this routine?')) {
            try {
                await ApiClient.deleteRoutine(id);
                App.router.navigate('routines');
            } catch (error) {
                alert(error.message);
            }
        }
    },
    
    closeModal() {
        const modal = document.getElementById('routine-modal');
        if (modal) modal.innerHTML = '';
    }
};