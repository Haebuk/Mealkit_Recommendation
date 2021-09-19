from market_kurly.kurly_scrapping import Kurly_Scrapping
import os
import market_kurly.constants as const
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement

try:
    with Kurly_Scrapping() as kurly:
        kurly.land_first_page()                             # 밀키트.메인요리 페이지 오픈
        product_list = kurly.get_product_list()             # 상품 리스트 저장
        print(f'product list length: {len(product_list)}')  # 상품 리스트 길이 출력
        product_image_urls = kurly.get_product_image_url()
        for iter in range(len(product_list)):               # iter: 0 ~ 리스트 길이 - 1         // product_list : 99개  -> 1페이지만 나오는 듯
            print('------' + str(iter+1) + '------')        # ------ 1 ------

            kurly.click_product(iter)                       # iter에 해당하는 상품 클릭 0~98
            kurly.refresh()
            product_url = kurly.get_product_url()

            image_url = product_image_urls[iter]
            print(f'product image url: {image_url}')
            product_name = kurly.get_product_name()
            product_price = kurly.get_product_price()

            kurly.land_first_page()

            if iter == 5:
                break
    # 페이지 넘기면서 계속 받아야함.
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
    else:
        raise