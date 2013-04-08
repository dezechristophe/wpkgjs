Ext.define('WPKGjs.view.MainView', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.mainview',
    defaults: {
        // applied to each contained panel
        border:false
    	},
	title: 'mainview',
	layout: 'column',
	frame: true,
	defaults: {
		height: 500,
		frame: true
	},
 
            items: [
                {
                	xtype: 'gmlist',
			columnWidth: .2
                },
		{
            xtype: 'packageslist',
			columnWidth: .2
		},
		{
			title: 'Panel Three',
			columnWidth: .3
		}, 
		{
			title: 'Panel Three',
			width: 100,
			html: 'Panel Three Content'
		}			   
            ]      
    
});