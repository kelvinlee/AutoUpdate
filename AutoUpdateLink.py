import sublime
import sublime_plugin
import os

class AutoUpdateLinkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print(self.view.sel())