# import config
import sys
sys.path.append('../')
from itertools import repeat
import pandas as pd
from utils.data_frame import DataFrame
import deepfm.config as config
from sklearn.preprocessing import MinMaxScaler

# Input : X data, X's columns, CONT_FIELDS, CAT_FIELDS, 연속형을 구간화할 것인지
def get_modified_data(X, all_fields, continuous_fields, categorical_fields, is_bin=False):
    field_dict = dict()
    field_index = []
    X_modified = pd.DataFrame()

    for index, col in enumerate(all_fields): # user, brand, category
        # col이 X의 columns 중에 없으면 오류 출력:
        # if col not in all_fields:
        #     print("{} not included: Check your column list".format(col))
        #     raise ValueError
        
        # 연속형 column
        if col in continuous_fields:
            # 스케일러 준비
            scaler = MinMaxScaler()

            if is_bin:
                X_bin = pd.cut(scaler.fit_transform(X[[col]]).reshape(-1, ), config.NUM_BIN, labels=False)
                X_bin = pd.Series(X_bin).astype('str')
                # 구간을 나누고 값을 줘서 원 핫 인코딩 진행
                X_bin_col = pd.get_dummies(X_bin, prefix=col, prefix_sep='-')
                field_dict[index] = list(X_bin_col.columns)
                field_index.extend(repeat(index, X_bin_col.shape[1]))
                X_modified = pd.concat([X_modified, X_bin_col], axis=1)
            else:
                X_cont_col = pd.DataFrame(scaler.fit_transform(X[[col]]), columns=[col])
                field_dict[index] = col
                field_index.append(index)
                X_modified = pd.concat([X_modified, X_cont_col], axis=1)
        if col in categorical_fields:
            # X_cat_col = pd.get_dummies(X[col], prefix=col) #, prefix_sep='-'
            X_cat_col = X.filter(regex=col)
            print('X_cat_col', X_cat_col.columns)
            field_dict[index] = list(X_cat_col.columns)
            field_index.extend(repeat(index, X_cat_col.shape[1]))
            X_modified = pd.concat([X_modified, X_cat_col], axis=1)
    print('Data Prepared...')
    print('X shape: {}'.format(X_modified.shape))
    print('# of Feature: {}'.format(len(field_index)))
    print('# of Field: {}'.format(len(field_dict)))
    # 원래 column번호 별 X_modified의 column, 원래 column번호, X_modified 반환
    return field_dict, field_index, X_modified
    
