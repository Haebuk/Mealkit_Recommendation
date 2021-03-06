from market_kurly.kurly_scrapping import Kurly_Scrapping
from utils.data_to_json import DataToJson
from utils.refine_information import RefineInformation
import time

"""
마켓컬리 크롤링 파일
&page 쿼리 스트링이 없기 때문에 하단의 페이지 버튼을 클릭하는 방법으로 자동화 해야함.
"""
try:

    with Kurly_Scrapping() as kurly:
        for page_idx in range(0,4):
            kurly.land_first_page()                             # 밀키트.메인요리 페이지 오픈
            time.sleep(1)
            kurly.land_next_page(page_idx)
            time.sleep(1)
            filename = '마켓컬리정보_1024.json'
            review_filename = '마켓컬리리뷰_1024.json'

            data = DataToJson(filename)
            review_data = DataToJson(review_filename)
            json_review = review_data.load_json()
            json_data = data.load_json()
            product_list = kurly.get_product_list()             # 상품 리스트 저장
            print(f'product list length: {len(product_list)}')  # 상품 리스트 길이 출력

            # product_image_urls = kurly.get_product_image_url()

            for iter in range(len(product_list)):               # iter: 0 ~ 리스트 길이 - 1         // product_list : 99개  -> 1페이지만 나오는 듯
                
                json_data = data.load_json()
                names = [d['name'] for d in json_data] # 마켓컬리 정보 json에 있는 상품명 리스트
                kurly.refresh()
                kurly.land_first_page()
                time.sleep(1) 
                kurly.land_next_page(page_idx)
                time.sleep(1)
                print('------' + str(iter+1) + '------')        # ------ 1 ------
                kurly.click_product(iter)                       # iter에 해당하는 상품 클릭 0~98
                kurly.refresh()
                product_name = kurly.get_product_name()
                if product_name in names: # 이미 저장된 상품이면 넘어감
                    print('중복된 상품명')
                    continue
                product_url = kurly.get_product_url()
                image_url = kurly.get_product_image_url()
                # product_name = kurly.optimize_name(product_name)
                product_brand = kurly.get_brand_name()
                product_information = kurly.get_product_information()
                product_price = kurly.get_product_price()
                is_sold_out = kurly.get_soldout_info()
                user, review = kurly.get_product_review()
                # print('--user--')
                # print(user)
                # print('--review--')
                # print(review)
                kurly.land_first_page()
                time.sleep(1)
                
                product_dict = RefineInformation().refine_information(
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
                review_dict = RefineInformation().refine_review_kurly(
                        title=product_name,
                        users=user,
                        contents=review
                )
                json_data.append(product_dict)
                json_review.append(review_dict)
                data.save_json(json_data)
                review_data.save_json(json_review)
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