 Ext.define('WPKGjs.controller.Packages', {
    extend: 'Ext.app.Controller',
	 views: [
		'packages.List'
		],
	stores: [
		'Packages'
		],
	models: [
		'Packages'
	],

    init: function() {
        this.control({
            'viewport > panel': {
                render: this.onPanelRendered
            }
        });
    },

    onPanelRendered: function() {
        console.log('The panel packages was rendered');
    }
});