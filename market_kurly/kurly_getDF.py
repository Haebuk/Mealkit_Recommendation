import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.data_frame import Data_frame
from utils.data_of_FM import Data_of_FM
DF_I = Data_frame('마켓컬리', '정보')
DF_R = Data_frame('마켓컬리', '리뷰')
kurly_infos = DF_I.get_DF()     # 마켓컬리 상품정보 데이터
kurly_reviews = DF_R.get_DF()   # 마켓컬리 리뷰 데이터

DF_FM = Data_of_FM('마켓컬리')
kurly_fmdata = DF_FM.get_FMdata()   # 마켓컬리 FM 데이터 
                                    # (name, user, brand, category) -> 지금은 여기까지
print(kurly_fmdata)