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

// test()