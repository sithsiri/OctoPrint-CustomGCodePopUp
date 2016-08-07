$(function() {
    function M117PopUpViewModel(parameters) {
        var self = this;

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "M117PopUp") {
				// console.log('Ignoring '+plugin);
                return;
            }
			
			if(data.type == "popup") {
				// console.log(data.msg);
				new PNotify({
					title: 'M117 Pop Up Message',
					text: data.msg,
					type: 'info'
					});
			}
		}

    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        M117PopUpViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["loginStateViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        document.getElementById('sidebar_plugin_M117PopUp')
    ]);
});