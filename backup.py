				# elif img.rfind("svg") > 0:
				# 	# 获取中文图片宽高
				# 	imgPath = self.thedir+"/"+img
				# 	# print(imgPath)
				# 	width, height = get_svg.getsvg(imgPath)
				# 	imgLinks = self.view.find_all("/"+img)
				# 	# print(imgLinks,width,height,img)
				# 	# 获取英文图片宽高
				# 	for i in imgLinks:
				# 		nlink = ""
				# 		tmp = ""
				# 		point = 0
				# 		imgLine = self.view.line(i)
				# 		tmp = self.view.substr(imgLine)
				# 		# print("tmp:",tmp)
				# 		n = tmp.split('url("')
				# 		oldImg = n[1].replace("\");","").replace("\")","")
				# 		oldImgPathTmp = self.thedir.split("/")
				# 		oldImgPath = ""
				# 		for index ,v in enumerate(oldImgPathTmp):
				# 			oldImgPath += v+"/"
				# 			if v == "branches":
				# 				oldImgPath += oldImgPathTmp[index+1]+"/"
				# 				break
				# 		oldImgPath += "us"+oldImg
				# 		oldImgPath = oldImgPath.replace("/gc/","/us/")
				# 		w, h = get_svg.getsvg(oldImgPath)
				# 		if len(n) >= 2:
				# 			nlink = n[0]+'url("'+url+self.view.substr(i)+'")'
				# 		tmp = ""
				# 		# 获取英文 css 块, large medium small.
				# 		point = imgLine.a - 1
				# 		# print("\n\n")
				# 		while True:
				# 			preLine = self.view.full_line(point)
				# 			preLineStr = self.view.substr(preLine)
				# 			tmpPreLineStr = preLineStr.strip()
				# 			size = "l"
				# 			# print("tmpPreLineStr:",tmpPreLineStr,"\n\n")
				# 			if tmpPreLineStr[0] == "." :
				# 				objectNmae = tmpPreLineStr.replace(" {", "")
				# 				if rewriteClass.get(objectNmae) == None:
				# 					rewriteClass[objectNmae] = {"run": True}
				# 					rewriteClass[objectNmae][size] = {"w": width, "h": height}
				# 					rewriteClass[objectNmae]["o"+size] = {"w": w, "h": h}
				# 					difVal = {}
				# 					widthP = round(int(width)/int(w)*100)
				# 					heightP = round(int(height)/int(h)*100)
				# 					difVal["l"] = "width:" + str(widthP) + "% height:" + str(heightP) + "%"
				# 					# print("objectNmae:",objectNmae)
				# 					tmp += getCssContentByCode(objectNmae, difVal, ["width","height","size","background"], True, self.view, False)
				# 					tmp = tmp.replace(oldImg,url+self.view.substr(i))
				# 					# print("tmp:",tmp)
				# 					if resetSVGWidthHeight:
				# 						tmp += setCssContentWithHeight(tmp, widthP/100, heightP/100)
				# 					svgContent += tmp+"\n"
				# 					# print(nextContent)
				# 				break
				# 			point = preLine.a-1
				# 			pass
				# 	# break