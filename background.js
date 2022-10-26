
	
	// function handleMessage(request,sender,sendResponse){
	// 	console.log(`good: ${request.greeting}`);
	// 	sendResponse({response: "Response from background script"});
	// }
	
	// chrome.runtime.onMessage.addListener(handleMessage);
	function setBackGroundStart(){
		chrome.tabs.query({active: true, currentWindow: true},(tab) => {
			chrome.scripting.executeScript({
			target: {tabId: tab[0].id},
			func: setHiddenBlock, //setBackGroundColor,
		});

		});

	}
	// let test;
	// test = setInterval(setBackGroundStart,1000);
	


	function setBackGroundColor(){
	
		// alert("선택정보에 대해 다시 한번 확인해 주세요.");

		try{
		let selected= [];
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
		
	chrome.tabs.onUpdated.addListener(setBackGroundStart);
	const test = setInterval(setBackGroundStart,1000);	
	chrome.tabs.onUpdated.addListener(test);
	// document.addEventListener('hashchange', setBackGroundStart);


	
