import json
import os
class DataToJson:
    def __init__(self, filename: os.PathLike):
        self.filename = './data/' + filename

    def load_json(self):
        """
        json 파일로부터 데이터를 로드하는 함수
        param: filename: json 파일명
        return: json 파일의 데이터
        """
        try: # json 로드 시도
            with open(os.path.join(os.getcwd(), self.filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
        except: # json 파일이 존재하지 않는 경우 빈 리스트를 json 파일에 추가해서 저장
            empty_list = [] # 빈 리스트 생성
            with open(os.path.join(os.getcwd(), self.filename), 'w') as f: # 빈 리스트 저장
                json.dump(empty_list, f, ensure_ascii=False, indent=4)
            with open(os.path.join(os.getcwd(), self.filename), 'r', encoding='utf-8') as f: # 빈 리스트를 저장한 파일을 로드
                data = json.load(f)
        return data

    def save_json(self, data):
        """
        데이터를 json 파일로 저장하는 함수
        params:
        data: 저장할 데이터
        filename: 저장할 파일명
        """
        with open(self.filename, 'w', encoding='utf-8') as f: # json 파일로 저장
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f'{self.filename} saved.') # 저장 완료 메시지 출력
        print(f'-- {self.filename} length: {len(data)}') # 저장된 파일의 데이터 길이 출력

    def check_json_file_length(self):
        """
        json 파일의 길이를 확인하는 함수
        param: filename: json 파일의 이름
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'{self.filename} 파일의 길이: {len(data)}')

    @staticmethod
    def integrate_file(file1, file2):
        """
        두 파일을 첫번째 파일 하나로 합치는 함수
        param: file2: 첫 번째 파일의 이름(해당 파일로 합쳐짐)
        param: file2: 두 번째 파일의 이름
        """
        list1 = DataToJson(file1).load_json()
        list2 = DataToJson(file2).load_json()
        print(f"{file1}의 길이: {len(list1)}")
        print(f"{file2}의 길이: {len(list2)}")
        run = input("합치시겠습니까? (y/n)")
        if run == 'y' or run == 'Y':
            list1.extend(list2)
            print(f"합쳤습니다. {file1}의 길이: {len(list1)}")
            save = input("저장하시겠습니까? (y/n)")
            if save == 'y' or save == 'Y':
                DataToJson(file1).save_json(list1)
                return True
            else:
                print("종료되었습니다.")
                return False
        else:
            print("종료되었습니다.")
            return False
        

if __name__ == '__main__':
    DataToJson('마켓컬리정보_1024_drop_duplicates.json').check_json_file_length()
    DataToJson('마켓컬리리뷰_1024_drop_duplicates.json').check_json_file_length()
    # DataToJson.integrate_file('마켓컬리리뷰.json', '마켓컬리리뷰_3_4.json')

