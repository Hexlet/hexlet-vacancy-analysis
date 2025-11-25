import json


def get_fixture_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def save_data(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
