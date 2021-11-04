import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.data_frame import Data_frame
from utils.data_of_FM import Data_of_FM
DF_I = Data_frame('이마트몰', '정보')
DF_R = Data_frame('이마트몰', '리뷰')

emart_infos = DF_I.get_DF()     # 이마트몰 상품정보 데이터
emart_reviews = DF_R.get_DF()   # 이마트몰 리뷰 데이터

DF_FM = Data_of_FM('이마트몰')
emart_fmdata = DF_FM.get_FMdata()   # 이마트몰 FM 데이터
                                    # (name, user, brand, category) -> 지금은 여기까지
print(emart_fmdata)