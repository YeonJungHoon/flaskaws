from selenium import webdriver
from flask import url_for
from selenium.webdriver.common.by import By
import os
from urllib.request import urlretrieve
import urllib
from selenium.webdriver.common.keys import Keys


class crawl():
    def __init__(self,path):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(path,options = options)
        self.driver = driver
        
    def naver(self):
        
        id = 'wolfself2'
        password = '1q2w3e4r5t6y'
        self.driver.implicitly_wait(3)
        self.driver.get('https://naver.com')
        ###driver.find_element_by_name('id').send_keys(id)
        ###driver.find_element_by_name('pw').send_keys(password)
        ###driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    def pixiv(self):
        
        url = 'https://www.pixiv.net/en/'
        self.driver.implicitly_wait(3)
        self.driver.get(url)
    def zerochan(self, data,epoch):
        url = 'https://www.zerochan.net/'
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        search_box = self.driver.find_element(By.XPATH, '//*[@id="q"]')
        search_box.send_keys(data)
        search_box.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(3)
        img_urls = []
        for i in range(epoch):

            img = self.driver.find_element(By.CSS_SELECTOR, '#thumbs2 > li:nth-child({}) > div > a:nth-child(1) > img'.format(i+1))
            url = img.get_attribute('src')
            img_urls.append(url)
        self.driver.implicitly_wait(3)

        
        return img_urls

    def url_to_img(self, img_urls):
        img_folder = 'static/img'
        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        
        if not os.path.isdir(img_folder):
            os.mkdir(img_folder)
            
        file_num = len(os.listdir(img_folder))
        

        for index, link in enumerate(img_urls):
            #start = link.rfind('.')
            #end = link.rfind('&')
            #filtype = link[start:end]
            urlretrieve(link, f'static/img/{index+ 1 + file_num}.jpg')

    def pinterest(self,data,epoch):
        id = 'wolfself2@naver.com'
        password = '1q2w3e4r5t6y'
        url = 'https://www.pinterest.co.kr/'
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        login_box = self.driver.find_element(By.XPATH, '//*[@id="fullpage-wrapper"]/div[1]/div/div/div[1]/div/div[2]/div[2]/button/div/div')
        login_box.click()
        self.driver.implicitly_wait(3)
        email = self.driver.find_element(By.XPATH, '//*[@id="email"]')
        email.send_keys(id)
        password_box = self.driver.find_element(By.XPATH,'//*[@id="password"]')
        password_box.send_keys(password)
        login_box_2 = self.driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[2]/div/div/div/div/div/div[4]/form/div[7]/button/div')
        login_box_2.click()
        self.driver.implicitly_wait(4)
        search_box = self.driver.find_element(By.XPATH, '//*[@id="searchBoxContainer"]/div/div/div[2]/input')
        self.driver.implicitly_wait(2)
        search_box.send_keys(data)
        search_box.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(3)
        img_urls = []
        for i in range(epoch):
            img = self.driver.find_element(By.CSS_SELECTOR,'#__PWS_ROOT__ > div:nth-child(1) > div.appContent > div > div > div:nth-child(4) > div.zI7.iyn.Hsu > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child({}) > div > div > div > div > div > div > div:nth-child(1) > a > div > div.zI7.iyn.Hsu > div > div > div > div > div > img'.format(i+1))
            url = img.get_attribute('src')
            img_urls.append(url)
        self.driver.implicitly_wait(3)
        return img_urls
            
#__PWS_ROOT__ > div:nth-child(1) > div.appContent > div > div > div:nth-child(4) > div.zI7.iyn.Hsu > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > div > div > div > div > div > div > div:nth-child(1) > a > div > div.zI7.iyn.Hsu > div > div > div > div > div > img
#__PWS_ROOT__ > div:nth-child(1) > div.appContent > div > div > div:nth-child(4) > div.zI7.iyn.Hsu > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(2) > div > div > div > div > div > div > div:nth-child(1) > a > div > div.zI7.iyn.Hsu > div > div > div > div > div > img

    def word_extracter(self):
        sentence = []
        url = 'https://www.google.com/'
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf.emcav > div.RNNXgb > div > div.a4bIc > input')
        search_box.send_keys('나무위키')
        search_box.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(3)
        element = self.driver.find_element(By.CSS_SELECTOR, '#rso > div:nth-child(1) > div > div > div > div > div > div > div > div.yuRUbf > a > h3')
        element.click()
        self.driver.implicitly_wait(3)
        path1 = self.driver.find_element(By.CSS_SELECTOR, '#VIVXXZe6L > div.\35 b7915a8 > div > div > div > article > div:nth-child(8) > div:nth-child(5) > div > div > div > div > div > div > div > div > div > div:nth-child(11) > div > div > div > div > div > div > div > div:nth-child(1) > div > div:nth-child(10) > div > ul:nth-child(3) > li > div > strong > a')
        path1.click()
        self.driver.implicitly_wait(3)
        next_link = self.driver.find_element(By.CLASS_NAME,'DCLJQsNO')
        next_link.click()
        self.driver.implicitly_wait(3)
        #self.driver.find_element(By.CSS_SELECTOR,) #Crafting

    def chat_data_extractor(self):
        sentence = []
        url = 'https://www.dcinside.com/'
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        

    
    
        
        

