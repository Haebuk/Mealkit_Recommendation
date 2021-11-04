from utils.data_frame import Data_frame
import pandas as pd

class Data_of_FM:
    def __init__(self, storename):
        self.storename = storename
    def get_FMdata(self):
        if self.storename == '마켓컬리':
            DF = Data_frame('마켓컬리','리뷰')
            kurly_reviews = DF.get_DF()
            DF2 = Data_frame('마켓컬리','정보')
            kurly_infos = DF2.get_DF()
            
            kurly_data = kurly_reviews[['name','user','star']]
            brands = []
            categories = []
            for name in kurly_reviews['name']:
                brands.append(kurly_infos[kurly_infos['name']==name]['brand'].tolist()[0])
                categories.append(kurly_infos[kurly_infos['name']==name]['category'].tolist()[0])
            kurly_data['brand'] = brands
            kurly_data['category'] = categories

            dummy_name_df = kurly_data['name'].str.get_dummies()
            dummy_user_df = kurly_data['user'].str.get_dummies()
            dummy_brand_df = kurly_data['brand'].str.get_dummies()
            dummy_category_df = kurly_data['category'].str.get_dummies()
            dummy_df = pd.concat([dummy_name_df,dummy_user_df,dummy_brand_df, dummy_category_df], axis=1)

            return dummy_df
        elif self.storename == '이마트몰':
            DF = Data_frame('이마트몰', '리뷰')
            emart_reviews = DF.get_DF()
            DF2 = Data_frame('이마트몰','정보')
            emart_infos = DF2.get_DF()

            emart_data = emart_reviews[['name','user']]
            brands = []
            categories = []
            for name in emart_reviews['name']:
                brands.append(emart_infos[emart_infos['name']==name]['brand'].tolist()[0])
                categories.append(emart_infos[emart_infos['name']==name]['category'].tolist()[0])
            emart_data['brand'] = brands
            emart_data['category'] = categories

            dummy_name_df = emart_data['name'].str.get_dummies()
            dummy_user_df = emart_data['user'].str.get_dummies()
            dummy_brand_df = emart_data['brand'].str.get_dummies()
            dummy_category_df = emart_data['category'].str.get_dummies()
            dummy_df = pd.concat([dummy_name_df,dummy_user_df,dummy_brand_df, dummy_category_df], axis=1)

            return dummy_df
        else:
            print("Store Name을 잘못 입력하셨습니다.")
            return 0


