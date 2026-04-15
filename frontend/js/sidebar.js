/**
 * Sidebar Module - Books list and chapter tree management
 */

const sidebar = {
    currentMode: 'books', // 'books' or 'journal'
    currentBookId: null,
    currentChapterId: null,
    draggedChapterId: null,
    
    // Initialize sidebar
    init() {
        this.bindEvents();
    },
    
    // Bind UI events
    bindEvents() {
        // Mode toggle
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = e.target.dataset.mode;
                this.setMode(mode);
            });
        });
        
        // Add book
        document.getElementById('add-book-btn').addEventListener('click', () => {
            this.addBook();
        });
        
        // Back to books
        document.getElementById('back-to-books').addEventListener('click', () => {
            this.showBooksList();
        });
        
        // Add chapter
        document.getElementById('add-chapter-btn').addEventListener('click', () => {
            this.addChapter();
        });
        
        // Add journal entry
        document.getElementById('add-journal-btn').addEventListener('click', () => {
            this.addJournalEntry();
        });
    },
    
    // Set mode (books or journal)
    setMode(mode) {
        this.currentMode = mode;
        
        // Update mode buttons
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
        
        // Show/hide sections
        if (mode === 'books') {
            document.getElementById('books-section').classList.remove('hidden');
            document.getElementById('chapters-section').classList.add('hidden');
            document.getElementById('journal-section').classList.add('hidden');
            this.loadBooks();
        } else {
            document.getElementById('books-section').classList.add('hidden');
            document.getElementById('chapters-section').classList.add('hidden');
            document.getElementById('journal-section').classList.remove('hidden');
            this.loadJournalEntries();
        }
        
        // Hide editor
        document.getElementById('editor-empty').classList.remove('hidden');
        document.getElementById('editor-container').classList.add('hidden');
        document.getElementById('snapshot-fab').classList.add('hidden');
        
        // Clear editor
        editor.clear();
        document.getElementById('doc-title').value = '';
    },
    
    // ==================== BOOKS ====================
    
    // Load and display books
    async loadBooks() {
        try {
            const books = await api.getBooks();
            this.renderBooksList(books);
        } catch (err) {
            console.error('Failed to load books:', err);
        }
    },
    
    // Render books list
    renderBooksList(books) {
        const container = document.getElementById('books-list');
        
        if (!books || books.length === 0) {
            container.innerHTML = '<p class="empty-message">No books yet. Click + to create one.</p>';
            return;
        }
        
        container.innerHTML = books.map(book => `
            <div class="item ${this.currentBookId === book.id ? 'active' : ''}" data-id="${book.id}">
                <div class="item-title">📖 ${book.title}</div>
                <div class="item-meta">${this.formatDate(book.updated_at)}</div>
            </div>
        `).join('');
        
        // Add click handlers
        container.querySelectorAll('.item').forEach(item => {
            item.addEventListener('click', () => {
                const bookId = parseInt(item.dataset.id);
                this.selectBook(bookId);
            });
        });
    },
    
    // Select a book
    async selectBook(bookId) {
        this.currentBookId = bookId;
        this.currentChapterId = null;
        
        // Update UI
        document.getElementById('books-section').classList.add('hidden');
        document.getElementById('chapters-section').classList.remove('hidden');
        
        // Get book title
        try {
            const book = await api.getBook(bookId);
            document.getElementById('current-book-title').textContent = book.title;
        } catch (err) {
            console.error('Failed to get book:', err);
        }
        
        // Load chapters
        await this.loadChapters(bookId);
        
        // Hide editor
        document.getElementById('editor-empty').classList.remove('hidden');
        document.getElementById('editor-container').classList.add('hidden');
        document.getElementById('snapshot-fab').classList.add('hidden');
    },
    
    // Show books list (back button)
    showBooksList() {
        this.currentBookId = null;
        this.currentChapterId = null;
        
        document.getElementById('books-section').classList.remove('hidden');
        document.getElementById('chapters-section').classList.add('hidden');
        
        this.loadBooks();
    },
    
    // Add new book
    async addBook() {
        try {
            const book = await api.createBook('Untitled Book');
            this.loadBooks();
            this.selectBook(book.id);
        } catch (err) {
            console.error('Failed to create book:', err);
        }
    },
    
    // ==================== CHAPTERS ====================
    
    // Load and display chapters
    async loadChapters(bookId) {
        try {
            const chapters = await api.getChapters(bookId);
            this.renderChapterTree(chapters);
        } catch (err) {
            console.error('Failed to load chapters:', err);
        }
    },
    
    // Render chapter tree (recursive)
    renderChapterTree(chapters, parentId = null, level = 1) {
        const container = document.getElementById('chapters-list');
        
        if (level === 1) {
            container.innerHTML = '';
        }
        
        const filtered = chapters.filter(ch => ch.parent_id === parentId);
        
        filtered.forEach(chapter => {
            const html = `
                <div class="chapter-item" data-level="${level}" data-id="${chapter.id}">
                    <div class="chapter-row" draggable="true">
                        <span class="drag-handle">⋮⋮</span>
                        <span class="chapter-title">${chapter.title}</span>
                        <div class="chapter-actions">
                            <button class="chapter-action add-sub" title="Add sub-chapter">+</button>
                            <button class="chapter-action delete" title="Delete">×</button>
                        </div>
                    </div>
                    <div class="chapter-children"></div>
                </div>
            `;
            
            if (level === 1) {
                container.insertAdjacentHTML('beforeend', html);
            }
            
            // Add event listeners
            const item = container.querySelector(`[data-id="${chapter.id}"]`);
            const row = item.querySelector('.chapter-row');
            
            // Click to select
            row.addEventListener('click', (e) => {
                if (!e.target.closest('.chapter-actions')) {
                    this.selectChapter(chapter.id);
                }
            });
            
            // Add sub-chapter
            item.querySelector('.add-sub').addEventListener('click', () => {
                this.addChapter(chapter.id);
            });
            
            // Delete chapter
            item.querySelector('.delete').addEventListener('click', () => {
                this.deleteChapter(chapter.id);
            });
            
            // Drag and drop
            row.addEventListener('dragstart', (e) => {
                this.draggedChapterId = chapter.id;
                e.dataTransfer.effectAllowed = 'move';
            });
            
            row.addEventListener('dragover', (e) => {
                e.preventDefault();
                row.style.background = 'var(--bg-tertiary)';
            });
            
            row.addEventListener('dragleave', () => {
                row.style.background = '';
            });
            
            row.addEventListener('drop', async (e) => {
                e.preventDefault();
                row.style.background = '';
                if (this.draggedChapterId && this.draggedChapterId !== chapter.id) {
                    await this.reorderChapter(this.draggedChapterId, chapter.parent_id, chapter.position);
                }
                this.draggedChapterId = null;
            });
            
            // Render children
            this.renderChapterTree(chapters, chapter.id, level + 1);
        });
    },
    
    // Select a chapter
    async selectChapter(chapterId) {
        // Save current chapter first if unsaved
        if (editor.hasUnsavedChanges() && editor.currentChapterId) {
            await editor.manualSave();
        }
        
        this.currentChapterId = chapterId;
        editor.setChapter(chapterId);
        
        // Update UI
        document.querySelectorAll('.chapter-row').forEach(row => {
            row.classList.remove('active');
        });
        document.querySelector(`.chapter-row[data-id="${chapterId}"]`)?.classList.add('active');
        
        // Load chapter content
        try {
            const chapter = await api.getChapter(chapterId);
            document.getElementById('doc-title').value = chapter.title;
            
            // Parse content
            let content = { type: 'doc', content: [] };
            if (chapter.content) {
                try {
                    content = JSON.parse(chapter.content);
                } catch (e) {
                    content = { type: 'doc', content: [] };
                }
            }
            
            editor.loadContent(content);
            
            // Show editor
            document.getElementById('editor-empty').classList.add('hidden');
            document.getElementById('editor-container').classList.remove('hidden');
            document.getElementById('snapshot-fab').classList.remove('hidden');
            
            // Load snapshots
            snapshots.load(chapterId);
            
        } catch (err) {
            console.error('Failed to load chapter:', err);
        }
    },
    
    // Add new chapter
    async addChapter(parentId = null) {
        if (!this.currentBookId) return;
        
        try {
            const chapter = await api.createChapter(this.currentBookId, {
                title: 'New Chapter',
                parent_id: parentId
            });
            
            await this.loadChapters(this.currentBookId);
            this.selectChapter(chapter.id);
        } catch (err) {
            console.error('Failed to create chapter:', err);
        }
    },
    
    // Delete chapter
    async deleteChapter(chapterId) {
        if (!confirm('Delete this chapter? This cannot be undone.')) return;
        
        try {
            await api.deleteChapter(chapterId);
            
            if (this.currentChapterId === chapterId) {
                this.currentChapterId = null;
                document.getElementById('editor-empty').classList.remove('hidden');
                document.getElementById('editor-container').classList.add('hidden');
                document.getElementById('snapshot-fab').classList.add('hidden');
                editor.clear();
            }
            
            await this.loadChapters(this.currentBookId);
        } catch (err) {
            console.error('Failed to delete chapter:', err);
        }
    },
    
    // Reorder chapter
    async reorderChapter(chapterId, newParentId, newPosition) {
        try {
            await api.updateChapter(chapterId, {
                parent_id: newParentId,
                position: newPosition
            });
            
            await this.loadChapters(this.currentBookId);
        } catch (err) {
            console.error('Failed to reorder chapter:', err);
        }
    },
    
    // ==================== JOURNAL ====================
    
    // Load journal entries
    async loadJournalEntries() {
        try {
            const entries = await api.getJournal();
            this.renderJournalEntries(entries);
        } catch (err) {
            console.error('Failed to load journal:', err);
        }
    },
    
    // Render journal entries
    renderJournalEntries(entries) {
        const container = document.getElementById('journal-list');
        
        if (!entries || entries.length === 0) {
            container.innerHTML = '<p class="empty-message">No entries yet. Click + to create one.</p>';
            return;
        }
        
        container.innerHTML = entries.map(entry => `
            <div class="item" data-id="${entry.id}">
                <div class="item-title">📝 ${entry.title || 'Untitled'}</div>
                <div class="item-meta">${this.formatDate(entry.updated_at)}</div>
            </div>
        `).join('');
        
        // Add click handlers
        container.querySelectorAll('.item').forEach(item => {
            item.addEventListener('click', () => {
                const entryId = parseInt(item.dataset.id);
                this.selectJournalEntry(entryId);
            });
        });
    },
    
    // Select journal entry
    async selectJournalEntry(entryId) {
        try {
            const entry = await api.getJournalEntry(entryId);
            document.getElementById('doc-title').value = entry.title || 'Untitled';
            
            // For journal, just use plain text for now
            // Could integrate with Tiptap if needed
            editor.clear();
            
            // Show editor
            document.getElementById('editor-empty').classList.add('hidden');
            document.getElementById('editor-container').classList.remove('hidden');
            
            // No snapshots for journal in v1
            document.getElementById('snapshot-fab').classList.add('hidden');
            
        } catch (err) {
            console.error('Failed to load journal entry:', err);
        }
    },
    
    // Add journal entry
    async addJournalEntry() {
        try {
            const entry = await api.createJournal({
                title: 'Untitled',
                content: ''
            });
            
            this.loadJournalEntries();
            this.selectJournalEntry(entry.id);
        } catch (err) {
            console.error('Failed to create journal entry:', err);
        }
    },
    
    // Format date
    formatDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;
        
        if (diff < 86400000) {
            return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
        }
        
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
};
