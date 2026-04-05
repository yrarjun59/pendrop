// Router - View Navigation

const router = {
    currentView: 'journal',
    
    init: function() {
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.target.dataset.view;
                this.navigate(view);
            });
        });
    },
    
    navigate: function(view) {
        this.currentView = view;
        
        // Update nav buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.view === view) {
                btn.classList.add('active');
            }
        });
        
        // Show/hide views
        document.querySelectorAll('.view').forEach(v => {
            v.classList.add('hidden');
        });
        document.getElementById(`${view}-view`).classList.remove('hidden');
        
        // Trigger load for current view
        this.onViewChange(view);
    },
    
    onViewChange: function(view) {
        // Dispatch event for components to load their data
        window.dispatchEvent(new CustomEvent('view-change', { detail: { view } }));
    }
};

export default router;