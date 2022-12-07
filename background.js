	

	
	function setBackGroundStart(){
		chrome.tabs.query({active: true, currentWindow: true},(tab) => {
			
			try{
			
			chrome.scripting.executeScript({
			target: {tabId: tab[0].id},
			func: setBackGroundDarkPattern,
			
		});
			}
			catch{
				null;
			}
		});
		

	}


	


	function setBackGroundDarkPattern(){
	
		try{
		const selected= [];
		//pseudo css로 선택글자를 매칭하는 경우 
		for (const element of document.querySelectorAll('label,a,span,li>div,p,h3,h1,h2,h4,em')) {
			if(getComputedStyle(element,'::after').content.includes('(선택') || getComputedStyle(element,'::after').content.includes('( 선택') || getComputedStyle(element,'::after').content.includes('[선택') || getComputedStyle(element,'::after').content.includes('[ 선택')   ){
				element.style.backgroundColor = 'yellow';

			}
			//오탐을 줄이기 위해 선택글자를 바로 색칠하지 않고 리스트에 저장 
			else if (element.textContent.includes('선택')) {   
				selected.push(element);		
			}
		}
		for (const element2 of selected){
			if (element2.textContent.includes('(선택)') || element2.textContent.includes('( 선택 )') || element2.textContent.includes('[선택]')|| element2.textContent.includes('[ 선택 ]')){
				 element2.style.backgroundColor = 'yellow';
				
			}
		
		}
		
		//태그 속성으로 role에 버튼을 주어 만든 경우
		for(const roles of document.querySelectorAll('div,ul')){
			if(roles.role ==='button' && roles.textContent.includes('탈퇴')){
				roles.style.fontSize ='35px';
				roles.style.color = 'red';
				roles.style.backgroundColor ='yellow';}
			
		
			// 숨겨져 있는 항목 체크 (에듀윌,밀리의서재,인터파크)
			if (roles.style.display == 'none') {
				const checkbox = roles.innerHTML.includes('checkbox')	
				if((checkbox && roles.textContent.includes('SMS')) || (checkbox && roles.textContent.includes('제 3자 제공')) || (checkbox && roles.textContent.includes('개인정보처리')) ){
					roles.style.display = 'block';
					roles.style.backgroundColor = 'yellow';
				}	
		}
	}
		//iframe으로 만들어진 사이트에서 탈퇴를 찾는 경우
		const fontArr=[];
		for (const iframeArr of document.querySelectorAll('iframe')){
			try{
				const good = iframeArr.contentDocument.querySelectorAll('a>span')
				if (good.length !== 0){
					for (const test2 of good){
						if(test2.textContent.includes('탈퇴')){
							test2.style.color = 'red'
							test2.style.backgroundColor ='yellow';
							test2.style.fontSize ='35px';

						}
					}
				}
			}		
			catch{
				continue
			}
					}
		
		//탈퇴버튼 크게 키우기
		for (const fontTest of document.querySelectorAll('a,button,p, a>span,button>span,li>div')){
			fontArr.push(fontTest)
		}
		for (const fontTest2 of fontArr){
	
			if(fontTest2.textContent.includes('탈퇴')){
				//오탐을 줄이기 위해 버튼이나 a태그의 탈퇴란 글자가 2글자 인경우 
				if ( (fontTest2.tagName ==='BUTTON' && fontTest2.textContent.length===2) || (fontTest2.textContent.length===2 && fontTest2.tagName ==='A')){
					fontTest2.style.fontSize ='35px';
					fontTest2.style.color = 'red';
					fontTest2.style.backgroundColor ='yellow';}
				
				//탈퇴 글자 포함 4~8글자인 경우에만 
				else if(fontTest2.textContent.replaceAll(' ','').length===4){
					fontTest2.style.fontSize ='35px';
					fontTest2.style.color = 'red';
					fontTest2.style.backgroundColor ='yellow';}
			
			
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
