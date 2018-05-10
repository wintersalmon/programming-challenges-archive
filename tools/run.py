import os
import time

from .compare import compare_file_content
from .settings import SRC_DIR


def find_case_path(target_path):
    cases = list()
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith("in.txt"):
                case_path = root
                cases.append((os.path.split(root)[-1], case_path))
    return sorted(cases)


def run_all_script(judge_alias, problem_id):
    base_dir = os.path.join(SRC_DIR, judge_alias, problem_id)
    base_name = '{j_id}_{p_id}'.format(j_id=judge_alias, p_id=problem_id)

    cases = find_case_path(base_dir)
    source_file_path = os.path.join(base_dir, base_name + '.py')

    print('RUNNING {}'.format(base_name))
    for case_name, case_path in cases:
        print('- with case {}:'.format(case_name), end=' ')
        input_file_path = os.path.join(case_path, base_name + '.in.txt')
        output_file_path = os.path.join(case_path, base_name + '.out.txt')
        answer_file_path = os.path.join(case_path, base_name + '.ans.txt')

        run_counter = run_script(
            in_file_path=input_file_path, out_file_path=output_file_path, src_file_path=source_file_path)

        cmp_result = compare_file_content(from_file_path=answer_file_path, to_file_path=output_file_path)

        if cmp_result:
            result_msg = '[{:.4f}] FAILED'.format(run_counter)
        else:
            result_msg = '[{:.4f}] OK'.format(run_counter)

        print(result_msg)
    print('DONE {}'.format(base_name))


def run_script(in_file_path, out_file_path, src_file_path):
    start = time.time()
    os.system(
        "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
            in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
    return time.time() - start
