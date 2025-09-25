import json


def get_fixture_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def save_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)
