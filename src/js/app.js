// App Entry Point - Main initialization

import api from './api.js';
import editor from './components/editor.js';

const app = {
    init: function() {
        // Initialize editor with DOM elements
        editor.init('journal', {
            titleInput: document.getElementById('journal-title'),
            contentEditor: document.getElementById('journal-content'),
            itemList: document.getElementById('journal-list'),
            saveStatus: document.getElementById('save-status'),
            newButton: document.getElementById('new-journal')
        });
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});

export default app;