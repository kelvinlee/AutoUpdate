import sublime
import sublime_plugin
import os

# 更新主程序的 v 到本地 (暂停).
class AutoUpdateLinkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		url = ""
		self.window = sublime.active_window()
		self.thedir = self.window.folders()[0]
		file = self.window.extract_variables().file
		# 修改成本地路径
		temp = self.thedir.split("/")
		temp.reverse()
		t = 0
		for id,i in enumerate(temp):
			if i == "branches":
				t = id-2
				break
			if i == "trunk":
				t = id-1
				break
		preNumbers = t+1
		_MAX = 0
		while preNumbers > _MAX:
			m = len(temp) - (len(temp) - preNumbers + 1)
			url += "/"+temp[m]
			preNumbers -= 1
		# 修改成本地路径 end

		url = "/cn/iphone-xs/img"
		workCountrys = ["cn","hk","tw","mo"]
		print("/(?:"+'|'.join(workCountrys)+")/")
		# url = url.replace("/(?:"+'|'.join(workCountrys)+")/","us")
		for i in workCountrys:
			url = url.replace("/"+i+"/","/us/")
		print(url)
