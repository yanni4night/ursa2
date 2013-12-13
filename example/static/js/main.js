define('main', ["text!./tpl/list.tpl", "./test/index", './common/testsuit'], function(tpl) {
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