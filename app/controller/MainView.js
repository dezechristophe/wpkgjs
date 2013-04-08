Ext.define('WPKGjs.controller.MainView', {
    extend: 'Ext.app.Controller',
views: [
        'MainView',
	'packages.List',
	'gm.List',
	'Editeur'
    ],
    stores: ['gm','Packages','Editeur'],
    models: ['gm','Packages','Editeur'],
    init: function() {
        console.log('Initialized Users! This happens before the Application launch function is called');
    }
});