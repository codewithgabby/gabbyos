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
        const itemsHtml = this.items.length > 0
            ? this.items.map(item => `
                <div class="card">
                    <div class="card-header">
                        <span>${item.content}</span>
                        ${item.is_organized ? '<span class="tag">Organized</span>' : '<span class="status-badge status-in_progress">New</span>'}
                    </div>
                    ${item.category_hint ? `<p class="text-tertiary" style="font-size:12px">Hint: ${item.category_hint}</p>` : ''}
                </div>
            `).join('')
            : '<div class="empty-state"><h3>Inbox is empty</h3><p>Quick capture ideas here.</p></div>';
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Inbox</h2>
                    <button class="btn btn-primary" onclick="Inbox.showCreateForm()">${Icons.plus} Quick Capture</button>
                </div>
                <p class="text-secondary mb-lg">Quickly save ideas to organize later.</p>
                <div class="cards-grid">${itemsHtml}</div>
            </div>
        `;
    },
    
    showCreateForm() {
        const content = prompt('What do you want to capture?');
        if (content) {
            ApiClient.createInboxItem(content).then(() => App.router.navigate('inbox'));
        }
    }
};