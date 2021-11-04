import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.data_frame import Data_frame
DF_I = Data_frame('마켓컬리', '정보')
DF_R = Data_frame('마켓컬리', '리뷰')

kurly_infos = DF_I.get_DF()
kurly_reviews = DF_R.get_DF()

print(kurly_infos)