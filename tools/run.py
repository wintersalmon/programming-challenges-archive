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


def run_all_script(judge_alias, problem_id, *, save_result=False):
    base_dir = os.path.join(SRC_DIR, judge_alias, problem_id)
    base_name = '{j_id}_{p_id}'.format(j_id=judge_alias, p_id=problem_id)

    cases = find_case_path(judge_alias, problem_id)
    source_file_path = os.path.join(base_dir, base_name + '.py')

    print('RUNNING {}'.format(base_name))
    for case_name, case_path in cases:
        print('- with case {}:'.format(case_name), end=' ')
        # input_file_path = os.path.join(case_path, '_'.join((base_name, case_name, 'in')) + '.txt')
        # output_file_path = os.path.join(case_path, '_'.join((base_name, case_name, 'out')) + '.txt')
        input_file_path = os.path.join(case_path, 'in.txt')
        output_file_path = os.path.join(case_path, 'out.txt')

        if save_result:
            case_temp_file = None
            result_file_path = os.path.join(TEMP_DIR, '_'.join((base_name, case_name, 'out')) + '.txt')
        else:
            case_temp_file = tempfile.NamedTemporaryFile()
            result_file_path = case_temp_file.name

        run_counter = run_script(
            in_file_path=input_file_path, out_file_path=result_file_path, src_file_path=source_file_path)

        cmp_result = compare_file_content(from_file_path=output_file_path, to_file_path=result_file_path)

        if cmp_result:
            result_msg = '[{:.4f}] FAILED'.format(run_counter)
        else:
            result_msg = '[{:.4f}] OK'.format(run_counter)

        if not save_result:
            case_temp_file.close()

        print(result_msg)
    print('DONE {}'.format(base_name))


def run_script(in_file_path, out_file_path, src_file_path):
    start = time.time()
    os.system(
        "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
            in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
    return time.time() - start
