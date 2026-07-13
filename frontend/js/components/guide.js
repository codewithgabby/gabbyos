const Guide = {
    async render() {
        return `
            <div class="page">
                <h2 class="section-title mb-lg">How to Use GabbyOS</h2>
                <p class="text-secondary mb-lg">Your Personal Operating System for intentional living.</p>
                
                <div class="cards-grid">
                    ${this.section('dashboard', 'Today (Dashboard)', 'Your morning command center', [
                        'See routines planned for today',
                        'Click any routine to cycle status: Not Started to In Progress to Completed',
                        'Track your daily completion percentage',
                        'View your active streaks',
                        'Read daily motivation quote'
                    ])}
                    
                    ${this.section('planner', 'Planner', 'Design your week', [
                        'Plan your entire week by assigning routines to specific days',
                        'Reuse the same routine across multiple days',
                        'Click Edit Plan to modify your week',
                        'Remove routines from days you want to skip',
                        'Best done every weekend for the upcoming week'
                    ])}
                    
                    ${this.section('routines', 'Routines', 'Your daily disciplines', [
                        'Create routines with duration, priority, and reason why',
                        'Assign each routine to a category (Tech, Health, Finance)',
                        'View history of past completions and notes',
                        'Activate or deactivate routines as needed',
                        'Edit or delete routines anytime'
                    ])}
                    
                    ${this.section('categories', 'Categories', 'Organize your life', [
                        'Create categories to group your routines and knowledge',
                        'Assign colors for visual organization',
                        'Examples: Tech, Wellness, Finance, French, Faith',
                        'Edit or delete categories as your life evolves'
                    ])}
                    
                    ${this.section('knowledge', 'Knowledge (Second Brain)', 'Capture what you learn', [
                        'Save articles, courses, books, and concepts',
                        'Add tags, notes, and source links',
                        'Track learning progress with the slider',
                        'Click any card to view details, edit, or delete',
                        'Use status: Inbox, Planned, In Progress, Completed'
                    ])}
                    
                    ${this.section('projects', 'Projects', 'Track what you build', [
                        'Create projects and track progress',
                        'Add tasks within each project',
                        'Mark tasks as complete with one click',
                        'Update project phase and progress percentage',
                        'Archive completed projects'
                    ])}
                    
                    ${this.section('goals', 'Goals', 'Set long-term targets', [
                        'Create goals with target values and deadlines',
                        'Track current progress',
                        'Set status: Not Started, In Progress, Completed',
                        'Edit or delete goals as priorities change'
                    ])}
                    
                    ${this.section('inbox', 'Inbox', 'Quick capture ideas', [
                        'Instantly save ideas before you forget them',
                        'Capture anything: tasks, thoughts, things to research',
                        'Mark as organized when processed',
                        'Delete items you no longer need',
                        'Organize later into Knowledge, Projects, or Routines'
                    ])}
                    
                    ${this.section('reflections', 'Reflections', 'End your day intentionally', [
                        'Write today\'s wins - what went well?',
                        'Note challenges you faced',
                        'Express gratitude',
                        'Set tomorrow\'s focus',
                        'Rate your mood (1-10)',
                        'Best done every evening'
                    ])}
                    
                    ${this.section('analytics', 'Analytics', 'See your progress', [
                        'Daily, weekly, and monthly completion rates',
                        'Hours spent by category',
                        'Most and least completed routines',
                        'Active streaks overview',
                        'System overview with totals'
                    ])}
                    
                    ${this.section('theme', 'Theme Toggle', 'Switch appearance', [
                        'Click the sun/moon icon in the sidebar footer',
                        'Choose between Light and Dark mode',
                        'Your preference is saved automatically'
                    ])}
                </div>
                
                <div class="daily-quote mt-lg">
                    <p class="quote-text">"Your future is created by what you do today, not tomorrow."</p>
                    <p class="quote-author">Robert Kiyosaki</p>
                </div>
            </div>
        `;
    },
    
    section(page, title, subtitle, items) {
        const icons = {
            'dashboard': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
            'planner': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>`,
            'routines': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
            'categories': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
            'knowledge': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>`,
            'projects': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>`,
            'goals': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
            'inbox': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 002 2h16a2 2 0 002-2v-6l-3.45-6.89A2 2 0 0016.76 4H7.24a2 2 0 00-1.79 1.11z"/></svg>`,
            'reflections': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>`,
            'analytics': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
            'theme': `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/></svg>`,
        };
        
        return `
            <div class="card">
                <div class="card-header">
                    <span style="display:flex;align-items:center;gap:8px">
                        ${icons[page] || ''}
                        <span class="card-title">${title}</span>
                    </span>
                </div>
                <p class="card-subtitle">${subtitle}</p>
                <div class="card-body">
                    <ul style="padding-left:18px;color:var(--text-secondary);font-size:13px;line-height:2">
                        ${items.map(i => `<li>${i}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }
};