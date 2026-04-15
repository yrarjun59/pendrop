/**
 * API Module - Fetch wrappers for all endpoints
 */

const API_BASE = 'http://127.0.0.1:8000/api';

const api = {
    // ==================== BOOKS ====================
    
    async getBooks() {
        const res = await fetch(`${API_BASE}/books`);
        return res.json();
    },
    
    async createBook(title) {
        const res = await fetch(`${API_BASE}/books`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        });
        return res.json();
    },
    
    async getBook(bookId) {
        const res = await fetch(`${API_BASE}/books/${bookId}`);
        return res.json();
    },
    
    async updateBook(bookId, data) {
        const res = await fetch(`${API_BASE}/books/${bookId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async deleteBook(bookId) {
        const res = await fetch(`${API_BASE}/books/${bookId}`, {
            method: 'DELETE'
        });
        return res.json();
    },
    
    // ==================== CHAPTERS ====================
    
    async getChapters(bookId) {
        const res = await fetch(`${API_BASE}/books/${bookId}/chapters`);
        return res.json();
    },
    
    async createChapter(bookId, data) {
        const res = await fetch(`${API_BASE}/books/${bookId}/chapters`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async getChapter(chapterId) {
        const res = await fetch(`${API_BASE}/chapters/${chapterId}`);
        return res.json();
    },
    
    async updateChapter(chapterId, data) {
        const res = await fetch(`${API_BASE}/chapters/${chapterId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async deleteChapter(chapterId) {
        const res = await fetch(`${API_BASE}/chapters/${chapterId}`, {
            method: 'DELETE'
        });
        return res.json();
    },
    
    // ==================== SNAPSHOTS ====================
    
    async getSnapshots(chapterId) {
        const res = await fetch(`${API_BASE}/chapters/${chapterId}/snapshots`);
        return res.json();
    },
    
    async createSnapshot(chapterId, data) {
        const res = await fetch(`${API_BASE}/chapters/${chapterId}/snapshots`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async restoreSnapshot(chapterId, snapshotId) {
        const res = await fetch(`${API_BASE}/chapters/${chapterId}/restore`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ snapshot_id: snapshotId })
        });
        return res.json();
    },
    
    // ==================== JOURNAL ====================
    
    async getJournal() {
        const res = await fetch(`${API_BASE}/journal`);
        return res.json();
    },
    
    async createJournal(data) {
        const res = await fetch(`${API_BASE}/journal`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async getJournalEntry(entryId) {
        const res = await fetch(`${API_BASE}/journal/${entryId}`);
        return res.json();
    },
    
    async updateJournalEntry(entryId, data) {
        const res = await fetch(`${API_BASE}/journal/${entryId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async deleteJournalEntry(entryId) {
        const res = await fetch(`${API_BASE}/journal/${entryId}`, {
            method: 'DELETE'
        });
        return res.json();
    }
};
