import time

#외부 라이브러리
from check_info import check_info

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import tldextract


class Privacy_Crawling(check_info):
    def __init__(self,urls):
        super().__init__()
        self.urls = urls
        self.check_chrome_driver()
    def __call__(self):
        return self.crawling()


    #chrome버전에 맞는 드라이버 설치
    def check_chrome_driver(self):
        chrome_driver = ChromeDriverManager().install()
        return chrome_driver

    #맨 하단으로 이동
    def infinity_scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            sleep(0.5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    #iframe존재할 시 아래 함수 실행
    def iframe_exist(self):
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            for iframe in iframes:
                iframe_url = iframe.get_attribute("src")
                iframe_domain = tldextract.extract(iframe_url).domain
                if self.urls.find(iframe_domain) != -1 and len(iframe_domain) != 0:
                    if iframe_url.lower().find("privacy") != -1 or iframe_url.lower().find(
                            "policy") != -1 or iframe_url.lower().find("terms"):
                        self.driver.switch_to.frame(iframe)
                        word = self.driver.find_element(By.TAG_NAME, "body").text
                        self.driver.switch_to.default_content()
                        word += self.driver.find_element(By.TAG_NAME, "body").text
                        return self.Check_info(word)
                    else:
                        word = self.driver.find_element(By.TAG_NAME, "body").text
                        return self.Check_info(word)
                else:
                    word = self.driver.find_element(By.TAG_NAME, "body").text
                    return self.Check_info(word)
        else:
            word = self.driver.find_element(By.TAG_NAME, "body").text
            return self.Check_info(word)
    #selenium으로 개인정보처리방침 매칭이 안되는 경우 (와디즈)
    def bs4_crawling(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
        }
        privacy_response = requests.get(self.website, verify=False, headers=headers)

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
                if tmp.lower().find('personalinfo') != -1 or tmp.lower().find('privacy') != -1 or tmp.lower().find('policy') != -1:
                    privacy_url = tmp
                    if privacy_url.find('www') == -1 and privacy_url.find(
                            'https://') == -1:
                        fqdn = tldextract.extract(self.website).fqdn
                        privacy_url = 'https://' + fqdn + privacy_url
                        self.driver.get(privacy_url)
                        try:
                            self.infinity_scroll()
                        except:
                            pass
                        word = self.driver.find_element(By.TAG_NAME, "body").text
                        return self.Check_info(word)

                    elif privacy_url.find('www') != -1 or privacy_url.find(
                            'https://') != -1:
                        self.driver.get(tmp)
                        word = self.driver.find_element(By.TAG_NAME, "body").text
                        return self.Check_info(word)
            return self.Check_info("개인정보처리방침없음")
    #크롤링
    def crawling(self):
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument('headless')
        options.add_argument("window-size=1920,1080")
        options.add_argument("disable-gpu")
        options.add_argument('Accept-Language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7')
        # options.add_argument("accept-language=ko-KR")
        # 쿠팡 같이 크롤링 막은 사이트 우회용으로 작성
        options.add_argument(
            f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
        self.websites = ['https://' + self.urls]
        for self.website in self.websites:
            # self.driver = webself.driver.Chrome('/home/ubuntu/dark_pattern/tool/chromeself.driver', chrome_options=options)
            self.driver = webdriver.Chrome(self.check_chrome_driver(), chrome_options=options)
            self.driver.get(self.website)
            sleep(2)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
                "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            }
            # en으로 들어오는 사이트는 ko로 변환하여 한글사이트로 바꿈
            if self.driver.current_url.find("/en/") != -1:
                privacy_url = self.driver.current_url.replace("/en/", "/ko/")
                self.driver.get(privacy_url)
                sleep(2)
            # 팝업창 제거
            main = self.driver.window_handles
            for i in main:
                if i != main[0]:
                    self.driver.switch_to.window(i)
                    self.driver.close()
            self.driver.switch_to.window(main[0])

            try:
                self.infinity_scroll()
            except:
                pass

            # 모든 사이트의 개인정보처리방침을 매칭하기 위한 방법
            try:
                self.driver.find_element(By.LINK_TEXT, "개인정보처리방침").send_keys(Keys.ENTER)
                scroll = self.driver.find_element(By.TAG_NAME, "body")
                # 셀레니움으로 들어가면 스크롤을 막아놓는 사이트를 우회하기 위해 작성
                self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                # 새창으로 뜨는 경우 새창으로 이동
                if len(self.driver.window_handles) >= 2:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    scroll = self.driver.find_element(By.TAG_NAME, "body")
                    self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

            except NoSuchElementException:
                try:
                    self.driver.find_element(By.LINK_TEXT, "개인정보 처리방침").send_keys(Keys.ENTER)
                    scroll = self.driver.find_element(By.TAG_NAME, "body")
                    self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                    if len(self.driver.window_handles) >= 2:
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        scroll = self.driver.find_element(By.TAG_NAME, "body")
                        self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                except NoSuchElementException:
                    try:
                        self.driver.find_element(By.LINK_TEXT, "개인정보 취급방침").send_keys(Keys.ENTER)
                        scroll = self.driver.find_element(By.TAG_NAME, "body")
                        self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                        if len(self.driver.window_handles) >= 2:
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            scroll = self.driver.find_element(By.TAG_NAME, "body")
                            self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)


                    except NoSuchElementException:
                        try:
                            self.driver.find_element(By.LINK_TEXT, "개인정보취급방침").send_keys(Keys.ENTER)
                            scroll = self.driver.find_element(By.TAG_NAME, "body")
                            self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                            if len(self.driver.window_handles) >= 2:
                                self.driver.switch_to.window(self.driver.window_handles[1])
                                scroll = self.driver.find_element(By.TAG_NAME, "body")
                                self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                        except NoSuchElementException:
                            try:
                                self.driver.find_element(By.LINK_TEXT, "개인(신용)정보 처리방침").send_keys(Keys.ENTER)
                                scroll = self.driver.find_element(By.TAG_NAME, "body")
                                self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                                if len(self.driver.window_handles) >= 2:
                                    self.driver.switch_to.window(self.driver.window_handles[1])
                                    scroll = self.driver.find_element(By.TAG_NAME, "body")
                                    self.driver.execute_script("arguments[0].setAttribute('style','overflow:none;')", scroll)

                            except NoSuchElementException:
                                try:
                                    # a태그가 아닌!! button으로 구현한 사이트 대상
                                    button_list = self.driver.find_elements(By.TAG_NAME, "button")
                                    if len(button_list) >= 1:
                                        for buttons in button_list:
                                            tmp = buttons.text.replace(" ", "")
                                            if tmp == '':
                                                continue
                                            if tmp == "개인정보처리방침" or tmp == '개인정보취급방침':
                                                buttons.send_keys(Keys.ENTER)
                                                scroll = self.driver.find_element(By.TAG_NAME, "body")
                                                self.driver.execute_script(
                                                    "arguments[0].setAttribute('style','overflow:none;')",
                                                    scroll)
                                                if len(self.driver.window_handles) >= 2:
                                                    self.driver.switch_to.window(self.driver.window_handles[1])
                                                    scroll = self.driver.find_element(By.TAG_NAME, "body")
                                                    self.driver.execute_script(
                                                        "arguments[0].setAttribute('style','overflow:none;')",
                                                        scroll)
                                                    break
                                            else:
                                                return self.bs4_crawling()
                                    else:
                                        return self.bs4_crawling()

                                except NoSuchElementException:
                                    return self.bs4_crawling()


            sleep(1)

            try:
                return self.iframe_exist()
            except NoSuchElementException:
                return '개인정보처리방침없음'

if __name__ == '__main__':
    obj = Privacy_Crawling()
    obj()








