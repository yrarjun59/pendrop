// Auth Module - Login/Signup handling

const auth = {
    currentUser: null,
    
    init: function() {
        this.loadUserFromStorage();
        this.bindEvents();
    },
    
    bindEvents: function() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.switchTab(tab);
            });
        });
        
        // Login/Signup buttons
        document.getElementById('login-btn').addEventListener('click', () => this.login());
        document.getElementById('signup-btn').addEventListener('click', () => this.signup());
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());
    },
    
    switchTab: function(tab) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tab) {
                btn.classList.add('active');
            }
        });
        
        document.getElementById('login-form').classList.toggle('hidden', tab !== 'login');
        document.getElementById('signup-form').classList.toggle('hidden', tab !== 'signup');
        this.setMessage('');
    },
    
    loadUserFromStorage: function() {
        const user = localStorage.getItem('pendrop_user');
        if (user) {
            this.currentUser = JSON.parse(user);
            this.showMainScreen();
        }
    },
    
    login: async function() {
        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;
        
        if (!email || !password) {
            this.setMessage('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const user = await api.login(email, password);
            this.currentUser = user;
            localStorage.setItem('pendrop_user', JSON.stringify(user));
            this.showMainScreen();
            window.dispatchEvent(new CustomEvent('user-logged-in'));
        } catch (err) {
            this.setMessage('Invalid credentials', 'error');
        }
    },
    
    signup: async function() {
        const name = document.getElementById('signup-name').value.trim();
        const email = document.getElementById('signup-email').value.trim();
        const password = document.getElementById('signup-password').value;
        
        if (!name || !email || !password) {
            this.setMessage('Please fill in all fields', 'error');
            return;
        }
        
        try {
            await api.register(name, email, password);
            this.setMessage('Account created! Please login.', 'success');
            this.switchTab('login');
        } catch (err) {
            this.setMessage(err.detail || 'Registration failed', 'error');
        }
    },
    
    logout: function() {
        this.currentUser = null;
        localStorage.removeItem('pendrop_user');
        document.getElementById('login-screen').classList.remove('hidden');
        document.getElementById('main-screen').classList.add('hidden');
        this.clearInputs();
    },
    
    showMainScreen: function() {
        document.getElementById('login-screen').classList.add('hidden');
        document.getElementById('main-screen').classList.remove('hidden');
        document.getElementById('user-name').textContent = this.currentUser.name;
    },
    
    setMessage: function(msg, type = '') {
        const el = document.getElementById('auth-message');
        el.textContent = msg;
        el.className = `message ${type}`;
    },
    
    clearInputs: function() {
        document.getElementById('login-email').value = '';
        document.getElementById('login-password').value = '';
        document.getElementById('signup-name').value = '';
        document.getElementById('signup-email').value = '';
        document.getElementById('signup-password').value = '';
    },
    
    getUserId: function() {
        return this.currentUser ? this.currentUser.id : null;
    }
};

export default auth;