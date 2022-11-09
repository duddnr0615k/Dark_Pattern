from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import requests


# 크롤링 한 것 중에서 정보를 찾아내는 함수
def check_info(info):
    result = []
    if '전화번호' in info or '휴대폰' in info:
        result.append('phone')
    if '이메일' in info or 'email' in info or 'Email' in info:
        result.append('email')
    if '성별' in info or 'gender' in info:
        result.append('gender')
    if '주소' in info:
        result.append('address')
    if '건강' in info:
        result.append('health')
    if '생년월일' in info or '생일' in info:
        result.append('birth')
    if '주민등록번호' in info:
        result.append('id')
    if '운전' in info or '면허' in info:
        result.append('driver_id')
    if '기기정보' in info:
        result.append('device')
    return result


# website_dic = {"사이트이름": [개인정보들]} 방식으로 저장되어 있다.
def crawling():
    website_dic = {}
    websites = ["http://www.naver.com", "http://www.daum.net"] #, "http://www.smilegate.com"
    for website in websites:
        # name = website_dic에 추가할 사이트 이름을 URL에서 가져온다.
        begin = website.index('.') + 1
        name = website[begin:]
        name = name[:name.index('.')]
        print(name)

        driver = webdriver.Chrome('./chromedriver.exe')
        driver.get(website)

        try:
            driver.find_element(By.LINK_TEXT, "개인정보처리방침").click()
        except NoSuchElementException as e:
            print(e)
        privacy_url = driver.current_url

        sleep(2)
        response = requests.get(privacy_url, verify=False)
        if response.status_code==200:
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

    print(website_dic)


if __name__ == '__main__':
    crawling()
