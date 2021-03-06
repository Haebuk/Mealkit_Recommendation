# 마켓컬리 스크래핑 코드 작성
import market_kurly.constants as const
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

class Kurly_Scrapping(webdriver.Chrome):
    def __init__(self, driver_path = '/mnt/nas3/rjs/chromedriver', teardown=False): # C 드라이브에 있는 크롬 드라이버를 사용하도록 설정
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
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


    # def get_product_image_url(self): # 상품 이미지 url을 가져오는 함수
    #     product_image_urls_css = self.find_elements_by_css_selector("#goodsList > div.list_goods > div > ul > li > div > div > a > img")
    #     product_image_urls = []
    #     for label in product_image_urls_css:
    #         product_image_urls.append(label.get_attribute('src'))
        
    #     return product_image_urls


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
        time.sleep(0.5)
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

        product_price = product_price.strip('원')                
        print(f'product price: {product_price}')
        return product_price
    def optimize_name(self, name):
        opt = " \(.*\)|\[.*\] |\(.*\)| \d{3}|[g]"
        optimized_name = re.sub(opt,"",name)
        return optimized_name

    def get_product_review(self): # 후기와 작성자명을 가져오는 함수
        # 리뷰 클릭
        self.find_element_by_xpath('//*[@id="goods-view-infomation"]/div[1]/ul/li[3]/a').send_keys(Keys.ENTER)
        time.sleep(1)
        reviews = []
        users = []
        try:
            for page in range(3,11):
                self.switch_to.frame('inreview')
                for i in range(2,9):
                    # 작성자명 수집
                    time.sleep(1)
                    user_path = '//*[@id="contents-wrapper"]/div[1]/div/form/div['+str(i)+']/table/tbody/tr/td[4]'
                    user_name = self.find_element_by_xpath(user_path).text
                    if user_name == 'Marketkurly' or user_name == 'MarketKurly': # 리뷰 중 공지사항 빼기
                        time.sleep(1)
                        continue
                    # 개별 리뷰 클릭
                    click_path = '//*[@id="contents-wrapper"]/div[1]/div/form/div['+str(i)+']/table/tbody/tr/td[2]/div[1]'
                    element = self.find_element_by_xpath(click_path)
                    self.execute_script("arguments[0].click();", element)
                    time.sleep(1)
                    # 개별 리뷰 수집
                    text_path = '//*[@id="contents-wrapper"]/div[1]/div/form/div['+str(i)+']/div/div[1]'
                    review = self.find_element_by_xpath(text_path).text 
                    if '\n\n\n' in review: # 그림 있는 경우
                        review = review.split('\n\n\n')[1:]
                        review = " ".join(review)
                    else: # 그림 없는 경우
                        review = review.split('\n')[1:]
                        review = " ".join(review)

                    value1 = {
                        'user': user_name,
                        'content': review
                    }
                    print(value1)
                    users.append(user_name)
                    reviews.append(review)
                # 다음 리뷰 페이지로
                page_path = '//*[@id="contents-wrapper"]/div[2]/a['+str(page)+']'
                self.find_element_by_xpath(page_path).send_keys(Keys.ENTER)
                time.sleep(1)
                self.switch_to.default_content() 

        except Exception as e:
            print(e)
            print(f'리뷰가 부족합니다. 리뷰 개수: {len(reviews)}')
            return users, reviews
        
        return users, reviews 


