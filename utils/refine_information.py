def refine_information(
    title: str,
    store_name:str,
    category:str,
    brand:str,
    price:int,
    img_url:str,
    product_url:str,
    is_sold_out:bool,
    detail:str
    ):
    """
    json 파일로 저장하기 위해 데이터를 딕셔너리 안에 저장하는 함수
    :param title: 상품명
    :param store_name: 상점명(마켓컬리, 이마트몰)
    :param category: 카테고리(한식, 웨스턴, 중식, 일식/아시안)
    :param brand: 브랜드명
    :param price: 가격
    :param img_url: 썸네일 URL
    :param product_url: 상품 URL
    :param is_sold_out: 품절 여부
    :param detail: 제품 정보
    :return dict: 딕셔너리
    """
    dict = {}
    dict['name'] = title
    dict['storeName'] = store_name
    dict['category'] = category
    dict['brand'] = brand
    dict['price'] = int(price)
    dict['thumbnailUrl'] = img_url
    dict['contentUrl'] = product_url
    dict['isSoldOut'] = is_sold_out
    dict['detail'] = detail
    return dict