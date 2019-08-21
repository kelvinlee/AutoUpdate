import sublime
import sublime_plugin
from . import get_image_size
import os
import io
import re


class GetSvgCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.window = sublime.active_window()
		self.thedir = self.window.folders()[0]

def getsvg(file_path):
		with io.open(file_path, "rb") as input:
			svgContent = str(input.read())
			w = re.findall(r"width=['\"]?(.*?)['\"].*?>", svgContent)[0]
			h = re.findall(r"height=['\"]?(.*?)['\"].*?>", svgContent)[0]
			if int(w) > 0 and int(h) > 0:
				return (w, h)
			else:
				return (-1, -1)
			# 如果获取不到 width height 使用 viewbox.
			# viewbox = re.findall(r"viewBox=['\"]?(.*?)['\"].*?>", svgContent)[0]
