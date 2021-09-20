def save_json(data, filename):
    """
    데이터를 json 파일로 저장하는 함수
    params:
    data: 저장할 데이터
    filename: 저장할 파일명
    """
    import json
    with open(filename, 'w', encoding='utf-8') as f: # json 파일로 저장
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'{filename} saved.') # 저장 완료 메시지 출력
    print(f'-- {filename} length: {len(data)}') # 저장된 파일의 데이터 길이 출력


