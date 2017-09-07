# Code by Kelvin
import sublime
import sublime_plugin
import os

class AutoUpdateCssCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# 初始化参数
		newContent = ""
		missFiles = ""
		self.window = sublime.active_window()
		if len(self.window.folders()) <= 0:
			sublime.error_message("You need put css and images in same folder.")
			return
		self.thedir = self.window.folders()[0]
		# 修改成本地路径
		temp = self.thedir.split("/")
		temp.reverse()
		url = ""
		t = 0
		for id,i in enumerate(temp):
			if i == "branches":
				t = id-2
				break
			if i == "trunk":
				t = id-1
				break
		preNumbers = t+1
		while preNumbers > 0:
			m = len(temp) - (len(temp) - preNumbers + 1)
			url += "/"+temp[m]
			preNumbers -= 1
		# 修改成本地路径 end print("url:",url)
		# Get all directories in the component directory
		allFolders = [ name for name in os.listdir(self.thedir) if os.path.isfile(os.path.join(self.thedir, name)) ]
		allImagesCount = 0
		finishedCss = 0
		for img in allFolders:
			if img.rfind("jpg")>0 or img.rfind("png")>0:
				css = ""
				imgLinks = self.view.find_all(img)
				imgLinks.reverse()
				allImagesCount += 1
				if len(imgLinks) <= 0:
					missFiles += img+"  "
				else:
					finishedCss += 1
				# 获取当前行。
				for i in imgLinks:
					tmp = ""
					point = 0
					preNumbers = 0
					# 获取当前image的行内容
					imgLine = self.view.line(i)
					tmp = self.view.substr(imgLine)
					n = tmp.split('url("')
					if len(n) >= 2:
						tmp = n[0]+'url("'+url+'/'+self.view.substr(i)+'")'
					point = imgLine.a-1
					# 获取前一行直到头部
					while True:
						preLine = self.view.full_line(point)
						preLineStr = self.view.substr(preLine)
						
						if preLineStr[0] == "@" or preLineStr[0] == "#" or preLineStr[0] == ".":
							preNumbers += 1
							tmp = preLineStr+tmp
							while preNumbers > 0:
								tmp = tmp+"\n}"
								preNumbers -= 1
							newContent += tmp+"\n"
							break
						tmpPreLineStr = preLineStr.strip()
						if tmpPreLineStr[0] == "@" or tmpPreLineStr[0] == "#" or tmpPreLineStr[0] == ".":
							preNumbers += 1
							tmp = preLineStr+tmp
						else if len(tmpPreLineStr) > 4 and tmpPreLineStr[0] == "h" and tmpPreLineStr[1] == "t" and tmpPreLineStr[2] == "m" and and tmpPreLineStr[3] == "l"
							preNumbers += 1
							tmp = preLineStr+tmp
						point = preLine.a-1
						pass

		newView = self.window.new_file()
		newView.insert(edit,0,newContent)
		if allImagesCount > finishedCss:
			sublime.error_message("Miss files plz double check:\n"+missFiles)
			print("missFiles:",missFiles)










