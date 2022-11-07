const elmColors = document.getElementsByName("color");
const colors = "yellow"

function setBackGroundStart(){
	chrome.tabs.query({active: true, currentWindow: true},(tab) => {
		chrome.scripting.executeScript({
		target: {tabId: tab[0].id},
		func: setBackGroundColor,
	});

	});

}

function setBackGroundColor(){
		const url = '';
		//test
		for (el of document.querySelectorAll('a')){
			if(el.textContent.includes('개인정보 처리방침')){
			const url = el.href }}
		
	
}

elmColors[0].onclick =() =>{
		
	setBackGroundStart();
	

}



