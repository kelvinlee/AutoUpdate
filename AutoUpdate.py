import sublime
import sublime_plugin
import json

class AutoUpdateCommand(sublime_plugin.TextCommand):
	def run(self, edit, lang):
		# 初始化参数
		haswechat = 0
		hasFont = 1
		gc = lang # HK/EN 需要单独制作
		gcHead = "zh"
		if gc == "hk/en":
			gcHead = "en"
			hasFont = 0
		fontLang = {"cn":"SC","hk":"HK","tw":"TC","mo":"HK"}
		# lang = "en_"
		# print(fontLang[gc],gc)

		# 更新链接为本地连接
		allShopLink = self.view.find_all('/us/shop', sublime.IGNORECASE)
		allShopLink.reverse()
		for i in allShopLink:
			self.view.replace(edit, i, '/'+gc+'/shop')

		countrys = ["cn","hk","tw","jp","uk","au","befr","ca","dk","fi","fr","de","ie","it","mx","nl","nz","no","sg","es","se","chfr","tr"]
		allLink = self.view.find_all('="/(?!(?:v|ac|metrics|105|'+'|'.join(countrys)+'|'+gc+'|wss|choose-your-country|jobs))([^\"]*)"', sublime.IGNORECASE)
		allLink.reverse()
		for i in allLink:
			# print(self.view.substr(i)[3:],i)
			self.view.replace(edit, i, '="/'+gc+'/'+self.view.substr(i)[3:])

		allFullLink = self.view.find_all('://www.apple.com/(?!(?:v|ac|metrics|105|'+gc+'|wss|choose-your-country|jobs))([^\"]*)', sublime.IGNORECASE)
		allFullLink.reverse()
		for i in allFullLink:
			self.view.replace(edit, i, '://www.apple.com/'+gc+self.view.substr(i)[21:])

		allShopLink = self.view.find_all('://itunes.apple.com/'+gc, sublime.IGNORECASE)
		allShopLink.reverse()
		for i in allShopLink:
			self.view.replace(edit, i, '://itunes.apple.com/'+gc)

		allSuportLink = self.view.find_all('://support.apple.com/(?i)en-us', sublime.IGNORECASE)
		allSuportLink.reverse()
		for i in allSuportLink:
			self.view.replace(edit, i, '://support.apple.com'+gcHead+'/-'+gc)
		
		iOSLink = self.view.find_all('<meta property="al:ios:url"(.*)>')
		iOSLink.reverse()
		# print("iOSLink:",iOSLink)
		for i in iOSLink:
			text = self.view.substr(i).replace("/us","/"+gc)
			self.view.replace(edit,i, text)
		

		# 更新语言为本地语言
		allLanguage = self.view.find_all('en-US')
		allLanguage.reverse()
		for i in allLanguage:
			self.view.replace(edit, i, gcHead+'-'+gc[:2].upper())

		allLanguage2 = self.view.find_all('en_US')
		allLanguage2.reverse()
		for i in allLanguage2:
			self.view.replace(edit, i, gcHead+'_'+gc[:2].upper())

		# 查询OG图片然后插入到body 如果不需要 haswechat = false
		if haswechat:
			og = self.view.find_all('<meta property="og:image"(.*)>')
			og.reverse()
			oglink = ""
			for i in og:
				print("og image=>", len(self.view.substr(i).split("/"+gc)))
				if len(self.view.substr(i).split("/"+gc)) > 1:
					oglink = "/"+gc+self.view.substr(i).split("/"+gc)[1].split("?")[0]
				else:
					# 这里使用默认链接
					oglink = "https"+self.view.substr(i).split("https")[1].split("?")[0]

			og_body = self.view.find_all("<body(.*)>")
			for i in og_body:
				wechatLine = self.view.full_line(self.view.line(i).b+1)
				wechat = self.view.substr(wechatLine).split("display:")
				# print("og body=>",i,self.view.line(i).b,"wechat=>",wechatLine)
				oglink = oglink.split(".")[0]+"_wechat."+oglink.split(".")[1]
				if len(wechat) <= 1:
					self.view.insert(edit, self.view.line(i).b, '\n	<div style="display:none;"><img src="'+oglink+'" alt=""></div>')
				# else:
				# 	self.view.replace(edit, wechatLine, '	<div style="display:none;"><img src="'+oglink+'" alt=""></div>\n')

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

