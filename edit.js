'use strict';

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var divContent, item, view;

view = sublime.active_window().active_view();

divContent = view.find_all('<div[^>]*>((?!</div>).*)</div>');

log(typeof divContent === 'undefined' ? 'undefined' : _typeof(divContent));

for (item in divContent) {
  log(view.substr(divContent[item]));
}

divContent;
