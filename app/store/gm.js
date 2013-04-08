Ext.define('WPKGjs.store.gm', {
    extend: 'Ext.data.Store',
    model: 'WPKGjs.model.gm',

    autoLoad: true,
    proxy: {
        // load using HTTP
        type: 'ajax',
        url: 'get/groupesesu',
        // the return will be XML, so lets set up a reader
        reader: {
        	type: 'json',
		model: 'WPKGjs.model.gm',
		root: 'data'
        }
    }
});