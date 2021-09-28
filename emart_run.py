import time
from tqdm import tqdm
from random import randint
from emart_mall.emart_scrapping import Emart_Scrapping


try:
    with Emart_Scrapping() as emart:
        
        input1 = int(input("시작할 페이지: ")) # 시작할 페이지
        input2 = int(input("종료할 페이지: ")) # 종료할 페이지
        for page in range(input1, input2+1):
            emart.land_first_page(page)
            product_list = emart.get_product_list()
            print(f'product list length: {len(product_list)}')
            product_image_urls = emart.get_product_image_url()
            for iter in range(len(product_list)):
                print(f'----- page: {page}, iter: {iter+1} -----')
                image_url = product_image_urls[iter]
                product_url = emart.access_product(iter)
                print(f'product image url: {image_url}')
                product_name = emart.get_product_name()
                product_brand = emart.get_product_brand() # 상품 브랜드 수집
                product_price = emart.get_product_price()
                is_sold_out = emart.get_soldout_info()
                product_info = emart.get_product_information() # 상품 정보 수집
                emart.land_first_page(page)
except Exception as e:
    
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else: # 셀레니움 경로 관련 오류가 아닐경우 해당 오류 출력
        print(e)