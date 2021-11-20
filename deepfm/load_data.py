import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# import sys
# sys.path.append('../')
from utils.data_frame import DataFrame

class load_data:
    def __init__(self, store_name='마켓컬리', data_type='정보'):
        self.store_name = store_name # 상점 이름 (마켓컬리 or 이마트몰)
        self.data_type = data_type # json 파일 타입 (정보 or 리뷰)
    def get_df(self):
        data = DataFrame(self.store_name, self.data_type).get_df()
        if self.data_type == '리뷰':
            return data[['user','name','star']]
        else:
            return data
if __name__ == '__main__':
    print(load_data('이마트몰','리뷰').get_df())
