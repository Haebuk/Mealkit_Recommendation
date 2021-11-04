import json
import pandas as pd
import numpy as np

class Data_frame:
    def __init__(self, a, b):
        self.name1 = a
        self.name2 = b
    def get_DF(self):
        if self.name2 == '정보':
            if self.name1 == '마켓컬리':
                path = './data/'+self.name1+'정보_1024_drop_duplicates.json'
            elif self.name1 == '이마트몰':
                path = './data/'+self.name1+'.json'
            with open(path) as f:
                result = pd.read_json(f)
            return result
        elif self.name2 == '리뷰':
            if self.name1 == '마켓컬리':
                path = './data/'+self.name1+'리뷰_1024_drop_duplicates.json'
            elif self.name1 == '이마트몰':
                path = './data/'+self.name1+'리뷰.json'
            with open(path) as f:
                data = json.load(f)

                names = []
                users = []
                stars = []
                contents = []

                result = pd.DataFrame(columns=['name', 'user','star','content'])

                for i in range(len(data)):
                    for j in range(len(data[i]['reviews'])):
                        names.append(data[i]['name'])
                        users.append(data[i]['reviews'][j]['user'])
                        stars.append(data[i]['reviews'][j]['star'])
                        contents.append(data[i]['reviews'][j]['content'])
    
                result['name'] = names
                result['user'] = users
                result['star'] = stars
                result['content'] = contents
            return result
    
    # def get_infoDF(self, name):
    #     path = '/Users/hyojin/Mealkit_Recommendation/data/'+name+'정보_1024_drop_duplicates.json'
    #     with open(path) as f:
    #         info_DF = pd.read_json(f)
    #     return info_DF
    # def get_reviewDF(self, name):
    #     path = '/Users/hyojin/Mealkit_Recommendation/data/'+name+'리뷰_1024_drop_duplicates.json'
    #     with open(path) as f:
    #         data = json.load(f)

    #         names = []
    #         users = []
    #         stars = []
    #         contents = []

    #         review_DF = pd.DataFrame(columns=['name', 'user','star','content'])

    #         for i in range(len(data)):
    #             for j in range(len(data[i]['reviews'])):
    #                 names.append(data[i]['name'])
    #                 users.append(data[i]['reviews'][j]['user'])
    #                 stars.append(data[i]['reviews'][j]['star'])
    #                 contents.append(data[i]['reviews'][j]['content'])
    
    #         review_DF['name'] = names
    #         review_DF['user'] = users
    #         review_DF['star'] = stars
    #         review_DF['content'] = contents
    #     return review_DF


