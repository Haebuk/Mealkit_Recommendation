# 마켓컬리 스크래핑 코드 작성

import market_kurly.constants as const
import os
from selenium import webdriver

class Kurly_Scrapping(webdriver.Chrome):
    def __init__(self, driver_path=r"C:"): # C드라이브에 크롬드라이버가 있어야 합니다
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwiches', ['enable-logging'])
        super(Kurly_Scrapping, self).__init__(options=options)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def land_first_page(self): # 페이지를 여는 함수
        self.get(const.BASE_URL)

    def get_product_list(self): # 상품 리스트를 가져오는 함수
        product_list = self.find_elements_by_id('goodsList')
        print(len(product_list))
        return product_list