'use strict';
var text1 = "Show SVG";
var text2 = "Hide SVG";

function click(e) {
  chrome.tabs.executeScript(null,
      {code:"runSVGShowOrHide();"});
  window.close();
}

document.addEventListener('DOMContentLoaded', function () {
	var divs = document.querySelectorAll('input');
  for (var i = 0; i < divs.length; i++) {
    divs[i].addEventListener('click', click);
  }
	chrome.tabs.executeScript({code:"checkSVGShowOrHide();"},(results) => {
  	if (results == 1) {
  		divs[0].value = text1;
  	}else{
  		divs[0].value = text2;
  	}
  });
	
  

});