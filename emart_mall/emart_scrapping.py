# 이마트몰 스크래핑 코드 작성

import time
import emart_mall.constants as const
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement

class Emart_Scrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/chromedriver.exe', teardown=False): # C 드라이브에 있는 크롬 드라이버를 사용하도록 설정
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Emart_Scrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self, num_page): # 페이지를 여는 함수
        self.get(const.BASE_URL + f'&page={num_page}')

    def get_product_list(self): # 상품 리스트를 가져오는 함수, 최대 99개
        goods_element = self.find_element_by_id('ty_thmb_view')
        product_list = goods_element.find_elements_by_tag_name('li')
        print(f'product_list length: {len(product_list)}')
        return product_list

    def access_product(self, iter: int): # 상품 URL 정보를 받고 이동하는 함수
        product_list = self.get_product_list()
        product_url = product_list[iter].find_element_by_css_selector(
            'a[href*="/item/"]'
            ).get_attribute('href')
        print(f'product url: {product_url}')
        self.get(product_url)
        return product_url

    def get_product_name(self): # 상품의 이름을 가져오는 함수
        product_name = self.find_element_by_class_name(
            'cdtl_prd_info'
        ).find_element_by_class_name('cdtl_info_tit').text.split('\n')
        print(f'product name: {product_name[0]}')
        return product_name

    def get_soldout_info(self): # 품절 여부 판단하는 함수
        if self.find_element_by_class_name(
                'cdtl_btn_wrap3'
            ).find_element_by_css_selector("span[class='notranslate']").text == '장바구니':
            print('판매중인 상품')
            return False
        else:
            print('품절 상품')
            return True

    def move_backward(self): # 뒤로가기를 실행하는 함수
        self.execute_script("window.history.go(-1)")
