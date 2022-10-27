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

	try{
	const selected= [];
	for (const element of document.querySelectorAll('label,a,span,li>div,p,h3,h1,h2,h4')) {
		if(getComputedStyle(element,'::after').content.includes('(선택') || getComputedStyle(element,'::after').content.includes('( 선택') || getComputedStyle(element,'::after').content.includes('[선택') || getComputedStyle(element,'::after').content.includes('[ 선택')   ){
			element.style.backgroundColor = 'yellow';

		}

		if (element.textContent.includes('선택')) {   
			selected.push(element);		
		}
	}
	for (const element2 of selected){
		if (element2.textContent.includes('(선택') || element2.textContent.includes('( 선택') || element2.textContent.includes('[선택')|| element2.textContent.includes('[ 선택')){
			 element2.style.backgroundColor = 'yellow';
			
		}
	
	}

	const fontArr=[];
	for (const fontTest of document.querySelectorAll('a,button,p, a>span')){
		fontArr.push(fontTest)
	}
	for (const fontTest2 of fontArr){

		if(fontTest2.textContent.includes('탈퇴')){
			if(fontTest2.textContent.length===4 || fontTest2.textContent.length===5){
				fontTest2.style.fontSize ='35px';
				fontTest2.style.color = 'red';
				fontTest2.style.backgroundColor ='yellow';
		}
		
		}
	}
	
}
catch{
	null;
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



