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
            <div class="card" style="cursor:pointer" onclick="Knowledge.showDetail('${item.id}')">
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
    
    showDetail(itemId) {
        const item = this.items.find(i => i.id === itemId);
        if (!item) return;
        
        const statusLabels = {
            'inbox': 'Inbox', 'planned': 'Planned', 'in_progress': 'In Progress',
            'paused': 'Paused', 'completed': 'Completed', 'archived': 'Archived'
        };
        
        const category = this.categories.find(c => c.id === item.category_id);
        const modal = document.getElementById('knowledge-modal');
        if (!modal) return;
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Knowledge.closeModal()">
                <div class="modal" onclick="event.stopPropagation()" style="max-width:550px">
                    <div class="modal-header">
                        <h3 class="modal-title">${item.title}</h3>
                        <div style="display:flex;gap:4px">
                            <button class="btn btn-ghost btn-sm" onclick="Knowledge.showEditForm('${item.id}')" title="Edit">
                                ${Icons.edit}
                            </button>
                            <button class="btn btn-ghost btn-sm" onclick="Knowledge.deleteItem('${item.id}')" title="Delete">
                                ${Icons.trash}
                            </button>
                            <button class="modal-close" onclick="Knowledge.closeModal()">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                            </button>
                        </div>
                    </div>
                    <div style="margin-bottom:16px">
                        <span class="tag">${statusLabels[item.status] || item.status}</span>
                        ${category ? `<span class="tag" style="margin-left:4px">${category.name}</span>` : ''}
                        ${item.priority ? `<span class="tag" style="margin-left:4px">${item.priority}</span>` : ''}
                    </div>
                    ${item.description ? `<p class="text-secondary mb-md">${item.description}</p>` : ''}
                    ${item.tags && item.tags.length ? `
                        <div class="tag-list mb-md">${item.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                    ` : ''}
                    ${item.source_link ? `
                        <p class="mb-md"><a href="${item.source_link}" target="_blank" style="color:var(--accent)">Source Link</a></p>
                    ` : ''}
                    ${item.notes ? `
                        <div class="card mb-md" style="background:var(--bg-secondary)">
                            <p style="white-space:pre-wrap;font-size:13px">${item.notes}</p>
                        </div>
                    ` : ''}
                    <div class="progress-section mb-md">
                        <div class="progress-label">
                            <span>Progress</span><span>${item.progress_percentage || 0}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width:${item.progress_percentage || 0}%"></div>
                        </div>
                    </div>
                    <div class="card-footer" style="border-top:none;padding-top:0;gap:8px">
                        <input type="range" min="0" max="100" value="${item.progress_percentage || 0}" 
                            onchange="Knowledge.updateProgress('${item.id}', this.value)" 
                            style="flex:1;accent-color:var(--accent)">
                        <button class="btn btn-ghost btn-sm" onclick="Knowledge.closeModal()">Close</button>
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
            App.clearAllCache();
            App.router.navigate('knowledge', true);
        } catch (error) {
            alert(error.message);
        }
    },

    showEditForm(itemId) {
        const item = this.items.find(i => i.id === itemId);
        if (!item) return;
        
        const modal = document.getElementById('knowledge-modal');
        const categoryOptions = this.categories.map(c => `<option value="${c.id}" ${item.category_id === c.id ? 'selected' : ''}>${c.name}</option>`).join('');
        const statusOptions = ['inbox','planned','in_progress','paused','completed','archived']
            .map(s => `<option value="${s}" ${item.status === s ? 'selected' : ''}>${s.replace('_',' ')}</option>`).join('');
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Knowledge.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3 class="modal-title">Edit Item</h3>
                        <button class="modal-close" onclick="Knowledge.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Knowledge.handleEdit(event, '${item.id}')">
                        <div class="form-group"><label class="form-label">Title</label><input type="text" class="form-input" id="ke-title" value="${item.title || ''}" required></div>
                        <div class="form-group"><label class="form-label">Description</label><input type="text" class="form-input" id="ke-desc" value="${item.description || ''}"></div>
                        <div class="form-group"><label class="form-label">Category</label><select class="form-select" id="ke-category"><option value="">None</option>${categoryOptions}</select></div>
                        <div class="form-group"><label class="form-label">Tags</label><input type="text" class="form-input" id="ke-tags" value="${(item.tags || []).join(', ')}"></div>
                        <div class="form-group"><label class="form-label">Priority</label><select class="form-select" id="ke-priority"><option value="low" ${item.priority==='low'?'selected':''}>Low</option><option value="medium" ${item.priority==='medium'?'selected':''}>Medium</option><option value="high" ${item.priority==='high'?'selected':''}>High</option></select></div>
                        <div class="form-group"><label class="form-label">Status</label><select class="form-select" id="ke-status">${statusOptions}</select></div>
                        <div class="form-group"><label class="form-label">Notes</label><textarea class="form-textarea" id="ke-notes">${item.notes || ''}</textarea></div>
                        <div class="form-group"><label class="form-label">Source Link</label><input type="url" class="form-input" id="ke-link" value="${item.source_link || ''}"></div>
                        <button type="submit" class="btn btn-primary btn-block">Save Changes</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleEdit(e, itemId) {
        e.preventDefault();
        const tagsStr = document.getElementById('ke-tags').value;
        
        const data = {
            title: document.getElementById('ke-title').value,
            description: document.getElementById('ke-desc').value,
            category_id: document.getElementById('ke-category').value || null,
            tags: tagsStr ? tagsStr.split(',').map(t => t.trim()).filter(t => t) : [],
            priority: document.getElementById('ke-priority').value,
            status: document.getElementById('ke-status').value,
            notes: document.getElementById('ke-notes').value,
            source_link: document.getElementById('ke-link').value || null
        };
        
        try {
            await ApiClient.request('PATCH', `/knowledge/${itemId}`, data);
            Knowledge.closeModal();
            App.clearAllCache();
            App.router.navigate('knowledge', true);
        } catch (error) {
            alert(error.message);
        }
    },
    
    async deleteItem(itemId) {
        if (confirm('Delete this knowledge item?')) {
            try {
                await ApiClient.request('DELETE', `/knowledge/${itemId}`);
                Knowledge.closeModal();
                App.clearAllCache();
                App.router.navigate('knowledge', true);
            } catch (error) {
                alert(error.message);
            }
        }
    },
    
    async updateProgress(itemId, progress) {
        try {
            await ApiClient.request('PATCH', `/knowledge/${itemId}/progress?progress=${progress}`);
            // Update local data
            const item = this.items.find(i => i.id === itemId);
            if (item) item.progress_percentage = parseFloat(progress);
            // Refresh the detail view
            this.showDetail(itemId);
        } catch (error) {
            alert(error.message);
        }
    },
    
    closeModal() {
        const modal = document.getElementById('knowledge-modal');
        if (modal) modal.innerHTML = '';
    }
};