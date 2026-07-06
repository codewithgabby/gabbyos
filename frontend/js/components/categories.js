const Categories = {
    categories: [],
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            this.categories = await ApiClient.getCategories();
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Categories</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template() {
        const catsHtml = this.categories.length > 0
            ? this.categories.map(c => `
                <div class="card">
                    <div class="card-header">
                        <div style="display:flex;align-items:center;gap:8px">
                            <span style="width:12px;height:12px;border-radius:3px;background:${c.color || '#000'};display:inline-block"></span>
                            <span class="card-title">${c.name}</span>
                        </div>
                    </div>
                    ${c.description ? `<p class="card-subtitle">${c.description}</p>` : ''}
                </div>
            `).join('')
            : '<div class="empty-state" style="grid-column:1/-1"><h3>No categories yet</h3><p>Create categories to organize your life.</p></div>';
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Categories</h2>
                    <button class="btn btn-primary" onclick="Categories.showCreateForm()">${Icons.plus} New Category</button>
                </div>
                <p class="text-secondary mb-lg">Organize your routines, knowledge, and goals.</p>
                <div class="cards-grid cards-grid-3">${catsHtml}</div>
                <div id="category-modal"></div>
            </div>
        `;
    },
    
    showCreateForm() {
        const modal = document.getElementById('category-modal');
        if (!modal) return;
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Categories.closeModal()">
                <div class="modal" onclick="event.stopPropagation()">
                    <div class="modal-header">
                        <h3 class="modal-title">New Category</h3>
                        <button class="modal-close" onclick="Categories.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Categories.handleCreate(event)">
                        <div class="form-group"><label class="form-label">Name</label><input type="text" class="form-input" id="cat-name" placeholder="e.g., AI/ML" required></div>
                        <div class="form-group"><label class="form-label">Description</label><input type="text" class="form-input" id="cat-desc" placeholder="Brief description"></div>
                        <div class="form-group"><label class="form-label">Color</label><input type="color" class="form-input" id="cat-color" value="#3B82F6" style="height:40px;padding:4px"></div>
                        <button type="submit" class="btn btn-primary btn-block">Create Category</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleCreate(e) {
        e.preventDefault();
        const data = {
            name: document.getElementById('cat-name').value,
            description: document.getElementById('cat-desc').value,
            color: document.getElementById('cat-color').value
        };
        try {
            await ApiClient.createCategory(data);
            Categories.closeModal();
            App.router.navigate('categories');
        } catch (error) {
            alert(error.message);
        }
    },
    
    closeModal() {
        const modal = document.getElementById('category-modal');
        if (modal) modal.innerHTML = '';
    }
};