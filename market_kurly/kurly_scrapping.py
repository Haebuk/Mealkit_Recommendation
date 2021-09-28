import os
# 마켓컬리 스크래핑 코드 작성

import market_kurly.constants as const
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement

class Kurly_Scrapping(webdriver.Chrome):
    def __init__(self, driver_path = '/Users/chromedriver', teardown=False): # C 드라이브에 있는 크롬 드라이버를 사용하도록 설정
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Kurly_Scrapping, self).__init__(options=options, executable_path=driver_path)
        # self.maximize_window()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self): # 페이지를 여는 함수
        self.get(const.BASE_URL)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def land_next_page(self, num): # 해당하는 페이지 클릭
        if num==0:
            pass
        else:
            page_bars = self.find_element_by_class_name('pagediv').find_elements_by_css_selector('#goodsList > div.layout-pagination > div > span > a')
            page_bars[num-1].click()
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def get_product_image_url(self): # 상품 이미지 url을 가져오는 함수
        # product_image_urls_class = self.find_element_by_class_name('inner_listgoods').find_elements_by_tag_name('img')
        # product_image_urls=[]
        # for img in product_image_urls_class: 
        #     product_image_urls.append(img.get_attribute('src'))

        # return product_image_urls
        product_image_url = self.find_element_by_css_selector('#sectionView > div > div.thumb').get_attribute('style')
        product_image_url = product_image_url.replace('background-image: url("','',1).replace('");','',1)
        print(f'product image url: {product_image_url}')
        return product_image_url


    def get_product_list(self): # 상품 리스트를 가져오는 함수, 최대 99개
        goods_element = self.find_element_by_class_name('inner_listgoods')
        product_list = goods_element.find_elements_by_tag_name('li')
        # print(f'product_list length: {len(product_list)}')
        return product_list

    def click_product(self, iter: int): # 상품을 클릭하는 함수
        product_list = self.get_product_list()
        product_list[iter].click()

    def get_product_url(self): # 상품의 url을 가져오는 함수
        product_url = self.current_url
        print(f'product url: {product_url}')
        return product_url

    def get_product_name(self): # 상품의 이름을 가져오는 함수
        product_name = self.find_element_by_class_name(
            'goods_name'
        ).find_element_by_class_name('name').text
        print(f'product name: {product_name}')
        return product_name

    def get_brand_name(self): # 상품의 브랜드를 가져오는 함수
        product_name = self.find_element_by_class_name(
            'goods_name'
        ).find_element_by_class_name('name').text
        idx = product_name.find(']') 
        brand = 'None' if idx==-1 else product_name[1:idx]
        print(f'product brand: {brand}')
        return brand
    
    def get_product_information(self): # 제품 정보를 가져오는 함수
        information = self.find_element_by_class_name('words').text
        print(f'product information: {information}')
        return information

    def get_soldout_info(self): # 품절 여부 판단하는 함수
        try:
            product_cart_button = self.find_element_by_id(
                'cartPut'
            ).find_element_by_class_name('btn btn_alarm on').text
            print('품절 상품')
            return True
        except:
            print('판매중인 상품')
            return False

    def move_backward(self): # 뒤로가기를 실행하는 함수
        self.execute_script("window.history.go(-1)")
    
    def get_product_price(self): # 상품의 가격을 가져오는 함수
        product_price = self.find_element_by_class_name(
            'goods_price'
        ).find_element_by_class_name('dc_price').text
        product_price = product_price.strip('원').replace(',','')                #int(product_price.strip('원').strip(',')
        print(f'product price: {product_price}')
        return int(product_price)
