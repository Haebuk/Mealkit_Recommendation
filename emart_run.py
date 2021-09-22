import time
from emart_mall.emart_scrapping import Emart_Scrapping
"""
이마트몰 크롤링 실행 파일
마켓컬리는 &page= 쿼리 스트링으로 url이 되어 있기 때문에 페이지를 입력해 자동화가 가능
실행 후 시작할 페이지와 종료할 페이지를 입력하여 실행
이마트몰의 경우 새로고침 간격이 2초로 제한되어 있음.
한 상품의 정보를 모두 수집한 후 2초간 일시정지 후 다음 상품을 수집함
"""

try:
    with Emart_Scrapping() as emart:
        
        input1 = int(input("시작할 페이지: ")) # 시작할 페이지
        input2 = int(input("종료할 페이지: ")) # 종료할 페이지
        for page in range(input1, input2+1):
            emart.land_first_page(page) # 첫 페이지로 이동
            product_list = emart.get_product_list() # 상품 리스트 수집
            print(f'product list length: {len(product_list)}') # 상품 리스트 길이 출력
            for iter in range(len(product_list)): # 상품 리스트 수만큼 반복
                print(f'----- page: {page}, iter: {iter+1} -----') # 페이지, 상품 번호 출력
                emart.click_product(iter) # 상품 클릭
                product_url = emart.get_product_url() # 상품 url 수집
                product_name = emart.get_product_name() # 상품 이름 수집
                product_brand = emart.get_product_brand() # 상품 브랜드 수집
                product_information = emart.get_product_information() # 상품 정보 수집
                emart.land_first_page(page) # 첫 페이지로 이동
                time.sleep(2) # 2초 일시정지

except Exception as e:
    """
    처음 실행시 셀레니움 경로 관련 오류가 발생할 수 있는데,
    본인의 os에 맞게 출력물에 나타난 내용을 입력하면 해결
    """
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