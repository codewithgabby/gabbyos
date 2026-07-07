/* ─── Auth Page ─── */

const AuthPage = {
    async render() {
        return `
            <div class="auth-container">
                <div class="auth-card">
                    <div class="logo" style="justify-content:center;margin-bottom:var(--space-md)">
                        <svg width="32" height="32" viewBox="0 0 28 28" fill="none">
                            <rect width="28" height="28" rx="8" fill="currentColor"/>
                            <path d="M7 14L12 19L21 9" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span class="logo-text" style="font-size:20px">GabbyOS</span>
                    </div>
                    <h2 class="auth-title">Welcome back</h2>
                    <p class="auth-subtitle">Sign in to your personal operating system</p>
                    
                    <form id="login-form" onsubmit="AuthPage.handleLogin(event); return false;">
                        <div class="form-group">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-input" id="login-email" placeholder="gabby@gabbyos.com" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-input" id="login-password" placeholder="Your password" required>
                        </div>
                        <div id="login-error" style="color:var(--danger);font-size:var(--font-sm);margin-bottom:var(--space-md);display:none"></div>
                        <button type="submit" class="btn btn-primary btn-block">Sign In</button>
                    </form>
                    
                    <p style="text-align:center;margin-top:var(--space-lg);font-size:var(--font-sm);color:var(--text-tertiary)">
                        Don't have an account? 
                        <a href="#" onclick="AuthPage.showRegister(event)" style="color:var(--text-primary);text-decoration:underline">Register</a>
                    </p>
                </div>
            </div>
        `;
    },
    
    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email');
        const password = document.getElementById('login-password');
        const errorEl = document.getElementById('login-error');
        const btn = document.querySelector('#login-form button[type="submit"]');
        
        if (!email || !password) return;
        
        try {
            errorEl.style.display = 'none';
            btn.textContent = 'Signing in...';
            btn.disabled = true;
            await ApiClient.login(email.value, password.value);
            App.clearAllCache();
            App.router.navigate('dashboard', true);
        } catch (error) {
            errorEl.textContent = error.message;
            errorEl.style.display = 'block';
            btn.textContent = 'Sign In';
            btn.disabled = false;
        }
    },
    
    showRegister(e) {
        e.preventDefault();
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = `
            <div class="auth-container">
                <div class="auth-card">
                    <h2 class="auth-title">Create account</h2>
                    <p class="auth-subtitle">Start your intentional journey</p>
                    <form id="register-form" onsubmit="AuthPage.handleRegister(event)">
                        <div class="form-group">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="form-input" id="reg-name" placeholder="Gabby" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-input" id="reg-email" placeholder="gabby@gabbyos.com" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-input" id="reg-password" placeholder="Min 8 characters" required minlength="8">
                        </div>
                        <div id="reg-error" style="color:var(--danger);font-size:var(--font-sm);margin-bottom:var(--space-md);display:none"></div>
                        <button type="submit" class="btn btn-primary btn-block">Create Account</button>
                    </form>
                    <p style="text-align:center;margin-top:var(--space-lg);font-size:var(--font-sm);color:var(--text-tertiary)">
                        Already have an account? 
                        <a href="#" onclick="App.router.navigate('dashboard')" style="color:var(--text-primary);text-decoration:underline">Sign in</a>
                    </p>
                </div>
            </div>
        `;
    },
    
    async handleRegister(e) {
        e.preventDefault();
        const name = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const errorEl = document.getElementById('reg-error');
        
        try {
            errorEl.style.display = 'none';
            await ApiClient.register(email, password, name);
            await ApiClient.login(email, password);
            App.router.navigate('dashboard');
        } catch (error) {
            errorEl.textContent = error.message;
            errorEl.style.display = 'block';
        }
    }
};