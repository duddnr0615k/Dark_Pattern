const elmColors = document.getElementsByName("color");
const colors = "yellow"

function setBackGroundStart(){
	chrome.tabs.query({active: true, currentWindow: true},(tab) => {
		chrome.scripting.executeScript({
		target: {tabId: tab[0].id},
		func: setBackGroundColor,
		//func: setHiddenBlock,
	});

	});

}

function setBackGroundStart2(){
	chrome.tabs.query({active: true, currentWindow: true},(tab) => {
		chrome.scripting.executeScript({
		target: {tabId: tab[0].id},
		func: setHiddenBlock,
	});

	});

}

function setBackGroundColor(){
	
	// alert("선택정보에 대해 다시 한번 확인해 주세요.");
	let selected=[];
	for (const element of document.querySelectorAll('label,a,span,li>div,p,h3,h1,h2,h4')) {
		if (element.textContent.includes('선택')) {   
			selected.push(element);		
		}
	}
	for (const element2 of selected){
		if (element2.textContent.includes('(선택') || element2.textContent.includes('( 선택') || element2.textContent.includes('[선택')|| element2.textContent.includes('[ 선택')){
			element2.style.backgroundColor = 'yellow';
			
		}
	
	}
	
}


function setHiddenBlock(){
	try{
		for (const element3 of document.querySelectorAll('div')) {	
			if (element3.style.display == 'none') {	
					if(element3.innerHTML.includes('checkbox') && element3.textContent.includes('이메일')){
						element3.style.display = 'block';
						element3.style.backgroundColor = 'yellow';
					}	
			}					
		}
	}
	catch{
		null;
	}
}

elmColors[0].onclick =() =>{
		
	setBackGroundStart();
	setBackGroundStart2()
	
}



