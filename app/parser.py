import json


def get_fixture_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data