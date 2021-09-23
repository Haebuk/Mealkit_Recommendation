from market_kurly.kurly_scrapping import Kurly_Scrapping
from utils.data_to_json import DataToJson
from utils.refine_information import refine_information
"""
마켓컬리 크롤링 파일
&page 쿼리 스트링이 없기 때문에 하단의 페이지 버튼을 클릭하는 방법으로 자동화 해야함.
"""
filename = '마켓컬리.json'
data = DataToJson(filename)
try:
    with Kurly_Scrapping() as kurly:
        kurly.land_first_page()
        product_list = kurly.get_product_list()
        print(f'product list length: {len(product_list)}')
        for iter in range(len(product_list)):
            json_data = data.load_json()
            print('------' + str(iter+1) + '------')
            kurly.click_product(iter)    
            kurly.refresh()
            product_url = kurly.get_product_url()
            product_name = kurly.get_product_name()
            is_sold_out = kurly.get_soldout_info()
            kurly.land_first_page()
            product_brand = 'test'
            product_img_url = 'test'
            product_information = 'test'
            product_price = '0'
            product_dict = refine_information(
                title=product_name,
                store_name='마켓컬리',
                category='',
                brand=product_brand,
                price=product_price,
                img_url=product_img_url,
                product_url=product_url,
                is_sold_out=is_sold_out,
                detail=product_information
                )
            json_data.append(product_dict)
            data.save_json(json_data)
            if iter == 2:
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