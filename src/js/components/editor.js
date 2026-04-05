// Shared Writing Editor Component - Reusable for Journal, Books, Essays, Fiction, Poems

const editor = {
    currentId: null,
    currentType: 'journal', // journal, books, essays, fiction, poems
    saveTimer: null,
    isSaved: true,
    
    // DOM Elements
    elements: {
        titleInput: null,
        contentEditor: null,
        itemList: null,
        saveStatus: null,
        newButton: null
    },
    
    // Initialize editor for a specific type
    init: function(type, elements) {
        this.currentType = type;
        this.elements = { ...this.elements, ...elements };
        
        this.bindEvents();
        this.initToolbar();
        this.load();
    },
    
    bindEvents: function() {
        if (this.elements.newButton) {
            this.elements.newButton.addEventListener('click', () => this.create());
        }
        
        if (this.elements.titleInput) {
            this.elements.titleInput.addEventListener('input', () => this.scheduleAutoSave());
        }
        
        if (this.elements.contentEditor) {
            this.elements.contentEditor.addEventListener('input', () => this.scheduleAutoSave());
        }
    },
    
    initToolbar: function() {
        const toolbar = document.querySelector('.toolbar');
        if (!toolbar) return;
        
        toolbar.querySelectorAll('.tool-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const command = btn.dataset.command;
                this.execCommand(command);
            });
        });
    },
    
    execCommand: function(command) {
        if (!this.elements.contentEditor) return;
        
        this.elements.contentEditor.focus();
        
        switch(command) {
            case 'bold':
                document.execCommand('bold', false, null);
                break;
            case 'italic':
                document.execCommand('italic', false, null);
                break;
            case 'underline':
                document.execCommand('underline', false, null);
                break;
            case 'h1':
                document.execCommand('formatBlock', false, '<h1>');
                break;
            case 'h2':
                document.execCommand('formatBlock', false, '<h2>');
                break;
            case 'h3':
                document.execCommand('formatBlock', false, '<h3>');
                break;
            case 'ul':
                document.execCommand('insertUnorderedList', false, null);
                break;
            case 'ol':
                document.execCommand('insertOrderedList', false, null);
                break;
            case 'quote':
                document.execCommand('formatBlock', false, '<blockquote>');
                break;
        }
        
        this.scheduleAutoSave();
    },
    
    // Load items list
    load: async function() {
        const userId = 1;
        let items = [];
        
        try {
            switch(this.currentType) {
                case 'journal':
                    items = await api.getJournals(userId);
                    break;
                case 'essays':
                    items = await api.getEssays(userId);
                    break;
                case 'fiction':
                    items = await api.getFictions(userId);
                    break;
                case 'poems':
                    items = await api.getPoems(userId);
                    break;
            }
            
            this.renderList(items);
            
            if (!this.currentId && items.length > 0) {
                this.select(items[0].id);
            } else if (items.length === 0) {
                this.create();
            }
        } catch (err) {
            console.error('Error loading items:', err);
        }
    },
    
    renderList: function(items) {
        if (!this.elements.itemList) return;
        
        if (items.length === 0) {
            this.elements.itemList.innerHTML = '<p style="padding: 12px; color: var(--text-secondary); font-size: 13px;">No entries yet</p>';
            return;
        }
        
        const icon = this.getIcon();
        
        this.elements.itemList.innerHTML = items.map(item => `
            <button class="item-btn ${this.currentId === item.id ? 'active' : ''}" data-id="${item.id}">
                <span class="title">${item.title || 'Untitled'}</span>
                <span class="date">${this.formatDate(item.updated_at)}</span>
            </button>
        `).join('');
        
        this.elements.itemList.querySelectorAll('.item-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.select(parseInt(btn.dataset.id));
            });
        });
    },
    
    getIcon: function() {
        const icons = {
            journal: '📝',
            essays: '📄',
            fiction: '🎭',
            poems: '🎵'
        };
        return icons[this.currentType] || '📝';
    },
    
    select: async function(id) {
        // Save current before switching
        if (!this.isSaved && this.currentId) {
            await this.save();
        }
        
        this.currentId = id;
        
        try {
            const userId = 1;
            let items = [];
            
            switch(this.currentType) {
                case 'journal':
                    items = await api.getJournals(userId);
                    break;
                case 'essays':
                    items = await api.getEssays(userId);
                    break;
                case 'fiction':
                    items = await api.getFictions(userId);
                    break;
                case 'poems':
                    items = await api.getPoems(userId);
                    break;
            }
            
            const item = items.find(i => i.id === id);
            
            if (item && this.elements.titleInput) {
                this.elements.titleInput.value = item.title || 'Untitled';
                this.elements.contentEditor.innerHTML = item.content || '';
            }
            
            this.renderList(items);
            this.updateSaveStatus('All changes saved');
        } catch (err) {
            console.error('Error selecting item:', err);
        }
    },
    
    create: async function() {
        const userId = 1;
        const titles = {
            journal: 'Untitled',
            essays: 'Untitled Essay',
            fiction: 'Untitled Story',
            poems: 'Untitled Poem'
        };
        
        try {
            let result;
            
            switch(this.currentType) {
                case 'journal':
                    result = await api.createJournal(userId, titles.journal, '');
                    break;
                case 'essays':
                    result = await api.createEssay(userId, titles.essays, '');
                    break;
                case 'fiction':
                    result = await api.createFiction(userId, titles.fiction, '');
                    break;
                case 'poems':
                    result = await api.createPoem(userId, titles.poems, '');
                    break;
            }
            
            this.currentId = result.id;
            
            if (this.elements.titleInput) {
                this.elements.titleInput.value = titles[this.currentType];
            }
            if (this.elements.contentEditor) {
                this.elements.contentEditor.innerHTML = '';
            }
            
            this.load();
            
            if (this.elements.titleInput) {
                this.elements.titleInput.focus();
            }
        } catch (err) {
            console.error('Error creating item:', err);
        }
    },
    
    scheduleAutoSave: function() {
        this.isSaved = false;
        this.updateSaveStatus('Saving...');
        
        clearTimeout(this.saveTimer);
        this.saveTimer = setTimeout(() => {
            this.save();
        }, 2000);
    },
    
    save: async function() {
        if (!this.currentId) return;
        
        const userId = 1;
        const title = this.elements.titleInput ? this.elements.titleInput.value : '';
        const content = this.elements.contentEditor ? this.elements.contentEditor.innerHTML : '';
        
        try {
            switch(this.currentType) {
                case 'journal':
                    await api.updateJournal(this.currentId, userId, title, content);
                    break;
                case 'essays':
                    await api.updateEssay(this.currentId, userId, title, content);
                    break;
                case 'fiction':
                    await api.updateFiction(this.currentId, userId, title, content);
                    break;
                case 'poems':
                    await api.updatePoem(this.currentId, userId, title, content);
                    break;
            }
            
            this.isSaved = true;
            this.updateSaveStatus('All changes saved');
            this.load();
        } catch (err) {
            console.error('Error saving:', err);
            this.updateSaveStatus('Save failed');
        }
    },
    
    updateSaveStatus: function(status) {
        if (this.elements.saveStatus) {
            this.elements.saveStatus.textContent = status;
        }
    },
    
    formatDate: function(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;
        
        if (diff < 86400000) {
            return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
        }
        
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    },
    
    // Switch between types (journal, essays, fiction, poems)
    switchType: function(type) {
        this.currentId = null;
        this.currentType = type;
        this.load();
    }
};

export default editor;