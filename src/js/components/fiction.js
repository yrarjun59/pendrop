// Fiction Component
const fiction = {
    init: function() {
        document.getElementById('new-fiction').addEventListener('click', () => this.create());
        document.getElementById('save-fiction').addEventListener('click', () => this.save());
    },
    load: async function() { },
    create: async function() { },
    select: function(id) { },
    save: async function() { }
};
export default fiction;