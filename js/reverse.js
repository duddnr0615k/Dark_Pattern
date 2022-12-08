const img_reverse = document.getElementsByClassName('reverse_icon')

function changeStyle(css)
        {
            if(css === true){
                
                document.getElementsByTagName('link')[0].href ='./css/style_white.css'
                
            }
            else {
                document.getElementsByTagName('link')[0].href ='./css/style.css'
            }
                       
        }


img_reverse[0].onclick = () =>{
    if(getComputedStyle(img_reverse[0]).content.includes('moon') === true){
        changeStyle(true)
    }
    else{
        changeStyle(false)
    }
    
}
