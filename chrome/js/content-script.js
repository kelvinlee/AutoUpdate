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

function moveToOneX() {
	var list = document.getElementsByTagName('figure');
	for (var i = list.length - 1; i >= 0; i--) {
		var style = list[i].currentStyle || window.getComputedStyle(list[i], false);
		var bgImage = style.backgroundImage.replace("_2x","");
		if (bgImage.length > 10) {
			list[i].style.backgroundImage = bgImage;
		}
	}
}

function moveToTwoX() {
	var list = document.getElementsByTagName('figure');
	for (var i = list.length - 1; i >= 0; i--) {
		var style = list[i].currentStyle || window.getComputedStyle(list[i], false);
		var bgImage = style.backgroundImage.replace("_2x","");
		if (bgImage.length > 10) {
			bgImage = bgImage.replace(/(\.jpg|\.png)/g,"_2x$1");
			list[i].style.backgroundImage = bgImage;
		}
	}
}

// test()