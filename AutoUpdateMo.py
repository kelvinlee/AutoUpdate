import sublime
import sublime_plugin
import json

class AutoUpdateMoCommand(sublime_plugin.TextCommand):
	def run(self, edit, lang):
		# 初始化参数
		haswechat = 0
		hasFont = 1
		gc = lang # HK/EN 需要单独制作
		gcHead = "zh"
		gcShopTitle = gc
		if gc == "hk/en":
			gcHead = "en"
			hasFont = 0
			gcShopTitle = "hk"
		if gc == "hk" or gc == "mo":
			gcShopTitle = "hk-zh"
		if gc == "mo":
			hasFont = 0
		fontLang = {"cn":"SC","hk":"HK","tw":"TC","mo":"HK"}
		# lang = "en_"
		# print(fontLang[gc],gc)
		if gc == "cn":
			haswechat = 1

		# # 更新链接为本地连接
		# allShopLink = self.view.find_all('/hk-zh/shop', sublime.IGNORECASE)
		# allShopLink.reverse()
		# # print("allShopLink",allShopLink)
		# for i in allShopLink:
		# 	self.view.replace(edit, i, '/'+gcShopTitle+'/shop')
		# xcLink = self.view.find_all('/hk-zh/xc/', sublime.IGNORECASE)
		# xcLink.reverse()
		# # print("xcLink",xcLink)
		# for i in xcLink:
		# 	self.view.replace(edit, i, '/'+gcShopTitle+'/xc/')
		appleDom("title", self.view, "香港", "澳門", edit)
		appleDom("meta(.*)site_name", self.view, "香港", "澳門", edit)


		countrys = ["cn","tw","hk-zh","us","jp","uk","au","befr","ca","dk","fr","de","ie","it","mx","nl","nz","no","sg","es","se","chfr","tr"]
		allLink = self.view.find_all('="/(?!(?:v|ac/|metrics|105|'+'|'.join(countrys)+'|'+gc+'|wss|choose-your-country|jobs))([^\"]*)"', sublime.IGNORECASE)
		allLink.reverse()
		for i in allLink:
			self.view.replace(edit, i, '="/'+gc+'/'+self.view.substr(i)[3:])

		secondTime = self.view.find_all('="/'+gc+'/hk(?!(?:/en/|-))([^\"]*)"')
		secondTime.reverse()
		for i in secondTime:
			nl = self.view.substr(i)[3:]
			nl = nl.replace(gc+'/hk', gc)
			print(nl)
			self.view.replace(edit, i, '="/'+nl)

		secondTime = self.view.find_all('="/'+gc+'/en/([^\"]*)"')
		secondTime.reverse()
		for i in secondTime:
			nl = self.view.substr(i)[3:]
			nl = nl.replace(gc+'/en/', gc)
			print(nl)
			self.view.replace(edit, i, '="/'+nl)

		thirdTime = self.view.find_all('="/'+gc+'/hk/en/([^\"]*)"')
		thirdTime.reverse()
		for i in thirdTime:
			nl = self.view.substr(i)[3:]
			nl = nl.replace(gc+'/hk/en/', "hk/en/")
			print(nl)
			self.view.replace(edit, i, '="/'+nl)


		appleLink("www", self.view, countrys, gc, edit)
		appleLink("tv", self.view, countrys, gc, edit)



		allShopLink = self.view.find_all('://itunes.apple.com/hk([^\"]*)', sublime.IGNORECASE)
		allShopLink.reverse()
		for i in allShopLink:
			itunesLink = self.view.substr(i)
			print("itunesLink",itunesLink)
			if len(itunesLink.split("?")) > 1:
				itunesLink = itunesLink+"&l=zh"
			else:
				itunesLink = itunesLink+"?l=zh"
			if gc == "hk/en":
				itunesLink = itunesLink.replace("/hk","/hk")
				itunesLink = itunesLink.replace("l=zh","l=en")
			else:
				itunesLink = itunesLink.replace("/hk","/"+gc)
			self.view.replace(edit, i, itunesLink)

		allSuportLink = self.view.find_all('support.apple.com/(?i)zh-hk', sublime.IGNORECASE)
		allSuportLink.reverse()
		for i in allSuportLink:
			if gc == "hk/en":
				self.view.replace(edit, i, 'support.apple.com/'+gcHead+'-hk')
			else:
				self.view.replace(edit, i, 'support.apple.com/'+gcHead+'-'+gc)
		
		iOSLink = self.view.find_all('<meta property="al:ios:url"(.*)>')
		iOSLink.reverse()
		# print("iOSLink:",iOSLink)
		for i in iOSLink:
			text = self.view.substr(i).replace("/hk","/"+gc)
			self.view.replace(edit,i, text)
		
		sameLink = self.view.find_all("/"+gc+"/"+gc)
		iOSLink.reverse()
		for i in iOSLink:
			text = self.view.substr(i).replace("/"+gc+"/"+gc,"/"+gc)
			self.view.replace(edit,i, text)

		# 更新语言为本地语言
		allLanguage = self.view.find_all('zh-HK')
		allLanguage.reverse()
		for i in allLanguage:
			self.view.replace(edit, i, gcHead+'-'+gc[:2].upper())

		allLanguage2 = self.view.find_all('zh_HK')
		allLanguage2.reverse()
		for i in allLanguage2:
			self.view.replace(edit, i, gcHead+'_'+gc[:2].upper())

		# 查询OG图片然后插入到body 如果不需要 haswechat = false
		if haswechat:
			og = self.view.find_all('<meta property="og:image"(.*)>')
			og.reverse()
			oglink = ""
			for i in og:
				# print("og image=>", len(self.view.substr(i).split("/"+gc)))
				if len(self.view.substr(i).split("/"+gc)) > 1:
					oglink = "/"+gc+self.view.substr(i).split("/"+gc)[1].split("?")[0]
				else:
					# 这里使用默认链接
					oglink = "https"+self.view.substr(i).split("https")[1].split("?")[0]
			# print("oglink",oglink)
			og_body = self.view.find_all("<body(.*)>")
			for i in og_body:
				wechatLine = self.view.full_line(self.view.line(i).b+1)
				wechat = self.view.substr(wechatLine).split("display:")
				# print("og body=>",i,self.view.line(i).b,"wechat=>",wechatLine,wechat)
				linkPoint = len(oglink.split("."))
				# oglink = oglink.split(".")[linkPoint-2]+"_wechat."+oglink.split(".")[linkPoint-1]
				oglinkSp = oglink.split(".")
				oglink = ""
				for j in range(linkPoint):
					if j >= len(oglinkSp)-1:
						oglink = oglink+oglinkSp[j]
					elif j >= len(oglinkSp)-2:
						oglink = oglink+oglinkSp[j]+"_wechat."
					else:
						oglink = oglink+oglinkSp[j]+"."
				oglink = oglink.replace("https://www.apple.com/v/","/"+gc+"/")
				# print(oglink,len(wechat),i,self.view.line(i).b)
				if len(wechat) <= 1:
					self.view.insert(edit, self.view.line(i).b, '\n	<div style="display:none;"><img src="'+oglink+'" alt=""></div>')
				# else:
					# self.view.replace(edit, wechatLine, '	<div style="display:none;"><img src="'+oglink+'" alt=""></div>\n')

		# 字体修改
		if hasFont:
			SFfont = self.view.find_all('(?i)fonts\?families=SF\+Pro')
			SFfontCN = self.view.find_all('/'+gc+'/global/styles/sfpro-'+gc+'.css')
			if len(SFfont) >= 1 and len(SFfontCN) < 1:
				EndHeadLine = self.view.find_all('</head>')[0]
				self.view.insert(edit, EndHeadLine.a-1,'\n\n	<link rel="stylesheet" href="/wss/fonts?family=SF+Pro+'+fontLang[gc]+'&amp;weights=300,400,500,600&amp;v=1" type="text/css">\n	<link rel="stylesheet" href="/'+gc+'/global/styles/sfpro-'+gc+'.css" />\n	<!--[if IE]>\n	<link rel="stylesheet" href="/wss/fonts?family=SF+Pro+'+fontLang[gc]+'&amp;weights=300,400,500,600&amp;v=1" type="text/css">\n	<link rel="stylesheet" href="/'+gc+'/global/styles/sfpro-'+gc+'-ie.css" />\n	<![endif]-->\n')

		# 增加NA check。
		NA = self.view.find_all('(?i)n/a')
		# print("NA:",NA)
		if len(NA)>=1:
			sublime.error_message("This page have N/A have to remove.")

		# 跟随美国v

	# def run("~/Develper")
def appleDom(dom, view, passName, replaceName, edit):
	allCityName = view.find_all('<'+dom+'(.*)'+passName)
	for i in allCityName:
		name = view.substr(i)[0:].replace(passName, replaceName)
		view.replace(edit, i, name)

def appleLink(prev, view, countrys, gc, edit):
	l = len(prev) + 13
	allFullLink = view.find_all(prev+'.apple.com/(?!(?:v|ac|metrics|105|'+'|'.join(countrys)+'|'+gc+'|wss|choose-your-country|jobs))([^\"]*)', sublime.IGNORECASE)
	allFullLink.reverse()
	for i in allFullLink:
		view.replace(edit, i, prev+'.apple.com/'+gc+view.substr(i)[l:])


	secondTime = view.find_all(prev+'.apple.com/'+gc+'/hk(?!(?:/en/))([^\"]*)"')
	secondTime.reverse()
	for i in secondTime:
		nl = view.substr(i)[0:]
		nl = nl.replace(gc+'/hk', gc)
		print(nl)
		view.replace(edit, i, ''+nl)

	thirdTime = view.find_all(prev+'.apple.com/'+gc+'/hk/en/([^\"]*)"')
	thirdTime.reverse()
	for i in thirdTime:
		nl = view.substr(i)[0:]
		nl = nl.replace(gc+'/hk/en/', "hk/en/")
		print(nl)
		view.replace(edit, i, ''+nl)


