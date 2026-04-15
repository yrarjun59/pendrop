/**
 * Editor Module - Tiptap initialization and management
 */

const editor = {
    instance: null,
    currentChapterId: null,
    autoSaveTimer: null,
    isSaved: true,
    
    // Initialize Tiptap editor
    init() {
        this.instance = new Tiptap.Editor({
            element: document.querySelector('#tiptap-editor'),
            extensions: [
                Tiptap.StarterKit.configure({
                    heading: {
                        levels: [1, 2, 3]
                    }
                }),
                Tiptap.Placeholder.configure({
                    placeholder: 'Start writing...'
                }),
                Tiptap.Underline,
                Tiptap.TextAlign.configure({
                    types: ['heading', 'paragraph']
                })
            ],
            content: '',
            onUpdate: ({ editor }) => {
                this.scheduleAutoSave(editor.getJSON());
            }
        });
    },
    
    // Load content into editor
    loadContent(content) {
        if (!this.instance) return;
        
        if (content && content.type === 'doc') {
            this.instance.commands.setContent(content);
        } else {
            this.instance.commands.setContent('');
        }
        
        this.isSaved = true;
        app.updateSaveStatus('saved');
    },
    
    // Get current content
    getContent() {
        if (!this.instance) return { type: 'doc', content: [] };
        return this.instance.getJSON();
    },
    
    // Clear editor
    clear() {
        if (!this.instance) return;
        this.instance.commands.clearContent();
    },
    
    // Focus editor
    focus() {
        if (!this.instance) return;
        this.instance.commands.focus();
    },
    
    // Schedule auto-save (debounced 30 seconds)
    scheduleAutoSave(content) {
        this.isSaved = false;
        app.updateSaveStatus('unsaved');
        
        clearTimeout(this.autoSaveTimer);
        this.autoSaveTimer = setTimeout(() => {
            this.autoSave(content);
        }, 30000); // 30 seconds
    },
    
    // Auto-save function
    async autoSave(content) {
        if (!this.currentChapterId) return;
        
        try {
            await api.updateChapter(this.currentChapterId, {
                content: JSON.stringify(content)
            });
            this.isSaved = true;
            app.updateSaveStatus('saved');
        } catch (err) {
            console.error('Auto-save failed:', err);
            app.updateSaveStatus('error');
        }
    },
    
    // Manual save (Ctrl+S or button) - save + create snapshot
    async manualSave() {
        if (!this.currentChapterId) return;
        
        const content = this.getContent();
        
        try {
            // First, update the chapter
            await api.updateChapter(this.currentChapterId, {
                content: JSON.stringify(content)
            });
            
            // Then create a manual snapshot
            await api.createSnapshot(this.currentChapterId, {
                description: 'Manual save',
                content_json: JSON.stringify(content)
            });
            
            this.isSaved = true;
            app.updateSaveStatus('saved');
            
            // Refresh snapshots list
            snapshots.load(this.currentChapterId);
            
        } catch (err) {
            console.error('Save failed:', err);
            app.updateSaveStatus('error');
        }
    },
    
    // Set current chapter
    setChapter(chapterId) {
        this.currentChapterId = chapterId;
    },
    
    // Check if has unsaved changes
    hasUnsavedChanges() {
        return !this.isSaved;
    }
};
