import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import requests
import tldextract


# 크롤링 한 것 중에서 정보를 찾아내는 함수
def check_info(info):
    result = []
    phone = ['phone', '휴대폰', '휴대폰 번호', '전화번호', '전화 번호']
    email = ['email', '이메일', '이메일 주소', '전자메일 주소']
    gender = ['성별','gender']
    arr = ['주소','배송 주소','배송지 주소']
    health = ['건강정보','건강 정보']
    birth = ['생년월일','생일']
    id = ['주민등록번호']
    driver_id = ['운전면허','면허']
    device = ['기기정보','기기 정보','디바이스']
    no_privacy = ['개인정보처리방침없음']
    cookie_info = ['쿠키']
    name = ['이름']
    credit_info=['계좌번호','계좌 번호','카드번호','카드 번호']
    location = ['위치정보','위치 정보']
    travel = ['여권번호','여권 번호']
    body_info =['신체정보','신체 정보','몸무게','신장']
    risk_normal = '보통'
    risk_hard = '신중'



    dic = [phone, email,gender,arr,health,birth,id,driver_id,device,no_privacy,cookie_info,name,credit_info,location,travel,body_info]
    for list1 in dic:
        for word in list1:
            if word in info:
                if list1[0] not in result:
                    result.append(list1[0])
    #위험도가 1등급인 경우  '주의'등급
    if '주민등록번호' in result or '여권번호' in result or '운전면허' in result or '건강정보' in result or '계좌번호' in result or '위치정보' in result:
        result.append(risk_hard)
        return result
    #위험도 2등급의 개수가 6개 이상일 경우 '주의' 등급
    compare_normal = ['주소','phone','email','생년월일','이름','신체정보','성별']
    marge_normal = list(set(result).intersection(compare_normal))
    if len(marge_normal) >=6 :
        marge_normal.append(risk_hard)
        return marge_normal
    else:
        if '개인정보처리방침없음' in result:
            return result
        #평시상태는 보통
        result.append(risk_normal)
        return result



def crawling(urls):
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    # options.add_argument('headless')
    options.add_argument("window-size=1920,1080")
    options.add_argument("disable-gpu")
    options.add_argument('Accept-Language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7')
    # options.add_argument("accept-language=ko-KR")
    #쿠팡 같이 크롤링 막은 사이트 우회용으로 작성
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
    websites = ['https://'+urls]
    for website in websites:

        driver = webdriver.Chrome('/home/ubuntu/dark_pattern/tool/chromedriver', chrome_options=options)
        driver.get(website)
        sleep(2)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
        }


        #en으로 들어오는 사이트는 ko로 변환하여 한글사이트로 바꿈
        if driver.current_url.find("/en/") != -1:
            privacy_url = driver.current_url.replace("/en/","/ko/")
            driver.get(privacy_url)
            sleep(2)


        try:
            # 스크롤을 최하단으로 내려서 개인정보처리방침을 클릭(전자상거래 사이트와 같이 무한 스크롤 우회)
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                    sleep(0.5)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
        except:
            pass

        #모든 사이트를 고려하기 위해 아래와 같이 짬ㅋㅋㅋㅋ
        try:

            driver.find_element(By.LINK_TEXT, "개인정보처리방침").send_keys(Keys.ENTER)
            scroll = driver.find_element(By.TAG_NAME, "body")
            #셀레니움으로 들어가면 스크롤을 막아놓는 사이트를 우회하기 위해 작성
            driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

            #새창으로 뜨는 경우 새창으로 이동
            if len(driver.window_handles) >=2:
                driver.switch_to.window(driver.window_handles[1])
                scroll = driver.find_element(By.TAG_NAME,"body")
                driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

        except NoSuchElementException:
            try:
                driver.find_element(By.LINK_TEXT, "개인정보 처리방침").send_keys(Keys.ENTER)
                scroll = driver.find_element(By.TAG_NAME,"body")
                driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                if len(driver.window_handles) >= 2:
                    driver.switch_to.window(driver.window_handles[1])
                    scroll = driver.find_element(By.TAG_NAME, "body")
                    driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

            except NoSuchElementException:
                try:
                    driver.find_element(By.LINK_TEXT, "개인정보 취급방침").send_keys(Keys.ENTER)
                    scroll = driver.find_element(By.TAG_NAME, "body")
                    driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                    if len(driver.window_handles) >= 2:
                        driver.switch_to.window(driver.window_handles[1])
                        scroll = driver.find_element(By.TAG_NAME, "body")
                        driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)


                except NoSuchElementException:
                    try:
                        driver.find_element(By.LINK_TEXT, "개인정보취급방침").send_keys(Keys.ENTER)
                        scroll = driver.find_element(By.TAG_NAME, "body")
                        driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                        if len(driver.window_handles) >= 2:
                            driver.switch_to.window(driver.window_handles[1])
                            scroll = driver.find_element(By.TAG_NAME, "body")
                            driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                    except NoSuchElementException:
                        try:
                            driver.find_element(By.LINK_TEXT, "개인(신용)정보 처리방침").send_keys(Keys.ENTER)
                            scroll = driver.find_element(By.TAG_NAME, "body")
                            driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                            if len(driver.window_handles) >= 2:
                                driver.switch_to.window(driver.window_handles[1])
                                scroll = driver.find_element(By.TAG_NAME, "body")
                                driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                        except NoSuchElementException:
                            try:
                                #a태그가 아닌!! button으로 구현한 사이트 대상
                                button_list = driver.find_elements(By.TAG_NAME,"button")
                                if len(button_list) >=1:
                                    for buttons in button_list:
                                        tmp = buttons.text.replace(" ","")
                                        if tmp == '':
                                            continue
                                        if tmp =="개인정보처리방침" or tmp =='개인정보취급방침':
                                            buttons.send_keys(Keys.ENTER)
                                            scroll = driver.find_element(By.TAG_NAME, "body")
                                            driver.execute_script("arguments[0].setAttribute('style','overflow:none;')",
                                                                  scroll)
                                            if len(driver.window_handles) >= 2:
                                                driver.switch_to.window(driver.window_handles[1])
                                                scroll = driver.find_element(By.TAG_NAME, "body")
                                                driver.execute_script("arguments[0].setAttribute('style','overflow:none;')",
                                                                      scroll)
                                                break
                                        else:
                                            # 버튼은 있으나, 개인정보처리방침이 안눌리는 경우 아래 코드 실행
                                            privacy_response = requests.get(website, verify=False, headers=headers)

                                            # 인코딩 안맞는 사이트 맞춰주는 소스
                                            content_type = privacy_response.headers['content-type']
                                            if not 'charset' in content_type:
                                                privacy_response.encoding = privacy_response.apparent_encoding

                                            if privacy_response.status_code == 200:
                                                html = privacy_response.text
                                                soup = BeautifulSoup(html, 'html.parser')
                                                a_tag = soup.find_all("a")
                                                for a in a_tag:
                                                    tmp = a.attrs['href']
                                                    if tmp.lower().find('personalinfo') != -1 or tmp.lower().find(
                                                            'privacy') != -1 or tmp.lower().find('policy') != -1:
                                                        privacy_url = tmp
                                                        if privacy_url.find('www') == -1 and privacy_url.find(
                                                                'https://') == -1:
                                                            fqdn = tldextract.extract(website).fqdn
                                                            privacy_url = 'https://' + fqdn + privacy_url
                                                            driver.get(privacy_url)
                                                            try:
                                                                last_height = driver.execute_script(
                                                                    "return document.body.scrollHeight")
                                                                while True:
                                                                    driver.execute_script(
                                                                        "window.scrollTo(0,document.body.scrollHeight);")
                                                                    sleep(0.5)
                                                                    new_height = driver.execute_script(
                                                                        "return document.body.scrollHeight")
                                                                    if new_height == last_height:
                                                                        break
                                                                    last_height = new_height
                                                            except:
                                                                pass
                                                            break
                                                        elif privacy_url.find('www') != -1 or privacy_url.find(
                                                                'https://') != -1:
                                                            driver.get(tmp)
                                                            break
                                                    # else:
                                                    #     return check_info('개인정보처리방침없음')
                                                break

                                else:
                                    # 버튼은 있으나, 개인정보처리방침이 안눌리는 경우 아래 코드 실행
                                    privacy_response = requests.get(website, verify=False, headers=headers)

                                    #인코딩 안맞는 사이트 맞춰주는 소스
                                    content_type = privacy_response.headers['content-type']
                                    if not 'charset' in content_type:
                                        privacy_response.encoding = privacy_response.apparent_encoding

                                    if privacy_response.status_code == 200:
                                        html = privacy_response.text
                                        soup = BeautifulSoup(html, 'html.parser')
                                        a_tag = soup.find_all("a")
                                        for a in a_tag:
                                            tmp = a.attrs['href']
                                            if tmp.lower().find('personalinfo') != -1 or tmp.lower().find(
                                                    'privacy') != -1 or tmp.lower().find('policy') != -1:
                                                privacy_url = tmp
                                                if privacy_url.find('www') == -1 and privacy_url.find('https://') == -1:
                                                    fqdn = tldextract.extract(website).fqdn
                                                    privacy_url = 'https://' + fqdn + privacy_url
                                                    driver.get(privacy_url)
                                                    try:
                                                        last_height = driver.execute_script(
                                                            "return document.body.scrollHeight")
                                                        while True:
                                                            driver.execute_script(
                                                                "window.scrollTo(0,document.body.scrollHeight);")
                                                            sleep(0.5)
                                                            new_height = driver.execute_script(
                                                                "return document.body.scrollHeight")
                                                            if new_height == last_height:
                                                                break
                                                            last_height = new_height
                                                    except:
                                                        pass
                                                    break
                                                elif privacy_url.find('www') != -1 or privacy_url.find('https://')!=-1:
                                                    driver.get(tmp)
                                                    break
                                            else:
                                                return check_info('개인정보처리방침없음')
                                        break


                            except NoSuchElementException:
                                #위의 코드를 전부 통과하면 최종적으로 되는 곳
                                # 와디즈처럼 개인정보처리방침이 2개로 되어있는 경우 매칭
                                privacy_response = requests.get(website, verify=False, headers=headers)
                                content_type = privacy_response.headers['content-type']
                                if not 'charset' in content_type:
                                    privacy_response.encoding = privacy_response.apparent_encoding
                                if privacy_response.status_code == 200:
                                    html = privacy_response.text
                                    soup = BeautifulSoup(html, 'html.parser')
                                    a_tag = soup.find_all("a")
                                    for a in a_tag:
                                        tmp = a.attrs['href']
                                        if tmp.lower().find('personalinfo') != -1 or tmp.lower().find('privacy') != -1 or tmp.lower().find('policy') != -1:
                                            privacy_url = tmp
                                            if privacy_url.find('www') == -1:
                                                fqdn = tldextract.extract(website).fqdn
                                                privacy_url = 'https://' + fqdn + privacy_url
                                                driver.get(privacy_url)
                                                break
                                            elif privacy_url.find('www') != -1:
                                                driver.get(tmp)

                                                break
                                        else:
                                            return check_info('개인정보처리방침없음')






        sleep(1)

        try:
            iframes = driver.find_elements(By.TAG_NAME,"iframe")
            # iframe이 존재하는 경우 실행
            if iframes:
                for iframe in iframes:
                    iframe_url = iframe.get_attribute("src")
                    iframe_domain = tldextract.extract(iframe_url).domain
                    if urls.find(iframe_domain) != -1 and len(iframe_domain) != 0 :
                        if iframe_url.lower().find("privacy") != -1 or iframe_url.lower().find("policy") != -1 or iframe_url.lower().find("terms") :
                            driver.switch_to.frame(iframe)
                            word = driver.find_element(By.TAG_NAME, "body").text
                            driver.switch_to.default_content()
                            word +=driver.find_element(By.TAG_NAME, "body").text
                            return check_info(word)
                        else:
                            word = driver.find_element(By.TAG_NAME, "body").text
                            return check_info(word)
                    else:
                        word = driver.find_element(By.TAG_NAME, "body").text
                        return check_info(word)
            else:
                word = driver.find_element(By.TAG_NAME,"body").text
                return check_info(word)
        except NoSuchElementException:
            return '개인정보처리방침없음'



if __name__ == '__main__':
    # start = time.time()
    # end = time.time()
    # print(end-start)
    # crawling()
    # print(crawling('www.coolstay.co.kr/'))
    # print(crawling('www.netflix.com/kr/'))
    # print(crawling('watcha.com/'))
    print(crawling('www.eduwill.net/'))




