if fileName.indexOf "Development" and fileName.indexOf "applecom"
	log(fileName)
	newName = fileName.replace(/(gc|cn|tw|mo|hk)/ig,"us")
	log(newName)
	win = sublime.active_window().open_file newName
	win.window().focus_view(win)
	win.find_all('<a')
	# sublime.Window().open_file(newName,sublime.TRANSIENT)
else
	log("a")