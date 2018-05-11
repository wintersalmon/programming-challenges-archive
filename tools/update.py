import json
import os

from tools.settings import RES_DIR


def update(judge_id, problem_id, case_id, *options):
    target_dir = os.path.join(RES_DIR, judge_id, problem_id)
    target_conf_path = os.path.join(target_dir, '.{}_{}.json'.format(judge_id, problem_id))

    with open(target_conf_path, 'r') as conf_file:
        conf = json.load(conf_file)

    for opt in options:
        if opt in conf['cases'][case_id]:
            conf['cases'][case_id][opt] = not conf['cases'][case_id][opt]
        else:
            conf['cases'][case_id][opt] = True

    with open(target_conf_path, 'w') as conf_file:
        json.dump(conf, conf_file)
