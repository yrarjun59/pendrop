// API Module - Backend communication

const API_URL = 'http://127.0.0.1:5000/api';

const api = {
    // Auth
    async register(name, email, password) {
        const res = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        return res.json();
    },
    
    async login(email, password) {
        const res = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        return res.json();
    },
    
    // Journal
    async getJournals(userId) {
        const res = await fetch(`${API_URL}/journal/${userId}`);
        return res.json();
    },
    
    async createJournal(userId, title, content) {
        const res = await fetch(`${API_URL}/journal`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    async updateJournal(id, userId, title, content) {
        const res = await fetch(`${API_URL}/journal/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    // Books
    async getBooks(userId) {
        const res = await fetch(`${API_URL}/books/${userId}`);
        return res.json();
    },
    
    async createBook(userId, title) {
        const res = await fetch(`${API_URL}/books`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title })
        });
        return res.json();
    },
    
    async updateBook(id, userId, title) {
        const res = await fetch(`${API_URL}/books/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title })
        });
        return res.json();
    },
    
    async getChapters(bookId) {
        const res = await fetch(`${API_URL}/chapters/${bookId}`);
        return res.json();
    },
    
    async createChapter(bookId, title, content) {
        const res = await fetch(`${API_URL}/chapters`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ book_id: bookId, title, content })
        });
        return res.json();
    },
    
    async updateChapter(id, bookId, title, content) {
        const res = await fetch(`${API_URL}/chapters/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ book_id: bookId, title, content })
        });
        return res.json();
    },
    
    async deleteChapter(id) {
        const res = await fetch(`${API_URL}/chapters/${id}`, { method: 'DELETE' });
        return res.json();
    },
    
    // Snapshots
    async createSnapshot(chapterId, content, note) {
        const res = await fetch(`${API_URL}/snapshots`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chapter_id: chapterId, content, note })
        });
        return res.json();
    },
    
    async getSnapshots(chapterId) {
        const res = await fetch(`${API_URL}/snapshots/${chapterId}`);
        return res.json();
    },
    
    // Essays
    async getEssays(userId) {
        const res = await fetch(`${API_URL}/essays/${userId}`);
        return res.json();
    },
    
    async createEssay(userId, title, content) {
        const res = await fetch(`${API_URL}/essays`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    async updateEssay(id, userId, title, content) {
        const res = await fetch(`${API_URL}/essays/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    // Fiction
    async getFictions(userId) {
        const res = await fetch(`${API_URL}/fictions/${userId}`);
        return res.json();
    },
    
    async createFiction(userId, title, content) {
        const res = await fetch(`${API_URL}/fictions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    async updateFiction(id, userId, title, content) {
        const res = await fetch(`${API_URL}/fictions/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    // Poems
    async getPoems(userId) {
        const res = await fetch(`${API_URL}/poems/${userId}`);
        return res.json();
    },
    
    async createPoem(userId, title, content) {
        const res = await fetch(`${API_URL}/poems`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    },
    
    async updatePoem(id, userId, title, content) {
        const res = await fetch(`${API_URL}/poems/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, title, content })
        });
        return res.json();
    }
};

export default api;