const Inbox = {
    items: [],
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            this.items = await ApiClient.getInbox();
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Inbox</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template() {
        const unorganized = this.items.filter(i => !i.is_organized);
        const organized = this.items.filter(i => i.is_organized);
        
        const unorganizedHtml = unorganized.length > 0
            ? unorganized.map(item => this.itemCard(item)).join('')
            : '<div class="empty-state"><p>Nothing to organize. Great job!</p></div>';
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Inbox</h2>
                    <button class="btn btn-primary" onclick="Inbox.showCreateForm()">${Icons.plus} Quick Capture</button>
                </div>
                <p class="text-secondary mb-lg">Quickly save ideas to organize later.</p>
                
                <div class="section-header">
                    <h3 style="font-size:14px;font-weight:600">Needs Organizing (${unorganized.length})</h3>
                </div>
                <div class="cards-grid mb-lg">${unorganizedHtml}</div>
                
                ${organized.length > 0 ? `
                    <div class="section-header">
                        <h3 style="font-size:14px;font-weight:600">Organized (${organized.length})</h3>
                    </div>
                    <div class="cards-grid">${organized.map(item => this.itemCard(item)).join('')}</div>
                ` : ''}
            </div>
        `;
    },
    
    itemCard(item) {
        return `
            <div class="card" style="${item.is_organized ? 'opacity:0.6' : ''}">
                <div class="card-header">
                    <span style="flex:1">${item.content}</span>
                    <div style="display:flex;gap:4px">
                        ${!item.is_organized ? `
                            <button class="btn btn-ghost btn-sm" onclick="Inbox.markOrganized('${item.id}')" title="Mark as organized">
                                ${Icons.check}
                            </button>
                        ` : ''}
                        <button class="btn btn-ghost btn-sm" onclick="Inbox.deleteItem('${item.id}')" title="Delete">
                            ${Icons.trash}
                        </button>
                    </div>
                </div>
                <div style="display:flex;gap:8px;align-items:center">
                    ${item.category_hint ? `<span class="tag">${item.category_hint}</span>` : ''}
                    <span class="tag" style="font-size:11px">${item.is_organized ? 'Organized' : 'New'}</span>
                </div>
            </div>
        `;
    },
    
    showCreateForm() {
        const content = prompt('What do you want to capture?');
        if (content && content.trim()) {
            ApiClient.createInboxItem(content.trim()).then(() => {
                App.clearAllCache();
                App.router.navigate('inbox', true);
            });
        }
    },
    
    async deleteItem(itemId) {
        if (confirm('Delete this item?')) {
            try {
                await ApiClient.request('DELETE', `/inbox/${itemId}`);
                App.clearAllCache();
                App.router.navigate('inbox', true);
            } catch (error) {
                alert(error.message);
            }
        }
    },
    
    async markOrganized(itemId) {
        try {
            await ApiClient.request('PATCH', `/inbox/${itemId}/organize?organized_to=processed`);
            App.clearAllCache();
            App.router.navigate('inbox', true);
        } catch (error) {
            alert(error.message);
        }
    }
};