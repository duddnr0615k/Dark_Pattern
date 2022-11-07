const test = [] ;
for (el of document.querySelectorAll('a')){
	if(el.textContent.includes('개인정보 처리방침')){
		test.push(el.href)}}
const request = new XMLHttpRequest();
const url = test[0]; // 소스 가져올 페이지 

request.open('GET', url, true);
request.onload = () => {
    let htmlText = request.responseText;
    return htmlText
}

console.log(htmlText);
