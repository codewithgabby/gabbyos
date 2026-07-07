const Reflections = {
    currentReflection: null,
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        try {
            const reflection = await ApiClient.getTodayReflection();
            this.currentReflection = reflection;
            return this.template(reflection);
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Reflections</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    template(reflection) {
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Today's Reflection</h2>
                                        <div style="display:flex;gap:8px">
                        ${reflection?.id ? `
                            <button class="btn btn-ghost btn-sm" onclick="Reflections.deleteReflection()" title="Delete">
                                ${Icons.trash} Delete
                            </button>
                        ` : ''}
                        <button class="btn btn-primary" onclick="Reflections.showEditForm()">
                            ${Icons.edit} ${reflection?.wins ? 'Edit' : 'Write'} Reflection
                        </button>
                    </div>
                </div>
                ${reflection ? `
                    <div class="card mb-md"><div class="card-header"><span class="card-title">Wins</span></div><p>${reflection.wins || 'Not yet written'}</p></div>
                    <div class="card mb-md"><div class="card-header"><span class="card-title">Challenges</span></div><p>${reflection.challenges || 'Not yet written'}</p></div>
                    <div class="card mb-md"><div class="card-header"><span class="card-title">Gratitude</span></div><p>${reflection.gratitude || 'Not yet written'}</p></div>
                    <div class="card"><div class="card-header"><span class="card-title">Tomorrow's Focus</span></div><p>${reflection.tomorrow_focus || 'Not yet written'}</p></div>
                ` : '<div class="empty-state"><h3>No reflection today</h3><p>Click "Write Reflection" to start.</p></div>'}
                <div id="reflection-modal"></div>
            </div>
        `;
    },
    
    showEditForm() {
        const modal = document.getElementById('reflection-modal');
        if (!modal) return;
        
        const r = this.currentReflection || {};
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Reflections.closeModal()">
                <div class="modal" onclick="event.stopPropagation()" style="max-width:550px">
                    <div class="modal-header">
                        <h3 class="modal-title">Today's Reflection</h3>
                        <button class="modal-close" onclick="Reflections.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Reflections.handleSave(event)">
                        <div class="form-group">
                            <label class="form-label">Today's Wins</label>
                            <textarea class="form-textarea" id="r-wins" placeholder="What went well today?">${r.wins || ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Challenges</label>
                            <textarea class="form-textarea" id="r-challenges" placeholder="What was difficult?">${r.challenges || ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Gratitude</label>
                            <textarea class="form-textarea" id="r-gratitude" placeholder="What are you grateful for?">${r.gratitude || ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Tomorrow's Focus</label>
                            <textarea class="form-textarea" id="r-focus" placeholder="What will you focus on tomorrow?">${r.tomorrow_focus || ''}</textarea>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Mood (1-10)</label>
                            <input type="number" class="form-input" id="r-mood" min="1" max="10" value="${r.mood_rating || 7}">
                        </div>
                        <button type="submit" class="btn btn-primary btn-block">Save Reflection</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleSave(e) {
        e.preventDefault();
        
        const data = {
            wins: document.getElementById('r-wins').value,
            challenges: document.getElementById('r-challenges').value,
            gratitude: document.getElementById('r-gratitude').value,
            tomorrow_focus: document.getElementById('r-focus').value,
            mood_rating: parseInt(document.getElementById('r-mood').value)
        };
        
        try {
            if (this.currentReflection?.id) {
                await ApiClient.request('PATCH', `/reflections/${this.currentReflection.id}`, data);
            } else {
                const today = new Date().toISOString().split('T')[0];
                await ApiClient.request('POST', '/reflections', { ...data, reflection_date: today });
            }
            Reflections.closeModal();
            App.clearAllCache();
            App.router.navigate('reflections', true);
        } catch (error) {
            alert(error.message);
        }
    },

    async deleteReflection() {
        if (!this.currentReflection?.id) return;
        if (confirm('Delete this reflection? This cannot be undone.')) {
            try {
                await ApiClient.request('DELETE', `/reflections/${this.currentReflection.id}`);
                App.clearAllCache();
                App.router.navigate('reflections', true);
            } catch (error) {
                alert(error.message);
            }
        }
    },
    
    closeModal() {
        const modal = document.getElementById('reflection-modal');
        if (modal) modal.innerHTML = '';
    }
};