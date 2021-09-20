def load_json(filename):
    """
    json 파일로부터 데이터를 로드하는 함수
    param: filename: json 파일명
    return: json 파일의 데이터
    """
    import json
    try: # json 로드 시도
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except: # json 파일이 존재하지 않는 경우 빈 리스트를 json 파일에 추가해서 저장
        empty_list = [] # 빈 리스트 생성
        with open(filename, 'w', encoding='utf-8') as f: # 빈 리스트 저장
            json.dump(empty_list, f, ensure_ascii=False, indent=4)
        with open(filename, 'r', encoding='utf-8') as f: # 빈 리스트를 저장한 파일을 로드
            data = json.load(f)
    return data