Ext.define('WPKGjs.controller.Login', {
    extend: 'Ext.app.Controller',
    init: function() {
     this.control({
      'authBox button[action=auth]':{
       click:this.auth
      }
     });
    },
    auth: function(button) {
     console.log("Authenticating...");
     var form = button.up('form').getForm();// get the basic form
        if (form.isValid()) { // make sure the form contains valid data before submitting
            form.submit({
                success: function(form, action) {
                   Ext.Msg.alert('Success', action.result.msg);
                        var redirect = 'main'; 
		                window.location = redirect;
                },
                failure: function(form, action) {
                 console.log(action.result);
                 var msg = action.result.msg;
           
                    Ext.Msg.alert('Failed', msg);
                }
            });
        } else { // display error alert if the data is invalid
            Ext.Msg.alert('Invalid Data', 'Please correct form errors.');
        }
    }
});
