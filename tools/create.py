import json
import os

from .api import APIUdebug
from .settings import RES_DIR, SRC_DIR, secret_settings


def get_or_create_dir(*paths, mode=0o755):
    target_dir = os.path.join(*paths)
    if not os.path.exists(target_dir):
        cur_path = paths[0]
        for path in paths[1:]:
            cur_path = os.path.join(cur_path, path)
            if not os.path.exists(cur_path):
                os.mkdir(path=cur_path, mode=mode)

    return target_dir


class FileExistDecoratorClass(object):
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, file_path, *args, **kwargs):
        if os.path.exists(file_path):
            print('already exist', file_path)
        else:
            self.original_function(file_path, *args, **kwargs)
            print('new file:', file_path)


@FileExistDecoratorClass
def new_file(file_path):
    with open(file_path, 'w'):
        pass


@FileExistDecoratorClass
def new_file_and_dump(file_path, content):
    with open(file_path, 'w') as file:
        json.dump(content, file)


@FileExistDecoratorClass
def new_file_and_write(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def create(judge_alias, problem_id):
    print('Download & Create {} {}'.format(judge_alias, problem_id))
    if input('Press ENTER to continue: '):
        return

    api = APIUdebug(secret_settings['username'], secret_settings['password'])

    input_list = api.get_input_list(judge_alias, problem_id)

    conf = {
        'judge_alias': judge_alias,
        'problem_id': problem_id,
        'cases': {item['id']: item for item in input_list}
    }

    res_root_dir = get_or_create_dir(RES_DIR, judge_alias, problem_id)
    conf_file_path = os.path.join(res_root_dir, '.{}_{}.json'.format(judge_alias, problem_id))

    src_root_dir = get_or_create_dir(SRC_DIR, judge_alias, problem_id)
    src_readme = os.path.join(src_root_dir, 'readme.md')
    src_file_path = os.path.join(src_root_dir, '{}_{}.py'.format(judge_alias, problem_id))

    print('new {}_{} {} cases'.format(judge_alias, problem_id, len(conf['cases'])))

    new_file_and_dump(conf_file_path, conf)
    new_file(src_readme)
    new_file(src_file_path)

    with open(conf_file_path, 'r') as conf_file:
        loaded_conf = json.load(conf_file)

        for case_id, case in conf['cases'].items():
            if case_id not in loaded_conf['cases']:
                loaded_conf['cases'][case_id] = conf['cases'][case_id]

            in_case_path = os.path.join(res_root_dir, '.'.join(('in', case_id, 'txt')))
            out_case_path = os.path.join(res_root_dir, '.'.join(('out', case_id, 'txt')))

            in_data = api.get_input(case['id'])
            out_data = api.get_output(case['id'])

            new_file_and_write(in_case_path, in_data)
            new_file_and_write(out_case_path, out_data)

        with open(conf_file_path, 'w') as save_conf_file:
            json.dump(loaded_conf, save_conf_file)

    print('DONE {}_{}'.format(judge_alias, problem_id))
