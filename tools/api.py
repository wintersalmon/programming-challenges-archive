import requests
import urllib3
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

from tools.settings import secret_settings


class APIError(Exception):
    pass


class ResourceNotFoundError(APIError):
    pass


class APIUdebug(object):
    hostname = 'https://www.udebug.com'
    retrieve_list_url = '/input_api/input_list/retrieve.json'
    retrieve_input_url = '/input_api/input/retrieve.json'
    retrieve_output_url = '/output_api/output/retrieve.json'

    def __init__(self, username, password):
        self._session = requests.Session()
        self._session.auth = HTTPBasicAuth(username, password)

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


def main():
    api = APIUdebug(secret_settings['username'], secret_settings['password'])
    judge_alias = 'uva'
    problem_id = '100'
    input_list = api.get_input_list(judge_alias, problem_id)
    print(input_list)

    for i in input_list:
        a = api.get_input(i['id'])
        b = api.get_output(i['id'])
        print(i['id'], 'PASS')


def main2():
    udebug_hostname = "https://www.udebug.com"
    taget = '{base_host}/{judge_alias}/{problem_id}'.format(
        base_host=udebug_hostname,
        judge_alias="UVa",
        problem_id="100"
    )
    udebug_result = requests.get(taget)
    soup = BeautifulSoup(udebug_result.content, 'html.parser')

    uva_problem_link = None
    for a in soup.find_all('a', href=True):
        if a.text == "Problem Statement":
            uva_problem_link = a["href"]

    if uva_problem_link is None:
        print('link Not found')

    print(uva_problem_link)
    input()

    uva_result = requests.get(uva_problem_link)
    print(uva_result.content)


def find_uva_problem_url(judge_alias: str, problem_id: str):
    url = 'https://www.udebug.com/{judge_alias}/{problem_id}'.format(
        judge_alias=judge_alias,
        problem_id=problem_id
    )

    udebug_result = requests.get(url)
    soup = BeautifulSoup(udebug_result.content, 'html.parser')

    for a in soup.find_all('a', href=True):
        if a.text == "Problem Statement":
            return a["href"]

    raise ResourceNotFoundError(url)


def find_uva_pdf(url):
    uva_result = requests.get(url, verify=False)

    soup = BeautifulSoup(uva_result.content, 'html.parser')
    img = soup.find('img', {"title": "Download as PDF"})

    if img:
        href = img.findParent()["href"]
        pdf_url = "https://uva.onlinejudge.org/{}".format(href)
        pdf_result = requests.get(pdf_url, verify=False)
        if pdf_result.status_code == 200:
            return pdf_result.content

    raise ResourceNotFoundError(url)


def search_and_download_problem_pdf(judge_alias: str, problem_id: str, save_file_path: str):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        uva_url = find_uva_problem_url(judge_alias, problem_id)
        pdf_content = find_uva_pdf(uva_url)
        with open(save_file_path, 'wb') as pdf_file:
            pdf_file.write(pdf_content)

    except ResourceNotFoundError as e:
        print(e)
        return False
    else:
        return True


if __name__ == '__main__':
    main()
