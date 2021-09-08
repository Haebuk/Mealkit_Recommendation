def save_json(data, filename):
    import json
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'{filename} saved.')
    print(f'-- {filename} length: {len(data)}')


