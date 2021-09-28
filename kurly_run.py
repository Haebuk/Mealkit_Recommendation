from market_kurly.kurly_scrapping import Kurly_Scrapping
from utils.data_to_json import DataToJson
from utils.refine_information import refine_information
import time

filename = '마켓컬리.json'
data = DataToJson(filename)

try:
    with Kurly_Scrapping() as kurly:
        for page_idx in range(3,4):
            kurly.land_first_page()                             # 밀키트.메인요리 페이지 오픈
            time.sleep(5)
            kurly.land_next_page(page_idx)
            time.sleep(5)

            product_list = kurly.get_product_list()             # 상품 리스트 저장
            print(f'product list length: {len(product_list)}')  # 상품 리스트 길이 출력
            # product_image_urls = kurly.get_product_image_url()

            for iter in range(len(product_list)):               # iter: 0 ~ 리스트 길이 - 1         // product_list : 99개  -> 1페이지만 나오는 듯

                json_data = data.load_json()
                kurly.refresh()
                kurly.land_first_page()
                time.sleep(5) 
                kurly.land_next_page(page_idx)
                time.sleep(5)
                print('------' + str(iter+1) + '------')        # ------ 1 ------
                kurly.click_product(iter)                       # iter에 해당하는 상품 클릭 0~98
                kurly.refresh()
                product_url = kurly.get_product_url()
                # image_url = product_image_urls[iter]
                # print(f'product image url: {image_url}')
                image_url = kurly.get_product_image_url()
                product_name = kurly.get_product_name()
                product_brand = kurly.get_brand_name()
                product_information = kurly.get_product_information()
                product_price = kurly.get_product_price()
                is_sold_out = kurly.get_soldout_info()
                kurly.land_first_page()
                time.sleep(3)
                
                product_dict = refine_information(
                    title=product_name,
                    store_name='마켓컬리',
                    category='',
                    brand=product_brand,
                    price=product_price,
                    img_url=image_url,
                    product_url=product_url,
                    is_sold_out=is_sold_out,
                    detail=product_information
                    )
                json_data.append(product_dict)
                data.save_json(json_data)
                if iter == len(product_list)-1:
                     break

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