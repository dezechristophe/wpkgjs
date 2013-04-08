 Ext.define('WPKGjs.controller.Editeur', {
    extend: 'Ext.app.Controller',
	 views: [
		'Editeur'
		],
	stores: [
		'Editeur'
		],
	models: [
		'Editeur'
	],

    init: function() {
        this.control({
            'viewport > panel': {
                render: this.onPanelRendered
            }
        });
    },

    onPanelRendered: function() {
        console.log('The panel Editor was rendered');
    }
});