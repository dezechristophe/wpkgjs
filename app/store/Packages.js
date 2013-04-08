Ext.define('WPKGjs.store.Packages', {
    extend: 'Ext.data.Store',
    model: 'WPKGjs.model.Packages',
	//fields: ['filename','id', 'name'],
    autoLoad: true,
    proxy: {
        // load using HTTP
        type: 'ajax',
        url: 'get/packages',

        reader: {
        		type: 'json',
			model: 'WPKGjs.model.Packages',
root:'data'
		}
    }
});