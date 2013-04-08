Ext.define('WPKGjs.view.Viewport', {
    extend: 'Ext.container.Viewport',
    requires: [
        'WPKGjs.view.Login',
    ],
    layout: 'fit',
    initComponent: function() {
        this.items = {
                xtype: 'panel',
                title: 'My App',
                height: 800,
                width: '100%',
                layout: {
                 type:'hbox',
                 align:'middle', 
                 pack:'center'},
                items:[{        
                    xtype: 'authBox',
                }]
        };
        this.callParent();
    }
});