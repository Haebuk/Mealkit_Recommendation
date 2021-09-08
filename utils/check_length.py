def check_length(filename):
    import json

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(len(data))

if __name__ == '__main__':
    check_length('프롬노웨어.json')