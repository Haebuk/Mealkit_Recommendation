def check_length(filename):
    """
    json 파일의 길이를 확인하는 함수
    param: filename: json 파일의 이름
    """
    import json

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'{filename} 파일의 길이: {len(data)}')


# test
if __name__ == '__main__':
    check_length('프롬노웨어.json')