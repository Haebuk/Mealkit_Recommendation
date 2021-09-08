def load_json(filename):
    import json
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        empty_list = []
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(empty_list, f, ensure_ascii=False, indent=4)
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    return data