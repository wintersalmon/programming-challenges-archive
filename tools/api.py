import json

import requests
from requests.auth import HTTPBasicAuth


class APIError(Exception):
    pass


class APIUdebug(object):
    hostname = 'https://www.udebug.com'
    retrieve_list_url = '/input_api/input_list/retrieve.json'
    retrieve_input_url = '/input_api/input/retrieve.json'
    retrieve_output_url = '/output_api/output/retrieve.json'

    def __init__(self, username, password):
        self._session = requests.Session()
        self._session.auth = HTTPBasicAuth(username, password)

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as secret_file:
            data = json.load(secret_file)
            return cls(username=data['username'], password=data['password'])

    def get_input_list(self, judge_alias, problem_id):

        params = {
            'judge_alias': judge_alias,
            'problem_id': problem_id
        }

        response = self._session.get(self.hostname + self.retrieve_list_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise APIError(response.status_code)

    def get_input(self, input_id):
        params = {
            'input_id': input_id
        }

        response = self._session.get(self.hostname + self.retrieve_input_url, params=params)

        if response.status_code == 200:
            return response.json()[0]
        else:
            raise APIError(response.status_code)

    def get_output(self, input_id):
        params = {
            'input_id': input_id
        }

        response = self._session.get(self.hostname + self.retrieve_output_url, params=params)

        if response.status_code == 200:
            return response.json()[0]
        else:
            raise APIError(response.status_code)


def load_username_and_password(file_path):
    with open(file_path, 'r') as secret_file:
        data = json.load(secret_file)
        return data['username'], data['password']


def main():
    api = APIUdebug.load_from_file('../.secret.json')

    judge_alias = 'uva'
    problem_id = '100'
    input_list = api.get_input_list(judge_alias, problem_id)
    print(input_list)

    for i in input_list:
        a = api.get_input(i['id'])
        b = api.get_output(i['id'])
        print(i['id'], 'PASS')


if __name__ == '__main__':
    main()
