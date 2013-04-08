Ext.define('WPKGjs.view.Editeur' ,{
    extend: 'Ext.grid.Panel',

 alias: 'widget.editeur',
    title: 'editeur',
store: 'Editeur',

    initComponent: function() {

	Ext.apply(this, {
		renderTo: Ext.getBody(),
		title: 'Editeur'

	});
        this.callParent(arguments);
    },
    
});

