from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.request
import time
from tqdm import tqdm


class CrawlingManager():
    def __init__(self):
        self.driver_setting()
    
    def driver_setting(self):
        try:
            options = Options()
            options.add_experimental_option("detach", True)  # 브라우저 바로 닫힘 방지
            options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 메시지 제거
            driver = webdriver.Chrome(options=options)
            self.driver = driver
        except:
            print('Chrome이 설치되어 있는지 확인해주세요.')
    
    def img_crawling(self, keyword='python', save_path='./save'):
        self.driver.get("https://www.google.com/search?q=%EB%88%88%EA%B0%90%EA%B3%A0+%EC%9E%88%EB%8A%94+%EC%82%AC%EC%A7%84&tbm=isch&ved=2ahUKEwj885mNq6-DAxUwmFYBHUxzAI4Q2-cCegQIABAA&oq=%EB%88%88%EA%B0%90%EA%B3%A0+%EC%9E%88%EB%8A%94+%EC%82%AC%EC%A7%84&gs_lcp=CgNpbWcQAzoECCMQJzoFCAAQgAQ6BggAEAcQHjoHCAAQgAQQGFD5B1iTFmC8F2gAcAB4AYABdIgBpA2SAQQyLjE0mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=zfKLZbzZN7Cw2roPzOaB8Ag&bih=1319&biw=2560&hl=ko")
        # time.sleep(2)
        # elem = self.driver.find_elements(By.ID, "APjFqb")
        # elem.send_keys(keyword)    # search word
        # elem.submit()

        SCROLL_PAUSE_TIME = 2
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:   # Repeat until break
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    self.driver.find_element(By.CSS_SELECTOR,".mye4qd").click()
                except:
                    break
            last_height = new_height

        images = self.driver.find_elements(By.CSS_SELECTOR,'.rg_i.Q4LuWd')
        
        idx = 1
        for image in tqdm(images):
            try:
                image.click()   # To get more quality images
                time.sleep(1)
                imgUrl = self.driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]').get_attribute("src")
                
                print(imgUrl)
                imgUrl = imgUrl.replace('https', 'http') # https로 요청할 경우 보안 문제로 SSL에러가 남
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'Mozilla/5.0')] # https://docs.python.org/3/library/urllib.request.html 참고
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(imgUrl, f'{save_path}/{idx}.jpg')
                idx += 1
            except:
                print('error')
                pass

        self.driver.close()


def main():
    # dir_path = '.'
    cm = CrawlingManager()
    cm.img_crawling(keyword='졸고있는 사진')



if __name__ == "__main__" :
    main()