Ext.define('WPKGjs.store.Editeur', {
    extend: 'Ext.data.Store',
    model: 'WPKGjs.model.Editeur',

    autoLoad: true,
    proxy: {
        // load using HTTP
        type: 'ajax',
        url: 'get/xmlcontent',

        reader: {
        	type: 'json',
			model: 'WPKGjs.model.Editeur',
			root:'data'
		}
    }
});