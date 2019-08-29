'use strict';
var text1 = "Show SVG";
var text2 = "Hide SVG";

function click(e) {
  chrome.tabs.executeScript(null,
      {code:"runSVGShowOrHide();"});
 	CheckSVGType();
  // window.close();
}

function oneX(e) {
  chrome.tabs.executeScript(null,
      {code:"moveToOneX();"});
  // window.close();
}
function twoX(e) {
  chrome.tabs.executeScript(null,
      {code:"moveToTwoX();"});
  // window.close();
}

function CheckSVGType() {
	var svg = document.getElementById('svg');
	chrome.tabs.executeScript({code:"checkSVGShowOrHide();"},(results) => {
  	if (results == 1) {
  		svg.value = text1;
  	}else{
  		svg.value = text2;
  	}
  });
}

document.addEventListener('DOMContentLoaded', function () {
	var svg = document.getElementById('svg');
	svg.addEventListener('click', click);
	
  var x1 = document.getElementById('1x');
  x1.addEventListener('click',oneX);

  var x2 = document.getElementById('2x');
  x2.addEventListener('click',twoX);

  CheckSVGType();

});