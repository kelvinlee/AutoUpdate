'use strict';

var main = null;
var text1 = "Show SVG";
var text2 = "Hide SVG";
var cmd = false;
var x1Size = true;

function setDefaultKey() {
	cmd = false;

	setKeyDown();
}

function setKeyDown() {
	if (cmd) {
		var parent = document.getElementById("changeCountry");
		for (var i = 0;i<parent.children.length;i++) {
			var item = parent.children[i];
			item.className += " btn-success";
		}
	}else{
		var parent = document.getElementById("changeCountry");
		for (var i = 0;i<parent.children.length;i++) {
			var item = parent.children[i];
			item.className = item.className.replace(" btn-success","");
		}
	}
}

function click(e) {
  chrome.tabs.executeScript(null,{code:"runSVGShowOrHide();"});
 	CheckSVGType();
  // window.close();
}

function oneX(e) {
	if (x1Size) {
  	chrome.tabs.executeScript(null,{code:"moveToOneX('figure');"});
  	chrome.tabs.executeScript(null,{code:"moveToOneX('h1');"});
  	chrome.tabs.executeScript(null,{code:"moveToOneX('h2');"});
  }else{
  	chrome.tabs.executeScript(null,{code:"moveToTwoX('figure');"});
  	chrome.tabs.executeScript(null,{code:"moveToTwoX('h1');"});
  	chrome.tabs.executeScript(null,{code:"moveToTwoX('h2');"});
  }
  // window.close();

  x1Size = !x1Size;
  e.target.value = x1Size ? "1x Image" : "2x Image"
}

function changeCountryEvent(e) {

	chrome.tabs.executeScript({code:"changeCountry('"+e.target.name+"',"+Math.ceil(cmd)+");"},(results)=>{
		// alert("aaa")
		setTimeout(function(){
			chrome.tabs.executeScript(null,{code:"viewScrollTo("+JSON.stringify(results)+");"});
		},600)
	});
}

function CheckSVGType() {
	var svg = document.getElementById('svg');
	chrome.tabs.executeScript(null,{code:"checkSVGShowOrHide();"},(results) => {
		if (results == 1) {
			svg.value = text1;
		}else{
			svg.value = text2;
		}
	});
}

document.addEventListener("keydown", function(){
	var oEvent = window.event;
	// alert(oEvent.keyCode);
	if (oEvent.keyCode == 91 || oEvent.keyCode == 17) {
		cmd = true;
	}
	setKeyDown();
})
document.addEventListener("keyup", function(){
	setDefaultKey();
})

document.addEventListener('DOMContentLoaded', function () {

	var svg = document.getElementById('svg');
	svg.addEventListener('click', click);
	
  var x1 = document.getElementById('1x');
  x1.addEventListener('click',oneX);

  var parent = document.getElementById("changeCountry");
  for (var i = 0;i<parent.children.length;i++) {
  	var item = parent.children[i];
  	item.addEventListener("click",changeCountryEvent);
  }

  CheckSVGType();

});