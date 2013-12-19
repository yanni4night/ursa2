define('main', ["text!./tpl/list.tpl"], function(tpl) {
	!window.console && (
		window.console = {
			log: function() {},
			debug: function() {},
			error: function() {},
			clear: function() {}
		}
	);


	return {
		common: function() {}
	};
});