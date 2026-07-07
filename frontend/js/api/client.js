/* ─── GabbyOS API Client ─── */

const API_BASE = 'https://gabbyos-production.up.railway.app/api/v1';

const ApiClient = {
    token: null,
    refreshToken: null,
    
    init() {
        this.token = localStorage.getItem('gabbyos-token');
        this.refreshToken = localStorage.getItem('gabbyos-refresh');
    },
    
    setToken(token) {
        this.token = token;
        localStorage.setItem('gabbyos-token', token);
    },
    
    setRefreshToken(token) {
        this.refreshToken = token;
        localStorage.setItem('gabbyos-refresh', token);
    },
    
    clearToken() {
        this.token = null;
        this.refreshToken = null;
        localStorage.removeItem('gabbyos-token');
        localStorage.removeItem('gabbyos-refresh');
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
        
        let response = await fetch(url, options);
        
        // If 401, try refreshing token
        if (response.status === 401 && this.refreshToken) {
            try {
                const refreshData = await fetch(`${API_BASE}/auth/refresh`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ refresh_token: this.refreshToken })
                }).then(r => r.json());
                
                this.setToken(refreshData.access_token);
                headers['Authorization'] = `Bearer ${this.token}`;
                response = await fetch(url, { ...options, headers });
            } catch (e) {
                this.clearToken();
                App.router.navigate('dashboard');
                throw new Error('Session expired. Please login again.');
            }
        }
        
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
        this.setRefreshToken(data.refresh_token);
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