import re
import emoji
from soynlp.normalizer import repeat_normalize

def review_clean(x):
    """ 리뷰 데이터 정제

    Args:
        x (str): 리뷰 데이터

    Returns:
        (str): 정제된 리뷰 데이터
    """
    emojis = ''.join(emoji.UNICODE_EMOJI.keys())
    pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣{emojis}]+')
    url_pattern = re.compile(
        r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

    x = pattern.sub(' ', x)
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)
    return x

def info_clean(x):
    """ 제목, 설명 정제
    1. 소괄호, 대괄호 제거
    2. 그램 수 제거
    3. 특수 문자 제거

    Args:
        x (str): 제목 또는 decription 데이터
    
    Returns:
        x (str): 정제된 데이터
    """
    regex = re.compile(r'\[.*\]|\s-\s.*|\(.*\)|[^가-힣   ]')
    x = regex.sub('', x).strip()
    return x

if __name__ == '__main__':
    x = '[브랜드] 브랜드 무언가  + & (rhkf) 500g'
    print(clean(x))