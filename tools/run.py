import json
import os
import tempfile
import time

from .compare import compare_file_content
from .settings import RES_DIR, SRC_DIR, TEMP_DIR


def find_case_path(judge_alias, problem_id):
    target_path = os.path.join(RES_DIR, judge_alias, problem_id)
    cases = list()
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith("in.txt"):
                case_path = root
                cases.append((os.path.split(root)[-1], case_path))
    return sorted(cases)


def run_all_script(judge_alias, problem_id, *, use_temp_files=True):
    with open(
            os.path.join(RES_DIR, judge_alias, problem_id, '.{}_{}.json'.format(judge_alias, problem_id))) as conf_file:
        conf = json.load(conf_file)

    base_dir = os.path.join(SRC_DIR, judge_alias, problem_id)
    # cases = find_case_path(judge_alias, problem_id)
    source_file_path = os.path.join(base_dir, '{j_id}_{p_id}'.format(j_id=judge_alias, p_id=problem_id) + '.py')

    print('RUNNING {} {}'.format(judge_alias, problem_id))
    for case_id, case in conf['cases'].items():
        print('- with case {}:'.format(case_id), end=' ')

        # input_file_path = os.path.join(case_path, '_'.join((base_name, case_name, 'in')) + '.txt')
        # output_file_path = os.path.join(case_path, '_'.join((base_name, case_name, 'out')) + '.txt')

        # input_file_path = os.path.join(case_path, 'in.txt')
        # output_file_path = os.path.join(case_path, 'out.txt')

        if 'skip' in case and case['skip'] is True:
            run_time = None
            run_result = 'SKIP'

        else:
            input_file_path = os.path.join(RES_DIR, judge_alias, problem_id, '.'.join(('in', case_id, 'txt')))
            output_file_path = os.path.join(RES_DIR, judge_alias, problem_id, '.'.join(('out', case_id, 'txt')))

            if use_temp_files:
                case_temp_file = tempfile.NamedTemporaryFile()
                result_file_path = case_temp_file.name
            else:
                case_temp_file = None
                result_file_path = os.path.join(TEMP_DIR, '.'.join((judge_alias, problem_id, case_id, 'txt')))

            run_time = run_script(
                in_file_path=input_file_path, out_file_path=result_file_path, src_file_path=source_file_path)

            cmp_result = compare_file_content(from_file_path=output_file_path, to_file_path=result_file_path)

            if cmp_result:
                run_result = 'FAIL'
            else:
                run_result = 'OK'

            if use_temp_files:
                case_temp_file.close()

        # print('[{run_time:7.4f}] {run_result}'.format(run_time=run_time, run_result=run_result))
        if run_time is None:
            print('[       ] {run_result}'.format(run_result=run_result))
        else:
            print('[{run_time:7.4f}] {run_result}'.format(run_time=run_time, run_result=run_result))

    print('DONE')


def run_script(in_file_path, out_file_path, src_file_path):
    start = time.time()
    os.system(
        "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
            in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
    return time.time() - start
