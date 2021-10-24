import re
import json
from data_to_json import DataToJson
from tqdm import tqdm
import pandas as pd


dt1 = DataToJson('마켓컬리sub.json')
dt2 = DataToJson('마켓컬리리뷰sub.json')
# dt3 = DataToJson('마켓컬리리뷰.json')
info = dt1.load_json()
review = dt2.load_json()
# review_original = dt3.load_json()
dt1.check_json_file_length()
dt2.check_json_file_length()
# dt3.check_json_file_length()

name_in_info = []
name_in_review = []
name_in_review_original = []

for i in info:
    name_in_info.append(i['name'])
for i in review:
    name_in_review.append(i['name'])
# for i in review_original:
#     name_in_review_original.append(i['name'])

review_series = pd.Series(name_in_review)
set_info = set(name_in_info)
set_review = set(name_in_review)
set_review_original = set(name_in_review_original)
print(f'set of files: {len(set_info)}, {len(set_review)}, {len(set_review_original)}')

print(review_series.value_counts()[:20])
not_exist_info = []
not_exist_review = []
not_exist_review_original = []

regex = " \(.*\)|\[.*\] |\(.*\)| \d{3}|[g]"

# for n, i in enumerate(review):
#     review[n]['name'] = re.sub(regex, "", i['name'])
# print(review)

# with open('data/마켓컬리리뷰sub.json', 'w', encoding='utf-8') as f:
#     json.dump(review, f, ensure_ascii=False, indent=4)
for idx, name in tqdm(enumerate(name_in_review)):
    if name not in name_in_info:
        not_exist_info.append(name)
    
print(not_exist_info, len(not_exist_info))
# print(set(not_exist_review), len(set(not_exist_review)))
# print(len(set(name_in_info)))
# print(len(set(name_in_review)))    
# print(name_in_review)

