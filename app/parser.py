import json
import logging


def get_fixture_data(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logging.warning(f"Fixture file not found: {path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in fixture file: {path}")
        return {}
    except PermissionError:
        logging.error(f"Permission denied for fixture file: {path}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error reading fixture: {path} - {str(e)}")
        raise


def save_data(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except PermissionError:
        logging.error(f"Permission denied for saving file: {path}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error saving file: {path} - {str(e)}")
        raise