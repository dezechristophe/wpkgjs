Ext.define('WPKGjs.model.Packages',{
    extend: 'Ext.data.Model',
    fields: [
    {name:'uid'},
    {name:'name'},
    {name:'filename'},
    {name: 'checked', type: 'bool'}
    ]
});