var stopAnimation = false;
var speed = 3;
var _lastY = -1;
function setSpeed(numb) {
	speed = numb;
}
function stopAnimate() {
	cancelAnimationFrame(scrollAnimationRunBottom);
	cancelAnimationFrame(scrollAnimationRunTop);
	stopAnimation = true;
	setTimeout(function(){
		stopAnimation = false;
	},100);
	return stopAnimation;
}
function scrollAnimationRunBottom() {
	var documentHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);
	var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.getElementsByTagName('body')[0].clientHeight;
	y = window.scrollY + speed
	if (y >= documentHeight - windowHeight || stopAnimation) {
		stopAnimate();
		return false;
	}
	window.scrollTo(0, y)
	_lastY = window.scrollY
	requestAnimationFrame(scrollAnimationRunBottom);
}

function scrollAnimationRunTop() {
	
	var documentHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);
	y = window.scrollY - speed
	if (y <= 0 || stopAnimation) {
		stopAnimate();
		return false;
	}
	window.scrollTo(0, y)

	requestAnimationFrame(scrollAnimationRunTop);
}

function viewScrollTo(position) {
	// alert(JSON.stringify(position[0])+position[0].x+","+position[0].y)
	window.scrollTo(position[0].x,position[0].y)
}
function changeCountry(country,newpage) {
	var href = window.location.href;
	if (country.toLowerCase() == "us") {
		href = href.replace(/\.apple\.com(\/)(cn|hk\/en|hk|tw|mo)/g,".apple.com");
		// alert(href)
	}else{
		href = href.replace(/\.apple\.com(\/)(cn|hk\/en|hk|tw|mo)/g,".apple.com$1"+country.toLowerCase()+"");
		if (href.indexOf("/"+country.toLowerCase()) <= -1) {
			href = href.replace(/\.apple\.com(\/)/g,".apple.com/"+country.toLowerCase()+"/");
		}
		// alert(href)
	}
	if (newpage) {
		window.open(href);
	}else{
		window.location.href = href;
	}
	return {x: window.scrollX, y: window.scrollY};
}

function runSVGShowOrHide() {
	var className = document.getElementsByTagName("html")[0].className;
	if (className.indexOf("no-svg") > -1) {
		className = className.replace(" no-svg","");
	}else{
		className += " no-svg";
	}

	document.getElementsByTagName("html")[0].className = className;
	return className;
}

function checkSVGShowOrHide() {
	var className = document.getElementsByTagName("html")[0].className;
	if (className.indexOf("no-svg") > -1) {
		return 1;
	}else{
		return 2;
	}
}

function moveToOneX(dom) {
	var list = document.getElementsByTagName(dom);
	for (var i = list.length - 1; i >= 0; i--) {
		var style = list[i].currentStyle || window.getComputedStyle(list[i], false);
		var bgImage = style.backgroundImage.replace("_2x","");
		if (bgImage.length > 10) {
			list[i].style.backgroundImage = bgImage;
		}
	}
}

function moveToTwoX(dom) {
	var list = document.getElementsByTagName(dom);
	for (var i = list.length - 1; i >= 0; i--) {
		var style = list[i].currentStyle || window.getComputedStyle(list[i], false);
		var bgImage = style.backgroundImage.replace("_2x","");
		if (bgImage.length > 10) {
			bgImage = bgImage.replace(/(\.jpg|\.png)/g,"_2x$1");
			list[i].style.backgroundImage = bgImage;
		}
		list[i].style.backgroundImage = null;
	}
}

// test()