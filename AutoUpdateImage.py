import sublime
import sublime_plugin
from . import get_image_size
import os
import json



class AutoUpdateImageCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# 初始化参数
		newContent = ""
		preContent = ""
		nextContent = ""
		missFiles = ""
		rewriteClass = {}
		# checkFolder = sublime.ok_cancel_dialog("如果页面有重名图片请选择OK，否则选择Cancel。")
		getWithHeight = sublime.ok_cancel_dialog("是否获取图片宽高请选择OK，否则选择Cancel。")
		checkFolder = False
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
		if checkFolder:
			_MAX = 1
		else:
			_MAX = 0
		while preNumbers > _MAX:
			m = len(temp) - (len(temp) - preNumbers + 1)
			url += "/"+temp[m]
			preNumbers -= 1

		if url == "":
			sublime.error_message("You need put css and images in same folder.")
		else:

			# Get all directories in the component directory
			allFolders = [ name for name in os.listdir(self.thedir) if os.path.isfile(os.path.join(self.thedir, name)) ]
			allImagesCount = 0
			finishedCss = 0
			allFolders.sort()
			# print(allFolders)
			for img in allFolders:
				if img.rfind("jpg")>0 or img.rfind("png")>0:
					imgPath = self.thedir+"/"+img
					try:
						# print(get_image_size)
						width, height = get_image_size.get_image_size(imgPath)
					except get_image_size.UnknownImageFormat:
						width, height = -1, -1

					css = ""
					if checkFolder:
						imgLinks = self.view.find_all("/"+temp[0]+"/"+img)
					else:
						imgLinks = self.view.find_all("/"+img)
					# imgLinks.reverse()
					allImagesCount += 1
					if len(imgLinks) <= 0:
						missFiles += img+"	"
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
						fallbackEnd = False
						if len(n) >= 2:
							tmp = n[0]+'url("'+url+self.view.substr(i)+'")'
						if len(tmp.split('fallback'))>=2:
							fallbackEnd = True
						point = imgLine.a-1
						if getWithHeight and width > -1 and height > -1 and img.rfind("_2x") < 0:
							tmp += ";\nwidth: "+str(width)+"px;"
							tmp += "\nheight: "+str(height)+"px;"
							tmp += "\nbackground-size: "+str(width)+"px "+str(height)+"px;"

						# 获取前一行直到头部
						while True:
							preLine = self.view.full_line(point)
							preLineStr = self.view.substr(preLine)
							tmpPreLineStr = preLineStr.strip()
							if preLineStr[0] == "h" or preLineStr[0] == "@" or preLineStr[0] == "#" or preLineStr[0] == ".":
								# print("preLineStr:"+preLineStr)
								if preLineStr[0] == ".":
									objectNmae = preLineStr.replace(" {\n", "")
									rewriteClass[objectNmae] = 1
								preNumbers += 1
								tmp = preLineStr+tmp
								while preNumbers > 0:
									tmp = tmp+"}"
									preNumbers -= 1
									# print("preNumbers:",preNumbers)
								if fallbackEnd:
									if preLineStr[0] == "@":
										nextContent += tmp+"\n"
									else:
										preContent += tmp+"\n"
								else:
									preContent += tmp+"\n"
								break
							if preNumbers < 1 and len(tmpPreLineStr)>=1 and (tmpPreLineStr[0] == "@" or tmpPreLineStr[0] == "#" or tmpPreLineStr[0] == "."):
								preNumbers += 1
								tmp = preLineStr+tmp
							if preNumbers < 1 and len(tmpPreLineStr)>=3 and (tmpPreLineStr[0] == "h" and tmpPreLineStr[1] == "t" and tmpPreLineStr[2] == "m" and tmpPreLineStr[3] == "l"):
								preNumbers += 1
								tmp = preLineStr+tmp
							point = preLine.a-1
							pass
						
						
					# break
			about = ""
			for k in rewriteClass:
				classLinks = self.view.find_all(k)
				for i in classLinks:
					Line = self.view.line(i)
					code = self.view.substr(Line)
					# print(code+" --- "+k)
					c = getCssContentByCode(code, self.view, True)
					print(c)
					about += c
					# break

			# print(rewriteClass)
			newContent = about + preContent + nextContent
			newView = self.window.new_file()
			newView.set_syntax_file("Packages/CSS/CSS.tmLanguage")
			newView.insert(edit,0,newContent)
			newViewName = url.split("/")[2]+"."+url.split("/")[3]+".build.css"
			newView.set_name(newViewName)
			try:
				newView.run_command("css_format",{"action": "expand"})
			except Exception as e:
				print(e)
			

			# print("allImagesCount:",allImagesCount,finishedCss)
			if allImagesCount > finishedCss:
				sublime.error_message("Miss files , double check:\n"+missFiles)
				print("missFiles:",missFiles)
		
def getCssContentByCode(code, view, samepass):
	# print("code: "+code)
	classLinks = view.find_all(code)
	reback = ""
	point = 0
	preNumbers = 0
	for i in classLinks:
		Line = view.line(i)
		tmp = view.substr(Line)
		if tmp.replace(" {\n", "").strip() == code.replace(" {\n", "").strip(): 
			# print("same")
			continue
		# print("temp:",tmp,tmp[0])
		if tmp[0] == ".":
			point = Line.b + 1
			while True:
				nextLine = view.full_line(point)
				LineContent = view.substr(nextLine)
				lineStr = LineContent.strip()
				if len(lineStr.split("left")) > 1 or len(lineStr.split("right")) > 1 or len(lineStr.split("top")) > 1 or len(lineStr.split("bottom")) > 1:
					tmp += lineStr
				if lineStr == "}":
					# tmp += lineStr
					break
				point = nextLine.b+1
				pass
			# tmp += "}"
			reback += tmp

		else:
			# tmp += "aaa}"
			point = Line.b + 1
			while True:
				nextLine = view.full_line(point)
				LineContent = view.substr(nextLine)
				lineStr = LineContent.strip()
				# print(len(lineStr.split("left")),len(lineStr.split("right")),lineStr)
				if len(lineStr.split("left")) > 1 or len(lineStr.split("right")) > 1 or len(lineStr.split("top")) > 1 or len(lineStr.split("bottom")) > 1:
					tmp += lineStr
				if lineStr == "}":
					tmp += lineStr
					break
				point = nextLine.b+1
				pass

			point = Line.a - 1
			numbEnd = 0
			while True:
				numbEnd += 1
				prevLine = view.full_line(point)
				LineContent = view.substr(prevLine)
				lineStr = LineContent.strip()
				if len(lineStr) > 0 and (lineStr[0] == "h" or lineStr[0] == "@" or lineStr[0] == "#"):
					tmp = lineStr + tmp
					break
				point = prevLine.a - 1
				pass
			if numbEnd > 0:
				tmp += "}"

			reback += tmp




	return reback


