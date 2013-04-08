Ext.define('WPKGjs.view.packages.List' ,{
    extend: 'Ext.grid.Panel',
    alias: 'widget.packageslist',
    title: 'Liste de applications',
store: 'Packages',
    initComponent: function() {

        this.columns = [
            {header: 'packages', dataIndex: 'uid', flex: 5},
            { header: 'checked', dataIndex: 'checked', flex: 1, xtype: 'checkcolumn'},
            { header: 'filename', dataIndex: 'filename', flex:1,hidden:true}
            
        ];
	Ext.apply(this, {
		renderTo: Ext.getBody(),
		title: 'Packages',

	items: []
	});
        this.callParent(arguments);
    },
    listeners: {
        click: {
            element: 'el', //bind to the underlying el property on the panel
            fn: function(dv, record, item, index, e)
            { var packagesStore = Ext.getStore('Packages');
            var editorStore = Ext.getStore('Editeur');
            var xmlfilename = packagesStore.findRecord('uid',record.textContent).raw.filename;
        	editorStore.load({url : 'get/xmlcontent/' + xmlfilename});
            console.log('click ' + xmlfilename);
            },
            
        },
        dblclick: {
            element: 'body', //bind to the underlying body property on the panel
            fn: function(){ console.log('dblclick body'); }
        }
    }
});
