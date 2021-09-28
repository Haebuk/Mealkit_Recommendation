import time
import emart_mall.constants as const
from selenium import webdriver

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
        ).find_element_by_class_name('cdtl_info_tit').text.split('\n')[0]
        print(f'product name: {product_name}')
        return product_name
    
    def get_product_brand(self): # 상품의 브랜드를 가져오는 함수
        product_name = self.find_element_by_class_name(
            'cdtl_prd_info'
        ).find_element_by_class_name('cdtl_info_tit').text.split('\n')
        idx = product_name[0].find(']')
        if idx == -1 : # 상품명에 브랜드가 없는 경우
            try:
                brand_store = self.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/span/a').text
                brand = brand_store[1:idx]
            except:
                brand_store = self.find_element_by_class_name('cdtl_store_tittx').text
                idx = brand_store.find('(')
                brand = brand_store.replace('스토어',"") if idx==-1 else brand_store[0:idx]
        else: # 상품명에 브랜드가 있는 경우
            brand = product_name[0][1:idx]
        print(f'product brand: {brand}')
        return brand

    def get_soldout_info(self): # 품절 여부 판단하는 함수
        if self.find_element_by_class_name(
                'cdtl_btn_wrap3'
            ).find_element_by_css_selector("span[class='notranslate']").text == '장바구니':
            print('판매중인 상품')
            return False
        else:
            print('품절 상품')
            return True

    def get_product_information(self): # 상품 정보를 가져오는 함수
        try:
            self.switch_to.frame("_ifr_html") # iframe 
            product_information = self.find_element_by_class_name(
                'tmpl_sub_tit'
            ).text
            print(f'product information: {product_information}')
            return product_information
        except:
            return ''

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

    def get_product_image_url(self): # 상품 이미지 url을 가져오는 함수
        product_image_urls_css = self.find_elements_by_css_selector("#ty_thmb_view > ul > li > div.cunit_prod > div.thmb > a > img.i1")
        product_image_urls = []
        for label in product_image_urls_css:
            product_image_urls.append(label.get_attribute('src'))
        
        return product_image_urls

    def get_product_price(self): # 상품의 가격을 가져오는 함수
        product_price = self.find_element_by_class_name(
            'cdtl_info_wrap'
        ).find_element_by_class_name('ssg_price').text.split('\n')[0]
        print(f'product price: {product_price}')
        return product_price

    def get_review_info(self): # 상품의 리뷰 정보를 가져오는 함수
        """
        return: reviews, starts, users
        """
        button_box = self.find_element_by_id('comment_navi_area') # 버튼박스
        reviews = [] # 리뷰를 저장할 리스트
        stars = [] # 별점을 저장할 리스트
        users = [] # 유저명을 저장할 리스트
        try:
            for page in range(2, 7):
                print(f'review page: {page-1}')
                review_box = self.find_element_by_id('cdtl_cmt_tbody') # 리뷰 컨테이너
                user_list = review_box.find_elements_by_class_name('user') # 유저명
                star_list = review_box.find_elements_by_class_name('star') # 평점
                desc_txt = review_box.find_elements_by_class_name('desc_txt') # 리뷰. desc 바로 잡으면 10개가 더잡히기 때문에 한번 더 찾아줌

                for i, (user, star, desc) in enumerate(zip(user_list, star_list, desc_txt)): # 리뷰 저장
                    desc = desc.text
                    if desc.split('\n')[0] == '사진' or desc.split('\n')[0] == '비디오':
                        desc = desc.split('\n')[1:]
                    if desc[0] == '사진' or desc[0] == '비디오':
                        desc = desc[1:]
                    users.append(user.text)
                    stars.append(star.text.split(' ')[-1][0])        
                    reviews.append(''.join(desc))

                time.sleep(1)
                button_box.find_element_by_link_text(str(page)).click()
                time.sleep(1)
        except Exception as e:
            print(f'리뷰가 부족합니다. 리뷰 개수: {len(reviews)}')
            return reviews, stars, users
        return reviews, stars, users

    def get_product_category(self): # 카테고리 가져오는 함수
        product_category = self.find_element_by_id(
            'area_disp_ctg_title'
            ).find_element_by_tag_name('a').text.strip()
        print(f'product category: {product_category}')
        if '일식/아시안' == product_category:
            return '일식_아시안'
        return product_category
