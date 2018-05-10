import json
import os

from .api import APIUdebug
from .settings import SRC_DIR


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
    api = APIUdebug.load_from_file('.secret.json')
    input_list = api.get_input_list(judge_alias, problem_id)

    conf = {
        'judge_alias': judge_alias,
        'problem_id': problem_id,
        'cases': input_list
    }

    project_root_dir = get_or_create_dir(SRC_DIR, judge_alias, problem_id)
    project_conf_file_path = os.path.join(project_root_dir, '.{}_{}.json'.format(judge_alias, problem_id))
    project_src_file_path = os.path.join(project_root_dir, '{}_{}.py'.format(judge_alias, problem_id))

    print(project_root_dir)

    with open(project_conf_file_path, 'w') as conf_file:
        json.dump(conf, conf_file)

    with open(project_src_file_path, 'w'):
        pass

    for c_num, case in enumerate(conf['cases'], 1):
        case_name = 'case_{:02d}'.format(c_num)
        case_dir = get_or_create_dir(project_root_dir, case_name)
        in_case_path = os.path.join(case_dir, '{}_{}.in.txt'.format(judge_alias, problem_id))
        ans_case_path = os.path.join(case_dir, '{}_{}.ans.txt'.format(judge_alias, problem_id))

        print(case_dir)

        in_case = api.get_input(case['id'])
        ans_case = api.get_output(case['id'])

        with open(in_case_path, 'w') as in_case_file:
            in_case_file.write(in_case)

        with open(ans_case_path, 'w') as ans_case_file:
            ans_case_file.write(ans_case)

        print('done')
