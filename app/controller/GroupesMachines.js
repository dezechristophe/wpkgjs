 Ext.define('WPKGjs.controller.GroupesMachines', {
    extend: 'Ext.app.Controller',
	 views: [
        	'gm.List',
   	 	],
	stores: [
		'gm',
		],
	models: [
		'gm',
	],

    init: function() {
        this.control({
            'viewport > panel': {
                render: this.onPanelRendered
            }
        });
    },

    onPanelRendered: function() {
        console.log('The panel was rendered');
    }
});