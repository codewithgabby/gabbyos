const Planner = {
    routines: [],
    currentPlan: null,
    
    async render() {
        if (!ApiClient.isAuthenticated()) return AuthPage.render();
        
        try {
            this.routines = await ApiClient.getRoutines({ is_active: 'true' });
            this.currentPlan = await this.getCurrentWeekPlan();
            return this.template();
        } catch (error) {
            return `<div class="page" style="padding:48px"><h2>Planner</h2><p class="text-secondary">${error.message}</p></div>`;
        }
    },
    
    async getCurrentWeekPlan() {
        try {
            const today = new Date();
            const year = today.getFullYear();
            const weekNumber = this.getWeekNumber(today);
            const plans = await ApiClient.request('GET', `/planner?year=${year}&week_number=${weekNumber}`);
            console.log('Plans received:', plans);
            if (plans && plans.length > 0) {
                console.log('Items in plan:', plans[0].items);
                return plans[0];
            }
            return null;
        } catch (error) {
            console.error('Failed to get plan:', error);
            return null;
        }
    },
    
    getWeekNumber(date) {
        const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
        const dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    },
    
    getWeekDates() {
        const today = new Date();
        const day = today.getDay();
        const diff = today.getDate() - day + (day === 0 ? -6 : 1);
        const monday = new Date(today.setDate(diff));
        const dates = [];
        for (let i = 0; i < 7; i++) {
            const d = new Date(monday);
            d.setDate(monday.getDate() + i);
            dates.push(d.toISOString().split('T')[0]);
        }
        return dates;
    },
    
    template() {
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const dayLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        
        console.log('Current plan:', this.currentPlan);
        
        const daysHtml = days.map((day, i) => {
            const items = this.currentPlan && this.currentPlan.items 
                ? this.currentPlan.items.filter(item => item.day_of_week === day) 
                : [];
            console.log(`Day ${day}:`, items.length, 'items');
            return this.dayColumn(dayLabels[i], day, items);
        }).join('');
        
        return `
            <div class="page">
                <div class="section-header">
                    <h2 class="section-title">Weekly Planner</h2>
                    <button class="btn btn-primary" onclick="Planner.showCreateForm()">
                        ${Icons.plus} ${this.currentPlan ? 'Edit Plan' : 'New Plan'}
                    </button>
                </div>
                <p class="text-secondary mb-lg">Plan your week by assigning routines to each day.</p>
                <div class="planner-grid">${daysHtml}</div>
                <div id="planner-modal"></div>
            </div>
        `;
    },
    
    dayColumn(label, day, items) {
        const itemsHtml = items.length > 0 
            ? items.map(item => `
                <div class="planner-item">
                    <div>
                        <div style="font-weight:500">${item.routine_title || 'Untitled'}</div>
                        <div style="font-size:11px;color:var(--text-tertiary)">${item.routine_duration || 0}min${item.category_name ? ' • ' + item.category_name : ''}</div>
                    </div>
                    <button class="btn btn-ghost btn-sm" onclick="Planner.removeItem('${item.id}')" title="Remove">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                    </button>
                </div>
            `).join('')
            : '<div class="planner-empty">-</div>';
        
        return `
            <div class="planner-day">
                <div class="planner-day-header">${label.substring(0, 3)}</div>
                <div class="planner-day-body">${itemsHtml}</div>
            </div>
        `;
    },
    
    showCreateForm() {
        const modal = document.getElementById('planner-modal');
        if (!modal) return;
        
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const dayLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        
        const routinesCheckboxes = this.routines.map(r => `
            <label class="checkbox-group" style="padding:6px 0">
                <input type="checkbox" value="${r.id}" class="routine-checkbox">
                <span>${r.title}</span>
                <span class="text-tertiary" style="font-size:11px">${r.duration_minutes}min</span>
            </label>
        `).join('');
        
        const daysInputs = dayLabels.map((label, i) => `
            <div class="planner-day-section">
                <h4 style="font-size:13px;font-weight:600;margin-bottom:8px">${label}</h4>
                <div class="checkbox-list" data-day="${days[i]}">${routinesCheckboxes}</div>
            </div>
        `).join('');
        
        modal.innerHTML = `
            <div class="modal-overlay" onclick="Planner.closeModal()">
                <div class="modal" onclick="event.stopPropagation()" style="max-width:650px;max-height:85vh">
                    <div class="modal-header">
                        <h3 class="modal-title">${this.currentPlan ? 'Edit' : 'Create'} Weekly Plan</h3>
                        <button class="modal-close" onclick="Planner.closeModal()">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                        </button>
                    </div>
                    <form onsubmit="Planner.handleSave(event)">
                        <div class="form-group">
                            <label class="form-label">Notes (optional)</label>
                            <input type="text" class="form-input" id="plan-notes" placeholder="e.g., Focus week - AI/ML priority">
                        </div>
                        <div class="planner-days-grid">${daysInputs}</div>
                        <button type="submit" class="btn btn-primary btn-block mt-md">Save Plan</button>
                    </form>
                </div>
            </div>
        `;
    },
    
    async handleSave(e) {
        e.preventDefault();
        
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const weekDates = this.getWeekDates();
        const today = new Date();
        const year = today.getFullYear();
        const weekNumber = this.getWeekNumber(today);
        
        const items = [];
        days.forEach(day => {
            const container = document.querySelector(`.checkbox-list[data-day="${day}"]`);
            if (container) {
                const checkboxes = container.querySelectorAll('input[type="checkbox"]:checked');
                checkboxes.forEach((checkbox, index) => {
                    items.push({
                        routine_id: checkbox.value,
                        day_of_week: day,
                        sort_order: index + 1
                    });
                });
            }
        });
        
        try {
            // Try to delete old plan if exists
            if (this.currentPlan) {
                try {
                    await ApiClient.request('DELETE', `/planner/${this.currentPlan.id}`);
                } catch(e) {
                    // Ignore if already deleted
                }
            }
            
            const data = {
                week_start_date: weekDates[0],
                week_end_date: weekDates[6],
                year: year,
                week_number: weekNumber,
                notes: document.getElementById('plan-notes')?.value || '',
                items: items
            };
            
            await ApiClient.request('POST', '/planner', data);
            Planner.closeModal();
            App.router.navigate('planner');
        } catch (error) {
            alert(error.message);
        }
    },
    
    async removeItem(itemId) {
        if (!this.currentPlan) return;
        if (confirm('Remove this routine from the plan?')) {
            try {
                await ApiClient.request('DELETE', `/planner/${this.currentPlan.id}/items/${itemId}`);
                App.router.navigate('planner');
            } catch (error) {
                alert(error.message);
            }
        }
    },
    
    closeModal() {
        const modal = document.getElementById('planner-modal');
        if (modal) modal.innerHTML = '';
    }
};