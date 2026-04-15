/**
 * App - Main application controller
 */

const app = {
    // Initialize application
    init() {
        // Initialize components
        editor.init();
        sidebar.init();
        
        // Bind global events
        this.bindEvents();
        
        // Load initial state
        sidebar.setMode('books');
    },
    
    // Bind global events
    bindEvents() {
        // Save button
        document.getElementById('save-btn').addEventListener('click', () => {
            if (sidebar.currentMode === 'books' && sidebar.currentChapterId) {
                editor.manualSave();
            }
        });
        
        // Title change
        document.getElementById('doc-title').addEventListener('input', (e) => {
            this.onTitleChange(e.target.value);
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl+S or Cmd+S
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                if (sidebar.currentMode === 'books' && sidebar.currentChapterId) {
                    editor.manualSave();
                }
            }
        });
        
        // Snapshot FAB
        document.getElementById('snapshot-fab').addEventListener('click', () => {
            snapshots.toggle();
        });
        
        // Close snapshots panel
        document.getElementById('close-snapshots').addEventListener('click', () => {
            snapshots.hide();
        });
    },
    
    // Handle title change
    async onTitleChange(newTitle) {
        if (sidebar.currentMode === 'books' && sidebar.currentChapterId) {
            try {
                await api.updateChapter(sidebar.currentChapterId, {
                    title: newTitle
                });
                
                // Reload chapters to update sidebar
                sidebar.loadChapters(sidebar.currentBookId);
            } catch (err) {
                console.error('Failed to update title:', err);
            }
        }
    },
    
    // Update save status indicator
    updateSaveStatus(status) {
        const el = document.getElementById('save-status');
        
        el.classList.remove('saving', 'saved', 'error');
        
        switch (status) {
            case 'saving':
                el.textContent = 'Saving...';
                el.classList.add('saving');
                break;
            case 'saved':
                el.textContent = 'Saved';
                el.classList.add('saved');
                break;
            case 'unsaved':
                el.textContent = 'Unsaved changes';
                break;
            case 'error':
                el.textContent = 'Save failed';
                el.classList.add('error');
                break;
            default:
                el.textContent = status;
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
