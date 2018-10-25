import requests
import urllib3
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

from tools.errors import APIError, ResourceNotFoundError


class UdebugAPI(object):
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


def extract_uva_url(judge_id: str, problem_id: str) -> str:
    udebug_url = 'https://www.udebug.com/{judge_id}/{problem_id}'.format(
        judge_id=judge_id,
        problem_id=problem_id
    )

    udebug_result = requests.get(udebug_url)
    if udebug_result.status_code != 200:
        raise ResourceNotFoundError('Get Request Failed: {}({})'.format(udebug_url, udebug_result.status_code))

    udebug_soup_result = BeautifulSoup(udebug_result.content, 'html.parser')

    for a in udebug_soup_result.find_all('a', href=True):
        if a.text == "Problem Statement":
            return a["href"]

    raise ResourceNotFoundError('Failed to find uva url: {}'.format(udebug_url))


def extract_pdf_url(uva_url: str) -> str:
    uva_result = requests.get(uva_url, verify=False)

    if uva_result.status_code != 200:
        raise ResourceNotFoundError('Get Request Failed: {}({})'.format(uva_url, uva_result.status_code))

    soup = BeautifulSoup(uva_result.content, 'html.parser')
    img = soup.find('img', {"title": "Download as PDF"})

    if img:
        href = img.findParent()["href"]
        return "https://uva.onlinejudge.org/{}".format(href)

    raise ResourceNotFoundError('Failed to find pdf url: {}'.format(uva_url))


def find_and_get_pdf_content(judge_id: str, problem_id: str) -> str:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    uva_url = extract_uva_url(judge_id, problem_id)
    pdf_url = extract_pdf_url(uva_url)
    pdf_get_result = requests.get(pdf_url, verify=False)

    if pdf_get_result.status_code == 200:
        return pdf_get_result.content

    raise ResourceNotFoundError('Failed to get pdf content: {}({})'.format(pdf_url, pdf_get_result.status_code))
