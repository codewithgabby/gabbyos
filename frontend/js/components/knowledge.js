const Knowledge = {
    items: [],
    categories: [],
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            const [items, categories] = await Promise.all([
                ApiClient.getKnowledge(),
                ApiClient.getCategories()
            ]);
            this.items = items;
            this.categories = categories;
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Knowledge</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template() {
        const itemsHtml = this.items.length > 0
            ? this.items.map(item => this.itemCard(item)).join('')
            : this.emptyState();
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Knowledge Workspace</h2>
                    <button class="btn btn-primary" onclick="Knowledge.showCreateForm()">
                        ${Icons.plus} New Item
                    </button>
                </div>
                <p class="text-secondary mb-lg">Your Second Brain. Capture everything you want to learn.</p>
                <div class="cards-grid cards-grid-2">${itemsHtml}</div>
                <div id="knowledge-modal"></div>
            </div>
        `;
    },
    
    itemCard(item) {
        const statusLabels = {
            'inbox': 'Inbox', 'planned': 'Planned', 'in_progress': 'In Progress',
            'paused': 'Paused', 'completed': 'Completed', 'archived': 'Archived'
        };
        
        const category = this.categories.find(c => c.id === item.category_id);
        
        return `
            <div class="card">
                <div class="card-header">
                    <span class="card-title">${item.title}</span>
                    <span class="tag">${statusLabels[item.status] || item.status}</span>
                </div>
                ${item.description ? `<p class="card-subtitle">${item.description}</p>` : ''}
                <div class="card-body">
                    ${item.tags && item.tags.length ? `
                        <div class="tag-list mb-md">${item.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                    ` : ''}
                    <div style="font-size:12px;color:var(--text-tertiary)">
                        ${category ? `Category: ${category.name}` : ''}
                        ${item.progress_percentage > 0 ? ` • Progress: ${item.progress_percentage}%` : ''}
                        ${item.priority ? ` • ${item.priority}` : ''}
                    </div>
                </div>
            </div>
        `;
    },
    
    emptyState() {
        return `
            <div class="empty-state" style="grid-column:1/-1">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3">
                    <path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>
                </svg>
                <h3>No knowledge items yet</h3>
                <p>Start capturing what you want to learn.</p>
            </div>
        `;
    },
    
    showCreateForm() {
        const modal = document.getElementById('knowledge-modal');
        if (!modal) return;
        
        const categoryOptions = this.categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Knowledge.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3 class="modal-title">New Knowledge Item</h3>
                        <button class="modal-close" onclick="Knowledge.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Knowledge.handleCreate(event)">
                        <div class="form-group">
                            <label class="form-label">Title</label>
                            <input type="text" class="form-input" id="k-title" placeholder="e.g., NumPy Fundamentals" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Description</label>
                            <input type="text" class="form-input" id="k-desc" placeholder="Brief description">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Category</label>
                            <select class="form-select" id="k-category"><option value="">None</option>${categoryOptions}</select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Tags (comma separated)</label>
                            <input type="text" class="form-input" id="k-tags" placeholder="python, numpy, data-science">
                        </div>
                        <div class="form-group">
                            <label class="form-label">Priority</label>
                            <select class="form-select" id="k-priority">
                                <option value="low">Low</option><option value="medium" selected>Medium</option><option value="high">High</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Source Link</label>
                            <input type="url" class="form-input" id="k-link" placeholder="https://...">
                        </div>
                        <button type="submit" class="btn btn-primary btn-block">Create Item</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleCreate(e) {
        e.preventDefault();
        
        const tagsStr = document.getElementById('k-tags').value;
        const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(t => t) : [];
        
        const data = {
            title: document.getElementById('k-title').value,
            description: document.getElementById('k-desc').value,
            category_id: document.getElementById('k-category').value || null,
            tags: tags,
            priority: document.getElementById('k-priority').value,
            source_link: document.getElementById('k-link').value || null,
            status: 'inbox'
        };
        
        try {
            await ApiClient.createKnowledge(data);
            Knowledge.closeModal();
            App.router.navigate('knowledge');
        } catch (error) {
            alert(error.message);
        }
    },
    
    closeModal() {
        const modal = document.getElementById('knowledge-modal');
        if (modal) modal.innerHTML = '';
    }
};