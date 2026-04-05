// Poems Component
const poems = {
    init: function() {
        document.getElementById('new-poem').addEventListener('click', () => this.create());
        document.getElementById('save-poem').addEventListener('click', () => this.save());
    },
    load: async function() { },
    create: async function() { },
    select: function(id) { },
    save: async function() { }
};
export default poems;