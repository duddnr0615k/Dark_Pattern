from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import requests



# 크롤링 한 것 중에서 정보를 찾아내는 함수
def check_info(info):
    result = []
    phone = ['phone', '휴대폰', '휴대폰 번호', '전화번호', '전화 번호']
    email = ['email', '이메일', '이메일 주소', '전자메일 주소']
    gender = ['성별','gender']
    arr = ['주소']
    health = ['건강']
    birth = ['생년월일','생일']
    id = ['주민등록번호']
    driver_id = ['운전','면허']
    device = ['기기정보']
    dic = [phone, email,gender,arr,health,birth,id,driver_id,device]
    for list in dic:
        for word in list:
            if word in info:
                if list[0] not in result:
                    result.append(list[0])
    # if '전화번호' in info or '휴대폰 번호' in info:
    #     result.append('phone')
    # if '이메일' in info or 'email' in info or 'Email' in info:
    #     result.append('email')
    # if '성별' in info or 'gender' in info:
    #     result.append('gender')
    # if '주소' in info:
    #     result.append('address')
    # if '건강' in info:
    #     result.append('health')
    # if '생년월일' in info or '생일' in info:
    #     result.append('birth')
    # if '주민등록번호' in info:
    #     result.append('id')
    # if '운전' in info or '면허' in info:
    #     result.append('driver_id')
    # if '기기정보' in info:
    #     result.append('device')
    return result


# website_dic = {"사이트이름": [개인정보들]} 방식으로 저장되어 있다.
def crawling():
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    #쿠팡 같이 크롤링 막은 사이트 우회용으로 작성
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
    website_dic = {}
    websites = ["http://www.naver.com"] #, "http://www.smilegate.com"
    # websites = ["https://www.gmarket.co.kr/"] #, "http://www.smilegate.com"
    # websites = ["https://www.11st.co.kr/main"] #, "http://www.smilegate.com"
    # websites = ["https://www.kisia.or.kr/"]
    # websites = ["https://www.coupang.com/"]
    for website in websites:
        # name = website_dic에 추가할 사이트 이름을 URL에서 가져온다.
        begin = website.index('.') + 1
        name = website[begin:]
        name = name[:name.index('.')]

        driver = webdriver.Chrome('./chromedriver.exe',chrome_options=options)
        driver.get(website)

        #아니 셀레니움은 except로 가기 때문에 이렇게 짬.. 이거 모르게씀,,,
        try:
            privacy_url = driver.find_element(By.LINK_TEXT, "개인정보처리방침").get_attribute('href')
        except:
            try:
                privacy_url = driver.find_element(By.LINK_TEXT, "개인정보 처리방침").get_attribute('href')
            except:
                try:
                    privacy_url = driver.find_element(By.LINK_TEXT, "개인정보 취급방침").get_attribute('href')
                except:
                    privacy_url = driver.find_element(By.LINK_TEXT, "개인정보취급방침").get_attribute('href')




        # privacy_url = driver.current_url #개인정보처리방침 위치
        sleep(1)
        #쿠팡 우회를 위한 것
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
	        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
        }
        response = requests.get(privacy_url, verify=False,headers = headers)

        #사이트마다 다른 인코딩을 맞추기 위해 작성
        content_type = response.headers['content-type']
        if not 'charset' in content_type:
            response.encoding = response.apparent_encoding

        if response.status_code==200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            iframes = soup.find_all('iframe')
            sleep(1)
            # iframe으로 구성된 사이트 대상
            for iframe in iframes:
                iframe_url = iframe['src']
                #오탐을 줄이기 위해 iframe 주소가 대상 사이트 이름이 포함된 url일 경우에만 크롤링
                if iframe_url.find(name) != -1:
                    response = requests.get(iframe_url, verify=False, headers=headers)
                    # 사이트마다 다른 인코딩을 맞추기 위해 작성
                    content_type = response.headers['content-type']
                    if not 'charset' in content_type:
                        response.encoding = response.apparent_encoding

                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        li_items = soup.find_all()
                        page_text = ""
                        for li in li_items:
                            page_text += li.text
                    result = check_info(page_text)
                    sleep(1)
                    if len(result) == 0:
                        website_dic[name] = "ERROR"

                    else:
                        website_dic[name] = result



            #iframe이 아닌 사이트는 요기로 실행
            li_items = soup.find_all()
            page_text = ""
            for li in li_items:
                page_text += li.text

            result = check_info(page_text)
            sleep(1)
            if len(result) == 0:
                website_dic[name] = "ERROR"

            else:
                website_dic[name] = result


    print(website_dic)


if __name__ == '__main__':
    crawling()
