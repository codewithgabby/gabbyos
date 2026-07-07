const Projects = {
    projects: [],
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            this.projects = await ApiClient.getProjects();
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Projects</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template() {
        const projectsHtml = this.projects.length > 0
            ? this.projects.map(p => this.projectCard(p)).join('')
            : this.emptyState();
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Projects</h2>
                    <button class="btn btn-primary" onclick="Projects.showCreateForm()">
                        ${Icons.plus} New Project
                    </button>
                </div>
                <p class="text-secondary mb-lg">Track what you're building.</p>
                <div class="cards-grid cards-grid-2">${projectsHtml}</div>
                <div id="project-modal"></div>
            </div>
        `;
    },
    
    projectCard(project) {
        const statusLabels = {
            'planned': 'Planned', 'in_progress': 'In Progress',
            'paused': 'Paused', 'completed': 'Completed', 'archived': 'Archived'
        };
        
        return `
            <div class="card">
                <div class="card-header">
                    <span class="card-title" style="cursor:pointer;flex:1" onclick="Projects.showDetail('${project.id}')">${project.title}</span>
                    <div style="display:flex;gap:4px;align-items:center">
                        <span class="status-badge ${project.status === 'in_progress' ? 'status-in_progress' : 'status-not_started'}">${statusLabels[project.status] || project.status}</span>
                        <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();Projects.deleteProject('${project.id}')" title="Delete">${Icons.trash}</button>
                    </div>
                </div>
                ${project.description ? `<p class="card-subtitle">${project.description}</p>` : ''}
                ${project.current_phase ? `<p class="text-tertiary" style="font-size:12px">Phase: ${project.current_phase}</p>` : ''}
                <div class="card-body">
                    <div class="progress-section">
                        <div class="progress-label"><span>Progress</span><span>${project.progress_percentage || 0}%</span></div>
                        <div class="progress-bar"><div class="progress-fill" style="width:${project.progress_percentage || 0}%"></div></div>
                    </div>
                </div>
                ${project.tags && project.tags.length ? `
                    <div class="tag-list mt-sm">${project.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                ` : ''}
                <div class="card-footer">
                    <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();Projects.showTasks('${project.id}')">Tasks</button>
                    <button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();Projects.showEditForm('${project.id}')">${Icons.edit} Edit</button>
                </div>
            </div>
        `;
    },
    
    emptyState() {
        return `<div class="empty-state" style="grid-column:1/-1"><h3>No projects yet</h3><p>Start tracking what you're building.</p></div>`;
    },
    
    showDetail(projectId) {
        this.showEditForm(projectId);
    },
    
    // ─── CREATE ───
    showCreateForm() {
        const modal = document.getElementById('project-modal');
        if (!modal) return;
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Projects.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header"><h3 class="modal-title">New Project</h3><button class="modal-close" onclick="Projects.closeModal()"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button></div>
                    <form onsubmit="Projects.handleCreate(event)">
                        <div class="form-group"><label class="form-label">Title</label><input type="text" class="form-input" id="p-title" required></div>
                        <div class="form-group"><label class="form-label">Description</label><input type="text" class="form-input" id="p-desc"></div>
                        <div class="form-group"><label class="form-label">Priority</label><select class="form-select" id="p-priority"><option value="low">Low</option><option value="medium" selected>Medium</option><option value="high">High</option></select></div>
                        <div class="form-group"><label class="form-label">Current Phase</label><input type="text" class="form-input" id="p-phase" placeholder="e.g., Development"></div>
                        <div class="form-group"><label class="form-label">Tags (comma separated)</label><input type="text" class="form-input" id="p-tags" placeholder="fastapi, python"></div>
                        <button type="submit" class="btn btn-primary btn-block">Create Project</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleCreate(e) {
        e.preventDefault();
        const tagsStr = document.getElementById('p-tags').value;
        const data = {
            title: document.getElementById('p-title').value,
            description: document.getElementById('p-desc').value,
            priority: document.getElementById('p-priority').value,
            current_phase: document.getElementById('p-phase').value || null,
            tags: tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(t => t) : [],
        };
        try {
            await ApiClient.createProject(data);
            Projects.closeModal();
            App.clearAllCache();
            App.router.navigate('projects', true);
        } catch (error) { alert(error.message); }
    },
    
    // ─── EDIT ───
    showEditForm(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;
        const modal = document.getElementById('project-modal');
        if (!modal) return;
        const statusOptions = ['planned','in_progress','paused','completed','archived'].map(s => `<option value="${s}" ${project.status===s?'selected':''}>${s.replace('_',' ')}</option>`).join('');
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Projects.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header"><h3 class="modal-title">Edit Project</h3><button class="modal-close" onclick="Projects.closeModal()"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button></div>
                    <form onsubmit="Projects.handleEdit(event, '${project.id}')">
                        <div class="form-group"><label class="form-label">Title</label><input type="text" class="form-input" id="pe-title" value="${project.title||''}" required></div>
                        <div class="form-group"><label class="form-label">Description</label><input type="text" class="form-input" id="pe-desc" value="${project.description||''}"></div>
                        <div class="form-group"><label class="form-label">Status</label><select class="form-select" id="pe-status">${statusOptions}</select></div>
                        <div class="form-group"><label class="form-label">Phase</label><input type="text" class="form-input" id="pe-phase" value="${project.current_phase||''}"></div>
                        <div class="form-group"><label class="form-label">Progress (%)</label><input type="number" class="form-input" id="pe-progress" value="${project.progress_percentage||0}" min="0" max="100"></div>
                        <div class="form-group"><label class="form-label">Tags</label><input type="text" class="form-input" id="pe-tags" value="${(project.tags||[]).join(', ')}"></div>
                        <button type="submit" class="btn btn-primary btn-block">Save Changes</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleEdit(e, projectId) {
        e.preventDefault();
        const tagsStr = document.getElementById('pe-tags').value;
        const data = {
            title: document.getElementById('pe-title').value,
            description: document.getElementById('pe-desc').value,
            status: document.getElementById('pe-status').value,
            current_phase: document.getElementById('pe-phase').value,
            progress_percentage: parseFloat(document.getElementById('pe-progress').value),
            tags: tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(t => t) : [],
        };
        try {
            await ApiClient.request('PATCH', `/projects/${projectId}`, data);
            Projects.closeModal();
            App.clearAllCache();
            App.router.navigate('projects', true);
        } catch (error) { alert(error.message); }
    },
    
    // ─── DELETE ───
    async deleteProject(projectId) {
        if (confirm('Delete this project and all its tasks?')) {
            try {
                await ApiClient.request('DELETE', `/projects/${projectId}`);
                App.clearAllCache();
                App.router.navigate('projects', true);
            } catch (error) { alert(error.message); }
        }
    },
    
    // ─── TASKS ───
    async showTasks(projectId) {
        const project = this.projects.find(p => p.id === projectId);
        if (!project) return;
        const modal = document.getElementById('project-modal');
        if (!modal) return;
        
        modal.innerHTML = `<div class="modal-overlay" onclick="Projects.closeModal()"><div class="modal" onclick="event.stopPropagation()" style="max-width:550px">
            <div class="modal-header"><h3 class="modal-title">${project.title} - Tasks</h3><button class="modal-close" onclick="Projects.closeModal()"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button></div>
            <div id="tasks-content" style="text-align:center;padding:20px;color:var(--text-tertiary)">Loading...</div>
            <form onsubmit="Projects.handleAddTask(event, '${projectId}')" style="padding:0 0 16px 0">
                <div style="display:flex;gap:8px"><input type="text" class="form-input" id="task-title" placeholder="New task..." required><button type="submit" class="btn btn-primary btn-sm">${Icons.plus}</button></div>
            </form>
        </div></div>`;
        
        try {
            const tasks = await ApiClient.request('GET', `/projects/${projectId}/tasks`);
            const content = document.getElementById('tasks-content');
            if (!tasks || tasks.length === 0) {
                content.innerHTML = '<p>No tasks yet. Add one below.</p>';
            } else {
                content.innerHTML = tasks.map(t => `
                    <div class="card mb-sm" style="text-align:left">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <span style="${t.status==='completed'?'text-decoration:line-through;opacity:0.5':''}">${t.title}</span>
                            <div style="display:flex;gap:4px">
                                ${t.status !== 'completed' ? `<button class="btn btn-ghost btn-sm" onclick="Projects.completeTask('${projectId}','${t.id}')">${Icons.check}</button>` : ''}
                                <button class="btn btn-ghost btn-sm" onclick="Projects.deleteTask('${projectId}','${t.id}')">${Icons.trash}</button>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            document.getElementById('tasks-content').innerHTML = `<p>Failed to load tasks</p>`;
        }
    },
    
    async handleAddTask(e, projectId) {
        e.preventDefault();
        const title = document.getElementById('task-title').value;
        try {
            await ApiClient.request('POST', `/projects/${projectId}/tasks`, { title, status: 'todo' });
            document.getElementById('task-title').value = '';
            Projects.showTasks(projectId);
        } catch (error) { alert(error.message); }
    },
    
    async completeTask(projectId, taskId) {
        try {
            await ApiClient.request('PATCH', `/projects/${projectId}/tasks/${taskId}/complete`);
            Projects.showTasks(projectId);
        } catch (error) { alert(error.message); }
    },
    
    async deleteTask(projectId, taskId) {
        if (confirm('Delete this task?')) {
            try {
                await ApiClient.request('DELETE', `/projects/${projectId}/tasks/${taskId}`);
                Projects.showTasks(projectId);
            } catch (error) { alert(error.message); }
        }
    },
    
    closeModal() {
        const modal = document.getElementById('project-modal');
        if (modal) modal.innerHTML = '';
    }
};