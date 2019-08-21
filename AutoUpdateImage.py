import sublime
import sublime_plugin
from . import get_image_size
from . import get_svg
import os
import re
import json


class AutoUpdateImageCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# 初始化参数
		newContent = ""
		preContent = ""
		nextContent = ""
		missFiles = ""
		resetSVGWidthHeight = True
		rewriteClass = {}
		# resetSVGWidthHeight = sublime.ok_cancel_dialog("如果文件中存在 SVG 是否修改 css 宽高,是 OK, 否 Cancle.")
		getWithHeight = True
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
				size = "none"
				if img.rfind("jpg")>0 or img.rfind("png")>0:
					imgPath = self.thedir+"/"+img
					try:
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
						oldImg = n[1].replace("\");","").replace("\")","")
						oldImgPathTmp = self.thedir.split("/")
						oldImgPath = ""
						for index ,v in enumerate(oldImgPathTmp):
							oldImgPath += v+"/"
							if v == "branches":
								oldImgPath += oldImgPathTmp[index+1]+"/"
								break
						oldImgPath += "us"+oldImg
						oldImgPath = oldImgPath.replace("/gc/","/us/")

						try:
							# print(get_image_size)
							w, h = get_image_size.get_image_size(oldImgPath)
						except get_image_size.UnknownImageFormat:
							w, h = -1, -1

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
							if img.rfind("large") > 0:
								size = "l"
							elif img.rfind("medium") > 0:
								size = "m"
							elif img.rfind("small") > 0:
								size = "s"
							# print("size:",i,size,img)

						# 获取前一行直到头部
						while True:
							preLine = self.view.full_line(point)
							preLineStr = self.view.substr(preLine)
							tmpPreLineStr = preLineStr.strip()
							
							if tmpPreLineStr[0] == "." and size != "none":
								objectNmae = tmpPreLineStr.replace(" {", "")
								if rewriteClass.get(objectNmae) == None:
									rewriteClass[objectNmae] = {"run": True}
								if size != "none":
									rewriteClass[objectNmae][size] = {"w": width, "h": height}
									rewriteClass[objectNmae]["o"+size] = {"w": w, "h": h}

							if preLineStr[0] == "h" or preLineStr[0] == "@" or preLineStr[0] == "#" or preLineStr[0] == ".":
								# print("preLineStr:"+preLineStr)
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
						
				elif img.rfind("svg") > 0:
					# 获取中文图片宽高
					imgPath = self.thedir+"/"+img
					# print(imgPath)
					width, height = get_svg.getsvg(imgPath)
					imgLinks = self.view.find_all("/"+img)
					# 获取英文图片宽高
					for i in imgLinks:
						nlink = ""
						tmp = ""
						point = 0
						imgLine = self.view.line(i)
						tmp = self.view.substr(imgLine)
						n = tmp.split('url("')
						oldImg = n[1].replace("\");","").replace("\")","")
						oldImgPathTmp = self.thedir.split("/")
						oldImgPath = ""
						for index ,v in enumerate(oldImgPathTmp):
							oldImgPath += v+"/"
							if v == "branches":
								oldImgPath += oldImgPathTmp[index+1]+"/"
								break
						oldImgPath += "us"+oldImg
						oldImgPath = oldImgPath.replace("/gc/","/us/")
						w, h = get_svg.getsvg(oldImgPath)
						if len(n) >= 2:
							nlink = n[0]+'url("'+url+self.view.substr(i)+'")'
						tmp = ""
						# 获取英文 css 块, large medium small.
						point = imgLine.a-1
						preLine = self.view.full_line(point)
						preLineStr = self.view.substr(preLine)
						tmpPreLineStr = preLineStr.strip()
						size = "l"
						if tmpPreLineStr[0] == "." :
							objectNmae = tmpPreLineStr.replace(" {", "")
							if rewriteClass.get(objectNmae) == None:
								rewriteClass[objectNmae] = {"run": True}
								rewriteClass[objectNmae][size] = {"w": width, "h": height}
								rewriteClass[objectNmae]["o"+size] = {"w": w, "h": h}
								difVal = {}
								widthP = round(int(width)/int(w)*100)
								heightP = round(int(height)/int(h)*100)
								difVal["l"] = "width:" + str(widthP) + "% height:" + str(heightP) + "%"
								tmp += getCssContentByCode(objectNmae, difVal, ["width","height","size","background"], self.view, False)
								tmp = tmp.replace(oldImg,url+self.view.substr(i))
								if resetSVGWidthHeight:
									tmp += setCssContentWithHeight(tmp, widthP/100, heightP/100)
								nextContent += tmp+"\n"

					# break
			about = ""
			# print(rewriteClass)
			for k in rewriteClass:
				v = rewriteClass[k]
				# print(v)
				classLinks = self.view.find_all(k)
				difVal = {}
				if v.get("l") != None and v.get("ol") != None :
					widthPX = int(v["l"]["w"]) - int(v["ol"]["w"])
					difVal["l"] = str(widthPX) + "px"
				if v.get("m") != None and v.get("om") != None :
					widthPX = int(v["m"]["w"]) - int(v["om"]["w"])
					difVal["m"] = str(widthPX) + "px"
				if v.get("s") != None and v.get("os") != None :
					widthPX = int(v["s"]["w"]) - int(v["os"]["w"])
					difVal["s"] = str(widthPX) + "px"

				for i in classLinks:
					Line = self.view.line(i)
					code = self.view.substr(Line)
					c = getCssContentByCode(code, difVal, ["left","right","top","bottom"], self.view, True)
					about += c
					# break

			# print(rewriteClass)
			newContent = about + preContent + nextContent
			newView = self.window.new_file()
			newView.set_syntax_file("Packages/CSS/CSS.tmLanguage")
			newView.insert(edit,0,newContent)
			
			try:
				newView.run_command("css_format",{"action": "expand"})
			except Exception as e:
				print(e)

			try:
				newViewName = url.split("/")[2]+"."+url.split("/")[3]+".build.css"
				newView.set_name(newViewName)
			except Exception as e:
				print(e)
			

			# print("allImagesCount:",allImagesCount,finishedCss)
			if allImagesCount > finishedCss:
				sublime.error_message("Miss files , double check:\n"+missFiles)
				print("missFiles:",missFiles)

# update width and height
def setCssContentWithHeight(content, baseW, baseH):
	# tmp = content
	tmp = content.split("@media")
	# print(tmp)
	size = {"large":{},"medium":{},"small":{}}
	for i,v in enumerate(tmp):
		tmp = re.findall(r"width:[\s]?(.*?)px", v)
		if i <= 0:
			size["large"]["w"] = int(tmp[0])
		elif len(tmp)>0 and int(tmp[0]) >= 1023 :
			size["medium"]["w"] = int(tmp[1])
		elif len(tmp)>0 and int(tmp[0]) >= 320 and int(tmp[0]) < 1023 :
			size["small"]["w"] = int(tmp[1])

	for item in size:
		print(size[item])
		c = round(float(size[item]["w"]) * baseW)
		owl = "width:"+str(size[item]["w"])+"px;"
		owl2 = "width: "+str(size[item]["w"])+"px;"
		nwl = "width: "+str(c)+"px;"


		content = content.replace(owl,nwl)
		content = content.replace(owl2,nwl)
	print(size)
	return content

# get css code by classname
def getCssContentByCode(code, difVal, rightCode, view, samepass):
	# print("code: "+code)
	classLinks = view.find_all(code)
	reback = ""
	point = 0
	preNumbers = 0
	for i in classLinks:
		Line = view.line(i)
		tmp = view.substr(Line)
		if samepass:
			if tmp.replace(" {\n", "").replace(" {", "").strip() == code.replace(" {\n", "").replace(" {", "").strip(): 
				continue
		else:
			# print(samepass,tmp)
			if tmp.replace(" {\n", "").replace(" {", "").strip() == code.replace(" {\n", "").replace(" {", "").strip(): 
				pass
			else:
				continue

		# print("temp:",tmp,tmp[0])
		if tmp[0] == ".":
			if difVal.get("l") != None :
				tmp = "/* "+str(difVal["l"])+" off the us.*/ \n" + tmp
			point = Line.b + 1
			while True:
				nextLine = view.full_line(point)
				LineContent = view.substr(nextLine)
				lineStr = LineContent.strip()
				# if len(lineStr.split("left")) > 1 or len(lineStr.split("right")) > 1 or len(lineStr.split("top")) > 1 or len(lineStr.split("bottom")) > 1:
				for i in rightCode:
					if len(lineStr.split(i))  > 1 :
						tmp += lineStr
						break

				if lineStr == "}":
					tmp += lineStr
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
				for i in rightCode:
					if len(lineStr.split(i))  > 1 :
						tmp += lineStr
						break
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
					# print(atoi(lineStr.split("max-width:")[1].split("px")[0]), lineStr.split("max-width:"))
					tmp = lineStr + tmp
					try:
						size = atoi(lineStr.split("max-width:")[1].split("px")[0])
						if int(size) >= 1023 and difVal.get("m") != None :
							tmp = "/* "+str(difVal["m"])+" px off the us.*/ \n" + tmp
						elif int(size) >= 320 and int(size) <= 736 and difVal.get("s") != None :
							tmp = "/* "+str(difVal["s"])+" px off the us.*/ \n" + tmp
					except Exception as e:
						print(e)
					break
				point = prevLine.a - 1
				pass
			if numbEnd > 0:
				tmp += "}"
			reback += tmp
	return reback

# string with number to number.
def atoi(string):
	string = string[::-1]
	num = 0
	for i, v in enumerate(string):
		for j in range(0,10):
			if v == str(j):
				num+=j * (10**i)
	return num
