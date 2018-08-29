view = sublime.active_window().active_view()
divContent = view.find_all('<div[^>]*>((?!</div>).*)</div>')
log(typeof divContent)
for item of divContent
	log(view.substr(divContent[item]))
	
	
divContent
