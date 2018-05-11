import json
import os
import tempfile
import time

from .compare import compare_file_content
from .settings import RES_DIR, SRC_DIR, TEMP_DIR


__all__ = [
    'run_all_cases',
    'run_one_case'
]


def run_all_cases(judge_alias, problem_id, *, save_results=False, show_details=False):
    conf_file_path = os.path.join(RES_DIR, judge_alias, problem_id, '.{}_{}.json'.format(judge_alias, problem_id))
    with open(conf_file_path, 'r') as conf_file:
        conf = json.load(conf_file)

    print('RUNNING {} {}'.format(judge_alias, problem_id))

    for case_id, case in conf['cases'].items():
        if 'skip' in case and case['skip'] is True:
            print('- with case {}: [       ] SKIP'.format(case_id))
        else:
            show_run_and_compare(judge_alias, problem_id, case_id, save_results=save_results, show_details=show_details)

    print('DONE')


def run_one_case(judge_alias, problem_id, case_id, *, save_results=False, show_details=False):
    print('RUNNING {} {}'.format(judge_alias, problem_id))
    show_run_and_compare(judge_alias, problem_id, case_id, save_results=save_results, show_details=show_details)
    print('DONE')


def show_run_and_compare(judge_id, problem_id, case_id, *, save_results=False, show_details=False):
    print('- with case {}: '.format(case_id), end='')

    running_time, compare_result = run_and_compare(judge_id, problem_id, case_id, save_results=save_results)

    running_time_fmt = '{:7.4f}'.format(running_time)
    compare_result_fmt = 'OK' if not compare_result else 'FAIL'

    print('[{}] {}'.format(running_time_fmt, compare_result_fmt))

    if show_details:
        for line in compare_result:
            print(line)


def run_and_compare(judge_id, problem_id, case_id, *, save_results=False):
    base_dir = os.path.join(SRC_DIR, judge_id, problem_id)
    source_file_path = os.path.join(base_dir, '{j_id}_{p_id}'.format(j_id=judge_id, p_id=problem_id) + '.py')
    input_file_path = os.path.join(RES_DIR, judge_id, problem_id, '.'.join(('in', case_id, 'txt')))
    output_file_path = os.path.join(RES_DIR, judge_id, problem_id, '.'.join(('out', case_id, 'txt')))

    if save_results:
        temp_result_file = None
        result_file_path = os.path.join(TEMP_DIR, '.'.join((judge_id, problem_id, case_id, 'txt')))
    else:
        temp_result_file = tempfile.NamedTemporaryFile()
        result_file_path = temp_result_file.name

    exe_time = run(in_file_path=input_file_path, out_file_path=result_file_path, src_file_path=source_file_path)
    cmp_result = compare_file_content(from_file_path=output_file_path, to_file_path=result_file_path)

    if temp_result_file:
        temp_result_file.close()

    return exe_time, cmp_result


def run(in_file_path, out_file_path, src_file_path):
    start = time.time()
    os.system(
        "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
            in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
    return time.time() - start
