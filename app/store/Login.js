Ext.define('WPKGjs.store.Login', {
    extend: 'Ext.data.Store',
    model: 'WPKGjs.model.Login',
 
autoLoad: true,
 
proxy: {
    type: 'ajax',
    url: 'log/in',
    method: 'GET',
    reader: {
        type: 'json',
        root: 'model',
        successProperty: 'model.success'
    }
}
 
});