/* ─── GabbyOS API Client ─── */

const API_BASE = 'https://gabbyos-production.up.railway.app/api/v1';

const ApiClient = {
    token: null,
    
    init() {
        this.token = localStorage.getItem('gabbyos-token');
    },
    
    setToken(token) {
        this.token = token;
        localStorage.setItem('gabbyos-token', token);
    },
    
    clearToken() {
        this.token = null;
        localStorage.removeItem('gabbyos-token');
    },
    
    isAuthenticated() {
        return !!this.token;
    },
    
    async request(method, endpoint, data = null) {
        const url = `${API_BASE}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        const options = { method, headers };
        
        if (data && (method === 'POST' || method === 'PATCH' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Request failed' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        
        return response.json();
    },
    
    // Auth
    async register(email, password, fullName) {
        return this.request('POST', '/auth/register', {
            email, password, full_name: fullName
        });
    },
    
    async login(email, password) {
        const data = await this.request('POST', '/auth/login', { email, password });
        this.setToken(data.access_token);
        return data;
    },
    
    async logout() {
        await this.request('POST', '/auth/logout');
        this.clearToken();
    },
    
    async getMe() {
        return this.request('GET', '/auth/me');
    },
    
    // Dashboard
    async getDashboard() {
        return this.request('GET', '/dashboard/today');
    },
    
    // Categories
    async getCategories() {
        return this.request('GET', '/categories');
    },
    
    async createCategory(data) {
        return this.request('POST', '/categories', data);
    },
    
    // Routines
    async getRoutines(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request('GET', `/routines?${query}`);
    },
    
    async createRoutine(data) {
        return this.request('POST', '/routines', data);
    },
    
    async updateRoutine(id, data) {
        return this.request('PATCH', `/routines/${id}`, data);
    },
    
    async toggleRoutine(id) {
        return this.request('PATCH', `/routines/${id}/toggle`);
    },
    
    async deleteRoutine(id) {
        return this.request('DELETE', `/routines/${id}`);
    },
    
    // Daily Logs
    async getTodayLogs() {
        return this.request('GET', '/logs/today');
    },
    
    async updateLog(id, data) {
        return this.request('PATCH', `/logs/${id}`, data);
    },
    
    // Streaks
    async getStreaks() {
        return this.request('GET', '/streaks');
    },
    
    // Knowledge
    async getKnowledge(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request('GET', `/knowledge?${query}`);
    },
    
    async createKnowledge(data) {
        return this.request('POST', '/knowledge', data);
    },
    
    // Projects
    async getProjects() {
        return this.request('GET', '/projects');
    },
    
    async createProject(data) {
        return this.request('POST', '/projects', data);
    },
    
    // Inbox
    async getInbox() {
        return this.request('GET', '/inbox');
    },
    
    async createInboxItem(content) {
        return this.request('POST', '/inbox', { content });
    },
    
    // Analytics
    async getAnalytics() {
        return this.request('GET', '/analytics');
    },
    
    // Goals
    async getGoals() {
        return this.request('GET', '/goals');
    },
    
    // Reflections
    async getTodayReflection() {
        return this.request('GET', '/reflections/today');
    },
};

// Initialize on load
ApiClient.init();