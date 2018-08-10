import json
import os
from typing import Dict

from tools.api import APIUdebug, search_and_download_problem_pdf
from tools.models import ProblemConf
from tools.settings import RES_DIR, SRC_DIR, secret_settings


def get_or_create_dir(*paths, mode=0o755):
    target_dir = os.path.join(*paths)
    if not os.path.exists(target_dir):
        cur_path = paths[0]
        for path in paths[1:]:
            cur_path = os.path.join(cur_path, path)
            if not os.path.exists(cur_path):
                os.mkdir(path=cur_path, mode=mode)

    return target_dir


class AutoCreateDirectoryDecorator(object):
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, file_path: str, *args, **kwargs):
        get_or_create_dir(os.path.split(file_path))
        self.original_function(file_path, *args, **kwargs)


@AutoCreateDirectoryDecorator
def create_empty_text_file(file_path: str):
    with open(file_path, 'w'):
        pass


@AutoCreateDirectoryDecorator
def create_empty_binary_file(file_path: str):
    with open(file_path, 'wb'):
        pass


@AutoCreateDirectoryDecorator
def create_json_file(file_path: str, json_content: Dict):
    with open(file_path, 'w') as file:
        json.dump(json_content, file)


@AutoCreateDirectoryDecorator
def create_text_file(file_path: str, text_content: str):
    with open(file_path, 'w') as file:
        file.write(text_content)


def create(judge_alias, problem_id, problem_alias=None):
    if problem_alias is None:
        problem_alias = '{}_{}'.format(judge_alias, problem_id)

    print('NEW {problem_alias} ({judge_id} / {problem_id})'.format(
        problem_alias=problem_alias,
        judge_id=judge_alias,
        problem_id=problem_id))
    print('  ENTER to continue')
    print('  ANY other keys to cancel')
    if input('Are you sure?: '):
        return

    api = APIUdebug(secret_settings['username'], secret_settings['password'])

    input_list = api.get_input_list(judge_alias, problem_id)

    cur_conf = ProblemConf(
        problem_alias=problem_alias,
        judge_alias=judge_alias,
        problem_id=problem_id,
        cases={case['id']: {"options": list()} for case in input_list}
    )

    source_directory = get_or_create_dir(SRC_DIR, problem_alias)
    resource_directory = get_or_create_dir(RES_DIR, judge_alias, problem_id)

    conf_file_path = os.path.join(source_directory, '.conf.json')
    readme_file_path = os.path.join(source_directory, 'readme.md')
    solution_file_path = os.path.join(source_directory, 'solution.py')
    problem_file_path = os.path.join(resource_directory, 'problem.pdf')

    # check if duplicate alias exists
    if os.path.exists(conf_file_path):
        prev_conf = ProblemConf.load(problem_alias)
        if cur_conf != prev_conf:
            print('problem alias {} already used: {}/{}'.format(
                problem_alias, prev_conf.judge_alias, prev_conf.problem_id))
            return False
        else:
            for case_id, case in prev_conf.cases.items():
                if case_id not in cur_conf.cases:
                    cur_conf.cases[case_id] = case
                else:
                    cur_conf.cases[case_id].update(case)

    cur_conf.save()

    # ToDo : require more efficient way to print messages

    if os.path.exists(readme_file_path):
        print('SKIP readme.md')
    else:
        create_empty_text_file(readme_file_path)
        print('NEW readme.md')

    if os.path.exists(solution_file_path):
        print('SKIP solution.py')
    else:
        create_empty_text_file(solution_file_path)
        print('NEW solution.py')

    if os.path.exists(problem_file_path):
        print('SKIP problem.pdf')
    else:
        search_and_download_problem_pdf(judge_alias, problem_id, problem_file_path)
        print('NEW problem.pdf')

    for case_id, case in cur_conf.cases.items():
        if 'options' in case and 'custom' in case['options']:
            print('PASS custom case {}'.format(case_id))
            continue

        in_case_path = os.path.join(resource_directory, case_id, 'in.txt')
        out_case_path = os.path.join(resource_directory, case_id, 'out.txt')

        if os.path.exists(in_case_path):
            print('SKIP {} in.txt'.format(case_id))
        else:
            in_data = api.get_input(case_id)
            create_text_file(in_case_path, in_data)
            print('NEW {} in.txt'.format(case_id))

        if os.path.exists(out_case_path):
            print('SKIP {} out.txt'.format(case_id))
        else:
            out_data = api.get_output(case_id)
            create_text_file(out_case_path, out_data)
            print('NEW {} out.txt'.format(case_id))

    print('COMPLETE')
