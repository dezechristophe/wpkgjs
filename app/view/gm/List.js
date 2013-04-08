Ext.define('WPKGjs.view.gm.List' ,{
	extend: 'Ext.grid.Panel',
	alias: 'widget.gmlist',
	store:'gm',  
	title: 'Machines ESU',

	initComponent: function() {
	        this.columns = [
	            {header: 'gm', dataIndex: 'grp', flex: 1}
	        ];
	        this.callParent(arguments);
	},
    listeners: {
        click: {
            element: 'el', //bind to the underlying el property on the panel
            fn: function(dv, record, item, index, e)
		{
            console.log('click ' + record.textContent); 
             var packagesStore = Ext.getStore('Packages');

            //packagesStore.proxy.extraParams = {url : 'get/packages/' + record.textContent};
            packagesStore.load({url : 'get/packages/' + record.textContent});
        }
        },
        dblclick: {
            element: 'body', //bind to the underlying body property on the panel
            fn: function(){ console.log('dblclick body'); }
        }
    }
});