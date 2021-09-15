import time
from emart_mall.emart_scrapping import Emart_Scrapping

try:
    with Emart_Scrapping() as emart:
        
        input1 = int(input("시작할 페이지: "))
        input2 = int(input("종료할 페이지: "))
        for page in range(input1, input2+1):
            emart.land_first_page(page)
            product_list = emart.get_product_list()
            print(f'product list length: {len(product_list)}')
            for iter in range(len(product_list)):
                print(f'----- page: {page}, iter: {iter+1} -----')
                emart.click_product(iter)    
                product_url = emart.get_product_url()
                product_name = emart.get_product_name()
                emart.land_first_page(page)

                if iter % 5 == 0: # 새로고침을 자주할 때 나오는 에러 창 방지
                    time.sleep(5)

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