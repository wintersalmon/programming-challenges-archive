import json
import os


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TOOL_DIR)

RES_DIR = os.path.join(ROOT_DIR, 'res')
SRC_DIR = os.path.join(ROOT_DIR, 'src')
TEMP_DIR = os.path.join(ROOT_DIR, 'temp')

secret_settings = load_json_data(os.path.join(ROOT_DIR, '.secret.json'))
