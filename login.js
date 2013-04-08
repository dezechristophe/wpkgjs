Ext.application({
    requires: ['Ext.container.Viewport'],
    name: 'WPKGjs',

    appFolder: 'app',

    controllers: [
	'Login'
    ],

    views: [
		'Login',
    ],
	autoCreateViewport: true,
    launch: function() {
console.log("Launching MyApp");
    }
});