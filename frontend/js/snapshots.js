/**
 * Snapshots Module - List, view, and restore snapshots
 */

const snapshots = {
    currentChapterId: null,
    
    // Load snapshots for a chapter
    async load(chapterId) {
        this.currentChapterId = chapterId;
        
        try {
            const list = await api.getSnapshots(chapterId);
            this.render(list);
        } catch (err) {
            console.error('Failed to load snapshots:', err);
        }
    },
    
    // Render snapshots list
    render(list) {
        const container = document.getElementById('snapshots-list');
        
        if (!list || list.length === 0) {
            container.innerHTML = '<p class="empty-message">No snapshots yet. Use Ctrl+S to create one.</p>';
            return;
        }
        
        container.innerHTML = list.map(snap => `
            <div class="snapshot-item" data-id="${snap.id}">
                <div class="snapshot-time">${this.formatDateTime(snap.created_at)}</div>
                <div class="snapshot-desc">${snap.description || 'Auto-save'}</div>
                <div class="snapshot-actions">
                    <button class="snapshot-action view">View</button>
                    <button class="snapshot-action restore">Restore</button>
                </div>
            </div>
        `).join('');
        
        // Add event listeners
        container.querySelectorAll('.snapshot-item').forEach(item => {
            const snapId = parseInt(item.dataset.id);
            
            item.querySelector('.view').addEventListener('click', () => {
                this.viewSnapshot(snapId);
            });
            
            item.querySelector('.restore').addEventListener('click', () => {
                this.restoreSnapshot(snapId);
            });
        });
    },
    
    // View snapshot content
    async viewSnapshot(snapshotId) {
        try {
            const list = await api.getSnapshots(this.currentChapterId);
            const snap = list.find(s => s.id === snapshotId);
            
            if (!snap) return;
            
            // Parse content
            let content = '';
            if (snap.content_json) {
                try {
                    const parsed = JSON.parse(snap.content_json);
                    content = this.contentToText(parsed);
                } catch (e) {
                    content = snap.content_json;
                }
            }
            
            // Show in alert (could be a modal)
            alert(`Snapshot from ${this.formatDateTime(snap.created_at)}\n\n${content.substring(0, 500)}${content.length > 500 ? '...' : ''}`);
            
        } catch (err) {
            console.error('Failed to view snapshot:', err);
        }
    },
    
    // Restore snapshot (safe restore)
    async restoreSnapshot(snapshotId) {
        if (!confirm('Restore this snapshot? Your current work will be saved as a backup first.')) {
            return;
        }
        
        try {
            // Get current content first (for backup)
            const currentContent = editor.getContent();
            
            // Create backup snapshot
            await api.createSnapshot(this.currentChapterId, {
                description: 'Auto-backup before restore',
                content_json: JSON.stringify(currentContent)
            });
            
            // Restore from selected snapshot
            await api.restoreSnapshot(this.currentChapterId, snapshotId);
            
            // Reload chapter content
            const chapter = await api.getChapter(this.currentChapterId);
            document.getElementById('doc-title').value = chapter.title;
            
            let content = { type: 'doc', content: [] };
            if (chapter.content) {
                try {
                    content = JSON.parse(chapter.content);
                } catch (e) {
                    content = { type: 'doc', content: [] };
                }
            }
            
            editor.loadContent(content);
            
            // Refresh snapshots list
            this.load(this.currentChapterId);
            
            app.updateSaveStatus('saved');
            alert('Snapshot restored successfully!');
            
        } catch (err) {
            console.error('Failed to restore snapshot:', err);
            alert('Failed to restore snapshot.');
        }
    },
    
    // Toggle snapshot panel
    toggle() {
        const panel = document.getElementById('snapshot-panel');
        panel.classList.toggle('hidden');
    },
    
    // Show panel
    show() {
        document.getElementById('snapshot-panel').classList.remove('hidden');
    },
    
    // Hide panel
    hide() {
        document.getElementById('snapshot-panel').classList.add('hidden');
    },
    
    // Convert Tiptap JSON to readable text
    contentToText(json) {
        if (!json || !json.content) return '';
        
        const lines = [];
        
        json.content.forEach(node => {
            if (node.type === 'paragraph') {
                const text = node.content ? node.content.map(n => n.text || '').join('') : '';
                lines.push(text);
            } else if (node.type === 'heading') {
                const text = node.content ? node.content.map(n => n.text || '').join('') : '';
                lines.push(`\n${'#'.repeat(node.attrs.level)} ${text}\n`);
            } else if (node.type === 'bulletList') {
                node.content.forEach(item => {
                    const text = item.content ? item.content.map(n => n.content ? n.content.map(m => m.text || '').join('') : '').join('') : '';
                    lines.push(`• ${text}`);
                });
            }
        });
        
        return lines.join('\n');
    },
    
    // Format datetime
    formatDateTime(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
        });
    }
};
