import sublime
import sublime_plugin
import json

countriesName = {
	"Australia": {
		"cn": "澳大利亚",
		"hk": "澳洲",
		"tw": "澳洲"
	},
	"Austria": {
		"cn": "奥地利",
		"hk": "奧地利",
		"tw": "奧地利"
	},
	"Bahrain": {
		"cn": "巴林",
		"hk": "巴林",
		"tw": "巴林"
	},
	"Bangladesh": {
		"cn": "孟加拉国",
		"hk": "孟加拉",
		"tw": "孟加拉"
	},
	"Belgium": {
		"cn": "比利时",
		"hk": "比利時",
		"tw": "比利時"
	},
	"Brazil": {
		"cn": "巴西",
		"hk": "巴西",
		"tw": "巴西"
	},
	"Bulgaria": {
		"cn": "保加利亚",
		"hk": "保加利亞",
		"tw": "保加利亞"
	},
	"Cambodia": {
		"cn": "柬埔寨",
		"hk": "柬埔寨",
		"tw": "柬埔寨"
	},
	"Canada": {
		"cn": "加拿大",
		"hk": "加拿大",
		"tw": "加拿大"
	},
	"Chile": {
		"cn": "智利",
		"hk": "智利",
		"tw": "智利"
	},
	"China mainland": {
		"cn": "中国大陆",
		"hk": "中國大陸",
		"tw": "中國大陸"
	},
	"Czech Republic": {
		"cn": "捷克共和国",
		"hk": "捷克共和國",
		"tw": "捷克共和國"
	},
	"Denmark": {
		"cn": "丹麦",
		"hk": "丹麥",
		"tw": "丹麥"
	},
	"Fiji": {
		"cn": "斐济",
		"hk": "斐濟",
		"tw": "斐濟"
	},
	"Finland": {
		"cn": "芬兰",
		"hk": "芬蘭",
		"tw": "芬蘭"
	},
	"France": {
		"cn": "法国",
		"hk": "法國",
		"tw": "法國"
	},
	"Germany": {
		"cn": "德国",
		"hk": "德國",
		"tw": "德國"
	},
	"Greece": {
		"cn": "希腊",
		"hk": "希臘",
		"tw": "希臘"
	},
	"Guam": {
		"cn": "关岛",
		"hk": "關島",
		"tw": "關島"
	},
	"Hong Kong": {
		"cn": "香港",
		"hk": "香港",
		"tw": "香港"
	},
	"Hungary": {
		"cn": "匈牙利",
		"hk": "匈牙利",
		"tw": "匈牙利"
	},
	"India": {
		"cn": "印度",
		"hk": "印度",
		"tw": "印度"
	},
	"Ireland": {
		"cn": "爱尔兰",
		"hk": "愛爾蘭",
		"tw": "愛爾蘭"
	},
	"Israel": {
		"cn": "以色列",
		"hk": "以色列",
		"tw": "以色列"
	},
	"Italy": {
		"cn": "意大利",
		"hk": "意大利",
		"tw": "義大利"
	},
	"Japan": {
		"cn": "日本",
		"hk": "日本",
		"tw": "日本"
	},
	"Korea": {
		"cn": "韩国",
		"hk": "韓國",
		"tw": "韓國"
	},
	"Kuwait": {
		"cn": "科威特",
		"hk": "科威特",
		"tw": "科威特"
	},
	"Laos": {
		"cn": "老挝",
		"hk": "寮國",
		"tw": "寮國"
	},
	"Liechtenstein": {
		"cn": "列支敦士登",
		"hk": "列支敦士登",
		"tw": "列支敦斯登"
	},
	"Luxembourg": {
		"cn": "卢森堡",
		"hk": "盧森堡",
		"tw": "盧森堡"
	},
	"Macau": {
		"cn": "澳门",
		"hk": "澳門",
		"tw": "澳門"
	},
	"Macao": {
		"cn": "澳门",
		"hk": "澳門",
		"tw": "澳門"
	},
	"Mexico": {
		"cn": "墨西哥",
		"hk": "墨西哥",
		"tw": "墨西哥"
	},
	"Mongolia": {
		"cn": "蒙古",
		"hk": "蒙古",
		"tw": "蒙古"
	},
	"Nepal": {
		"cn": "尼泊尔",
		"hk": "尼泊爾",
		"tw": "尼泊爾"
	},
	"Netherlands": {
		"cn": "荷兰",
		"hk": "荷蘭",
		"tw": "荷蘭"
	},
	"New Zealand": {
		"cn": "新西兰",
		"hk": "紐西蘭",
		"tw": "紐西蘭"
	},
	"Norway": {
		"cn": "挪威",
		"hk": "挪威",
		"tw": "挪威"
	},
	"Philippines": {
		"cn": "菲律宾",
		"hk": "菲律賓",
		"tw": "菲律賓"
	},
	"Poland": {
		"cn": "波兰",
		"hk": "波蘭",
		"tw": "波蘭"
	},
	"Portugal": {
		"cn": "葡萄牙",
		"hk": "葡萄牙",
		"tw": "葡萄牙"
	},
	"Puerto Rico": {
		"cn": "波多黎各",
		"hk": "波多黎各",
		"tw": "波多黎各"
	},
	"Qatar": {
		"cn": "卡塔尔",
		"hk": "卡達",
		"tw": "卡達"
	},
	"Romania": {
		"cn": "罗马尼亚",
		"hk": "羅馬尼亞",
		"tw": "羅馬尼亞"
	},
	"Russia": {
		"cn": "俄罗斯",
		"hk": "俄羅斯",
		"tw": "俄羅斯"
	},
	"Saudi Arabia": {
		"cn": "沙特",
		"hk": "沙特阿拉伯",
		"tw": "沙烏地阿拉伯"
	},
	"Singapore": {
		"cn": "新加坡",
		"hk": "新加坡",
		"tw": "新加坡"
	},
	"Slovakia": {
		"cn": "斯洛伐克",
		"hk": "斯洛伐克",
		"tw": "斯洛伐克"
	},
	"South Africa": {
		"cn": "南非",
		"hk": "南非",
		"tw": "南非"
	},
	"Spain": {
		"cn": "西班牙",
		"hk": "西班牙",
		"tw": "西班牙"
	},
	"Sri Lanka": {
		"cn": "斯里兰卡",
		"hk": "斯里蘭卡",
		"tw": "斯里蘭卡"
	},
	"Sweden": {
		"cn": "瑞典",
		"hk": "瑞典",
		"tw": "瑞典"
	},
	"Switzerland": {
		"cn": "瑞士",
		"hk": "瑞士",
		"tw": "瑞士"
	},
	"Taiwan": {
		"cn": "台湾",
		"hk": "台灣",
		"tw": "台灣"
	},
	"Thailand": {
		"cn": "泰国",
		"hk": "泰國",
		"tw": "泰國"
	},
	"Tunisia": {
		"cn": "突尼斯",
		"hk": "突尼西亞",
		"tw": "突尼西亞"
	},
	"Turkey": {
		"cn": "土耳其",
		"hk": "土耳其",
		"tw": "土耳其"
	},
	"United Arab Emirates": {
		"cn": "阿联酋",
		"hk": "阿拉伯聯合酋長國",
		"tw": "阿拉伯聯合大公國"
	},
	"United Kingdom": {
		"cn": "英国",
		"hk": "英國",
		"tw": "英國"
	},
	"United States": {
		"cn": "美国",
		"hk": "美國",
		"tw": "美國"
	},
	"Vietnam": {
		"cn": "越南",
		"hk": "越南",
		"tw": "越南"
	},
}

# 自动化更新本地连接
class AutoCountryNameCommand(sublime_plugin.TextCommand):
	def run(self, edit, lang):
		print("auto country name")
		gc = lang
		runReplaceCountry(gc,self.view,edit)

		sublime.error_message("愿圣光，保佑着你的代码不报错")

def runReplaceCountry(gc,view,edit):
	for country in countriesName:
		countryInside = view.find_all('>'+country+'<', sublime.IGNORECASE)
		for i in countryInside:
			view.replace(edit, i, '>'+countriesName[country][gc]+'<')
			runReplaceCountry(gc,view,edit)
			return 1
	return 0
