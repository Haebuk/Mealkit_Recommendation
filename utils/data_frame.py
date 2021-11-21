import json
import os
import pandas as pd
from tqdm import tqdm

class DataFrame:
    """
    dataframe 가공 관련 클래스
    :params store_name: 상점 이름 (마켓컬리 or 이마트몰)
    :params data_type: 정보 or 리뷰
    """
    def __init__(self, store_name='마켓컬리', data_type='정보'):
        self.store_name = store_name # 상점 이름 (마켓컬리 or 이마트몰)
        self.data_type = data_type # json 파일 타입 (정보 or 리뷰)
        
    def get_df(self):
        """
        정보나 리뷰 json 파일을 불러와 pandas dataframe으로 바꾸는 함수
        """
        if os.getcwd().split('/')[-1] == 'Mealkit_Recommendation':
            path = './data/' + self.store_name + self.data_type + '.json' # json 파일 경로
        else:
            path = '../data/' + self.store_name + self.data_type + '.json'
        if self.data_type == '정보':
            with open(path, encoding='utf-8') as f:
                result = pd.read_json(f) # 정보 json은 pandas 에서 바로 로드 가능
        elif self.data_type == '리뷰':
            with open(path, encoding='utf-8') as f:
                data = json.load(f) # 리뷰 json은 변환해야함

                names, users, stars, contents = [], [], [], []

                result = pd.DataFrame(columns=['name', 'user', 'star', 'content'])

                for i in range(len(data)): # nested json 펼치기
                    for j in range(len(data[i]['reviews'])):
                        names.append(data[i]['name'])
                        users.append(data[i]['reviews'][j]['user'])
                        stars.append(data[i]['reviews'][j]['star'])
                        contents.append(data[i]['reviews'][j]['content'])
    
                result['name'] = names
                result['user'] = users
                result['star'] = stars
                result['content'] = contents
        return result # 리뷰 dataframe

    def get_FMdata(self):
        """
        Factorization Machine 모델에 적합한 데이터로 변환하는 함수
        """
        info = DataFrame(self.store_name, '정보').get_df()
        review = DataFrame(self.store_name, '리뷰').get_df()
        data = review[['name', 'user', 'star']]
        brands, categories = [], []
        for name in tqdm(data['name'], desc='brand&category'):
            brands.append(info.loc[info['name'] == name, 'brand'].iloc[0])
            categories.append(info.loc[info['name'] == name, 'category'].iloc[0])
        data['brand'] = brands
        data['category'] = categories

        dummy_df = pd.DataFrame()
        for col in tqdm(['user', 'name', 'brand', 'category'], desc='더미 변수 변환 중...'):
            dummy_df = pd.concat([dummy_df, data[col].str.get_dummies()], axis=1)

        return dummy_df
        
    

