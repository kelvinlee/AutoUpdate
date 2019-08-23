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
			cw = re.findall(r"width=['\"]?(.*?)['\"].*?>", svgContent)
			ch = re.findall(r"height=['\"]?(.*?)['\"].*?>", svgContent)
			w = str(cw[0]).replace("px","") if len(cw) > 0 else -1
			h = str(ch[0]).replace("px","") if len(ch) > 0 else -1
			if int(w) > 0 and int(h) > 0:
				return (int(w), int(h))
			else:
				cv = re.findall(r"viewBox=['\"]?(.*?)['\"].*?>", svgContent)
				if len(cv) > 0:
					viewbox = re.findall(r"viewBox=['\"]?(.*?)['\"].*?>", svgContent)[0]
					# print("viewbox:", viewbox.split(" "))
					w = viewbox.split(" ")[2]
					h = viewbox.split(" ")[3]
					return (int(w), int(h))
				else:
					return (-1,-1)

			# 如果获取不到 width height 使用 viewbox.
			# viewbox = re.findall(r"viewBox=['\"]?(.*?)['\"].*?>", svgContent)[0]
