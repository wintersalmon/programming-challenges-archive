import json
import os

from .api import APIUdebug
from .settings import RES_DIR, SRC_DIR


def get_or_create_dir(*paths, mode=0o755):
    target_dir = os.path.join(*paths)
    if not os.path.exists(target_dir):
        cur_path = paths[0]
        for path in paths[1:]:
            cur_path = os.path.join(cur_path, path)
            if not os.path.exists(cur_path):
                os.mkdir(path=cur_path, mode=mode)

    return target_dir


def create(judge_alias, problem_id):
    with open('.secret.json', 'r') as secret_file:
        data = json.load(secret_file)
        api = APIUdebug(**data)

    input_list = api.get_input_list(judge_alias, problem_id)

    conf = {
        'judge_alias': judge_alias,
        'problem_id': problem_id,
        'cases': {item['id']: item for item in input_list}
    }

    res_root_dir = get_or_create_dir(RES_DIR, judge_alias, problem_id)
    conf_file_path = os.path.join(res_root_dir, '.{}_{}.json'.format(judge_alias, problem_id))

    src_root_dir = get_or_create_dir(SRC_DIR, judge_alias, problem_id)
    src_file_path = os.path.join(src_root_dir, '{}_{}.py'.format(judge_alias, problem_id))

    print('NEW {}_{} {} cases'.format(judge_alias, problem_id, len(conf['cases'])))

    with open(conf_file_path, 'w') as conf_file:
        json.dump(conf, conf_file)

    if not os.path.exists(src_file_path):
        with open(src_file_path, 'w'):
            pass

    for case_id, case in conf['cases'].items():
        case_dir = get_or_create_dir(res_root_dir, case_id)
        in_case_path = os.path.join(case_dir, '809768.in.txt')
        out_case_path = os.path.join(case_dir, 'out.txt')

        print(case_dir)
        print(in_case_path)
        print(out_case_path)

        in_data = api.get_input(case['id'])
        out_data = api.get_output(case['id'])

        with open(in_case_path, 'w') as in_case_file:
            in_case_file.write(in_data)

        with open(out_case_path, 'w') as ans_case_file:
            ans_case_file.write(out_data)

    print('DONE {}_{}'.format(judge_alias, problem_id))

