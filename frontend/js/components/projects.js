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
                    <div>
                        <span class="card-title">${project.title}</span>
                        ${project.current_phase ? `<span class="tag" style="margin-left:8px">${project.current_phase}</span>` : ''}
                    </div>
                    <span class="status-badge ${project.status === 'in_progress' ? 'status-in_progress' : 'status-not_started'}">
                        ${statusLabels[project.status] || project.status}
                    </span>
                </div>
                ${project.description ? `<p class="card-subtitle">${project.description}</p>` : ''}
                <div class="card-body">
                    <div class="progress-section">
                        <div class="progress-label">
                            <span>Progress</span><span>${project.progress_percentage || 0}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width:${project.progress_percentage || 0}%"></div>
                        </div>
                    </div>
                </div>
                ${project.tags && project.tags.length ? `
                    <div class="tag-list mt-md">${project.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                ` : ''}
            </div>
        `;
    },
    
    emptyState() {
        return `
            <div class="empty-state" style="grid-column:1/-1">
                <h3>No projects yet</h3>
                <p>Start tracking what you're building.</p>
            </div>
        `;
    },
    
    showCreateForm() {
        const modal = document.getElementById('project-modal');
        if (!modal) return;
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Projects.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3 class="modal-title">New Project</h3>
                        <button class="modal-close" onclick="Projects.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
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
            App.router.navigate('projects');
        } catch (error) {
            alert(error.message);
        }
    },
    
    closeModal() {
        const modal = document.getElementById('project-modal');
        if (modal) modal.innerHTML = '';
    }
};