
function getKeyByValue(obj,value){
    return Object.keys(obj).find(key => obj[key] === value);
}

function setUrl (){
chrome.tabs.query({active: true, currentWindow: true},(tab) => {


    try{
        let tabUrl = tab[0].url 
        let url = 'http://3.34.215.57/api/' + tabUrl.replace('https://','').replaceAll('/','...'); //django에서 https://와 /를 인식못해서 야매로함
        const data = {url : tabUrl};
        fetch(url,{
            method: 'GET',
            headers:{
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
                'Content-Type': 'application/json',
                "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",

            },
            
        })
        .then(response => response.json())
        .then((data) => {

                const datas = Object.values(data);
                const dataList = datas[0]
                if (dataList.length === 0) {
                    const no_test = document.getElementsByClassName('no_test');
                    no_test[0].style.display = 'block';
                }
                else{
                    dataList.find(e => {
                        if (e ==='phone'){
                            const phone = document.getElementsByClassName("icon1");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        
                        }
                        else if(e ==='email'){
                            const phone = document.getElementsByClassName("icon2");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
    
                            
                        }
                        else if(e ==='성별'){
                            const phone = document.getElementsByClassName("icon3");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='주소'){
                            const phone = document.getElementsByClassName("icon4");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='건강'){
                            const phone = document.getElementsByClassName("icon5");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='생년월일'){
                            const phone = document.getElementsByClassName("icon6");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='주민등록번호'){
                            const phone = document.getElementsByClassName("icon7");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='운전'){
                            const phone = document.getElementsByClassName("icon8");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='기기정보'){
                            const phone = document.getElementsByClassName("icon9");
                            const danger = document.getElementsByClassName("danger");
                            const word = document.getElementsByClassName("word");
                            danger[0].style.display = 'block';
                            word[0].style.display = 'block';
                            phone[0].style.display = 'block';
                            
                        }
                        else if(e ==='개인정보처리방침없음'){
                            const no_privacy = document.getElementsByClassName('no_privacy');
                            no_privacy[0].style.display = 'block';
                        }
                        wait2[0].style.display = 'none'
                    })
                }
 
            
                

        })
    }
    catch{
       const wait = document.getElementsByClassName("wait");
       wait[0].style.display = 'block';
       wait2[0].style.display = 'none';
    }
    });


    
}


const btn = document.getElementsByClassName('btn')
const renderHtml = document.getElementsByClassName('hidden')
const wait2 = document.getElementsByClassName('wait2')




btn[0].onclick = () =>{
    btn[0].style.display = 'none'
    renderHtml[0].style.display = 'block'
    wait2[0].style.display = 'block'
    setUrl();

}

