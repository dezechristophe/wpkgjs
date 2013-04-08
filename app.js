Ext.Loader.setPath('Ext.ux', 'extjs/examples/ux');
Ext.application({
    requires: ['Ext.container.Viewport'],
    name: 'WPKGjs',
    appFolder: 'app',
	controllers: [
	'MainView'
    ],
    autoCreateViewport: false,
    requires: [
        'WPKGjs.view.gm.List',
        'WPKGjs.view.packages.List',
        'WPKGjs.view.Editeur',
        'Ext.ux.CheckColumn',
	//'Ext.ux.edit_area.edit_area'
    ],

    launch: function() {
Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: {
                xtype: 'mainview'
            }
        });
    }
});