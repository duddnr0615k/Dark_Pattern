


function setUrl (){
chrome.tabs.query({active: true, currentWindow: true},(tab) => {

    try{
        let tabUrl = tab[0].url 
        let url = 'http://54.180.213.248/api/' + tabUrl.replace('https://','').replaceAll('/','...'); //django에서 https://와 /를 인식못해서 야매로함
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
                // console.log(dataList)
                loading.style.display = 'none'
                info_hidden.style.display ='block'
                if (dataList.length === 0) {
                    const no_info = document.getElementsByClassName('no_info');
                    no_info[0].style.display = 'block';
                    main_hidden.style.display = 'none';
                    info_hidden.style.display = 'none';
                }
                else{
                    dataList.find(e => {
                        if (e ==='phone'){
                            const phone = document.getElementById("call");
                            phone.style.display = 'block';
                            
                        
                        }
                        else if(e ==='email'){
                            const email = document.getElementById("email");
                            email.style.display = 'block';
    
                            
                        }
                        else if(e ==='성별'){
                            const gender = document.getElementById("gender");
                            gender.style.display = 'block';
                            
                        }
                        else if(e ==='주소'){
                            const address = document.getElementById("address");
                            address.style.display = 'block';
                            
                        }
                        else if(e ==='건강정보'){
                            const health = document.getElementById("health");
                            health.style.display = 'block';
                            
                        }
                        else if(e ==='생년월일'){
                            const birthday = document.getElementById("birthday");
                            birthday.style.display = 'block';
                            
                        }
                        else if(e ==='주민등록번호'){
                            const human_id = document.getElementById("human_id");
                            human_id.style.display = 'block';
                            
                        }
                        else if(e ==='운전면허'){
                            const drive = document.getElementById("drive");
                            drive.style.display = 'block';
                            
                        }
                        else if(e ==='기기정보'){
                            const device = document.getElementById("device");
                            device.style.display = 'block';
                            
                        }
                        else if(e ==='개인정보처리방침없음'){
                            const no_privacy = document.getElementsByClassName('no_privacy');
                            no_privacy[0].style.display = 'block';
                            info_hidden.style.display='none';
                            
                        }
                        else if(e ==='쿠키'){
                            const cookie = document.getElementById("cookie");
                            cookie.style.display = 'block';
                            
                        }
                        else if(e ==='이름'){
                            const name = document.getElementById("name");
                            name.style.display = 'block';
                        }
                        else if(e ==='계좌번호'){
                            const credit = document.getElementById("credit");
                            credit.style.display = 'block';
                            
                        }
                        else if(e ==='위치정보'){
                            const location = document.getElementById("location");
                            location.style.display = 'block';
                            
                        }
                        else if(e ==='여권번호'){
                            const travel = document.getElementById("travel");
                            travel.style.display = 'block';
                            
                        }
                        else if(e ==='신체정보'){
                            const body_info = document.getElementById("body_info");
                            body_info.style.display = 'block';
                        }

                        else if(e ==='보통'){
                            // const normal_bar = document.getElementsByClassName('danger_bar_normal');
                            // normal_bar[0].style.display ='block';
                            // main_hidden.style.display = 'block';
                        }
                        else if(e ==='신중'){
                            // const hard_bar = document.getElementsByClassName('danger_bar_caution');
                            // hard_bar[0].style.display = 'block';
                            // main_hidden.style.display = 'block';
                        }
                        loading.style.display = 'none';
                    })
                }
 
            
                

        })
    }
    catch{
       const no_service = document.getElementsByClassName("no_service");
       no_service[0].style.display = 'block';
       loading.style.display = 'none';
    }
    });


}


const btn = document.getElementsByClassName('btn')

const main_hidden = document.getElementById('main_hidden')

const loading = document.getElementById('loading')
const info_hidden = document.getElementById('info_hidden')

btn[0].onclick = () =>{
    main_hidden.style.display='none'
    loading.style.display = 'block'
    setUrl();

}

