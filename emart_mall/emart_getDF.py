import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.data_frame import Data_frame
DF_I = Data_frame('이마트몰', '정보')
DF_R = Data_frame('이마트몰', '리뷰')

emart_infos = DF_I.get_DF()
emart_reviews = DF_R.get_DF()

print(emart_reviews)