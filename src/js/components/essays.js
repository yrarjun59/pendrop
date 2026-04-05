// Essays Component
const essays = {
    init: function() {
        document.getElementById('new-essay').addEventListener('click', () => this.create());
        document.getElementById('save-essay').addEventListener('click', () => this.save());
    },
    load: async function() { },
    create: async function() { },
    select: function(id) { },
    save: async function() { }
};
export default essays;