import enum
from data_to_json import DataToJson
from tqdm import tqdm

dt1 = DataToJson('마켓컬리.json')
dt2 = DataToJson('마켓컬리리뷰1.json')
dt3 = DataToJson('마켓컬리리뷰.json')

info = dt1.load_json()
review = dt2.load_json()
review_original = dt3.load_json()
dt1.check_json_file_length()
dt2.check_json_file_length()
dt3.check_json_file_length()

name_in_info = []
name_in_review = []
name_in_ori_review = []
for i in info:
    name_in_info.append(i['name'])
for i in review:
    name_in_review.append(i['name'])
for i in review_original:
    name_in_ori_review.append(i['name'])

not_exist_info = []
not_exist_review = []
not_exist_review_original = []

for idx, name in tqdm(enumerate(name_in_info)):
    appended = False
    if name not in name_in_ori_review:
        not_exist_review_original.append(name)
        appended = True
    if name not in name_in_
    if not appended:
        not_exist_review.append(name)

print(not_exist_info)
# print(not_exist_review)
print(not_exist_review_original)
print(len(not_exist_info), len(not_exist_review_original))
    


